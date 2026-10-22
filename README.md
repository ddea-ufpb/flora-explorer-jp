# Flora Explorer JP

Exploração urbana com propósito: fotografar a flora de João Pessoa, identificar a espécie e
transformar o resultado em catálogo coletivo e mapa de incidência.

> **Status:** repositório recém-criado. Nenhuma linha de aplicação escrita. Este README existe para
> receber os artefatos que alimentam o `/paul:init` de cada módulo.
>
> **Disciplina:** DINF00071 — Desenvolvimento Dirigido por Especificação com Agentes · CI/UFPB · 2026.2

---

## O problema

A cidade tem uma flora que quem mora nela não enxerga: a pessoa passa todo dia pela mesma árvore e
não sabe o nome dela, nem se é nativa, nem se é uma espécie invasora tomando o lugar de outra. Do
outro lado, quem gere o verde urbano não tem levantamento atualizado — o inventário, quando existe,
é caro, pontual e envelhece rápido.

Há gente com celular na rua todo dia passando por essa informação. Ninguém está coletando.

## O que o sistema faz

O explorador fotografa uma planta, o sistema identifica a espécie com apoio de um modelo de visão,
o registro entra num catálogo pessoal e coletivo, e o conjunto vira um mapa de incidência que
distingue nativas de exóticas e invasoras. A gamificação existe para sustentar a coleta ao longo do
tempo — sem ela, a base morre na terceira semana.

## Quem usa

| Papel | O que precisa |
|---|---|
| Explorador (morador, estudante) | Descobrir o que tem na rua dele e ter motivo para voltar amanhã |
| Gestor ambiental / pesquisador | Ver onde há concentração de invasoras e como isso muda no tempo |
| Escola | Usar a coleta como atividade de campo |

## Fora de escopo (preliminar — o grupo fecha e justifica)

- Identificação de fauna: outro problema, outro modelo.
- Treinar um classificador botânico próprio: o sistema usa um identificador, não o produz.
- Laudo técnico ou valor legal da identificação: o resultado é indicativo e assumido como tal.
- Rede social completa: perfis, seguir, comentar.

## Módulos

Um repositório, quatro módulos independentes. Cada módulo tem persistência, API, componente
concorrente, desempenho medido e testes — os cinco, sozinho.

| # | Módulo | Responsável | O que faz |
|---|---|---|---|
| 1 | `captura` | *a definir* | Recebe foto geolocalizada, valida, comprime, enfileira e persiste o registro |
| 2 | `identificacao` | *a definir* | Consulta o identificador, aplica limiar de confiança e guarda o resultado com a evidência |
| 3 | `catalogo` | *a definir* | Catálogo pessoal e coletivo, missões, pontuação e progressão |
| 4 | `mapa` | *a definir* | Consultas geoespaciais, incidência por espécie e painel do gestor |

**Contrato principal:** o registro de observação — foto, coordenada, espécie sugerida e confiança.
Captura publica; identificação enriquece; catálogo e mapa leem.

**Confiança não é detalhe:** abaixo do limiar, o registro entra como *não identificado* e continua
valendo como ocorrência. Dizer a espécie errada com segurança é pior do que não dizer.

## Dados e privacidade

A foto é tirada na rua e **pode capturar o que não deveria**: fachada, janela, quintal de terceiro,
pessoa passando. A coordenada exata de um registro é, na prática, um endereço. Decisões preliminares:

- A camada pública mostra o registro agregado em célula, não o ponto exato.
- Coordenada precisa fica restrita a quem tem papel de gestão ou pesquisa.
- Fotos em armazenamento privado, com acesso assinado — nunca URL pública.
- Política de recorte ou borrão quando a foto captura pessoa ou residência: **em aberto**, a decidir
  antes de qualquer exposição pública de imagem.

**Dados:** gerados pelos usuários, com enriquecimento opcional de base botânica pública.

## Estrutura do repositório

```
flora-explorer-jp/
├── README.md              # este arquivo — brief do projeto
├── CONTRATOS.md           # FI-02: módulos, contratos e duplos
├── modulos/
│   ├── captura/        .paul/
│   ├── identificacao/  .paul/
│   ├── catalogo/       .paul/
│   └── mapa/           .paul/
└── .gitignore             # .claude/ fora do versionamento
```

## Artefatos de entrada do `/paul:init`

O init de cada módulo só roda depois que isto estiver no repositório:

- [ ] **FI-01 de cada integrante**, com as seções 7 e 8 escritas no nível do módulo
- [ ] **CONTRATOS.md** do grupo: os quatro módulos, os contratos entre pares que se tocam e o duplo de cada contrato
- [ ] **Teste de independência** respondido por cada integrante
- [ ] **Telas do sistema** (Trabalho 1): no mínimo dez, como mock, descrição detalhada ou desenho
- [ ] **Artefatos de arquitetura** (Trabalho 1): padrão de especificação escolhido, justificativa e os artefatos produzidos

## Como o trabalho é conduzido

Cada módulo roda o ciclo **Plan → Audit → Apply → Unify**: o plano declara critérios de aceitação
verificáveis, a auditoria revisa antes de qualquer código, a execução segue o plano aprovado e o
fechamento compara planejado com entregue.

A **Fase 1 (Fundação)** é a mesma para todos os projetos da turma: scaffold com CI que falha quando
deve, banco com as restrições de dados no schema, e deploy que só publica com o CI verde. A
diferença entre os projetos começa na Fase 2.

## Licença

MIT.
