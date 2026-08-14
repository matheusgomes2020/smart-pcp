# Modelo Físico

## Banco de Dados

PostgreSQL 17

---

# Convenções

## Chaves Primárias

Todas as tabelas utilizarão UUID como chave primária.

Exemplo:

id UUID PRIMARY KEY

---

## Chaves Estrangeiras

Todas as FK utilizarão UUID.

Exemplo:

cliente_id UUID REFERENCES cliente(id)

---

## Datas

DATE

Utilizado para:

- data_inicio
- data_prazo
- data_prevista
- data_realizada

---

## Data/Hora

TIMESTAMP

Utilizado para:

- criação
- atualização
- logs

---

## Texto

VARCHAR

---

## Valores monetários

NUMERIC(12,2)

---

## Peso

NUMERIC(10,3)

---

## Medidas

NUMERIC(10,2)

---

## Booleano

BOOLEAN

---

# Padrões

- nomes em snake_case
- tabelas no singular
- sem espaços
- sem acentos
- chaves sempre "id"

Exemplo

cliente

pedido

item_pedido

ordem_fabricacao
