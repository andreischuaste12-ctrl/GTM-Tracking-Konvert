# Documentação oficial e pontos que exigem atualização

Consulte estas páginas ao tomar decisões de produção. Revisão dos links e orientações: 16/10/2026. Os detalhes de plataforma mudam; confirme a versão atual, requisitos do destino, região/consentimento e arquitetura implantada. Esta lista direciona a pesquisa, não substitui a leitura da documentação.

## Web e camada de dados

- [The data layer — Tag Platform](https://developers.google.com/tag-platform/tag-manager/datalayer): eventos `dataLayer.push`, fila de mensagens, estado e requisitos de nomenclatura.
- [Google tag — Tag Platform](https://developers.google.com/tag-platform/gtagjs): configuração e eventos do Google tag.
- [Measure single-page applications with Google Tag Manager — GA4](https://developers.google.com/analytics/devguides/collection/ga4/measure-spa-gtm): mudanças de rota, pageviews manuais, gatilhos de histórico e prevenção de duplicidade.
- [Custom templates quick start — GTM Templates](https://developers.google.com/tag-platform/tag-manager/templates): templates, campos, permissões e testes.
- [Sandboxed JavaScript — GTM Templates](https://developers.google.com/tag-platform/tag-manager/templates/sandboxed-javascript): restrições de runtime; custom template não é JavaScript de navegador comum.
- [Custom template APIs](https://developers.google.com/tag-platform/tag-manager/templates/api): APIs disponíveis em templates Web e testes.
- [Custom template permissions](https://developers.google.com/tag-platform/tag-manager/templates/permissions): capacidades concedidas e restrições de template Web.
- [Template tests](https://developers.google.com/tag-platform/tag-manager/templates/tests): mocks e asserts; unit tests não verificam regras de validação nem permissões reais de APIs simuladas.
- [Custom template policies](https://developers.google.com/tag-platform/tag-manager/templates/policies): política de página pode limitar permissões de templates.

## Consentimento, segurança e privacidade

- [Consent mode overview](https://developers.google.com/tag-platform/security/concepts/consent-mode): responsabilidade pela escolha, sinalização e comportamento de tags; basic vs. advanced.
- [Set up consent mode on websites](https://developers.google.com/tag-platform/security/guides/consent): APIs e ordem de consentimento; implemente segundo CMP e jurisdição.
- [Consent mode with server-side Tag Manager](https://developers.google.com/tag-platform/tag-manager/server-side/consent-mode): fluxo Web → Server e exigências do container.
- [Tag Manager consent mode support](https://support.google.com/tagmanager/answer/10718549): Consent Initialization, checks built-in/adicionais e Consent Overview.
- [Tag Platform security and privacy](https://developers.google.com/tag-platform/security): permissões, governança de container e privacidade.

Consent Mode é mecanismo técnico de comunicação de sinais e comportamento de tags; não é banner, CMP, base legal nem conclusão de conformidade. A configuração permitida depende dos requisitos de negócio e jurídicos atuais.

## Server-side Tag Manager

- [Introduction to server-side tagging](https://developers.google.com/tag-platform/tag-manager/server-side/intro): arquitetura, Clients, event data e controles.
- [Send data to server-side Tag Manager](https://developers.google.com/tag-platform/tag-manager/server-side/send-data): origens de tráfego, configuração de Clients, prioridade e event data.
- [Transformations](https://developers.google.com/tag-platform/tag-manager/server-side/transformations): incluir, enriquecer ou excluir campos expostos às tags e verificar em Preview.
- [Preview and debug server containers](https://developers.google.com/tag-platform/tag-manager/server-side/debug): inspeção de requests, client vencedor, eventos e saídas.
- [Server-side tagging APIs](https://developers.google.com/tag-platform/tag-manager/server-side/api): APIs e permissões para templates.
- [Manual setup guide](https://developers.google.com/tag-platform/tag-manager/server-side/manual-setup-guide): provisionamento, configuração e manutenção da infraestrutura.
- [Google Ads user-provided data in Server-side GTM](https://developers.google.com/tag-platform/tag-manager/server-side/ads-user-data): arquitetura e migração; confirmar requisitos atuais de identidade e consentimento.

Avalie domínio first-party, TLS, latência, disponibilidade, escalabilidade, observabilidade, acesso, custo, retenção e o controlador do ambiente. Server-side permite controlar processamento e roteamento, mas o provedor de hospedagem ainda opera a infraestrutura. Não afirmar que remove restrições de navegador, garante atribuição, torna dado first-party por si só ou contorna consentimento.

Para custos e dimensionamento, consulte a documentação oficial vigente de [Server-side Tag Manager](https://developers.google.com/tag-platform/tag-manager/server-side/overview), [setup no Cloud Run](https://developers.google.com/tag-platform/tag-manager/server-side/cloud-run-setup-guide) e a calculadora de preços do Cloud Run; exemplos de preços e recomendações de instâncias são snapshots, não cotação atual.

## Governança, APIs e Single-page Applications

- [Tag Manager API overview](https://developers.google.com/tag-platform/tag-manager/api/v2): recursos, hierarquia de contas/containers/workspaces e versões.
- [Tag Manager API developer's guide](https://developers.google.com/tag-platform/tag-manager/api/v2/devguide): fluxo programático e OAuth.
- [Tag Manager API reference](https://developers.google.com/tag-platform/tag-manager/api/reference/rest): métodos para workspace, status, versão e publicação.
- [Tag Manager API quotas](https://developers.google.com/tag-platform/tag-manager/api/v2/limits-quotas): limites atuais e políticas de quota.
No Server-side, diferencie requests recebidos por um Client de chamadas ao endpoint Measurement Protocol; confira as capacidades do Client e do destino antes de escolher a rota.

## Analytics e e-commerce

- [Measure ecommerce — GA4](https://developers.google.com/analytics/devguides/collection/ga4/ecommerce): eventos e parâmetros de ecommerce, `items`, moeda e valores.
- [Recommended events — Analytics Help](https://support.google.com/analytics/answer/9267735): nomes e parâmetros recomendados.
- [Validate ecommerce setup](https://developers.google.com/analytics/devguides/collection/ga4/validate-ecommerce): DebugView e diagnóstico de duplicidade/estrutura.
- [Ecommerce scopes — Analytics Help](https://support.google.com/analytics/answer/12947610): parâmetros no escopo de evento e item.

Confirme destino, parâmetros obrigatórios/recomendados, limites, deduplicação, modelagem, atribuição e latência na documentação atual de cada plataforma. Uma regra GA4 não deve ser generalizada para Ads, Meta ou outro endpoint.

## Registro de revisão

Ao acrescentar regras dependentes de plataforma, registre link oficial, data de conferência e qual versão/feature foi confirmada. Remova detalhes obsoletos em vez de acumular instruções contraditórias.


