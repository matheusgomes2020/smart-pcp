# Modelo Conceitual

## Objetivo

O modelo conceitual define as principais entidades do SmartPCP e seus relacionamentos, representando o processo produtivo da empresa de forma independente da tecnologia utilizada.

O SmartPCP atua como uma camada de inteligência sobre o ERP Delta, utilizando seus dados para apoiar o Planejamento e Controle da Produção (PCP).

---

# Modelo Conceitual

```text
Cliente
    │
    │ 1:N
    ▼
Pedido
    │
    │ 1:N
    ▼
ItemPedido (OF)
    │
    ├──────────────► Produto
    │                    │
    │                    │ 1:N
    │                    ▼
    │             ProdutoComponente
    │                    │
    │                    ▼
    │               Componente
    │
    └──────────────► EtapaItem
```

---

# Entidades

## Cliente

Representa o cliente responsável pelos pedidos.

### Principais informações

- Código
- Nome
- Nome Fantasia
- Situação

Relacionamentos

- Um cliente pode possuir vários pedidos.

---

## Pedido

Representa um pedido comercial.

### Principais informações

- Número do pedido
- Cliente
- Data de início
- Data de entrega
- Data prevista
- Data realizada
- Observações
- Status geral
- Semana
- Prioridade

Relacionamentos

- Pertence a um cliente.
- Possui vários itens.

---

## ItemPedido

Representa cada item pertencente ao pedido.

Cada ItemPedido gera uma Ordem de Fabricação (OF).

### Principais informações

- Número do item
- OF
- Produto
- Quantidade
- Material principal
- Status

Relacionamentos

- Pertence a um pedido.
- Referencia um produto.
- Possui diversas etapas.
- Possui diversos componentes (através do produto).

---

## Produto

Representa um produto cadastrado no ERP.

Um mesmo produto pode aparecer em vários pedidos diferentes.

### Principais informações

- Código
- Descrição
- Material principal

Relacionamentos

- Pode estar presente em vários itens.
- Possui uma estrutura de componentes.

---

## ProdutoComponente

Representa a estrutura do produto (BOM).

Relaciona um produto aos componentes utilizados.

Relacionamentos

- Um produto possui vários componentes.
- Um componente pode pertencer a vários produtos.

---

## Componente

Representa peças fabricadas ou itens comprados.

### Informações

- Código
- Descrição
- Tipo
- Material
- Espessura
- Peso bruto
- Peso líquido
- Medidas pronta
- Medidas planificadas
- Possui corte
- Possui dobra
- Valor estimado

Tipos

- Fabricado
- Comprado
- Insumo

---

## EtapaItem

Representa o acompanhamento produtivo do item.

Cada etapa possui prazo, previsão e realização.

### Exemplos de etapas

- Projeto
- Aprovação Cliente
- Compras
- Corte
- Dobra
- Solda
- Montagem
- Qualidade
- Expedição

Cada etapa possui

- Data prevista
- Data prazo
- Data realizada
- Status

Status possíveis

- Não iniciado
- Em andamento
- Concluído

---

# Fluxo Principal

Cliente

↓

Pedido

↓

Item

↓

Produto

↓

Componentes

↓

Produção

↓

Expedição

---

# Observações

O SmartPCP não substitui o ERP Delta.

O ERP permanece como fonte oficial das informações cadastrais.

O SmartPCP centraliza dados, gera indicadores, organiza o fluxo produtivo e apoia a tomada de decisão do PCP.
