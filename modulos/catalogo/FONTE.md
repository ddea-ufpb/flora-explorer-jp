**Trabalho 2 · Lucas Gabriel · Flora Explorer JP** — Fonte: *Flora e Funga do Brasil – Lista Oficial* (JBRJ/REFLORA), Darwin Core Archive v393.433 de 2026-11-01, licença CC-BY 4.0, https://ipt.jbrj.gov.br/jbrj/resource?r=lista_especies_flora_brasil. Recorte: espécies de plantas com ocorrência registrada na Paraíba, com nome aceito, sinônimos e nomes populares (alimenta `especie_catalogo`, ADR-0006). Etapa 2: o modelo local normaliza nome popular → `nome_cientifico` aceito e classifica `origem` (`nativa | exotica | exotica_invasora`).

## Revisão do recorte da Etapa 2 (2026-11-19, antes da Etapa 1)

Ao explorar o bruto, verifiquei que a fonte já traz `establishmentMeans` (`Nativa` / `Exótica`) por estado, preenchido para 100% das espécies com ocorrência em BR-PB. Classificar nativa × exótica com o modelo seria trabalho de parser, então isso passa a ser regra determinística (R14 do `coleta/REGRAS.md`).

O que muda:

- **Etapa 1 (sem mudança de fonte):** item do corpus = um nome popular em português associado a espécies da PB (2.413 itens, 292 ambíguos).
- **Etapa 2 (o que o modelo decide):** dado um nome popular ambíguo, isto é, associado pela fonte a mais de uma espécie da PB, decidir a qual `nome_cientifico` aceito ele se refere no contexto de João Pessoa (ex.: `alecrim` → *Rosmarinus officinalis* ou *Pectis elongata*), ou responder `indeterminado`. Nomes com um único candidato (2.121 dos 2.413) são resolvidos por consulta, sem modelo.
- **`origem`:** `nativa` / `exotica` vêm por regra a partir da fonte. `exotica_invasora` não existe nesta fonte e fica fora do Trabalho 2.
