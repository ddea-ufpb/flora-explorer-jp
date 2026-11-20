# Medições (gerado por `medir.py`)

| Medida | exec2-boa | exec3-boa-gemma |
|---|---|---|
| Especificação | boa | boa |
| Formato válido | 40/40 | 40/40 |
| **Acurácia** (indeterminado conta como classe) | **27.5%** | **32.5%** |
| Acurácia só nos itens decididos no gabarito | 52.4% (n=21) | 61.9% (n=21) |
| Tempo total | 11.1 min | 8.3 min |
| Passos por item (média · mediana · máx.) | 2.15 · 2.0 · 5 | 3.73 · 4.0 · 6 |
| Itens não resolvidos | 0 | 0 |
| Chamadas inválidas · respostas sem ferramenta | 0 · 3 | 0 · 0 |

## Matriz de confusão · exec2-boa

| gabarito ↓ / modelo → | mesma espécie do gabarito | outra espécie | indeterminado | não resolvido |
|---|---|---|---|---|
| decidido | 11 | 10 | 0 | 0 |
| indeterminado | 0 | 19 | 0 | 0 |

Acurácia por confiança declarada: alta: 11/40

### Erros · exec2-boa (29)

| id | nome | gabarito | modelo | conf. | ferramentas |
|---|---|---|---|---|---|
| flora-2026-000129 | `amor-de-velho` | indeterminado | Desmodium adscendens (22931) | alta | consultar_nome_popular → registrar |
| flora-2026-000132 | `amor-seco` | indeterminado | Desmodium axillare (22933) | alta | consultar_nome_popular → registrar |
| flora-2026-000323 | `batatarana` | indeterminado | Distimake macrocalyx (604876) | alta | consultar_nome_popular → registrar |
| flora-2026-000357 | `boa-noite` | Turnera subulata (21354) | Catharanthus roseus (80256) | alta | consultar_nome_popular → registrar |
| flora-2026-000465 | `calumbi` | indeterminado | Piptadenia adiantoides (18944) | alta | consultar_nome_popular → registrar |
| flora-2026-000534 | `capim-bambu` | indeterminado | Pharus lappulaceus (13520) | alta | consultar_nome_popular → registrar |
| flora-2026-000730 | `carrapicho-namorado` | indeterminado | Desmodium axillare (22933) | alta | consultar_nome_popular → registrar |
| flora-2026-000742 | `carvão-branco` | Croton glandulosus (17514) | Callisthene fasciculata (15275) | alta | consultar_nome_popular → consultar_especie → consultar_especie → buscar_semelhante → registrar |
| flora-2026-000840 | `cipó-de-cobra` | indeterminado | Aristolochia disticha (80577) | alta | consultar_nome_popular → registrar |
| flora-2026-000929 | `corriola` | indeterminado | Ipomoea aristolochiifolia (7025) | alta | consultar_nome_popular → registrar |
| flora-2026-000987 | `dama-da-noite` | indeterminado | Cestrum axillare (14636) | alta | consultar_nome_popular → registrar |
| flora-2026-001015 | `enxerto` | indeterminado | Rhipsalis baccifera (1683) | alta | consultar_nome_popular → consultar_especie → buscar_semelhante → registrar |
| flora-2026-001066 | `espinheiro` | Piptadenia retusa (618368) | Lachesiodendron viridiflorum (605431) | alta | consultar_nome_popular → registrar |
| flora-2026-001247 | `grama-marinha` | Halophila decipiens (105838) | Halodule wrightii (17116) | alta | consultar_nome_popular → registrar |
| flora-2026-001266 | `guaçatonga` | Casearia sylvestris (14384) | Casearia decandra (14367) | alta | consultar_nome_popular → registrar |
| flora-2026-001273 | `guamirim` | indeterminado | Eugenia florida (10400) | alta | consultar_nome_popular → registrar |
| flora-2026-001414 | `jambú` | Acmella oleracea (15913) | Acmella ciliata (15912) | alta | consultar_nome_popular → registrar |
| flora-2026-001542 | `língua-de-vaca` | indeterminado | Echinodorus paniculatus (4266) | alta | consultar_nome_popular → registrar |
| flora-2026-001562 | `maçaranduba` | indeterminado | Manilkara rufula (14481) | alta | consultar_nome_popular → registrar |
| flora-2026-001599 | `mamica-de-cadela` | indeterminado | Brosimum gaudichaudii (19772) | alta | consultar_nome_popular → registrar |
| flora-2026-001685 | `marmelada-de-cavalo` | indeterminado | Desmodium adscendens (22931) | alta | consultar_nome_popular → registrar |
| flora-2026-001709 | `mastruz` | Dysphania ambrosioides (139867) | Amaranthus spinosus (15408) | alta | consultar_nome_popular → registrar |
| flora-2026-001711 | `mata-brasil` | indeterminado | Commelina benghalensis (16910) | alta | consultar_nome_popular → registrar |
| flora-2026-001743 | `milhã` | Panicum peladoense (13393) | Digitaria ciliaris (13176) | alta | consultar_nome_popular → registrar |
| flora-2026-001870 | `palma` | indeterminado | Opuntia ficus-indica (1614) | alta | consultar_nome_popular → registrar |
| flora-2026-002039 | `pindaíba-branca` | indeterminado | Duguetia lanceolata (110319) | alta | consultar_nome_popular → registrar |
| flora-2026-002238 | `sucupira` | Diplotropis incexis (79057) | Dahlstedtia araripensis (135542) | alta | consultar_nome_popular → registrar |
| flora-2026-002285 | `tapereba` | Spondias tuberosa (4405) | Spondias mombin (4404) | alta | consultar_nome_popular → registrar |
| flora-2026-002301 | `tembetaru` | indeterminado | Zanthoxylum petiolare (1152) | alta | consultar_nome_popular → registrar |

## Matriz de confusão · exec3-boa-gemma

| gabarito ↓ / modelo → | mesma espécie do gabarito | outra espécie | indeterminado | não resolvido |
|---|---|---|---|---|
| decidido | 13 | 8 | 0 | 0 |
| indeterminado | 0 | 19 | 0 | 0 |

Acurácia por confiança declarada: alta: 12/37 · media: 1/3

### Erros · exec3-boa-gemma (27)

| id | nome | gabarito | modelo | conf. | ferramentas |
|---|---|---|---|---|---|
| flora-2026-000129 | `amor-de-velho` | indeterminado | Desmodium incanum (115339) | alta | consultar_nome_popular → consultar_especie → consultar_especie → registrar |
| flora-2026-000132 | `amor-seco` | indeterminado | Desmodium axillare (22933) | alta | consultar_nome_popular → consultar_especie → consultar_especie → registrar |
| flora-2026-000323 | `batatarana` | indeterminado | Ipomoea alba (7022) | alta | consultar_nome_popular → consultar_especie → consultar_especie → registrar |
| flora-2026-000357 | `boa-noite` | Turnera subulata (21354) | Ipomoea alba (7022) | alta | consultar_nome_popular → consultar_especie → registrar |
| flora-2026-000457 | `cajarana` | Spondias dulcis (21760) | Spondias mombin (4404) | media | consultar_nome_popular → consultar_especie → consultar_especie → registrar |
| flora-2026-000465 | `calumbi` | indeterminado | Piptadenia adiantoides (18944) | alta | consultar_nome_popular → consultar_especie → registrar |
| flora-2026-000534 | `capim-bambu` | indeterminado | Pharus lappulaceus (13520) | alta | consultar_nome_popular → consultar_especie → registrar |
| flora-2026-000730 | `carrapicho-namorado` | indeterminado | Desmodium incanum (115339) | alta | consultar_nome_popular → consultar_especie → consultar_especie → registrar |
| flora-2026-000840 | `cipó-de-cobra` | indeterminado | Aristolochia trilobata (15766) | alta | consultar_nome_popular → consultar_especie → consultar_especie → consultar_especie → consultar_especie → registrar |
| flora-2026-000929 | `corriola` | indeterminado | Ipomoea aristolochiifolia (7025) | alta | consultar_nome_popular → consultar_especie → registrar |
| flora-2026-000987 | `dama-da-noite` | indeterminado | Ipomoea alba (7022) | alta | consultar_nome_popular → consultar_especie → consultar_especie → registrar |
| flora-2026-001015 | `enxerto` | indeterminado | Rhipsalis lindbergiana (1707) | alta | consultar_nome_popular → consultar_especie → consultar_especie → registrar |
| flora-2026-001066 | `espinheiro` | Piptadenia retusa (618368) | Lachesiodendron viridiflorum (605431) | alta | consultar_nome_popular → consultar_especie → consultar_especie → registrar |
| flora-2026-001247 | `grama-marinha` | Halophila decipiens (105838) | Halodule wrightii (17116) | alta | consultar_nome_popular → consultar_especie → consultar_especie → registrar |
| flora-2026-001266 | `guaçatonga` | Casearia sylvestris (14384) | Casearia decandra (14367) | alta | consultar_nome_popular → consultar_especie → registrar |
| flora-2026-001273 | `guamirim` | indeterminado | Eugenia florida (10400) | alta | consultar_nome_popular → consultar_especie → consultar_especie → registrar |
| flora-2026-001414 | `jambú` | Acmella oleracea (15913) | Acmella ciliata (15912) | alta | consultar_nome_popular → consultar_especie → registrar |
| flora-2026-001515 | `leiteira` | Sebastiania jacobinensis (17677) | Tabernaemontana laeta (4864) | alta | consultar_nome_popular → consultar_especie → consultar_especie → registrar |
| flora-2026-001542 | `língua-de-vaca` | indeterminado | Echinodorus paniculatus (4266) | alta | consultar_nome_popular → consultar_especie → registrar |
| flora-2026-001562 | `maçaranduba` | indeterminado | Manilkara rufula (14481) | alta | consultar_nome_popular → consultar_especie → consultar_especie → registrar |
| flora-2026-001599 | `mamica-de-cadela` | indeterminado | Zanthoxylum rhoifolium (1162) | alta | consultar_nome_popular → consultar_especie → consultar_especie → registrar |
| flora-2026-001685 | `marmelada-de-cavalo` | indeterminado | Desmodium adscendens (22931) | alta | consultar_nome_popular → consultar_especie → registrar |
| flora-2026-001711 | `mata-brasil` | indeterminado | Commelina diffusa (16911) | alta | consultar_nome_popular → consultar_especie → consultar_especie → registrar |
| flora-2026-001870 | `palma` | indeterminado | Opuntia ficus-indica (1614) | alta | consultar_nome_popular → consultar_especie → consultar_especie → consultar_especie → registrar |
| flora-2026-002039 | `pindaíba-branca` | indeterminado | Duguetia lanceolata (110319) | alta | consultar_nome_popular → consultar_especie → registrar |
| flora-2026-002301 | `tembetaru` | indeterminado | Zanthoxylum rhoifolium (1162) | alta | consultar_nome_popular → consultar_especie → consultar_especie → registrar |
| flora-2026-002405 | `violeta` | Dalbergia cearensis (79037) | Erythroxylum barbatum (17415) | media | consultar_nome_popular → consultar_especie → consultar_especie → registrar |

## Erros que persistiram em exec2-boa e exec3-boa-gemma (24)

- flora-2026-000129 `amor-de-velho`: gabarito indeterminado; modelo Desmodium incanum (115339)
- flora-2026-000132 `amor-seco`: gabarito indeterminado; modelo Desmodium axillare (22933)
- flora-2026-000323 `batatarana`: gabarito indeterminado; modelo Ipomoea alba (7022)
- flora-2026-000357 `boa-noite`: gabarito Turnera subulata (21354); modelo Ipomoea alba (7022)
- flora-2026-000465 `calumbi`: gabarito indeterminado; modelo Piptadenia adiantoides (18944)
- flora-2026-000534 `capim-bambu`: gabarito indeterminado; modelo Pharus lappulaceus (13520)
- flora-2026-000730 `carrapicho-namorado`: gabarito indeterminado; modelo Desmodium incanum (115339)
- flora-2026-000840 `cipó-de-cobra`: gabarito indeterminado; modelo Aristolochia trilobata (15766)
- flora-2026-000929 `corriola`: gabarito indeterminado; modelo Ipomoea aristolochiifolia (7025)
- flora-2026-000987 `dama-da-noite`: gabarito indeterminado; modelo Ipomoea alba (7022)
- flora-2026-001015 `enxerto`: gabarito indeterminado; modelo Rhipsalis lindbergiana (1707)
- flora-2026-001066 `espinheiro`: gabarito Piptadenia retusa (618368); modelo Lachesiodendron viridiflorum (605431)
- flora-2026-001247 `grama-marinha`: gabarito Halophila decipiens (105838); modelo Halodule wrightii (17116)
- flora-2026-001266 `guaçatonga`: gabarito Casearia sylvestris (14384); modelo Casearia decandra (14367)
- flora-2026-001273 `guamirim`: gabarito indeterminado; modelo Eugenia florida (10400)
- flora-2026-001414 `jambú`: gabarito Acmella oleracea (15913); modelo Acmella ciliata (15912)
- flora-2026-001542 `língua-de-vaca`: gabarito indeterminado; modelo Echinodorus paniculatus (4266)
- flora-2026-001562 `maçaranduba`: gabarito indeterminado; modelo Manilkara rufula (14481)
- flora-2026-001599 `mamica-de-cadela`: gabarito indeterminado; modelo Zanthoxylum rhoifolium (1162)
- flora-2026-001685 `marmelada-de-cavalo`: gabarito indeterminado; modelo Desmodium adscendens (22931)
- flora-2026-001711 `mata-brasil`: gabarito indeterminado; modelo Commelina diffusa (16911)
- flora-2026-001870 `palma`: gabarito indeterminado; modelo Opuntia ficus-indica (1614)
- flora-2026-002039 `pindaíba-branca`: gabarito indeterminado; modelo Duguetia lanceolata (110319)
- flora-2026-002301 `tembetaru`: gabarito indeterminado; modelo Zanthoxylum rhoifolium (1162)
