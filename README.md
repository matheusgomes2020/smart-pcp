# SmartPCP

> Plataforma de apoio ao Planejamento e Controle da Produção (PCP), desenvolvida para consolidar informações do ERP Delta e transformar dados operacionais em inteligência para tomada de decisão.

---

## 📌 Sobre o Projeto

O SmartPCP nasceu da necessidade de reduzir o tempo gasto na consulta de informações distribuídas em diferentes módulos do ERP Delta.

Em vez de substituir o ERP, o SmartPCP atua como uma camada de inteligência, reunindo informações de pedidos, itens, ordens de fabricação, componentes, compras, estoque e produção em uma única plataforma.

O objetivo é substituir controles paralelos em planilhas, facilitar o trabalho do PCP e fornecer indicadores para tomada de decisão.

---

## 🎯 Objetivos

- Centralizar informações do processo produtivo.
- Reduzir consultas em diferentes módulos do ERP.
- Substituir controles realizados em planilhas.
- Auxiliar o PCP na priorização das Ordens de Fabricação.
- Identificar gargalos produtivos.
- Gerar indicadores em tempo real.
- Apoiar previsões de entrega.
- Criar uma base para futuras funcionalidades com Inteligência Artificial.

---

## 🏗 Arquitetura

```
ERP Delta
     │
     ▼
ETL / Integração
     │
     ▼
Banco SmartPCP
     │
     ▼
API (FastAPI)
     │
     ▼
Frontend (React)
     │
     ├────────► Dashboard (Power BI)
     │
     └────────► Inteligência e Análises
```

---

## 🚀 Principais Funcionalidades

- Consulta unificada de pedidos.
- Visualização completa das Ordens de Fabricação.
- Acompanhamento dos itens e componentes.
- Controle de prioridades.
- Indicadores para PCP.
- Dashboards executivos.
- Análise de gargalos.
- Previsão de atrasos.
- Integração com o ERP Delta.

---

## 🛠 Tecnologias

### Backend

- Python
- FastAPI

### Banco de Dados

- PostgreSQL

### Frontend

- React

### ETL

- Python

### BI

- Power BI

### DevOps

- Docker
- Git
- GitHub

---

## 📁 Estrutura do Projeto

```
smart-pcp/

├── docs/
├── backend/
├── frontend/
├── database/
├── etl/
├── dashboard/
├── assets/
└── README.md
```

---

## 📚 Documentação

A documentação completa encontra-se na pasta `docs`.

- Visão Geral
- Problemas
- Objetivos
- Processos
- Requisitos
- Regras de Negócio
- Dicionário de Dados
- Modelo de Dados
- Arquitetura
- Roadmap

---

## 🎯 Status do Projeto

🚧 Em desenvolvimento

Atualmente o projeto encontra-se na fase de levantamento de requisitos, modelagem de dados e definição da arquitetura.

---

## 📈 Roadmap

- [x] Levantamento de requisitos
- [ ] Modelagem do banco de dados
- [ ] Desenvolvimento da API
- [ ] ETL de integração
- [ ] Frontend
- [ ] Dashboards
- [ ] Inteligência Artificial

---

## 💡 Filosofia

O SmartPCP não tem como objetivo substituir o ERP existente.

Seu propósito é fornecer uma visão consolidada da produção, apoiando o Planejamento e Controle da Produção com informações integradas, indicadores e inteligência para tomada de decisão.

---

## 👨‍💻 Autor

**Matheus Gomes**

Projeto desenvolvido como iniciativa de estudo e aplicação prática de Engenharia de Software, Banco de Dados, Desenvolvimento Web, Business Intelligence e Inteligência Artificial voltados ao ambiente industrial.
