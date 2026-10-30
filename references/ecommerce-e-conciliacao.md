# E-commerce, dinheiro e conciliação

## Um contrato por produtor e evento

Antes de normalizar valores, construir uma tabela de fonte/consumidor/evento com caminho do dado, moeda, unidade (reais/centavos), se o campo inclui desconto, frete e imposto, ID do pedido e evidência de Preview. Só depois definir conversão. Nunca dividir todos os números por 100 nem inferir unidade por magnitude. `899` pode ser R$ 899,00; `89900` pode ser centavos; a origem determina a interpretação.

Separar:

- `purchase.value` GA4: valor de itens após desconto, sem frete e impostos incluídos separadamente, segundo a documentação GA4 atual.
- Total pago pelo comprador: total da transação conforme contrato da origem.
- Valor usado pela Meta/Google Ads: contrato e campos próprios de cada integração; conferir documentação vigente e tag/template real.
- `shipping`, `tax`, item `price`, quantidade e moeda: campos explícitos com unidade definida.

Não igualar relatórios de plataformas antes de alinhar janela, moeda, atribuição, definição de receita, estorno/cancelamento e evento efetivamente recebido. Uma compra cancelada após emissão de `purchase` não prova que o evento estava incorreto; examine refund/cancelamento e política de reporte.

## Integridade do pedido

Para compra, resolver ID, itens, moeda, subtotal líquido, frete, imposto e total como **um único pedido validado**. Não selecionar ID de um objeto e valor/itens de outra transação sem comprovar que pertencem ao mesmo evento. `orderFormId`, `transaction_id` e identificador do pagamento não são intercambiáveis.

Validar itens e cálculo com precisão numérica/centavos conforme a plataforma: price válido e não negativo, quantity válida, moeda coerente, IDs presentes e total reconciliado com a definição da origem. Fazer todas as rejeições explicitamente com motivo útil. Não remover `discount` nem ratear desconto global por SKU sem evidência sobre a distribuição. A soma do pedido pode bater embora a receita por item esteja errada.

Não permitir que um fallback envie `purchase` que a validação principal rejeitou. Se recuperação for necessária, aplicar os mesmos critérios financeiros e de identidade e registrar status e motivo. Caso dados insuficientes sejam comuns, reportar a compra como não conciliada em diagnóstico controlado; `undefined` numa variável não impede automaticamente uma tag de disparar.

## Evidência em camadas

Rotule o estado de uma compra/evento:

- esperado pela configuração;
- evento/dataLayer visto no Web Preview;
- variável e objeto resolvidos no evento;
- tag disparada e hit Web criado;
- evento recebido pelo Server;
- tag de saída executada e request externo feito;
- resposta/aceitação do fornecedor;
- evento e transação visíveis no produto/reporting;
- conciliado com pedido e regra financeira.

Uma etapa não prova as seguintes. Para eventos ausentes na loja, ausência em um relatório não localiza a falha. Sem logs de navegador, consentimento, Server e respostas, declare a causa como desconhecida e procure denominadores/controles. Não atribua causalidade a meio de pagamento, atraso antifraude, origem ou desconto a partir de poucos exemplos sem grupo de comparação e denominadores.

Para quantificar, de-duplique pelo ID de pedido apropriado, alinhe intervalo/timezone, estados finais, moeda, bruto/líquido, frete/taxa e cancelamento/refund. Separe pedidos sem match, receita divergente e duplicatas; use taxas por categoria apenas com denominadores comparáveis.

## Ciclo financeiro do pedido

`purchase` registra a venda no momento definido pelo contrato de origem; receita efetiva pode mudar após pagamento, cancelamento e reembolso. Para medir receita líquida, use os estados da fonte financeira e envie `refund` ou ajustes de conversão conforme o contrato vigente de cada destino. Preserve o ID da mesma transação; uma atualização de pagamento não deve emitir uma segunda compra. Métricas derivadas em [metricas-e-negocio.md](metricas-e-negocio.md).

Qualquer decisão que dependa de requisitos atuais de Google Analytics, GTM, Ads ou Meta deve ser conferida nas documentações oficiais antes de implementação de produção.
