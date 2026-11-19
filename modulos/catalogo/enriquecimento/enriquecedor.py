#!/usr/bin/env python3
"""Trabalho 2 · Etapa 2 — enriquecedor: nome popular ambíguo → espécie aceita.

O modelo local (Ollama) só recebe o que nenhuma regra resolve: nomes populares que a
fonte associa a MAIS DE UMA espécie da PB. Nomes com um único candidato são resolvidos
por consulta direta em `gerar_dados.py`, sem modelo.

Laço escrito à mão (§5.3), sem framework de agente:
  para cada item → histórico [sistema, item] → até MAX_PASSOS chamadas →
  ferramenta da lista branca | registrar (encerra) | estourou o teto → NÃO RESOLVIDO.

Uso:
  python3 enriquecedor.py --spec boa --itens gabarito --rodada exec2-boa
  python3 enriquecedor.py --spec boa --itens ambiguos --rodada producao-boa
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import json
import platform
import subprocess
import time
import unicodedata
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
COLETA = AQUI.parent / "coleta"
OLLAMA = "http://localhost:11434"


# --------------------------------------------------------------------------- referência (lida de arquivo)
def _jsonl(p: Path) -> list[dict]:
    with p.open(encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def chave_nome(nome: str) -> str:
    """Mesma chave do coletor (R16): minúsculas, sem acento, espaço ≡ hífen."""
    s = " ".join(nome.split()).lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return s.replace(" ", "-")


class Referencia:
    def __init__(self, arquivo_regras: str | None):
        self.corpus = _jsonl(COLETA / "corpus.jsonl")
        self.especies = {e["fonte_reflora_id"]: e for e in _jsonl(COLETA / "especies_pb.jsonl")}
        self.por_chave = {chave_nome(it["texto"]): it for it in self.corpus}
        self.nomes_da_especie: dict[str, list[str]] = {}
        for it in self.corpus:
            for c in it["campos"]["candidatos"]:
                self.nomes_da_especie.setdefault(c["fonte_reflora_id"], []).append(it["texto"])
        self.regras = (AQUI / arquivo_regras).read_text(encoding="utf-8") if arquivo_regras else None

    # ---- ferramentas de domínio
    def consultar_nome_popular(self, nome: str) -> dict:
        it = self.por_chave.get(chave_nome(nome))
        if it is None:
            return {"erro": f"nome '{nome}' não está no catálogo; tente buscar_semelhante"}
        saida = {"nome": it["texto"], "candidatos": [
            {**{k: c[k] for k in ("fonte_reflora_id", "nome_cientifico", "familia", "origem", "localidades_do_nome")},
             "dominios": self.especies[c["fonte_reflora_id"]]["dominios_fitogeograficos"]}
            for c in it["campos"]["candidatos"]]}
        if self.regras:
            saida["regras_desempate"] = self.regras
        return saida

    def consultar_especie(self, fonte_reflora_id: str) -> dict:
        e = self.especies.get(fonte_reflora_id)
        if e is None:
            return {"erro": f"fonte_reflora_id '{fonte_reflora_id}' não existe no catálogo da PB"}
        return {
            "fonte_reflora_id": fonte_reflora_id, "nome_cientifico": e["nome_cientifico"],
            "familia": e["familia"], "origem": e["origem"], "endemismo": e["endemismo"],
            "dominios": e["dominios_fitogeograficos"], "sinonimos": e["sinonimos"][:10],
            "nomes_populares": sorted(set(self.nomes_da_especie.get(fonte_reflora_id, [])))[:20],
        }

    def buscar_semelhante(self, nome: str, limite: int = 5) -> dict:
        limite = max(1, min(int(limite), 10))
        alvo = chave_nome(nome)
        parecidos = difflib.get_close_matches(alvo, list(self.por_chave), n=limite + 1, cutoff=0.75)
        return {"nome": nome, "semelhantes": [
            {"nome": self.por_chave[k]["texto"],
             "especies": [c["nome_cientifico"] + " (" + c["fonte_reflora_id"] + ")" for c in self.por_chave[k]["campos"]["candidatos"]]}
            for k in parecidos if k != alvo][:limite]}


# --------------------------------------------------------------------------- contrato de ferramentas
def montar_tools(spec: dict) -> list[dict]:
    d = spec["descricoes"]

    def f(nome, props, req):
        return {"type": "function", "function": {"name": nome, "description": d[nome],
                "parameters": {"type": "object", "properties": props, "required": req}}}

    return [
        f("consultar_nome_popular", {"nome": {"type": "string", "description": "nome popular, como recebido"}}, ["nome"]),
        f("consultar_especie", {"fonte_reflora_id": {"type": "string", "description": "id de um candidato"}}, ["fonte_reflora_id"]),
        f("buscar_semelhante", {"nome": {"type": "string"},
                                "limite": {"type": "integer", "description": "máximo de nomes (1–10)"}}, ["nome"]),
        f("registrar", {
            "fonte_reflora_id": {"type": "string", "description": "id do candidato escolhido ou 'indeterminado'"},
            "confianca": {"type": "string", "enum": ["alta", "media", "baixa"]},
            "justificativa": {"type": "string", "description": "uma frase: qual evidência decidiu"},
        }, ["fonte_reflora_id", "confianca"]),
    ]


# --------------------------------------------------------------------------- normalização de argumentos
def normalizar_args(bruto) -> dict:
    """Argumentos do modelo chegam como dict ou como string JSON. Parser, nunca eval."""
    if isinstance(bruto, str):
        try:
            bruto = json.loads(bruto) if bruto.strip() else {}
        except json.JSONDecodeError:
            return {"_erro": "argumentos não são JSON válido"}
    if not isinstance(bruto, dict):
        return {"_erro": "argumentos não são um objeto"}
    args = {}
    for k, v in bruto.items():
        if isinstance(v, (int, float)) and k == "fonte_reflora_id":
            v = str(int(v))
        if isinstance(v, str):
            v = " ".join(v.split())
        args[k] = v
    if "fonte_reflora_id" in args and isinstance(args["fonte_reflora_id"], str):
        fid = args["fonte_reflora_id"].strip().strip("'\"")
        args["fonte_reflora_id"] = "indeterminado" if fid.lower().startswith("indetermin") else fid
    if "confianca" in args and isinstance(args["confianca"], str):
        c = "".join(ch for ch in unicodedata.normalize("NFD", args["confianca"].lower()) if unicodedata.category(ch) != "Mn")
        args["confianca"] = c
    return args


# --------------------------------------------------------------------------- modelo
def chamar(modelo: str, historico: list[dict], tools: list[dict], think: bool, seed: int) -> dict:
    corpo = {"model": modelo, "messages": historico, "tools": tools, "stream": False, "think": think,
             "options": {"temperature": 0, "seed": seed}}
    req = urllib.request.Request(f"{OLLAMA}/api/chat", data=json.dumps(corpo).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.load(r)["message"]


# --------------------------------------------------------------------------- laço
def processar(item: dict, ref: Referencia, spec: dict, tools: list[dict], cfg: argparse.Namespace) -> tuple[dict, list]:
    candidatos = [c["fonte_reflora_id"] for c in item["campos"]["candidatos"]]
    executores = {  # LISTA BRANCA: só estas três executam; registrar é tratado à parte
        "consultar_nome_popular": lambda a: ref.consultar_nome_popular(str(a["nome"])),
        "consultar_especie": lambda a: ref.consultar_especie(str(a["fonte_reflora_id"])),
        "buscar_semelhante": lambda a: ref.buscar_semelhante(str(a["nome"]), a.get("limite", 5)),
    }
    obrigatorios = {t["function"]["name"]: t["function"]["parameters"]["required"] for t in tools}

    historico = [{"role": "system", "content": spec["sistema"]},
                 {"role": "user", "content": f"Nome popular: {item['texto']}"}]
    chamadas, invalidas, sem_tool = [], 0, 0
    t0 = time.monotonic()
    resultado = None
    passo = 0
    for passo in range(1, cfg.max_passos + 1):
        msg = chamar(cfg.modelo, historico, tools, cfg.think, cfg.seed)
        historico.append({k: msg[k] for k in ("role", "content", "tool_calls") if k in msg})
        calls = msg.get("tool_calls") or []
        if not calls:
            sem_tool += 1
            historico.append({"role": "user", "content": "Responda chamando uma ferramenta. Para encerrar, chame registrar."})
            continue
        for call in calls:
            nome = call.get("function", {}).get("name", "")
            args = normalizar_args(call.get("function", {}).get("arguments", {}))
            chamadas.append({"passo": passo, "ferramenta": nome, "args": args})
            if "_erro" in args:
                saida = {"erro": args["_erro"]}
            elif nome not in obrigatorios:
                saida = {"erro": f"ferramenta '{nome}' não existe; use uma de {sorted(obrigatorios)}"}
            elif faltando := [p for p in obrigatorios[nome] if p not in args]:
                saida = {"erro": f"faltam parâmetros obrigatórios: {faltando}"}
            elif nome == "registrar":
                fid, conf = args["fonte_reflora_id"], args["confianca"]
                if fid != "indeterminado" and fid not in candidatos:
                    saida = {"erro": f"fonte_reflora_id '{fid}' não é candidato; escolha entre {candidatos} ou 'indeterminado'"}
                elif conf not in ("alta", "media", "baixa"):
                    saida = {"erro": "confianca deve ser alta, media ou baixa"}
                else:
                    resultado = {"fonte_reflora_id": None if fid == "indeterminado" else fid,
                                 "indeterminado": fid == "indeterminado", "confianca": conf,
                                 "justificativa": args.get("justificativa", "")}
                    break
            else:
                try:
                    saida = executores[nome](args)
                except (KeyError, TypeError, ValueError) as e:
                    saida = {"erro": f"argumentos inválidos: {e}"}
            if "erro" in saida:
                invalidas += 1
            historico.append({"role": "tool", "tool_name": nome, "content": json.dumps(saida, ensure_ascii=False)})
        if resultado:
            break

    linha = {
        "id": item["id"], "texto": item["texto"], "candidatos": candidatos,
        "resolvido": resultado is not None,
        "fonte_reflora_id": resultado["fonte_reflora_id"] if resultado else None,
        "indeterminado": resultado["indeterminado"] if resultado else None,
        "confianca": resultado["confianca"] if resultado else None,
        "justificativa": resultado["justificativa"] if resultado else None,
        "motivo_nao_resolvido": None if resultado else f"estourou o teto de {cfg.max_passos} passos sem registrar válido",
        "formato_valido": resultado is not None,
        "passos": passo, "chamadas_invalidas": invalidas, "respostas_sem_ferramenta": sem_tool,
        "tempo_s": round(time.monotonic() - t0, 2), "chamadas": chamadas,
    }
    return linha, historico


# --------------------------------------------------------------------------- execução
def digest_modelo(modelo: str) -> str | None:
    try:
        with urllib.request.urlopen(f"{OLLAMA}/api/tags", timeout=10) as r:
            for m in json.load(r)["models"]:
                if m["name"] == modelo:
                    return m["digest"]
    except OSError:
        return None
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, choices=["pobre", "boa"])
    ap.add_argument("--itens", required=True, choices=["gabarito", "ambiguos"])
    ap.add_argument("--rodada", required=True, help="nome da pasta em execucoes/")
    ap.add_argument("--modelo", default="qwen3:1.7b")
    ap.add_argument("--max-passos", type=int, default=6)
    ap.add_argument("--think", action="store_true", help="liga o modo thinking (padrão: desligado)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--limite", type=int, default=0, help="processa só os N primeiros (teste)")
    cfg = ap.parse_args()
    if cfg.modelo.endswith(":latest") or ":" not in cfg.modelo:
        raise SystemExit("modelo precisa de tag explícita (nada de :latest)")

    spec_path = AQUI / "especificacoes" / f"{cfg.spec}.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    ref = Referencia(spec["arquivo_regras"])
    tools = montar_tools(spec)

    if cfg.itens == "gabarito":
        ids = [g["id"] for g in _jsonl(AQUI / "gabarito.jsonl")]
        por_id = {it["id"]: it for it in ref.corpus}
        itens = [por_id[i] for i in ids]
    else:
        itens = [it for it in ref.corpus if it["campos"]["ambiguo"]]
    if cfg.limite:
        itens = itens[: cfg.limite]

    pasta = AQUI / "execucoes" / cfg.rodada
    pasta.mkdir(parents=True, exist_ok=True)
    arquivos_spec = [spec_path] + ([AQUI / spec["arquivo_regras"]] if spec["arquivo_regras"] else [])
    meta = {
        "rodada": cfg.rodada, "spec": cfg.spec, "itens": cfg.itens, "n_itens": len(itens),
        "modelo": cfg.modelo, "digest_modelo": digest_modelo(cfg.modelo),
        "temperature": 0, "seed": cfg.seed, "think": cfg.think, "max_passos": cfg.max_passos,
        "sha256_spec": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in arquivos_spec},
        "git_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=AQUI, capture_output=True, text=True).stdout.strip(),
        "git_nao_commitado": subprocess.run(["git", "status", "--porcelain", "."], cwd=AQUI, capture_output=True, text=True).stdout.split("\n")[:20],
        "maquina": {"so": platform.platform(), "cpu": _cpu(), "ram_gb": _ram_gb(), "gpu": "integrada (AMD Radeon/Barcelo), sem GPU dedicada"},
        "inicio": dt.datetime.now().isoformat(timespec="seconds"),
        "observacao": "temperature 0 e seed fixa; mesmo assim a saída pode variar entre rodadas (threads/CPU).",
    }
    t0 = time.monotonic()
    with (pasta / "saida.jsonl").open("w", encoding="utf-8") as fs, (pasta / "transcricoes.jsonl").open("w", encoding="utf-8") as ft:
        for n, item in enumerate(itens, 1):
            linha, historico = processar(item, ref, spec, tools, cfg)
            fs.write(json.dumps(linha, ensure_ascii=False) + "\n"); fs.flush()
            ft.write(json.dumps({"id": item["id"], "historico": historico}, ensure_ascii=False) + "\n"); ft.flush()
            r = linha["fonte_reflora_id"] or ("indeterminado" if linha["indeterminado"] else "NÃO RESOLVIDO")
            print(f"[{n}/{len(itens)}] {item['texto']!r} → {r} · {linha['passos']} passos · {linha['tempo_s']}s", flush=True)
    meta["fim"] = dt.datetime.now().isoformat(timespec="seconds")
    meta["tempo_total_s"] = round(time.monotonic() - t0, 1)
    (pasta / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _cpu() -> str:
    try:
        for l in Path("/proc/cpuinfo").read_text().splitlines():
            if l.startswith("model name"):
                return l.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor()


def _ram_gb() -> float | None:
    try:
        kb = int(Path("/proc/meminfo").read_text().split()[1])
        return round(kb / 1024 / 1024, 1)
    except (OSError, ValueError, IndexError):
        return None


if __name__ == "__main__":
    main()
