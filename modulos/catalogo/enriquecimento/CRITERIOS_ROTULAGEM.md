# Critérios de rotulagem do gabarito

Escritos **antes** de rotular, para que o gabarito meça a mesma pergunta que o enriquecedor vai responder.

## A pergunta

> Um explorador em João Pessoa digita ou fala este nome popular. A qual espécie do catálogo da PB ele mais provavelmente se refere?

## Como rotular cada item

1. Leia os candidatos em `ROTULAGEM.md`. A resposta é **sempre um dos candidatos** ou **indeterminado**.
2. Escolha o candidato que um morador de João Pessoa mais provavelmente chama por esse nome. Em ordem de peso:
   1. a planta é comum em praças, ruas, quintais e parques urbanos de JP (cultivada ou espontânea);
   2. o nome é registrado para o Nordeste, a PB ou estados vizinhos (coluna *localidades do nome*);
   3. a espécie ocorre na Mata Atlântica ou na Caatinga (coluna *domínios*).
3. Se dois ou mais candidatos continuarem igualmente plausíveis depois desses critérios, marque `indeterminado: true` e deixe `rotulo_fonte_reflora_id: null`.
4. Escreva em `justificativa` uma frase dizendo qual critério decidiu (ex.: "critério 2.1: cultivada comum em quintais de JP").

## O que pode e o que não pode ser consultado

- **Pode:** conhecimento próprio, a ficha Reflora de cada candidato e guias de flora urbana do Nordeste.
- **Não pode:** LLM de qualquer tipo, nem a saída do enriquecedor (que ainda não pode ter rodado).

## Formato de cada linha preenchida em `gabarito.jsonl`

```json
{"id": "...", "texto": "...", "candidatos": [...],
 "rotulo_fonte_reflora_id": "621403", "indeterminado": false,
 "justificativa": "critério 2.1: ..."}
```

`rotulado_por` e a data ficam registrados no commit, que tem que ser anterior à primeira execução do enriquecedor.
