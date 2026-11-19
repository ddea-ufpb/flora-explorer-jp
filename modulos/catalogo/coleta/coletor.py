#!/usr/bin/env python3
"""Trabalho 2 · Etapa 1 — coletor do catálogo de espécies da Paraíba.

Fonte: Flora e Funga do Brasil – Lista Oficial (JBRJ/REFLORA), Darwin Core Archive.
Recorte: espécies de plantas (nome aceito) com ocorrência em BR-PB e seus nomes populares.

Item do corpus = um nome popular em português (agrupado por grafia sem acento),
com as espécies da PB a que a fonte o associa. É esse nome que a Etapa 2 vai julgar.

Esqueleto (§4.2 do tutorial): obter → extrair → normalizar → deduplicar → gravar.
Nenhum modelo de linguagem é usado aqui. Só biblioteca padrão do Python.

Uso:  python3 coletor.py            (reaproveita o bruto se já existir)
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json
import re
import sys
import unicodedata
import urllib.request
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

# --------------------------------------------------------------------------- config
VERSAO = "393.433"  # versão fixa do recurso no IPT: reprodutibilidade
URL = f"https://ipt.jbrj.gov.br/jbrj/archive.do?r=lista_especies_flora_brasil&v={VERSAO}"
PAGINA = "https://ipt.jbrj.gov.br/jbrj/resource?r=lista_especies_flora_brasil"
LICENCA = "CC-BY 4.0"
UF = "BR-PB"
PREFIXO_BRUTO = f"flora-brasil-lista-oficial_v{VERSAO}_"

AQUI = Path(__file__).resolve().parent
BRUTO = AQUI / "bruto"
SAIDA_CORPUS = AQUI / "corpus.jsonl"
SAIDA_ESPECIES = AQUI / "especies_pb.jsonl"
SAIDA_DESCARTES = AQUI / "descartes.jsonl"
SAIDA_REGRAS = AQUI / "REGRAS.md"

csv.field_size_limit(10**9)


# --------------------------------------------------------------------------- regras
@dataclass(frozen=True)
class Regra:
    codigo: str
    tipo: str  # "descarte" | "transformação" | "agrupamento" | "derivação"
    descricao: str
    motivo: str  # item do bruto que motivou a regra


REGRAS = [
    Regra("R01", "descarte", "Táxon sem ocorrência em BR-PB (distribution.txt) fica fora do corpus: `DESCARTE(fora do recorte)`",
          "Recorte declarado em FONTE.md. Ex.: vernacularname.txt L2 `guambixima` (id 274) não tem ocorrência em BR-PB"),
    Regra("R02", "descarte", "Táxon do reino `Fungi` é descartado: o catálogo do jogo é só de plantas",
          "514 dos 3.494 táxons da PB são fungos; ex.: id 94847 *Glomus sinuosum* tem ocorrência em BR-PB"),
    Regra("R03", "descarte", "`taxonRank` diferente de `ESPECIE` (variedade, subespécie, forma) é descartado: `especie_catalogo` trabalha em nível de espécie",
          "vernacularname.txt L5126 `angico-­verdadeiro` aponta para *Mimosa arenosa* var. *arenosa*"),
    Regra("R04", "descarte", "Nome popular com `language` diferente de `PORTUGUES` é descartado: o público do app é de JP",
          "vernacularname.txt L1995 `barin pakex kabia` (KAXINAWA), *Piper arboreum*"),
    Regra("R05", "transformação", "Caracteres invisíveis (soft hyphen U+00AD, zero-width, BOM) são removidos do nome popular",
          "vernacularname.txt L5126 `angico-\\xadverdadeiro` e L5127 `calumbí-\\xadpreto` (no v393.433 ambos caem antes em R03, por serem variedade; a regra fica para lotes futuros)"),
    Regra("R06", "transformação", "Hífens tipográficos (U+02D7, U+2010–U+2014, U+2212) viram `-`",
          "vernacularname.txt L5176 `calumbi˗de˗riacho` (U+02D7)"),
    Regra("R07", "transformação", "Apóstrofos variantes (`` ` ``, `´`, `’`, `‘`) viram `'`",
          "vernacularname.txt L6785 `lentilha-d`água`; L1847 `juti´airimbo`"),
    Regra("R08", "transformação", "Aspas tipográficas ao redor do nome são removidas",
          "vernacularname.txt L4557 `“lodinho-branco”`"),
    Regra("R09", "transformação", "Espaços colapsados e aparados nas pontas",
          "Prevenção: nenhum caso no bruto v393.433 (verificado na exploração); a regra fica para lotes futuros"),
    Regra("R10", "transformação", "Nome popular em minúsculas",
          "vernacularname.txt L1102 `Lagartissa`; L1956 `Dois de Julho`"),
    Regra("R11", "descarte", "Nome com `/` (alternativas condensadas num campo só) é descartado: separar as alternativas exigiria adivinhar",
          "vernacularname.txt L4672 `páo-/-pau-/-pao-marfim`"),
    Regra("R12", "descarte", "Nome popular vazio após a normalização é descartado",
          "Prevenção: nenhum caso no bruto v393.433; protege contra linhas só com caracteres removidos por R05–R08"),
    Regra("R13", "descarte", "Origem ausente ou conflitante na PB (`establishmentMeans` vazio ou com dois valores) é descartada",
          "21.537 linhas de distribution.txt têm `establishmentMeans` vazio (nenhuma em BR-PB no v393.433)"),
    Regra("R14", "derivação", "`origem` derivada por regra: `Nativa` → `nativa`, `Exótica` → `exotica`, a partir da linha BR-PB de distribution.txt",
          "distribution.txt: id 414 `BR-PB … Exótica`; id 461 `BR-PB … Nativa`"),
    Regra("R15", "agrupamento", "Duplicata exata (mesmo táxon + mesmo nome normalizado) conta uma vez só",
          "vernacularname.txt L395 e L402: `imbuzeiro` duas vezes para o mesmo táxon (id 4405)"),
    Regra("R16", "agrupamento", "Chave do item = nome sem acento e com espaço tratado como hífen; variantes de acento/espaço entram no mesmo item, em `variantes`",
          "vernacularname.txt L394 `taperebá` e L396 `tapereba`; L14049 `aveloz` e L14051 `avelóz`. Espaço vs. hífen (ex.: L1211 `mamão de porca`) não gerou fusão no v393.433"),
]
R = {r.codigo: r for r in REGRAS}


class Descarte(Exception):
    def __init__(self, codigo: str, motivo: str):
        super().__init__(motivo)
        self.codigo = codigo
        self.motivo = motivo


# --------------------------------------------------------------------------- 1. OBTER
def obter(destino: Path = BRUTO) -> Path:
    """Baixa o DwC-A uma única vez e guarda o bruto com a data da coleta no nome.

    Se já existir um bruto desta versão, ele é reaproveitado: rodar de novo não baixa
    nem muda nada. Uma única requisição; não há paginação, logo não há intervalo a respeitar.
    """
    destino.mkdir(parents=True, exist_ok=True)
    existentes = sorted(destino.glob(PREFIXO_BRUTO + "*.zip"))
    if existentes:
        print(f"[obter] reaproveitando {existentes[0].name}")
        return existentes[0]
    hoje = dt.date.today().isoformat()
    alvo = destino / f"{PREFIXO_BRUTO}{hoje}.zip"
    print(f"[obter] baixando {URL}")
    req = urllib.request.Request(URL, headers={"User-Agent": "flora-explorer-jp-coletor/1.0 (trabalho academico)"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        dados = resp.read()
    if not zipfile.is_zipfile(io.BytesIO(dados)):
        sys.exit("[obter] a resposta não é um arquivo zip; abortando sem gravar")
    alvo.write_bytes(dados)
    (destino / f"{alvo.stem}.proveniencia.json").write_text(json.dumps({
        "url": URL, "pagina": PAGINA, "versao": VERSAO, "licenca": LICENCA,
        "baixado_em": hoje, "bytes": len(dados),
        "sha256": hashlib.sha256(dados).hexdigest(),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return alvo


# --------------------------------------------------------------------------- 2. EXTRAIR
def _tsv(z: zipfile.ZipFile, nome: str):
    """Lê um arquivo do DwC-A com o parser csv (TSV sem aspas, conforme meta.xml)."""
    with z.open(nome) as f:
        texto = io.TextIOWrapper(f, encoding="utf-8", newline="")
        leitor = csv.DictReader(texto, delimiter="\t", quoting=csv.QUOTE_NONE)
        for linha_n, row in enumerate(leitor, start=2):  # linha 1 é o cabeçalho
            yield linha_n, row


def extrair(arquivo: Path) -> dict:
    """Do DwC-A para registros: táxons, ocorrência em BR-PB, sinônimos e nomes populares."""
    with zipfile.ZipFile(arquivo) as z:
        taxons = {row["id"]: row for _, row in _tsv(z, "taxon.txt")}

        dist_pb: dict[str, list[dict]] = defaultdict(list)
        for _, row in _tsv(z, "distribution.txt"):
            if row["locationID"] == UF:
                dist_pb[row["id"]].append(row)

        sinonimos: dict[str, list[str]] = defaultdict(list)
        for row in taxons.values():
            if row["taxonomicStatus"] == "SINONIMO" and row["acceptedNameUsageID"]:
                sinonimos[row["acceptedNameUsageID"]].append(row["scientificName"])

        vernaculos = [(n, row) for n, row in _tsv(z, "vernacularname.txt")]
    print(f"[extrair] {len(taxons)} táxons · {len(dist_pb)} com ocorrência em {UF} · {len(vernaculos)} nomes populares")
    return {"taxons": taxons, "dist_pb": dist_pb, "sinonimos": sinonimos, "vernaculos": vernaculos}


# --------------------------------------------------------------------------- 3. NORMALIZAR
INVISIVEIS = re.compile("[­​‌‍﻿]")
HIFENS = re.compile("[˗‐‑‒–—−]")
APOSTROFOS = re.compile("[`´’‘]")
ASPAS_PONTAS = "“”\""

ORIGEM = {"Nativa": "nativa", "Exótica": "exotica"}


def _aplica(cont: Counter, codigo: str, antes: str, depois: str) -> str:
    if antes != depois:
        cont[codigo] += 1
    return depois


def normalizar_nome(bruto: str, cont: Counter) -> str:
    s = _aplica(cont, "R05", bruto, INVISIVEIS.sub("", bruto))
    s = _aplica(cont, "R06", s, HIFENS.sub("-", s))
    s = _aplica(cont, "R07", s, APOSTROFOS.sub("'", s))
    s = _aplica(cont, "R08", s, s.strip(ASPAS_PONTAS))
    s = _aplica(cont, "R09", s, " ".join(s.split()))
    s = _aplica(cont, "R10", s, s.lower())
    if "/" in s:
        raise Descarte("R11", "nome com alternativas condensadas por '/'")
    if not s:
        raise Descarte("R12", "nome popular vazio após normalização")
    return s


def normalizar(linha_n: int, row: dict, ctx: dict, cont: Counter) -> dict:
    """Um nome popular bruto → registro normalizado, ou Descarte(motivo)."""
    tid = row["id"]
    tax = ctx["taxons"].get(tid)
    if tid not in ctx["dist_pb"]:
        raise Descarte("R01", f"táxon {tid} sem ocorrência em {UF}")
    if tax is None:
        raise Descarte("R01", f"táxon {tid} ausente de taxon.txt")
    if tax["kingdom"] != "Plantae":
        raise Descarte("R02", f"reino {tax['kingdom']}")
    if tax["taxonRank"] != "ESPECIE":
        raise Descarte("R03", f"nível {tax['taxonRank']}")
    if row["language"] != "PORTUGUES":
        raise Descarte("R04", f"idioma {row['language']}")
    meios = {d["establishmentMeans"] for d in ctx["dist_pb"][tid]}
    if len(meios) != 1 or next(iter(meios)) not in ORIGEM:
        raise Descarte("R13", f"origem ausente ou conflitante na PB: {sorted(meios)}")
    nome = normalizar_nome(row["vernacularName"], cont)
    return {
        "linha": linha_n,
        "nome": nome,
        "taxon_id": tid,
        "localidade": " ".join(row["locality"].split()),
    }


def especie(tid: str, ctx: dict) -> dict:
    tax = ctx["taxons"][tid]
    dist = ctx["dist_pb"][tid][0]
    try:
        obs = json.loads(dist["occurrenceRemarks"]) if dist["occurrenceRemarks"] else {}
    except json.JSONDecodeError:
        obs = {}
    return {
        "fonte_reflora_id": tid,
        "nome_cientifico": " ".join(p for p in (tax["genus"], tax["specificEpithet"]) if p),
        "autoria": tax["scientificNameAuthorship"],
        "familia": tax["family"],
        "origem": ORIGEM[dist["establishmentMeans"]],  # R14: derivação por regra, não por modelo
        "endemismo": obs.get("endemism"),
        "dominios_fitogeograficos": obs.get("phytogeographicDomain", []),
        "sinonimos": sorted(set(ctx["sinonimos"].get(tid, []))),
        "referencia": tax["references"],
    }


# --------------------------------------------------------------------------- 4. DEDUPLICAR
def chave_nome(nome: str) -> str:
    """R16: sem acento, espaço ≡ hífen. Estável: depende só do texto, não da posição."""
    sem_acento = "".join(c for c in unicodedata.normalize("NFD", nome) if unicodedata.category(c) != "Mn")
    return sem_acento.replace(" ", "-")


def chave(nome_chave: str) -> str:
    return hashlib.sha256(nome_chave.encode("utf-8")).hexdigest()[:16]


def deduplicar(registros: list[dict], cont: Counter) -> dict[str, dict]:
    grupos: dict[str, dict] = {}
    vistos: set[tuple[str, str]] = set()
    for r in registros:
        k = chave_nome(r["nome"])
        par = (r["taxon_id"], r["nome"])
        if par in vistos:
            cont["R15"] += 1
            continue
        vistos.add(par)
        g = grupos.setdefault(k, {"formas": Counter(), "linhas": [], "por_taxon": defaultdict(set)})
        g["formas"][r["nome"]] += 1
        g["linhas"].append(r["linha"])
        if r["localidade"]:
            g["por_taxon"][r["taxon_id"]].add(r["localidade"])
        else:
            g["por_taxon"][r["taxon_id"]]
    for g in grupos.values():
        if len(g["formas"]) > 1:
            cont["R16"] += 1
    return grupos


# --------------------------------------------------------------------------- 5. GRAVAR
def _jsonl(caminho: Path, linhas: list[dict]) -> None:
    # Reescreve o arquivo inteiro, em ordem determinística: rodar duas vezes não duplica.
    with caminho.open("w", encoding="utf-8", newline="\n") as f:
        for item in linhas:
            f.write(json.dumps(item, ensure_ascii=False, sort_keys=False) + "\n")


def gravar(grupos: dict[str, dict], especies: dict[str, dict], descartes: list[dict],
           cont: Counter, arquivo_bruto: Path) -> None:
    coletado_em = arquivo_bruto.stem.rsplit("_", 1)[-1]  # data do bruto, não de hoje
    fonte_base = f"{arquivo_bruto.name}:vernacularname.txt"

    itens = []
    for k in sorted(grupos):
        g = grupos[k]
        # forma canônica: a mais frequente; empate → ordem alfabética (determinístico)
        texto = sorted(g["formas"].items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        candidatos = [{
            "fonte_reflora_id": tid,
            "nome_cientifico": especies[tid]["nome_cientifico"],
            "familia": especies[tid]["familia"],
            "origem": especies[tid]["origem"],
            "localidades_do_nome": sorted(locs),
        } for tid, locs in sorted(g["por_taxon"].items(), key=lambda kv: especies[kv[0]]["nome_cientifico"])]
        itens.append({
            "texto": texto,
            "campos": {
                "nome_popular": texto,
                "variantes": sorted(g["formas"]),
                "n_candidatos": len(candidatos),
                "ambiguo": len(candidatos) > 1,
                "candidatos": candidatos,
            },
            "fonte": f"{fonte_base}:" + ",".join(f"L{n}" for n in sorted(g["linhas"])),
            "coletado_em": coletado_em,
            "chave": chave(k),
        })
    corpus = [{"id": f"flora-2026-{i:06d}", **item} for i, item in enumerate(itens, start=1)]
    _jsonl(SAIDA_CORPUS, corpus)

    usadas = sorted({c["fonte_reflora_id"] for it in itens for c in it["campos"]["candidatos"]},
                    key=lambda t: especies[t]["nome_cientifico"])
    _jsonl(SAIDA_ESPECIES, [especies[t] for t in usadas])
    _jsonl(SAIDA_DESCARTES, descartes)
    _regras_md(cont, corpus, descartes, len(usadas), coletado_em)
    amb = sum(1 for it in corpus if it["campos"]["ambiguo"])
    print(f"[gravar] corpus.jsonl: {len(corpus)} itens ({amb} ambíguos) · especies_pb.jsonl: {len(usadas)} · descartes.jsonl: {len(descartes)}")


def _regras_md(cont: Counter, corpus: list, descartes: list, n_especies: int, coletado_em: str) -> None:
    linhas = [
        "# REGRAS.md — normalização do corpus (gerado por `coletor.py`, não editar à mão)",
        "",
        f"Fonte: *Flora e Funga do Brasil – Lista Oficial*, DwC-A v{VERSAO}, {LICENCA}, {PAGINA} · bruto de {coletado_em}.",
        f"Resultado: **{len(corpus)} itens** no corpus · {n_especies} espécies de referência · {len(descartes)} linhas descartadas.",
        "",
        "Uma regra por linha. *Afetou* = linhas de `vernacularname.txt` (ou grupos, em R16) em que a regra disparou.",
        "",
        "| Regra | Tipo | O que faz | Item do bruto que motivou | Afetou |",
        "|---|---|---|---|---|",
    ]
    for r in REGRAS:
        linhas.append(f"| {r.codigo} | {r.tipo} | {r.descricao} | {r.motivo} | {cont.get(r.codigo, 0)} |")
    linhas += ["", "R14 afeta todas as espécies de referência (`especies_pb.jsonl`): "
               f"{n_especies} espécies, cada uma com `origem` vinda de `establishmentMeans`.", ""]
    SAIDA_REGRAS.write_text("\n".join(linhas), encoding="utf-8")


# --------------------------------------------------------------------------- main
def main() -> None:
    arquivo = obter()
    ctx = extrair(arquivo)
    cont: Counter = Counter()
    registros, descartes = [], []
    for linha_n, row in ctx["vernaculos"]:
        try:
            registros.append(normalizar(linha_n, row, ctx, cont))
        except Descarte as d:
            cont[d.codigo] += 1
            descartes.append({
                "fonte": f"{arquivo.name}:vernacularname.txt:L{linha_n}",
                "regra": d.codigo,
                "motivo": d.motivo,
                "bruto": {"id": row["id"], "vernacularName": row["vernacularName"],
                          "language": row["language"], "locality": row["locality"]},
            })
    tids = {r["taxon_id"] for r in registros}
    especies = {t: especie(t, ctx) for t in tids}
    cont["R14"] = len(especies)
    grupos = deduplicar(registros, cont)
    gravar(grupos, especies, descartes, cont, arquivo)


if __name__ == "__main__":
    main()
