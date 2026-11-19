#!/usr/bin/env python3
"""Trabalho 2 · Etapa 2 — carga no módulo catalogo.

Lê dados.jsonl e especies_pb.jsonl e gera:
  seed/especie_catalogo.sql       — INSERT … ON CONFLICT (nome_cientifico) DO UPDATE, idempotente
  seed/especie_nome_popular.sql   — PROPOSTA de tabela nome popular → espécie (ver ESQUEMA.md)
  seed/revisao_pendente.jsonl     — o que NÃO entra sem revisão humana: confiança baixa,
                                    indeterminado e não resolvido

Regra de entrada (§5.2 do tutorial): só entra no módulo o mapeamento com confiança alta ou média.

Uso:
  python3 carregar.py                     # gera os arquivos .sql
  python3 carregar.py --testar-sqlite     # gera e executa contra um SQLite em memória
  psql "$DATABASE_URL" -f seed/especie_catalogo.sql   # carga real no Postgres do módulo
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from collections import defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent
COLETA = AQUI.parent / "coleta"
SEED = AQUI / "seed"
ENTRA = {"alta", "media"}


def _jsonl(p: Path) -> list[dict]:
    with p.open(encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def q(v) -> str:
    """Literal SQL: NULL, número ou texto com aspas simples escapadas."""
    if v is None:
        return "NULL"
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def n_linhas(fonte: str) -> int:
    return fonte.rsplit(":", 1)[-1].count("L")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--testar-sqlite", action="store_true")
    cfg = ap.parse_args()

    dados = _jsonl(AQUI / "dados.jsonl")
    especies = {e["fonte_reflora_id"]: e for e in _jsonl(COLETA / "especies_pb.jsonl")}

    aceitos = [d for d in dados if d["fonte_reflora_id"] and d["confianca"] in ENTRA]
    revisao = [d for d in dados if d not in aceitos]

    # nome_popular principal de cada espécie: o nome aceito com mais registros na fonte; empate → alfabético
    nomes = defaultdict(list)
    for d in aceitos:
        nomes[d["fonte_reflora_id"]].append((-n_linhas(d["fonte"]), d["nome_popular"]))
    principal = {fid: sorted(v)[0][1] for fid, v in nomes.items()}

    SEED.mkdir(exist_ok=True)
    cat = ["-- Gerado por carregar.py a partir de especies_pb.jsonl e dados.jsonl. Idempotente.",
           "-- id = fonte_reflora_id (inteiro estável entre cargas). descricao/curiosidade ficam NULL:",
           "-- pela ADR-0006 são revisados manualmente na importação.",
           "BEGIN;"]
    for fid in sorted(especies, key=int):
        e = especies[fid]
        cols = {
            "id": int(fid), "nome_cientifico": e["nome_cientifico"], "nome_popular": principal.get(fid),
            "familia": e["familia"], "bioma": ", ".join(e["dominios_fitogeograficos"]) or None,
            "origem": e["origem"], "status_ameaca": "nao_avaliada", "descricao": None, "curiosidade": None,
            "foto_referencia_url": None, "fonte_reflora_id": fid,
        }
        atualiza = ", ".join(f"{c} = excluded.{c}" for c in cols if c not in ("id", "nome_cientifico", "descricao", "curiosidade", "foto_referencia_url"))
        cat.append(f"INSERT INTO especie_catalogo ({', '.join(cols)}) VALUES ({', '.join(q(v) for v in cols.values())}) "
                   f"ON CONFLICT (nome_cientifico) DO UPDATE SET {atualiza};")
    cat.append("COMMIT;")
    (SEED / "especie_catalogo.sql").write_text("\n".join(cat) + "\n", encoding="utf-8")

    np = ["-- PROPOSTA (ver ESQUEMA.md, 'decisão que muda'): especie_catalogo.nome_popular guarda um nome só,",
          "-- mas a fonte tem vários nomes por espécie e nomes que apontam para várias espécies.",
          "CREATE TABLE IF NOT EXISTS especie_nome_popular (",
          "  nome_popular text NOT NULL,",
          "  especie_id int NOT NULL REFERENCES especie_catalogo(id),",
          "  metodo text NOT NULL CHECK (metodo IN ('regra', 'modelo')),",
          "  confianca text NOT NULL CHECK (confianca IN ('alta', 'media')),",
          "  PRIMARY KEY (nome_popular)",
          ");",
          "BEGIN;"]
    for d in sorted(aceitos, key=lambda d: d["nome_popular"]):
        np.append(f"INSERT INTO especie_nome_popular (nome_popular, especie_id, metodo, confianca) VALUES "
                  f"({q(d['nome_popular'])}, {int(d['fonte_reflora_id'])}, {q(d['metodo'])}, {q(d['confianca'])}) "
                  f"ON CONFLICT (nome_popular) DO UPDATE SET especie_id = excluded.especie_id, "
                  f"metodo = excluded.metodo, confianca = excluded.confianca;")
    np.append("COMMIT;")
    (SEED / "especie_nome_popular.sql").write_text("\n".join(np) + "\n", encoding="utf-8")

    with (SEED / "revisao_pendente.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for d in revisao:
            f.write(json.dumps({k: d[k] for k in ("id", "nome_popular", "candidatos", "fonte_reflora_id", "confianca",
                                                  "motivo_nao_resolvido", "justificativa")}, ensure_ascii=False) + "\n")

    print(f"especie_catalogo.sql: {len(especies)} espécies · especie_nome_popular.sql: {len(aceitos)} nomes · "
          f"revisao_pendente.jsonl: {len(revisao)}")

    if cfg.testar_sqlite:
        con = sqlite3.connect(":memory:")
        con.executescript("""
            CREATE TABLE especie_catalogo (
              id int PRIMARY KEY, nome_cientifico text UNIQUE, nome_popular text, familia text, bioma text,
              origem text CHECK (origem IN ('nativa','exotica','exotica_invasora')), status_ameaca text,
              descricao text, curiosidade text, foto_referencia_url text, fonte_reflora_id text);""")
        for _ in range(2):  # duas cargas seguidas: a segunda não pode duplicar
            con.executescript((SEED / "especie_catalogo.sql").read_text(encoding="utf-8"))
            con.executescript((SEED / "especie_nome_popular.sql").read_text(encoding="utf-8"))
        n_esp = con.execute("SELECT count(*) FROM especie_catalogo").fetchone()[0]
        n_nom = con.execute("SELECT count(*) FROM especie_nome_popular").fetchone()[0]
        por_origem = dict(con.execute("SELECT origem, count(*) FROM especie_catalogo GROUP BY origem").fetchall())
        assert n_esp == len(especies) and n_nom == len(aceitos), (n_esp, n_nom)
        print(f"[sqlite] carga dupla OK: {n_esp} espécies {por_origem} · {n_nom} nomes populares")


if __name__ == "__main__":
    main()
