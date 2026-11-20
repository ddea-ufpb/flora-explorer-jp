# ESQUEMA.md — o que o módulo `catalogo` recebe deste trabalho

**Para quem:** quem implementa o módulo `catalogo` (tabela `especie_catalogo`, telas A07 e A08).
**Nomes de campo:** o repositório ainda não tem `CONTRATOS.md`. Os nomes seguem `especificacoes/lucas-gabriel/arquitetura/contratos/modelo-dados.md` (tabela `especie_catalogo`) e a ADR-0006. Quando o `CONTRATOS.md` do grupo existir e divergir, o ajuste fica em `carregar.py`, não nos dados.

## Como usar (sem perguntar nada a ninguém)

```bash
cd modulos/catalogo/enriquecimento
python3 carregar.py --testar-sqlite          # gera seed/ e valida a carga dupla num SQLite em memória
psql "$DATABASE_URL" -f seed/especie_catalogo.sql
psql "$DATABASE_URL" -f seed/especie_nome_popular.sql   # opcional: cria a tabela proposta
```

Pré-requisito no Postgres: a tabela `especie_catalogo` do modelo de dados, com `UNIQUE (nome_cientifico)`. Os dois scripts são idempotentes: rodar de novo atualiza, não duplica. Só biblioteca padrão do Python 3.10+.

## `dados.jsonl` — um item por nome popular (2.413 linhas)

| Campo | Tipo | Obrig. | Significado |
|---|---|---|---|
| `id` | string | sim | Id estável do item no corpus (`flora-2026-NNNNNN`) |
| `nome_popular` | string | sim | Nome popular normalizado (minúsculas, grafia canônica). Ver `coleta/REGRAS.md` |
| `variantes` | string[] | sim | Grafias da fonte agrupadas neste item (ex.: `["tapereba", "taperebá"]`) |
| `n_candidatos` | int | sim | Quantas espécies da PB a fonte associa a este nome |
| `candidatos` | string[] | sim | `fonte_reflora_id` de cada candidata |
| `fonte_reflora_id` | string \| null | sim | **Espécie decidida.** Nulo quando indeterminado ou não resolvido. É o `especie_catalogo.fonte_reflora_id` e também o `id` usado no seed |
| `nome_cientifico` | string \| null | sim | `especie_catalogo.nome_cientifico` da espécie decidida (gênero + epíteto, sem autor) |
| `familia` | string \| null | sim | `especie_catalogo.familia` |
| `origem` | `nativa` \| `exotica` \| null | sim | `especie_catalogo.origem`. Vem **por regra** do `establishmentMeans` da fonte para BR-PB (R14), nunca do modelo. `exotica_invasora` não existe nesta fonte |
| `metodo` | `regra` \| `modelo` | sim | `regra`: o nome tem um único candidato. `modelo`: o nome é ambíguo e foi decidido por `qwen3:1.7b` |
| `confianca` | `alta` \| `media` \| `baixa` \| null | sim | Para `regra`, sempre `alta`. Para `modelo`, a declarada no `registrar`. **Nenhuma decisão do modelo entra no módulo sem revisão** (ver abaixo) |
| `justificativa` | string \| null | não | Frase do modelo (ou "único candidato na fonte") |
| `motivo_nao_resolvido` | string \| null | sim | Preenchido quando `fonte_reflora_id` é nulo: indeterminado, teto de passos estourado ou não processado |
| `modelo`, `rodada` | string \| null | não | Modelo com digest e rodada que decidiu (só `metodo = modelo`) |
| `fonte`, `coletado_em`, `chave` | string | sim | Proveniência: arquivo bruto e linhas, data da coleta e hash de deduplicação |

## O que `carregar.py` produz

| Arquivo | Conteúdo | Regra |
|---|---|---|
| `seed/especie_catalogo.sql` | Uma linha por espécie de `coleta/especies_pb.jsonl` (872) | `id = fonte_reflora_id`. `nome_popular` = nome aceito com mais registros na fonte (nulo se a espécie só tem nomes ambíguos não resolvidos). `bioma` = domínios fitogeográficos. `status_ameaca = 'nao_avaliada'`. `descricao`, `curiosidade` e `foto_referencia_url` ficam NULL (revisão manual, ADR-0006) |
| `seed/especie_nome_popular.sql` | **Proposta**: tabela `nome_popular → especie_id` | Só `metodo = regra` (nome com um único candidato na fonte) |
| `seed/revisao_pendente.jsonl` | Itens fora da carga | **Todo item decidido pelo modelo**, mais indeterminados e não resolvidos, com o motivo |

**Por que a decisão do modelo não entra direto, mesmo com confiança `alta`:** no gabarito, o modelo declarou `alta` em 40 de 40 itens e acertou 11 (`execucoes/MEDICOES.md`). A confiança declarada não separa acerto de erro, então não serve de filtro. Quem revisar `revisao_pendente.jsonl` pode mover itens para a carga à mão.

## Decisão que muda no projeto (item C4)

`modelo-dados.md` define `especie_catalogo.nome_popular` como **um** texto. A coleta mostrou que isso não representa o domínio: 872 espécies da PB têm 2.413 nomes populares, e 292 desses nomes apontam para mais de uma espécie. Proposta: manter `especie_catalogo.nome_popular` como nome de exibição e acrescentar `especie_nome_popular (nome_popular PK, especie_id FK, metodo, confianca)` para a busca por nome popular. A justificativa com os números medidos está em `RELATORIO.md`.
