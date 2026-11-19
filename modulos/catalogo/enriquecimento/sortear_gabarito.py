#!/usr/bin/env python3
"""Trabalho 2 · Etapa 2 — sorteio reprodutível dos 40 itens do gabarito.

Sorteia só entre os itens ambíguos do corpus (n_candidatos > 1): nos demais o nome
aponta para uma única espécie e a resposta sai de uma consulta, sem modelo.

Gera dois arquivos, ambos SEM rótulo:
  gabarito.jsonl  — os 40 itens com os campos de rótulo vazios (null), para preencher à mão
  ROTULAGEM.md    — folha de leitura: candidatos, família, origem, localidades e link da ficha Reflora

Não sobrescreve um gabarito existente (para não apagar rótulos), a não ser com --forcar.
Uso: python3 sortear_gabarito.py [--forcar]
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

SEMENTE = 20261126  # fixa: o mesmo corpus sempre sorteia os mesmos 40
N = 40

AQUI = Path(__file__).resolve().parent
CORPUS = AQUI.parent / "coleta" / "corpus.jsonl"
ESPECIES = AQUI.parent / "coleta" / "especies_pb.jsonl"
SAIDA = AQUI / "gabarito.jsonl"
FOLHA = AQUI / "ROTULAGEM.md"


def carregar(caminho: Path) -> list[dict]:
    with caminho.open(encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def main() -> None:
    if SAIDA.exists() and "--forcar" not in sys.argv:
        sys.exit(f"{SAIDA.name} já existe; não vou sobrescrever rótulos. Use --forcar se for mesmo o caso.")

    corpus = carregar(CORPUS)
    especies = {e["fonte_reflora_id"]: e for e in carregar(ESPECIES)}
    ambiguos = sorted((it for it in corpus if it["campos"]["ambiguo"]), key=lambda it: it["id"])
    sorteados = sorted(random.Random(SEMENTE).sample(ambiguos, N), key=lambda it: it["id"])

    with SAIDA.open("w", encoding="utf-8", newline="\n") as f:
        for it in sorteados:
            f.write(json.dumps({
                "id": it["id"],
                "texto": it["texto"],
                "candidatos": [c["fonte_reflora_id"] for c in it["campos"]["candidatos"]],
                "rotulo_fonte_reflora_id": None,  # id escolhido, ou null se indeterminado
                "indeterminado": None,            # true quando nenhum candidato predomina
                "justificativa": None,            # uma frase: por que essa espécie
            }, ensure_ascii=False) + "\n")

    linhas = [
        "# Folha de rotulagem do gabarito (gerada por `sortear_gabarito.py`)",
        "",
        f"{N} itens sorteados entre os {len(ambiguos)} nomes ambíguos do corpus · semente `{SEMENTE}`.",
        "Os critérios de rotulagem estão em `CRITERIOS_ROTULAGEM.md`. Os rótulos vão em `gabarito.jsonl`.",
        "",
    ]
    for it in sorteados:
        linhas.append(f"## {it['id']} · `{it['texto']}`")
        linhas.append("")
        linhas.append("| fonte_reflora_id | nome_cientifico | família | origem | domínios | localidades do nome | ficha |")
        linhas.append("|---|---|---|---|---|---|---|")
        for c in it["campos"]["candidatos"]:
            e = especies[c["fonte_reflora_id"]]
            linhas.append(
                f"| {c['fonte_reflora_id']} | *{c['nome_cientifico']}* | {c['familia']} | {c['origem']} | "
                f"{', '.join(e['dominios_fitogeograficos']) or '—'} | "
                f"{'; '.join(c['localidades_do_nome']) or '—'} | [Reflora]({e['referencia']}) |"
            )
        linhas.append("")
    FOLHA.write_text("\n".join(linhas), encoding="utf-8")
    print(f"{N} itens sorteados de {len(ambiguos)} ambíguos → {SAIDA.name}, {FOLHA.name}")


if __name__ == "__main__":
    main()
