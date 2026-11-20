#!/usr/bin/env python3
"""Trabalho 2 · Etapa 2 — medição de uma ou mais rodadas contra o gabarito.

Para cada rodada: formato válido, acurácia, tempo total, passos por item e itens não
resolvidos (§5.4), mais a matriz de confusão e a lista de erros para comentar.
Com duas rodadas, também lista os erros que persistiram nas duas.

Uso: python3 medir.py exec1-pobre exec2-boa
Saída: execucoes/<rodada>/metricas.json e execucoes/MEDICOES.md (ou o nome dado em --saida=)
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
EXEC = AQUI / "execucoes"
COLS = ["mesma espécie do gabarito", "outra espécie", "indeterminado", "não resolvido"]


def _jsonl(p: Path) -> list[dict]:
    with p.open(encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def desfecho(g: dict, s: dict) -> str:
    if not s["resolvido"]:
        return "não resolvido"
    if s["indeterminado"]:
        return "indeterminado"
    return "mesma espécie do gabarito" if s["fonte_reflora_id"] == g["rotulo_fonte_reflora_id"] else "outra espécie"


def acertou(g: dict, s: dict) -> bool:
    if not s["resolvido"]:
        return False
    if g["indeterminado"]:
        return bool(s["indeterminado"])
    return s["fonte_reflora_id"] == g["rotulo_fonte_reflora_id"]


def medir(rodada: str, gabarito: dict[str, dict], especies: dict[str, str]) -> dict:
    pasta = EXEC / rodada
    saida = {s["id"]: s for s in _jsonl(pasta / "saida.jsonl")}
    meta = json.loads((pasta / "meta.json").read_text(encoding="utf-8"))
    faltam = sorted(set(gabarito) - set(saida))
    if faltam:
        raise SystemExit(f"{rodada}: faltam {len(faltam)} itens do gabarito na saída")

    linhas = {"decidido": Counter(), "indeterminado": Counter()}
    erros, por_conf = [], {}
    for i, g in gabarito.items():
        s = saida[i]
        linha = "indeterminado" if g["indeterminado"] else "decidido"
        d = desfecho(g, s)
        linhas[linha][d] += 1
        ok = acertou(g, s)
        c = s["confianca"] or "—"
        por_conf.setdefault(c, [0, 0])
        por_conf[c][0] += ok
        por_conf[c][1] += 1
        if not ok:
            erros.append({
                "id": i, "texto": g["texto"],
                "gabarito": "indeterminado" if g["indeterminado"] else f"{especies[g['rotulo_fonte_reflora_id']]} ({g['rotulo_fonte_reflora_id']})",
                "gabarito_justificativa": g["justificativa"],
                "modelo": d if d in ("indeterminado", "não resolvido") else f"{especies[s['fonte_reflora_id']]} ({s['fonte_reflora_id']})",
                "modelo_confianca": s["confianca"], "modelo_justificativa": s["justificativa"],
                "ferramentas": [c["ferramenta"] for c in s["chamadas"]],
            })

    n = len(gabarito)
    decididos = [i for i, g in gabarito.items() if not g["indeterminado"]]
    passos = [saida[i]["passos"] for i in gabarito]
    m = {
        "rodada": rodada, "spec": meta["spec"], "modelo": meta["modelo"], "digest_modelo": meta["digest_modelo"],
        "n_itens": n,
        "formato_valido": sum(saida[i]["formato_valido"] for i in gabarito),
        "acuracia": round(sum(acertou(gabarito[i], saida[i]) for i in gabarito) / n, 3),
        "acuracia_decididos": round(sum(acertou(gabarito[i], saida[i]) for i in decididos) / len(decididos), 3),
        "n_decididos": len(decididos),
        "tempo_total_s": meta["tempo_total_s"],
        "passos_media": round(statistics.mean(passos), 2), "passos_mediana": statistics.median(passos), "passos_max": max(passos),
        "nao_resolvidos": sum(not saida[i]["resolvido"] for i in gabarito),
        "chamadas_invalidas": sum(saida[i]["chamadas_invalidas"] for i in gabarito),
        "respostas_sem_ferramenta": sum(saida[i]["respostas_sem_ferramenta"] for i in gabarito),
        "matriz": {k: {c: v.get(c, 0) for c in COLS} for k, v in linhas.items()},
        "acuracia_por_confianca": {c: {"acertos": a, "itens": t} for c, (a, t) in sorted(por_conf.items())},
        "erros": erros,
    }
    (pasta / "metricas.json").write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return m


def relatorio(ms: list[dict]) -> str:
    L = ["# Medições (gerado por `medir.py`)", "",
         "| Medida | " + " | ".join(m["rodada"] for m in ms) + " |", "|---|" + "---|" * len(ms)]
    def row(nome, f):
        L.append(f"| {nome} | " + " | ".join(f(m) for m in ms) + " |")
    row("Especificação", lambda m: m["spec"])
    row("Formato válido", lambda m: f"{m['formato_valido']}/{m['n_itens']}")
    row("**Acurácia** (indeterminado conta como classe)", lambda m: f"**{m['acuracia']:.1%}**")
    row("Acurácia só nos itens decididos no gabarito", lambda m: f"{m['acuracia_decididos']:.1%} (n={m['n_decididos']})")
    row("Tempo total", lambda m: f"{m['tempo_total_s']/60:.1f} min")
    row("Passos por item (média · mediana · máx.)", lambda m: f"{m['passos_media']} · {m['passos_mediana']} · {m['passos_max']}")
    row("Itens não resolvidos", lambda m: str(m["nao_resolvidos"]))
    row("Chamadas inválidas · respostas sem ferramenta", lambda m: f"{m['chamadas_invalidas']} · {m['respostas_sem_ferramenta']}")
    for m in ms:
        L += ["", f"## Matriz de confusão · {m['rodada']}", "",
              "| gabarito ↓ / modelo → | " + " | ".join(COLS) + " |", "|---|" + "---|" * len(COLS)]
        for k, v in m["matriz"].items():
            L.append(f"| {k} | " + " | ".join(str(v[c]) for c in COLS) + " |")
        L += ["", "Acurácia por confiança declarada: " + " · ".join(
            f"{c}: {v['acertos']}/{v['itens']}" for c, v in m["acuracia_por_confianca"].items())]
        L += ["", f"### Erros · {m['rodada']} ({len(m['erros'])})", "",
              "| id | nome | gabarito | modelo | conf. | ferramentas |", "|---|---|---|---|---|---|"]
        for e in m["erros"]:
            L.append(f"| {e['id']} | `{e['texto']}` | {e['gabarito']} | {e['modelo']} | {e['modelo_confianca'] or '—'} | {' → '.join(e['ferramentas'])} |")
    if len(ms) >= 2:
        persist = sorted(set(e["id"] for e in ms[0]["erros"]) & set(e["id"] for e in ms[-1]["erros"]))
        por_id = {e["id"]: e for e in ms[-1]["erros"]}
        L += ["", f"## Erros que persistiram em {ms[0]['rodada']} e {ms[-1]['rodada']} ({len(persist)})", ""]
        L += [f"- {i} `{por_id[i]['texto']}`: gabarito {por_id[i]['gabarito']}; modelo {por_id[i]['modelo']}" for i in persist]
    return "\n".join(L) + "\n"


def main() -> None:
    args = sys.argv[1:]
    saida_md = "MEDICOES.md"
    if args and args[0].startswith("--saida="):  # ex.: --saida=MEDICOES-modelos.md exec2-boa exec3-boa-gemma
        saida_md, args = args[0].split("=", 1)[1], args[1:]
    rodadas = args or ["exec1-pobre", "exec2-boa"]
    gabarito = {g["id"]: g for g in _jsonl(AQUI / "gabarito.jsonl")}
    especies = {e["fonte_reflora_id"]: e["nome_cientifico"] for e in _jsonl(AQUI.parent / "coleta" / "especies_pb.jsonl")}
    ms = [medir(r, gabarito, especies) for r in rodadas]
    (EXEC / saida_md).write_text(relatorio(ms), encoding="utf-8")
    for m in ms:
        print(f"{m['rodada']}: acurácia {m['acuracia']:.1%} · decididos {m['acuracia_decididos']:.1%} · "
              f"válido {m['formato_valido']}/{m['n_itens']} · não resolvidos {m['nao_resolvidos']} · {m['tempo_total_s']/60:.1f} min")


if __name__ == "__main__":
    main()
