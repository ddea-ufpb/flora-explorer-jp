#!/usr/bin/env python3
"""Trabalho 2 · Etapa 2 — monta dados.jsonl: o corpus inteiro, enriquecido.

- Nome com UM candidato (n_candidatos == 1): resolvido por regra, sem modelo (metodo = "regra").
- Nome ambíguo: resultado da rodada de produção do enriquecedor (metodo = "modelo").
- Item ambíguo que o modelo não resolveu (ou que não foi processado) continua no arquivo,
  com fonte_reflora_id nulo e motivo_nao_resolvido preenchido.

Uso: python3 gerar_dados.py [--rodada producao-boa]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
COLETA = AQUI.parent / "coleta"


def _jsonl(p: Path) -> list[dict]:
    with p.open(encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rodada", default="producao-boa")
    cfg = ap.parse_args()

    corpus = _jsonl(COLETA / "corpus.jsonl")
    especies = {e["fonte_reflora_id"]: e for e in _jsonl(COLETA / "especies_pb.jsonl")}
    pasta = AQUI / "execucoes" / cfg.rodada
    meta = json.loads((pasta / "meta.json").read_text(encoding="utf-8"))
    modelo = {s["id"]: s for s in _jsonl(pasta / "saida.jsonl")}

    saida, cont = [], {"regra": 0, "modelo": 0, "indeterminado": 0, "nao_resolvido": 0}
    for it in corpus:
        cand = it["campos"]["candidatos"]
        base = {"id": it["id"], "nome_popular": it["texto"], "variantes": it["campos"]["variantes"],
                "n_candidatos": len(cand), "candidatos": [c["fonte_reflora_id"] for c in cand]}
        if len(cand) == 1:
            fid, metodo, conf, just, motivo = cand[0]["fonte_reflora_id"], "regra", "alta", "único candidato na fonte", None
            cont["regra"] += 1
        else:
            s = modelo.get(it["id"])
            metodo = "modelo"
            if s is None:
                fid, conf, just, motivo = None, None, None, "item ambíguo não processado pelo enriquecedor"
            elif not s["resolvido"]:
                fid, conf, just, motivo = None, None, None, s["motivo_nao_resolvido"]
            elif s["indeterminado"]:
                fid, conf, just, motivo = None, s["confianca"], s["justificativa"], "indeterminado: as regras de desempate não separam os candidatos"
            else:
                fid, conf, just, motivo = s["fonte_reflora_id"], s["confianca"], s["justificativa"], None
            if fid:
                cont["modelo"] += 1
            elif s is not None and s["resolvido"]:
                cont["indeterminado"] += 1
            else:
                cont["nao_resolvido"] += 1
        e = especies.get(fid) if fid else None
        saida.append({
            **base,
            "fonte_reflora_id": fid,
            "nome_cientifico": e["nome_cientifico"] if e else None,
            "familia": e["familia"] if e else None,
            "origem": e["origem"] if e else None,
            "metodo": metodo,
            "confianca": conf,
            "justificativa": just,
            "motivo_nao_resolvido": motivo,
            "modelo": f"{meta['modelo']}@{meta['digest_modelo'][:12]}" if metodo == "modelo" else None,
            "rodada": cfg.rodada if metodo == "modelo" else None,
            "fonte": it["fonte"], "coletado_em": it["coletado_em"], "chave": it["chave"],
        })

    with (AQUI / "dados.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for linha in saida:
            f.write(json.dumps(linha, ensure_ascii=False) + "\n")
    print(f"dados.jsonl: {len(saida)} itens · regra {cont['regra']} · modelo {cont['modelo']} · "
          f"indeterminado {cont['indeterminado']} · não resolvido {cont['nao_resolvido']}")


if __name__ == "__main__":
    main()
