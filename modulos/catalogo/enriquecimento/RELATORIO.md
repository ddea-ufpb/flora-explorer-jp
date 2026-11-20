# Relatório · Trabalho 2 · Lucas Gabriel · Flora Explorer JP (módulo `catalogo`)

> **RASCUNHO.** Trechos marcados com ✍️ são para o Lucas escrever. Trechos marcados com ⏳ dependem da rodada de produção.

## 1. Resumo

Coletei da *Flora e Funga do Brasil* os nomes populares das 872 espécies de plantas com ocorrência na Paraíba (2.413 nomes). 2.121 desses nomes apontam para uma única espécie e são resolvidos por consulta. Os outros 292 são ambíguos e foram dados a um modelo local (`qwen3:1.7b`), que decide a qual espécie um morador de João Pessoa se refere.

Resultado no gabarito de 40 itens: **27,5% de acurácia** com a especificação boa, contra 25,0% com a pobre. A especificação boa melhorou sobretudo o comportamento do laço (respostas sem ferramenta: 34 → 3; tempo: −27%). O achado central é outro: **o modelo nunca respondeu `indeterminado` e declarou confiança `alta` em 40 de 40 itens**, acertando 11. Por isso, as decisões do modelo não entram no módulo sem revisão humana (§9).

## 2. Fonte e Etapa 1

Fonte, licença e recorte em [`../FONTE.md`](../FONTE.md). Regras de normalização com o item que motivou cada uma e quantos itens afetou em [`../coleta/REGRAS.md`](../coleta/REGRAS.md). O coletor é idempotente: apagar o `corpus.jsonl` e rodar de novo produz arquivos byte a byte iguais (verificado por sha256).

## 3. Onde o modelo entra e onde não entra (B1)

| Tarefa | Quem faz | Por quê |
|---|---|---|
| Ler o DwC-A, filtrar BR-PB, descartar fungos, infraespecíficos e nomes em outras línguas | parser (`coletor.py`) | Campos estruturados da fonte |
| Normalizar grafia (hífens, apóstrofos, acentos, caixa) | parser (R05–R10, R16) | Regra que acerta 100% |
| `origem` nativa / exótica | parser (R14) | A fonte traz `establishmentMeans` por estado, preenchido para 100% das espécies da PB. **Isso estava previsto para o modelo no recorte original e foi retirado** (ver `FONTE.md`) |
| Nome popular com um único candidato (2.121) | consulta (`gerar_dados.py`) | A resposta está na tabela |
| **Nome popular ambíguo (292): qual espécie, ou indeterminado** | **modelo** | Não há regra: depende de conhecimento sobre uso urbano e regional da planta, que a fonte não codifica |

## 4. Contrato de ferramentas (B2) e o que mudou entre as especificações

Ferramentas (`enriquecedor.py`): `consultar_nome_popular`, `consultar_especie`, `buscar_semelhante` (domínio) e `registrar` (encerra, com `confianca` em enum). A referência é lida de arquivo (`coleta/corpus.jsonl`, `coleta/especies_pb.jsonl` e, na especificação boa, `especificacoes/regras_desempate.md`).

| | Pobre (`especificacoes/pobre.json`) | Boa (`especificacoes/boa.json`) |
|---|---|---|
| Sistema | 1 frase | Contexto de JP e procedimento em 3 passos |
| Descrições | Só o que a ferramenta faz | O que faz **e quando chamar** |
| Regras de desempate | Ausentes | 4 regras ordenadas + definição de confiança, devolvidas por `consultar_nome_popular` |

## 5. Laço, parada e robustez (B3)

Laço escrito à mão, sem framework. Teto `--max-passos` (padrão 6). Lista branca de 3 executores; ferramenta desconhecida, parâmetro faltando ou id fora dos candidatos voltam ao modelo como erro, sem executar nada. Argumentos lidos com `json.loads` e normalizados (id numérico → string, `"Indeterminado"` → `indeterminado`, `média` → `media`); sem `eval` e sem shell. Item que estoura o teto é gravado como não resolvido, com motivo.

✍️ *O que mudou em relação ao `agente.sh` da aula e por quê.*

Ponto de partida: o agente.sh da aula. Reescrevi o laço em Python, mantendo a estrutura (histórico → chamada → executa ferramenta → repete até registrar ou o teto). O que mudou:

Shell → Python. Os argumentos do modelo são lidos com json.loads e nunca chegam a um shell nem a um eval. Em shell, interpolar a saída do modelo num comando é exatamente o risco que zera o item B3.
Lista branca explícita. Três executores de domínio + registrar. Ferramenta desconhecida, parâmetro faltando ou id fora dos candidatos voltam ao modelo como erro, sem executar nada.
Normalização de argumentos. Id numérico → string, "Indeterminado" → indeterminado, média → media. Um modelo de 1,7B erra a forma com frequência; sem isso, respostas certas apareciam como formato inválido.
Teto configurável e item não resolvido preservado. Com --max-passos (padrão 6), o item que estoura o teto entra no dados.jsonl com o motivo, em vez de sumir.
Especificação fora do código. O prompt de sistema, as descrições e as regras de desempate ficam em pobre.json, boa.json e regras_desempate.md. As duas execuções rodam com o mesmo código e diferem só no arquivo de especificação, que é o que a medição compara.
think: false e seed: 42. O modo thinking quadruplicava o tempo (16,3 s contra 4,3 s) sem mudar a ferramenta escolhida.

## 6. Modelo e máquina

`qwen3:1.7b` (digest `8f68893c685c…`), Ollama 0.40.16, `temperature: 0`, `seed: 42`, `think: false`. Mesmo assim a saída pode variar entre rodadas. Desliguei o modo thinking depois de medir uma chamada com ferramenta: 4,3 s sem contra 16,3 s com, escolhendo a mesma ferramenta.

Máquina: AMD Ryzen 7 5825U, 15 GB de RAM, GPU integrada Radeon (Barcelo), **sem GPU dedicada**, Linux 7.0.

## 7. Gabarito e ordem dos commits

40 itens sorteados entre os 292 ambíguos (`sortear_gabarito.py`, semente `20261126`), rotulados à mão seguindo `CRITERIOS_ROTULAGEM.md`, sem LLM. 19 rotulados `indeterminado`.

| Evento | Quando | Commit |
|---|---|---|
| Gabarito rotulado | 19/11 19:42 | `4129679` |
| Teste de fumaça (3 itens **fora** do gabarito) | 19/11 19:49 | — |
| Execução 1 (pobre) | 19/11 19:50–20:05 | código idêntico ao de `b98e7ba` (sem diff; sha256 da especificação confere) |
| Enriquecedor commitado | 19/11 19:56 | `b98e7ba` |
| Execução 2 (boa) | 19/11 20:05–20:16 | `b98e7ba` |
| Produção (boa, 292 ambíguos) | 19/11 20:16–21:49 | `b98e7ba` |
| Execução 3 (boa, `gemma4:e2b`) | 19/11 21:57–22:06 | `c4b7dd4` |

## 8. Medições (B4)

Gerado por `medir.py`. Completo, com todos os erros, em [`execucoes/MEDICOES.md`](execucoes/MEDICOES.md).

| Medida | Execução 1 (pobre) | Execução 2 (boa) |
|---|---|---|
| Formato válido | 39/40 | 40/40 |
| **Acurácia** (indeterminado conta como classe) | 25,0% | **27,5%** |
| Acurácia nos 21 itens decididos no gabarito | 47,6% | 52,4% |
| Tempo total | 15,1 min | 11,1 min |
| Passos por item (média · mediana · máx.) | 2,85 · 3 · 6 | 2,15 · 2 · 5 |
| Não resolvidos | 1 | 0 |
| Respostas sem ferramenta | 34 | 3 |

Matriz de confusão, execução 2:

| gabarito ↓ / modelo → | mesma espécie | outra espécie | indeterminado | não resolvido |
|---|---|---|---|---|
| decidido (21) | 11 | 10 | 0 | 0 |
| indeterminado (19) | 0 | 19 | 0 | 0 |

Confiança declarada × acerto, execução 2: `alta` em 40/40 itens, 11 acertos. A coluna `indeterminado` está zerada nas duas execuções.

### Execução 3: mesma especificação, outro modelo

Para separar o efeito da especificação do efeito do modelo, repeti a execução 2 trocando só o modelo: `gemma4:e2b` (digest `b37049369adf…`, mesmos `temperature`, `seed` e `think: false`). Completo em [`execucoes/MEDICOES-modelos.md`](execucoes/MEDICOES-modelos.md).

| Medida | Execução 2 (`qwen3:1.7b`) | Execução 3 (`gemma4:e2b`) |
|---|---|---|
| Formato válido | 40/40 | 40/40 |
| **Acurácia** | 27,5% | **32,5%** |
| Acurácia nos 21 decididos | 52,4% | 61,9% |
| Tempo total | 11,1 min | 8,3 min |
| Passos por item (média · mediana · máx.) | 2,15 · 2 · 5 | 3,73 · 4 · 6 |
| Respostas sem ferramenta | 3 | 0 |
| Indeterminado respondido (de 19) | 0 | 0 |
| Confiança × acerto | `alta` 11/40 | `alta` 12/37 · `media` 1/3 |

- **Saldo de 2 itens:** o gemma acertou 5 que o qwen errou (`carvão-branco`, `mastruz`, `milhã`, `sucupira`, `tapereba`) e errou 3 que o qwen acertou (`cajarana`, `leiteira`, `violeta`).
- **Processo:** consultou mais, com 4 passos típicos contra 2, e mesmo assim levou menos tempo.
- **O que não mudou:** **também nunca se absteve**, nos 19 indeterminados. 24 erros persistem nos dois modelos: os 19 indeterminados do gabarito e 5 decididos (`boa-noite`, `espinheiro`, `grama-marinha`, `guaçatonga`, `jambú`).

## 9. Análise de erros

Os dados de cada erro foram copiados de `execucoes/*/metricas.json`. Os comentários são do Lucas.

### Erro 1 · `mastruz` (flora-2026-001709), nas duas execuções
- **Gabarito:** *Dysphania ambrosioides*. Justificativa do rótulo: "sem restrição regional e é o mastruz do Nordeste; *Amaranthus spinosus* só no Acre".
- **Modelo (exec. 2):** *Amaranthus spinosus*, confiança alta. Justificativa: "o nome é registrado para o Nordeste e estados vizinhos". A ferramenta tinha devolvido `localidades_do_nome: ["Acre"]` para essa espécie.
- ✍️ *Comentário:* O modelo recitou a regra em vez de aplicá-la. A ferramenta devolveu localidades_do_nome: ["Acre"] para Amaranthus spinosus, e a justificativa diz “registrado para o Nordeste”. Ou seja, ela não descreve a evidência: repete a regra de desempate (“prefira registros do Nordeste”) como se fosse um fato sobre o candidato escolhido. A justificativa foi escrita para combinar com a regra, não a partir do que a ferramenta retornou. Por isso a justificativa do modelo não serve como garantia. A correção cabe ao código: o registrar exigiria que o modelo citasse a localidade do candidato escolhido, e o laço compararia essa citação com a saída da ferramenta, devolvendo como erro quando não batesse.

### Erro 2 · `jambú` (flora-2026-001414), nas duas execuções
- **Gabarito:** *Acmella oleracea*. Justificativa do rótulo: "fonte não desempata (ambos Acre); decisão por conhecimento botânico".
- **Modelo (exec. 2):** *Acmella ciliata*, alta. Justificativa: "comum em áreas urbanas; domínio Mata Atlântica".
- ✍️ *Comentário:* Este erro não dá para cobrar do modelo. As duas Acmella têm o nome registrado só no Acre, e o gabarito decidiu por conhecimento que a fonte não contém (jambu é a hortaliça A. oleracea). A justificativa do modelo (“comum em áreas urbanas; domínio Mata Atlântica”) usa atributos que valem para os dois candidatos, então não desempata nada. Na prática é um empate resolvido pela posição. O item mede se um modelo de 1,7B sabe botânica regional, e ele não sabe. A resposta defensável seria indeterminado, o que liga este erro ao erro persistente.

### Erro 3 · `carvão-branco` (flora-2026-000742), nas duas execuções
- **Gabarito:** *Croton glandulosus*. Justificativa do rótulo: "'carvão-branco' no Nordeste; *Callisthene fasciculata* só no Mato Grosso".
- **Modelo (exec. 2):** *Callisthene fasciculata*, alta, depois de 5 passos (`consultar_nome_popular → consultar_especie ×2 → buscar_semelhante → registrar`). A especificação boa fez o modelo buscar mais evidência, e a decisão não mudou.
- ✍️ *Comentário:* É o caso mais revelador: a evidência era limpa (Croton glandulosus no Nordeste contra Callisthene fasciculata no Mato Grosso), o modelo consultou mais (5 passos) e manteve a resposta errada. A especificação boa mudou o processo (mais consultas, menos respostas sem ferramenta), mas não a decisão. O modelo coleta a evidência e depois não a usa. Isso também tem consequência para o B1: esse desempate é determinístico, porque comparar a localidade de cada candidato com “Nordeste” uma regra faz com 100% de acerto. Esse filtro deveria estar no gerar_dados.py, e o modelo só deveria receber o que sobra depois dele.

### Erro persistente · abstenção que nunca acontece (ex.: `dama-da-noite`, flora-2026-000987)
- **Gabarito:** indeterminado ("*Cestrum axillare*, *Ipomoea alba* e *Selenicereus undatus* sem localidade; empate").
- **Modelo (exec. 1 e 2):** *Cestrum axillare*, alta. Na exec. 2 a justificativa afirma "o nome é registrado para o Nordeste", o que a fonte não diz.
- Vale para os 19 itens indeterminados do gabarito: nenhum foi acertado em nenhuma execução.
- ✍️ *Comentário:* Os três candidatos não têm localidade registrada, então nenhuma evidência favorece nenhum deles, e mesmo assim o modelo escolhe um e declara confiança alta. Pior: inventa evidência (“registrado para o Nordeste”). Nos 19 indeterminados do gabarito, ele nunca se absteve, nas duas execuções. Uma hipótese: para um modelo pequeno, preencher um id é o caminho natural do registrar, e “indeterminado” é uma resposta que ele quase nunca dá. Como a confiança foi alta em 40 de 40 itens, ela não informa nada. A correção é tirar essas duas decisões do modelo:

o código detecta o empate: se nenhum candidato tem evidência regional que o distinga, o item vira indeterminado sem chamar o modelo;
a confiança é calculada pelo código, a partir de quanto a evidência discrimina, e não declarada pelo modelo.

Isso reforça a decisão da seção 10: nada decidido pelo modelo entra no módulo sem revisão humana.

### Possíveis erros de rotulagem, notados depois da medição (gabarito mantido)
- ✍️ `tapereba` e `boa-noite`: *mantenha ou retire, conforme a sua avaliação. O gabarito não foi alterado.*

## 10. Uma decisão que muda (C4)

**Linha que muda:** `especificacoes/lucas-gabriel/arquitetura/contratos/modelo-dados.md`, tabela `especie_catalogo`, campo `nome_popular` (um único `text`), e a ADR-0006 ("Origem e textos de curiosidade são revisados manualmente na importação").

**O que mudaria, pelo que medi:**
1. `especie_catalogo.nome_popular` passa a ser só o nome de exibição. A busca por nome popular vai para uma tabela nova, `especie_nome_popular (nome_popular PK, especie_id FK, metodo, confianca)`, porque 872 espécies têm 2.413 nomes e 292 desses nomes são ambíguos.
2. `origem` deixa de ser revisão manual: vem do `establishmentMeans` da fonte para BR-PB (R14). Revisão manual fica só para `exotica_invasora`, que a fonte não traz.
3. Mapeamentos decididos por modelo **não entram automaticamente**: a confiança declarada não discriminou acerto de erro (40/40 `alta`, 11 acertos). `carregar.py` só carrega `metodo = regra` e manda o resto para `seed/revisao_pendente.jsonl`.

## 11. Entrega ao projeto (B5)

`dados.jsonl`, [`ESQUEMA.md`](ESQUEMA.md) e `carregar.py` (seed SQL idempotente, testado com carga dupla em SQLite).

**Rodada de produção** (`execucoes/producao-boa/`): especificação boa, `qwen3:1.7b@8f68893c685c`, commit `b98e7ba`, 19/11 20:16–21:49 (92,7 min).

| | Itens |
|---|---|
| Nomes no corpus | 2.413 |
| Resolvidos por regra (1 candidato) | 2.121 |
| Ambíguos decididos pelo modelo | 285 (todos com confiança `alta`) |
| Indeterminado | 1 (`amarra-amarra`, confiança `baixa`) |
| Não resolvidos (teto de 6 passos) | 6 (`azedinha`, `catinga-de-bode`, `catinga-de-mulata`, `limãozinho`, `maracujá`, `milhomes`) |

Por item: 2,4 passos em média (mediana 2) e 19,0 s em média (mediana 16,2 s). O máximo foi `vassourinha`, com 233 s em 2 passos, uma resposta isolada lenta do Ollama e não um laço longo.

A taxa de abstenção na produção (1 em 292) repete o que o gabarito mostrou (0 em 19 indeterminados). Se a acurácia medida no gabarito valer aqui, a maior parte das 285 decisões está errada, por isso nenhuma entra na carga.

**Carga:** `carregar.py --testar-sqlite` carrega 872 espécies (612 nativas, 260 exóticas) e 2.121 nomes populares, duas vezes seguidas, sem duplicar. Os 292 ambíguos vão para `seed/revisao_pendente.jsonl`.

✍️ *Confirmação do colega: nome e link da mensagem.*

## 12. Limites e próximo experimento

- O modelo recita as regras de desempate em vez de aplicá-las, chegando a afirmar evidência que a ferramenta não devolveu (`mastruz`, `dama-da-noite`).
- A acurácia foi medida em 40 itens: 1 item = 2,5 pontos percentuais. A diferença entre as execuções (1 item) está dentro do ruído.
- Trocar o modelo (`gemma4:e2b`, execução 3) rendeu 2 itens: 5 pontos percentuais, ainda perto do ruído. Também não fez o modelo se abster. A falta de abstenção não é de um modelo específico: é do desenho, em que `registrar` aceita qualquer candidato.
- **Próximo experimento:** tirar do modelo o que uma regra faz. Antes da chamada, um filtro determinístico elimina os candidatos sem localidade no Nordeste. Se nenhum ou mais de um candidato tiver evidência, a resposta é `indeterminado` por regra, e o modelo só desempata quando houver evidência que separe os candidatos. Depois, medir de novo no mesmo gabarito.
