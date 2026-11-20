# Medições (gerado por `medir.py`)

| Medida | exec1-pobre | exec2-boa |
|---|---|---|
| Especificação | pobre | boa |
| Formato válido | 39/40 | 40/40 |
| **Acurácia** (indeterminado conta como classe) | **25.0%** | **27.5%** |
| Acurácia só nos itens decididos no gabarito | 47.6% (n=21) | 52.4% (n=21) |
| Tempo total | 15.1 min | 11.1 min |
| Passos por item (média · mediana · máx.) | 2.85 · 3.0 · 6 | 2.15 · 2.0 · 5 |
| Itens não resolvidos | 1 | 0 |
| Chamadas inválidas · respostas sem ferramenta | 0 · 34 | 0 · 3 |

## Matriz de confusão · exec1-pobre

| gabarito ↓ / modelo → | mesma espécie do gabarito | outra espécie | indeterminado | não resolvido |
|---|---|---|---|---|
| decidido | 10 | 11 | 0 | 0 |
| indeterminado | 0 | 18 | 0 | 1 |

Acurácia por confiança declarada: alta: 10/39 · —: 0/1

### Erros · exec1-pobre (30)

| id | nome | gabarito | modelo | conf. | ferramentas |
|---|---|---|---|---|---|
| flora-2026-000129 | `amor-de-velho` | indeterminado | Desmodium adscendens (22931) | alta | consultar_nome_popular → registrar |
| flora-2026-000132 | `amor-seco` | indeterminado | Desmodium axillare (22933) | alta | consultar_nome_popular → registrar |
| flora-2026-000323 | `batatarana` | indeterminado | Distimake macrocalyx (604876) | alta | consultar_nome_popular → registrar |
| flora-2026-000357 | `boa-noite` | Turnera subulata (21354) | Mirabilis jalapa (10920) | alta | buscar_semelhante → consultar_especie → registrar |
| flora-2026-000465 | `calumbi` | indeterminado | Piptadenia adiantoides (18944) | alta | consultar_nome_popular → registrar |
| flora-2026-000534 | `capim-bambu` | indeterminado | Pharus lappulaceus (13520) | alta | consultar_nome_popular → registrar |
| flora-2026-000730 | `carrapicho-namorado` | indeterminado | Desmodium axillare (22933) | alta | consultar_nome_popular → registrar |
| flora-2026-000742 | `carvão-branco` | Croton glandulosus (17514) | Callisthene fasciculata (15275) | alta | consultar_nome_popular → registrar |
| flora-2026-000840 | `cipó-de-cobra` | indeterminado | não resolvido | — | consultar_nome_popular |
| flora-2026-000929 | `corriola` | indeterminado | Ipomoea quamoclit (7056) | alta | consultar_nome_popular → registrar |
| flora-2026-000987 | `dama-da-noite` | indeterminado | Cestrum axillare (14636) | alta | consultar_nome_popular → registrar |
| flora-2026-001015 | `enxerto` | indeterminado | Rhipsalis baccifera (1683) | alta | consultar_nome_popular → registrar |
| flora-2026-001066 | `espinheiro` | Piptadenia retusa (618368) | Lachesiodendron viridiflorum (605431) | alta | consultar_nome_popular → registrar |
| flora-2026-001247 | `grama-marinha` | Halophila decipiens (105838) | Halodule wrightii (17116) | alta | consultar_nome_popular → registrar |
| flora-2026-001266 | `guaçatonga` | Casearia sylvestris (14384) | Casearia decandra (14367) | alta | consultar_nome_popular → registrar |
| flora-2026-001273 | `guamirim` | indeterminado | Eugenia florida (10400) | alta | consultar_nome_popular → registrar |
| flora-2026-001414 | `jambú` | Acmella oleracea (15913) | Acmella ciliata (15912) | alta | consultar_nome_popular → registrar |
| flora-2026-001462 | `jucá` | Libidibia ferrea (109828) | Libidibia juca (632753) | alta | consultar_nome_popular → registrar |
| flora-2026-001542 | `língua-de-vaca` | indeterminado | Echinodorus paniculatus (4266) | alta | consultar_nome_popular → registrar |
| flora-2026-001562 | `maçaranduba` | indeterminado | Manilkara rufula (14481) | alta | consultar_nome_popular → registrar |
| flora-2026-001599 | `mamica-de-cadela` | indeterminado | Brosimum gaudichaudii (19772) | alta | consultar_nome_popular → registrar |
| flora-2026-001685 | `marmelada-de-cavalo` | indeterminado | Desmodium adscendens (22931) | alta | consultar_nome_popular → registrar |
| flora-2026-001709 | `mastruz` | Dysphania ambrosioides (139867) | Amaranthus spinosus (15408) | alta | consultar_nome_popular → registrar |
| flora-2026-001711 | `mata-brasil` | indeterminado | Commelina benghalensis (16910) | alta | consultar_nome_popular → registrar |
| flora-2026-001743 | `milhã` | Panicum peladoense (13393) | Digitaria ciliaris (13176) | alta | consultar_nome_popular → registrar |
| flora-2026-001870 | `palma` | indeterminado | Nopalea cochenillifera (1609) | alta | consultar_nome_popular → registrar |
| flora-2026-002039 | `pindaíba-branca` | indeterminado | Duguetia lanceolata (110319) | alta | consultar_nome_popular → registrar |
| flora-2026-002238 | `sucupira` | Diplotropis incexis (79057) | Dahlstedtia araripensis (135542) | alta | consultar_nome_popular → registrar |
| flora-2026-002285 | `tapereba` | Spondias tuberosa (4405) | Spondias mombin (4404) | alta | consultar_nome_popular → registrar |
| flora-2026-002301 | `tembetaru` | indeterminado | Zanthoxylum petiolare (1152) | alta | consultar_nome_popular → registrar |

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

## Erros que persistiram em exec1-pobre e exec2-boa (29)

- flora-2026-000129 `amor-de-velho`: gabarito indeterminado; modelo Desmodium adscendens (22931)
- flora-2026-000132 `amor-seco`: gabarito indeterminado; modelo Desmodium axillare (22933)
- flora-2026-000323 `batatarana`: gabarito indeterminado; modelo Distimake macrocalyx (604876)
- flora-2026-000357 `boa-noite`: gabarito Turnera subulata (21354); modelo Catharanthus roseus (80256)
- flora-2026-000465 `calumbi`: gabarito indeterminado; modelo Piptadenia adiantoides (18944)
- flora-2026-000534 `capim-bambu`: gabarito indeterminado; modelo Pharus lappulaceus (13520)
- flora-2026-000730 `carrapicho-namorado`: gabarito indeterminado; modelo Desmodium axillare (22933)
- flora-2026-000742 `carvão-branco`: gabarito Croton glandulosus (17514); modelo Callisthene fasciculata (15275)
- flora-2026-000840 `cipó-de-cobra`: gabarito indeterminado; modelo Aristolochia disticha (80577)
- flora-2026-000929 `corriola`: gabarito indeterminado; modelo Ipomoea aristolochiifolia (7025)
- flora-2026-000987 `dama-da-noite`: gabarito indeterminado; modelo Cestrum axillare (14636)
- flora-2026-001015 `enxerto`: gabarito indeterminado; modelo Rhipsalis baccifera (1683)
- flora-2026-001066 `espinheiro`: gabarito Piptadenia retusa (618368); modelo Lachesiodendron viridiflorum (605431)
- flora-2026-001247 `grama-marinha`: gabarito Halophila decipiens (105838); modelo Halodule wrightii (17116)
- flora-2026-001266 `guaçatonga`: gabarito Casearia sylvestris (14384); modelo Casearia decandra (14367)
- flora-2026-001273 `guamirim`: gabarito indeterminado; modelo Eugenia florida (10400)
- flora-2026-001414 `jambú`: gabarito Acmella oleracea (15913); modelo Acmella ciliata (15912)
- flora-2026-001542 `língua-de-vaca`: gabarito indeterminado; modelo Echinodorus paniculatus (4266)
- flora-2026-001562 `maçaranduba`: gabarito indeterminado; modelo Manilkara rufula (14481)
- flora-2026-001599 `mamica-de-cadela`: gabarito indeterminado; modelo Brosimum gaudichaudii (19772)
- flora-2026-001685 `marmelada-de-cavalo`: gabarito indeterminado; modelo Desmodium adscendens (22931)
- flora-2026-001709 `mastruz`: gabarito Dysphania ambrosioides (139867); modelo Amaranthus spinosus (15408)
- flora-2026-001711 `mata-brasil`: gabarito indeterminado; modelo Commelina benghalensis (16910)
- flora-2026-001743 `milhã`: gabarito Panicum peladoense (13393); modelo Digitaria ciliaris (13176)
- flora-2026-001870 `palma`: gabarito indeterminado; modelo Opuntia ficus-indica (1614)
- flora-2026-002039 `pindaíba-branca`: gabarito indeterminado; modelo Duguetia lanceolata (110319)
- flora-2026-002238 `sucupira`: gabarito Diplotropis incexis (79057); modelo Dahlstedtia araripensis (135542)
- flora-2026-002285 `tapereba`: gabarito Spondias tuberosa (4405); modelo Spondias mombin (4404)
- flora-2026-002301 `tembetaru`: gabarito indeterminado; modelo Zanthoxylum petiolare (1152)
