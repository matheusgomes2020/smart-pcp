# Regras de Negócio

## Origem dos Dados

RN001 - O ERP Delta é a fonte oficial dos dados.

RN002 - O SmartPCP não substitui o ERP.

RN003 - O SmartPCP utiliza informações sincronizadas do ERP.

RN004 - Alterações cadastrais devem ser realizadas exclusivamente no ERP.

---

## Pedidos

RN005 - Todo pedido pertence a um cliente.

RN006 - Um pedido possui um ou mais itens.

RN007 - Cada item possui exatamente uma Ordem de Fabricação.

RN008 - Uma Ordem de Fabricação pertence a apenas um item.

---

## Produtos

RN009 - Cada item referencia um produto cadastrado no ERP.

RN010 - Um produto possui uma estrutura composta por componentes.

RN011 - Um componente pode ser utilizado em diversos produtos.

RN012 - Componentes podem ser classificados como:
- Fabricado
- Comprado
- Insumo
- Chapa
- Perfil

---

## Produção

RN013 - Apenas componentes fabricados possuem etapas produtivas.

RN014 - Cada etapa pode possuir diversos apontamentos.

RN015 - O andamento da produção é determinado pelos apontamentos.

---

## Compras

RN016 - Componentes comprados podem atender diversas OFs.

RN017 - O estoque controla apenas matérias-primas e itens comprados.

RN018 - Peças fabricadas não são controladas como estoque.

---

## PCP

RN019 - A prioridade é calculada pelo SmartPCP.

RN020 - O SmartPCP pode gerar previsões utilizando informações do ERP.

RN021 - O SmartPCP pode armazenar observações próprias do PCP sem alterar os dados do ERP.
