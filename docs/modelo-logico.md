# Modelo Lógico

## Objetivo

Este documento descreve o modelo lógico do banco de dados do SmartPCP.

O SmartPCP utiliza o ERP Delta como fonte oficial de dados, armazenando também informações próprias relacionadas ao Planejamento e Controle da Produção (PCP).

---

# Visão Geral

```text
Cliente
    │
    │ 1:N
Pedido
    │
    │ 1:N
ItemPedido
    │
    │ 1:1
OrdemFabricacao
    │
    ├──────────────┐
    │              │
    ▼              ▼
EtapaOF         Produto
                   │
                   │ N:N
                   ▼
          ProdutoComponente
                   │
                   ▼
              Componente
                   │
                   ▼
               Material
```

---

# Entidades

## Cliente

Descrição

Representa o cliente responsável pelos pedidos.

### Campos

| Campo | Tipo | Chave |
|--------|------|-------|
| id | UUID | PK |
| codigo | VARCHAR(20) | UK |
| nome | VARCHAR(200) | |
| nome_fantasia | VARCHAR(200) | |
| ativo | BOOLEAN | |

Relacionamentos

- Cliente possui vários pedidos.

---

## Pedido

Descrição

Representa o pedido comercial importado do ERP.

### Campos

| Campo | Tipo |
|--------|------|
| id | UUID |
| numero | VARCHAR(20) |
| cliente_id | UUID |
| observacao | TEXT |
| data_inicio | DATE |
| data_prazo | DATE |
| data_prevista | DATE |
| data_realizada | DATE |
| prioridade | INTEGER |

Relacionamentos

- Pertence a um Cliente.
- Possui vários Itens.

---

## ItemPedido

Descrição

Representa um item pertencente ao pedido.

Cada Item gera uma Ordem de Fabricação.

### Campos

| Campo | Tipo |
|--------|------|
| id | UUID |
| pedido_id | UUID |
| produto_id | UUID |
| numero_item | INTEGER |
| quantidade | DECIMAL |
| status | VARCHAR |

Relacionamentos

- Pertence a um Pedido.
- Referencia um Produto.
- Possui uma Ordem de Fabricação.

---

## OrdemFabricacao

Descrição

Representa a Ordem de Fabricação (OF) vinculada ao Item.

É a principal entidade acompanhada pelo PCP.

### Campos

| Campo | Tipo |
|--------|------|
| id | UUID |
| numero_of | VARCHAR |
| item_pedido_id | UUID |
| status | VARCHAR |
| data_abertura | DATE |
| data_prazo | DATE |
| data_prevista | DATE |
| data_finalizada | DATE |
| responsavel | VARCHAR |
| observacao | TEXT |

Relacionamentos

- Pertence a um Item.
- Possui diversas Etapas.

---

## Etapa

Descrição

Cadastro das etapas produtivas.

### Campos

| Campo | Tipo |
|--------|------|
| id | UUID |
| nome | VARCHAR |
| ordem | INTEGER |

Exemplos

- Projeto
- Aprovação Cliente
- Compras
- Corte
- Dobra
- Solda
- Montagem
- Qualidade
- Expedição

---

## EtapaOF

Descrição

Representa a execução de uma etapa da Ordem de Fabricação.

### Campos

| Campo | Tipo |
|--------|------|
| id | UUID |
| ordem_fabricacao_id | UUID |
| etapa_id | UUID |
| data_prevista | DATE |
| data_prazo | DATE |
| data_realizada | DATE |
| status | VARCHAR |
| responsavel | VARCHAR |
| observacao | TEXT |

---

## Produto

Descrição

Representa um produto cadastrado no ERP Delta.

Um mesmo produto pode ser utilizado em diversos pedidos.

### Campos

| Campo | Tipo |
|--------|------|
| id | UUID |
| codigo | VARCHAR |
| descricao | VARCHAR |
| material_principal_id | UUID |

---

## ProdutoComponente

Descrição

Relaciona Produtos aos Componentes.

### Campos

| Campo | Tipo |
|--------|------|
| produto_id | UUID |
| componente_id | UUID |
| quantidade | DECIMAL |

---

## Componente

Descrição

Representa peças fabricadas, insumos ou itens comprados.

### Campos

| Campo | Tipo |
|--------|------|
| id | UUID |
| codigo | VARCHAR |
| descricao | VARCHAR |
| tipo | VARCHAR |
| material_id | UUID |
| espessura | DECIMAL |
| peso_bruto | DECIMAL |
| peso_liquido | DECIMAL |
| largura_planificada | DECIMAL |
| comprimento_planificado | DECIMAL |
| largura_pronta | DECIMAL |
| comprimento_pronto | DECIMAL |
| possui_corte | BOOLEAN |
| possui_dobra | BOOLEAN |

---

## Material

Descrição

Cadastro dos materiais.

Exemplos

- Inox 201
- Inox 304
- Inox 430
- Carbono
- Alumínio
- PEAD

---

# Relacionamentos

Cliente

↓

Pedido

↓

ItemPedido

↓

OrdemFabricacao

↓

EtapaOF

---

Produto

↓

ProdutoComponente

↓

Componente

↓

Material

---

# Decisões de Projeto

- O ERP Delta permanece como fonte oficial dos dados.
- O SmartPCP armazena informações complementares para apoio ao PCP.
- O acompanhamento da produção ocorre através da Ordem de Fabricação (OF).
- Produtos podem ser reutilizados em diversos pedidos.
- Componentes podem ser compartilhados entre diferentes produtos.
- As etapas produtivas pertencem à Ordem de Fabricação.
