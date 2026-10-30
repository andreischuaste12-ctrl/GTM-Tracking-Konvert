---
name: gtm-organizador-konvert
description: "Projeta, implementa e audita tracking no Google Tag Manager Web e Server-side. Acione para dataLayer, contratos de eventos, GA4/e-commerce, consentimento, deduplicação, templates, GTM API ou arquitetura Server-side. GTM aqui significa Google Tag Manager; não use para Go-to-Market ou analytics sem GTM."
metadata:
  short-description: "Engenharia de dados e tracking com GTM"
---

# Engenharia de dados e tracking com GTM

Trate tracking como um sistema de dados de produção: eventos representam fatos de negócio com semântica, identidade, momento, unidade, origem e consumidores definidos. O objetivo é produzir dados corretos, minimizados, observáveis e reconciliáveis — não maximizar quantidade de tags nem buscar uma promessa de coleta perfeita.

GTM executa e encaminha instrumentação. Não substitui o sistema transacional, uma camada de integração durável, o warehouse, a governança de dados, a CMP ou a validação financeira. GTM Server muda onde parte do processamento ocorre; por si só não torna dados completos, consentidos, atribuíveis ou aceitos por destinos.

## Escolha a rota e leia apenas o apoio necessário

- Projetar tracking ou dataLayer: [contratos e arquitetura](references/contratos-e-arquitetura.md), depois [workflow Web](references/workflow-web.md).
- Auditar export ou workspace: [auditoria e evidência](references/auditoria-evidencia.md); consulte [nomes e estrutura](references/contratos-e-nomenclatura.md) se houver organização do container.
- Investigar SPA, VTEX, consentimento ou navegador: [workflow Web](references/workflow-web.md).
- Server-side, Clients, Transformations, templates, infraestrutura ou privacidade de saída: [workflow Server](references/workflow-server.md).
- Permissões, workspaces, ambientes, API, versionamento e publicação: [governança e release](references/governanca-e-release.md).
- Desenvolver/revisar template customizado Web ou Server: [templates e API](references/templates-e-api.md).
- Avaliar, provisionar ou operar arquitetura Server-side e custos: [desenho Server-side](references/desenho-server-side.md).
- CMP, Consent Mode ou políticas de permissão da página: consulte [fontes oficiais](references/fontes-oficiais.md) e [workflow Web](references/workflow-web.md); leia as referências de templates e Server-side conforme o escopo.
- E-commerce, pedidos, reembolso, moeda, receita e conciliação: [e-commerce e conciliação](references/ecommerce-e-conciliacao.md).
- Plano de mensuração, KPIs e definições financeiras: [métricas e negócio](references/metricas-e-negocio.md).
- Alteração, importação, publicação, teste de produção ou pedido para agir pela interface: [modo de trabalho e release](references/modo-de-trabalho.md).
- Avaliar recomendação de outro modelo: confira cada alegação contra artefatos atuais; use [auditoria e evidência](references/auditoria-evidencia.md). Não aceite nem rejeite a análise em bloco.
- Erro técnico específico já documentado: [lições técnicas](references/licoes-tecnicas.md).
- Decisão dependente de feature, parâmetro ou requisito de plataforma: confirme [fontes oficiais](references/fontes-oficiais.md) e a documentação vigente do destino.

## Princípios de engenharia

1. **Comece no fato de negócio e na fonte.** Descubra quem produz o evento, quando o fato é verdadeiro, qual sistema é fonte da verdade e quais consumidores precisam dele. Não crie evento GTM para compensar um fato ausente ou ambíguo no produtor.
2. **Defina contrato antes de mapear tags.** Especifique nome, grão, gatilho semântico, identidade, timestamp e fuso quando relevante, propriedades, tipos, unidades, nulabilidade, consentimento, destinos e política de duplicação. Consulte [contratos e arquitetura](references/contratos-e-arquitetura.md).
3. **Trace a linhagem de ponta a ponta.** Para cada evento crítico: produtor → dataLayer/request → variável ou Client → acionador → tag → request de saída → destino → relatório ou sistema de conciliação. Registre onde cada etapa foi observada.
4. **Preserve a separação Web/Server.** São containers e runtimes diferentes. Client interpreta requisições no Server e produz event data; tags de saída consomem esses dados. Não presuma equivalência entre variáveis, acionadores, consent checks ou Preview nos dois lados.
5. **Privacidade por finalidade e minimização.** Identifique dados pessoais e identificadores, justifique cada destino, controle consentimento e remova campos desnecessários antes da saída. Hashing não anonimiza por si só. Não exponha valores sensíveis em logs, exports de resposta ou exemplos.
6. **Projete para qualidade e manutenção.** Evite regra de negócio duplicada em muitas tags, nomes que escondem comportamento, conversões implícitas de moeda, fallback que transforma inválido em zero e deduplicação baseada em temporizador sem identidade estável.
7. **Valide cada camada com evidência adequada.** Configuração não comprova execução; execução não comprova request; request não comprova aceite; aceite não comprova contabilização nem conciliação. Use os estados e limites definidos em [auditoria e evidência](references/auditoria-evidencia.md).
8. **Consulte a documentação oficial atual quando a decisão depende de plataforma.** APIs, requisitos de destino, consentimento, parâmetros recomendados, deduplicação, limites e infraestrutura mudam. Use as fontes oficiais indicadas nas referências e verifique a página vigente antes de orientar produção.
9. **Governe mudanças como releases.** Distingua workspace, versão criada, ambiente de teste e versão live. Faça diff, valide dependências e conflitos, registre escopo e plano de reversão; criar uma versão não é publicar e Preview não é produção. Veja [governança e release](references/governanca-e-release.md).
10. **Trate custom templates como código executável com capacidade limitada.** Leia implementação, campos, permissões e proveniência; valide no sandbox e com testes próprios. Um template da Gallery ou repositório upstream não prova equivalência ao código instalado. Veja [templates e API](references/templates-e-api.md).
11. **Avalie Server-side por requisitos e custo total.** Defina quais dados precisam ser processados/roteados no servidor e quais controles isso realmente permite. Inclua origem do evento, consentimento, domínio, disponibilidade, observabilidade, latência, limites, escalabilidade e custo. Veja [desenho Server-side](references/desenho-server-side.md).

## Sequência de trabalho

Use a ordem adequada ao pedido, sem transformar uma auditoria em refatoração:

Execute o trabalho solicitado no escopo autorizado. Em pedido de implementação, altere os artefatos disponíveis e valide o resultado; não encerre com recomendações quando a mudança foi pedida. Em pedido de auditoria, mantenha leitura. Não importe, publique, dispare eventos reais ou altere produção sem autorização explícita para essa ação.

1. Fixe o objetivo, escopo, sistema de origem, destinos, container/ID e estado da fonte (export, workspace, publicado ou observado em produção).
2. Leia implementação e convenções existentes. Marque fatos, inferências, desconhecidos e dados necessários. Não invente nomes de eventos, chaves, IDs, CMPs ou contratos.
3. Defina ou valide o contrato do evento e o resultado de negócio esperado, incluindo grão, identidade, moeda/unidade e tratamento de reenvio.
4. Mapeie dependências Web e Server: ordem do dataLayer, variáveis resolvidas, condições, exceções, consentimento, template/permissões e rotas de saída.
5. Faça a menor alteração coerente com o contrato e preserve comportamento não relacionado. Separe proposta, alteração em arquivo, alteração no workspace e publicação.
6. Valide cenários positivos, negativos e repetidos, consentimento aplicável, campos ausentes/inválidos, tipos/unidades, SPA e eventuais rotas alternativas. Use export offline, testes de template, Preview, requests, ferramentas do destino e conciliação conforme a pergunta.
7. Relate o que foi observado, o que passou/falhou, o alcance do teste, diferenças por destino e o que ainda depende de ambiente ou acesso externo.
8. Em mudanças de container, documente estado inicial/final, diff, dependências afetadas, validação, versão/workspace e se foi apenas salvo, versionado, enviado a ambiente ou publicado.

## Regras de interpretação e risco

- Leia tipo, destino, configuração, acionadores, exceções, consentimento, sequência e status da tag. Nome de objeto não prova comportamento.
- Não assuma que `purchase`, `page_view`, `event_id`, uma tag GA4, um Pixel/CAPI ou resposta HTTP significam o que o nome sugere. Confirme payload e semântica na origem e no destino.
- Não conclua que evento faltou ou duplicou apenas comparando contagens agregadas. Compare mesmo grão, período, fuso, filtros, consentimento, identidade e regras de cada plataforma.
- Verifique referências e dependências antes de renomear, pausar, apagar, importar ou reorganizar objetos. Pasta e nome não corrigem tracking.
- Não publique, importe em workspace, dispare compra real, altere consentimento de produção nem faça outras mudanças externas sem autorização explícita aplicável. Para análise, mantenha somente leitura.
- Nunca reproduza tokens, credenciais, e-mails, telefone ou payload pessoal em resposta ou arquivo. Informe presença, origem e risco sem ecoar o valor.
- Se uma análise externa divergir do export ou UI, fixe o snapshot atual, confirme hash/versão e reavalie apenas os componentes e dependências afetados.
- Ao orientar alguém pela interface, use nomes exatos observados e forneça uma etapa executável por vez. Diferencie salvar no workspace de publicar.

## Entrega de auditoria

Resuma: fonte e estado analisados; objetivo e escopo; fatos com evidência; problemas por impacto e confiança; itens corretos a preservar; plano de correção por dependência; validação realizada e seus limites; próximos dados necessários. Para mudanças, liste arquivos ou objetos alterados e o estado final (local, workspace, Preview, destino, conciliação ou publicado). Nunca declare produção validada com base apenas em configuração, simulação ou Preview.


