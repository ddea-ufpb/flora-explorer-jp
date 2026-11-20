# REGRAS.md — normalização do corpus (gerado por `coletor.py`, não editar à mão)

Fonte: *Flora e Funga do Brasil – Lista Oficial*, DwC-A v393.433, CC-BY 4.0, https://ipt.jbrj.gov.br/jbrj/resource?r=lista_especies_flora_brasil · bruto de 2026-11-19.
Resultado: **2413 itens** no corpus · 872 espécies de referência · 16117 linhas descartadas.

Uma regra por linha. *Afetou* = linhas de `vernacularname.txt` (ou grupos, em R16) em que a regra disparou.

| Regra | Tipo | O que faz | Item do bruto que motivou | Afetou |
|---|---|---|---|---|
| R01 | descarte | Táxon sem ocorrência em BR-PB (distribution.txt) fica fora do corpus: `DESCARTE(fora do recorte)` | Recorte declarado em FONTE.md. Ex.: vernacularname.txt L2 `guambixima` (id 274) não tem ocorrência em BR-PB | 15762 |
| R02 | descarte | Táxon do reino `Fungi` é descartado: o catálogo do jogo é só de plantas | 514 dos 3.494 táxons da PB são fungos; ex.: id 94847 *Glomus sinuosum* tem ocorrência em BR-PB | 23 |
| R03 | descarte | `taxonRank` diferente de `ESPECIE` (variedade, subespécie, forma) é descartado: `especie_catalogo` trabalha em nível de espécie | vernacularname.txt L5126 `angico-­verdadeiro` aponta para *Mimosa arenosa* var. *arenosa* | 125 |
| R04 | descarte | Nome popular com `language` diferente de `PORTUGUES` é descartado: o público do app é de JP | vernacularname.txt L1995 `barin pakex kabia` (KAXINAWA), *Piper arboreum* | 205 |
| R05 | transformação | Caracteres invisíveis (soft hyphen U+00AD, zero-width, BOM) são removidos do nome popular | vernacularname.txt L5126 `angico-\xadverdadeiro` e L5127 `calumbí-\xadpreto` (no v393.433 ambos caem antes em R03, por serem variedade; a regra fica para lotes futuros) | 0 |
| R06 | transformação | Hífens tipográficos (U+02D7, U+2010–U+2014, U+2212) viram `-` | vernacularname.txt L5176 `calumbi˗de˗riacho` (U+02D7) | 1 |
| R07 | transformação | Apóstrofos variantes (`` ` ``, `´`, `’`, `‘`) viram `'` | vernacularname.txt L6785 `lentilha-d`água`; L1847 `juti´airimbo` | 6 |
| R08 | transformação | Aspas tipográficas ao redor do nome são removidas | vernacularname.txt L4557 `“lodinho-branco”` | 1 |
| R09 | transformação | Espaços colapsados e aparados nas pontas | Prevenção: nenhum caso no bruto v393.433 (verificado na exploração); a regra fica para lotes futuros | 0 |
| R10 | transformação | Nome popular em minúsculas | vernacularname.txt L1102 `Lagartissa`; L1956 `Dois de Julho` | 34 |
| R11 | descarte | Nome com `/` (alternativas condensadas num campo só) é descartado: separar as alternativas exigiria adivinhar | vernacularname.txt L4672 `páo-/-pau-/-pao-marfim` | 2 |
| R12 | descarte | Nome popular vazio após a normalização é descartado | Prevenção: nenhum caso no bruto v393.433; protege contra linhas só com caracteres removidos por R05–R08 | 0 |
| R13 | descarte | Origem ausente ou conflitante na PB (`establishmentMeans` vazio ou com dois valores) é descartada | 21.537 linhas de distribution.txt têm `establishmentMeans` vazio (nenhuma em BR-PB no v393.433) | 0 |
| R14 | derivação | `origem` derivada por regra: `Nativa` → `nativa`, `Exótica` → `exotica`, a partir da linha BR-PB de distribution.txt | distribution.txt: id 414 `BR-PB … Exótica`; id 461 `BR-PB … Nativa` | 872 |
| R15 | agrupamento | Duplicata exata (mesmo táxon + mesmo nome normalizado) conta uma vez só | vernacularname.txt L395 e L402: `imbuzeiro` duas vezes para o mesmo táxon (id 4405) | 14 |
| R16 | agrupamento | Chave do item = nome sem acento e com espaço tratado como hífen; variantes de acento/espaço entram no mesmo item, em `variantes` | vernacularname.txt L394 `taperebá` e L396 `tapereba`; L14049 `aveloz` e L14051 `avelóz`. Espaço vs. hífen (ex.: L1211 `mamão de porca`) não gerou fusão no v393.433 | 18 |

R14 afeta todas as espécies de referência (`especies_pb.jsonl`): 872 espécies, cada uma com `origem` vinda de `establishmentMeans`.
