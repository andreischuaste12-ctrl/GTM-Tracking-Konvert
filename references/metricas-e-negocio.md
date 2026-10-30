# Métricas de negócio e plano de mensuração

Use este arquivo quando o pedido for plano de mensuração, KPIs, painel/BI, priorização de dados além do funil ou conciliação com receita.

## 1. Defina cada métrica antes de instrumentar

Para cada métrica do painel, registrar:

- fórmula e denominador;
- unidade e moeda;
- janela temporal e fuso;
- fonte (GA4, plataforma de anúncios, e-commerce/ERP, Merchant Center);
- responsável;
- frequência de atualização;
- segmentações permitidas;
- limitações conhecidas (consentimento, bloqueadores, atribuição, cancelamentos).

Mantenha denominadores e coortes consistentes entre períodos. Uma métrica sem fonte e responsável não vai para o painel.

## 2. Árvore de métricas para e-commerce

Resultado de negócio → visitantes elegíveis → conversão (funil `view_item` → `add_to_cart` → `begin_checkout` → `add_shipping_info` → `add_payment_info` → `purchase`) → recompra/retenção → receita líquida e margem.

Métricas de proteção, que não podem piorar enquanto se otimiza a principal: cancelamentos e reembolsos, pedidos não conciliados, eventos duplicados, compras bloqueadas pelo validador, reclamações e carga de suporte.

## 3. Definições econômicas que o tracking precisa sustentar

- **Receita líquida:** depois de descontos, cancelamentos, devoluções e tributos aplicáveis. `purchase` sozinho mede receita registrada, não efetiva — exige o ciclo financeiro do pedido (pago, cancelado, reembolsado; GA4 `refund` com o mesmo `transaction_id`; ajustes de conversão no Google Ads).
- **Margem bruta:** (receita líquida − custos diretos) ÷ receita líquida. Em Google Ads, viabilizada por dados do carrinho na conversão + custo dos produtos no feed do Merchant Center.
- **CAC:** custo atribuível à aquisição ÷ **clientes novos** do mesmo recorte e período. Exige critério confiável de cliente novo (histórico de compras, não só cookie/visitante).
- **LTV e retenção:** explicitar modelo, margem e horizonte; não extrapolar coortes imaturas.
- LTV/CAC isolado engana quando churn, margem, atribuição ou período estão mal definidos.

## 4. Atribuição e evidência

- Atribuição de canal é aproximação. Para decisões de investimento, triangular com incrementalidade/experimentos e com a fonte financeira.
- Classificar afirmações: **fato observado** (dado verificável), **relato** (o que alguém diz), **interpretação**, **hipótese**. Combina com os níveis de evidência do tracking (configurado → Preview → hit → aceito → deduplicado → conciliado).
- Amostra pequena ou de conveniência (poucos pedidos de teste) não representa o comportamento real.

## 5. Escolha dados adicionais pela decisão de negócio

Colete somente o que muda a decisão e tem uma fonte observável:

1. Para receita líquida, associe pedidos a estados de pagamento, cancelamento e reembolso da fonte financeira.
2. Para margem, obtenha custos diretos por item e alinhe-os à mesma moeda, período e definição de receita.
3. Para divergências entre plataformas, concilie pedido a pedido antes de comparar totais agregados.
4. Para aquisição e retenção, use histórico confiável do cliente; cookie ou visitante não prova que alguém é novo.
5. Para abandono de checkout, instrumente falhas apenas quando a plataforma de origem expuser o resultado e o denominador puder ser definido.

## 6. Brief de experimento de mensuração

Pergunta de negócio · hipótese e mecanismo · coorte · alteração testada · baseline · métrica principal e proteções · critério de sucesso/fracasso definido antes · duração e limitações · custo e responsável · resultado · decisão (continuar, ajustar, pausar, encerrar).

## 7. Checklist de lançamento (parte de dados)

Antes de ativar campanha ou mudança relevante: eventos do funil instrumentados, consentimento verificado, atribuição e conversões principais validadas, cancelamento/reembolso tratados, critérios de sucesso e pausa registrados antes de começar.
