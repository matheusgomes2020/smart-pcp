-- ============================================================
-- SMART PCP
-- 13-views.sql
-- Views principais do PCP
-- =========================================A===================


-- ============================================================
-- 1. RESUMO DO PCP
-- ============================================================
-- RESUMO
CREATE OR REPLACE VIEW vw_pcp_resumo AS

SELECT
    p.numero AS pedido,
    c.nome AS cliente,

    p.data_inicio,
    p.data_prazo AS prazo_pedido,
    p.data_prevista AS previsao_pedido,
    p.data_realizada AS realizada_pedido,

    ip.numero_item AS item,
    ip.quantidade AS quantidade_item,
    ip.material_principal,
    ip.status AS status_item,

    pr.codigo AS codigo_produto,
    pr.descricao AS produto,

    ofa.numero_of AS of,
    ofa.status AS status_of,
    ofa.prioridade,

    ofa.data_abertura,
    ofa.data_prazo AS prazo_of,
    ofa.data_prevista AS previsao_of,
    ofa.data_realizada AS realizada_of

FROM pedido p

JOIN cliente c
    ON c.id = p.cliente_id

JOIN item_pedido ip
    ON ip.pedido_id = p.id

JOIN produto pr
    ON pr.id = ip.produto_id

JOIN ordem_fabricacao ofa
    ON ofa.item_id = ip.id;

-- ETAPAS

CREATE OR REPLACE VIEW vw_pcp_etapas AS

SELECT
    p.numero AS pedido,
    c.nome AS cliente,

    ip.numero_item AS item,

    pr.codigo AS codigo_produto,
    pr.descricao AS produto,

    ofa.numero_of AS of,
    ofa.status AS status_of,

    e.ordem AS ordem_etapa,
    e.nome AS etapa,

    eof.prevista,
    eof.prazo,
    eof.realizada,

    eof.status AS status_manual,

    CASE
        WHEN eof.realizada IS NOT NULL
            THEN 'REALIZADO'

        WHEN eof.prazo < CURRENT_DATE
            THEN 'ATRASADO'

        WHEN eof.prevista <= CURRENT_DATE
            THEN 'EM_ANDAMENTO'

        ELSE 'PENDENTE'
    END AS status_calculado

FROM pedido p

JOIN cliente c
    ON c.id = p.cliente_id

JOIN item_pedido ip
    ON ip.pedido_id = p.id

JOIN produto pr
    ON pr.id = ip.produto_id

JOIN ordem_fabricacao ofa
    ON ofa.item_id = ip.id

JOIN etapa_of eof
    ON eof.of_id = ofa.id

JOIN etapa e
    ON e.id = eof.etapa_id;

-- COMPONENTES

CREATE OR REPLACE VIEW vw_pcp_componentes AS

SELECT
    p.numero AS pedido,

    ip.numero_item AS item,

    pr.codigo AS codigo_produto,
    pr.descricao AS produto,

    c.codigo AS codigo_componente,
    c.descricao AS componente,
    c.tipo AS tipo_componente,

    pc.quantidade AS quantidade_componente,

    m.nome AS material,
    m.sigla AS material_sigla,

    c.espessura,

    c.largura_plan,
    c.comprimento_plan,

    c.largura_pronta,
    c.comprimento_pronto,
    c.altura_pronta,

    c.peso_bruto,
    c.peso_liquido,

    c.corte,
    c.dobra

FROM pedido p

JOIN item_pedido ip
    ON ip.pedido_id = p.id

JOIN produto pr
    ON pr.id = ip.produto_id

JOIN produto_componente pc
    ON pc.produto_id = pr.id

JOIN componente c
    ON c.id = pc.componente_id

LEFT JOIN material m
    ON m.id = c.material_id;

-- ATRASADOS

CREATE OR REPLACE VIEW vw_pcp_atrasados AS

SELECT
    p.numero AS pedido,
    c.nome AS cliente,

    ip.numero_item AS item,

    pr.codigo AS codigo_produto,
    pr.descricao AS produto,

    ofa.numero_of AS of,

    e.nome AS etapa,

    eof.prevista,
    eof.prazo,

    CURRENT_DATE - eof.prazo AS dias_atrasado

FROM etapa_of eof

JOIN ordem_fabricacao ofa
    ON ofa.id = eof.of_id

JOIN item_pedido ip
    ON ip.id = ofa.item_id

JOIN pedido p
    ON p.id = ip.pedido_id

JOIN cliente c
    ON c.id = p.cliente_id

JOIN produto pr
    ON pr.id = ip.produto_id

JOIN etapa e
    ON e.id = eof.etapa_id

WHERE eof.realizada IS NULL
  AND eof.prazo < CURRENT_DATE;


