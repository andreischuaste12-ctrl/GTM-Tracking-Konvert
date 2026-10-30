# Container GTM Web

## Data Layer e fluxo

Antes de criar tags, observar o evento do navegador e documentar nome, ordem temporal, `dataLayer` e mudanças de rota. Em aplicações SPA/VTEX, não presumir que page load, navegação, DOM Ready e eventos de ecommerce ocorram uma vez ou na mesma página. Usar Preview para conferir se o evento dispara uma tag uma única vez no cenário e momento pretendidos.

Preservar dataLayer do produtor. Não criar no GTM eventos de negócio que duplicam o produtor sem definir claramente o responsável. Para `page_view`, distinguir envio automático da Google tag, tags manuais, mudanças de rota e eventos enviados pelo Server. `send_page_view: false` é uma evidência de configuração daquela tag, não prova ausência de outro emissor.

Para eventos de busca interna, conferir com e sem resultados se o evento e termo aparecem na origem. Mapear os campos reais para `view_search_results`, com quantidade igual a zero permitida quando não houver resultados. Configuração de pesquisa no GA4 não garante que o app VTEX envie o evento.

## Prévia por evento

Para cada evento selecionado, revisar em sequência:

1. `dataLayer` no momento do evento.
2. Variáveis resolvidas no evento (não apenas sua configuração).
3. Acionadores que dispararam e tags que executaram, inclusive exceções.
4. Hit Web e parâmetros de e-commerce/destino.
5. Dados correspondentes no Preview Server quando houver encaminhamento.
6. Resposta do destino e DebugView/Event Manager quando a pergunta exigir recebimento externo.

Use primeiro ações não financeiras — page view, lista, produto, busca, carrinho e etapas do checkout. Confirme moeda, itens, ID de variante/SKU e `event_id` para eventos úteis ao downstream. Eventos em etapas anteriores não comprovam `purchase`.

## Consentimento, identificadores e dados pessoais

Encontre a CMP real e verifique consentimento inicial, atualização, recusa, aceitação e revogação, além das tags que executaram em cada estado. Um objeto `consent` em dataLayer não prova que o estado consumido pelas tags mudou. No GTM, confirme template/API compatível com Consent Mode e ordem correta; a documentação atual do Google orienta usar `setDefaultConsentState` e `updateConsentState` em templates GTM. No `gtag.js`, os comandos de consentimento seguem outra interface. Não substitua a API do GTM por comandos enfileirados sem validar a ordem. Não presuma nome/API da CMP nem trate Consent Mode como banner ou prova de conformidade. Confira [fontes oficiais](fontes-oficiais.md) e regras aplicáveis.

Mantenha dados de usuário em recurso próprio das plataformas quando aplicável, não em parâmetros de evento analítico genéricos. Revise normalização, hashing e origem apenas contra o contrato oficial vigente. Trate payload de e-mail, token e identificadores como sensíveis; não replique valores em relatórios, testes ou arquivos de saída.

## Deduplicação do Pixel e Server

Mapeie todos os emissores do mesmo evento: pixel nativo do app/checkout, tags HTML, template Meta no Server e quaisquer integrações. Registre `event_name`, origem e identificador de evento. Só alegue deduplicação após confirmar, para o mesmo evento lógico, nomes e IDs idênticos nos canais e evidência do Event Manager. Um ID GTM único por ocorrência não é necessariamente um ID estável por pedido. Um event ID de compra tem de seguir o contrato do fornecedor e coordenar browser/server; não inventar um emissor novo para preencher lacuna.

Não contar dois disparos como duas conversões contabilizadas; também não assumir que a Meta os deduplicou sem confirmação. Tipos standard/custom event, Pixel ID e parâmetros de catálogo precisam ser conferidos.

O `eventID` do Pixel em tag HTML personalizada pode ser calculado tarde demais (depois da próxima mensagem do produtor) e divergir do enviado ao Server. No Preview, comparar o ID do Pixel com o número da **própria** mensagem do evento, não com o evento seguinte. Padrão de correção em [licoes-tecnicas.md](licoes-tecnicas.md).

## SPA e eventos repetidos

Em SPA (VTEX IO), page views de terceiros precisam disparar no evento de rota, não só em "All Pages". O produtor pode repetir `pageView` da mesma URL, `view_cart` do minicarrinho ou `add_payment_info` a cada troca de forma de pagamento: tratar com exceção ou chave de deduplicação testada nos dois momentos (acionador e registro).

