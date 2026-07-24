
# Dicionário de Dados

## Pedido

| Campo | Tipo | Descrição |
|--------|------|-----------|
| id | bigint | Identificador |
| numero | varchar | Número do pedido |
| cliente_id | FK | Cliente |
| data_inicio | date | Data início |
| data_entrega | date | Data prevista |
| status | enum | Situação |

---

## Item

| Campo | Tipo |
|--------|------|
| id | bigint |
| pedido_id | FK |
| of | varchar |
| codigo | varchar |
| descricao | text |
| quantidade | decimal |

---

## Componentes

| Campo | Tipo |
|--------|------|
| id | bigint |
| item_id | FK |
| codigo | varchar |
| descricao | text |
| tipo | enum |
| material | varchar |
| espessura | decimal |
| quantidade | decimal |
