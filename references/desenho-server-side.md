# Desenho e operação de Server-side Tagging

Use quando a decisão envolve desenho, provisionamento, migração, custo, desempenho, privacidade, disponibilidade ou operação de GTM Server-side.

## Decida pelo requisito

Escreva qual problema se quer resolver: reduzir execução de scripts no navegador, padronizar roteamento, filtrar/enriquecer payload, controlar acesso a dados, coletar em domínio próprio ou integrar fontes servidoras. Compare com alternativas na origem (backend/webhook), GTM Web, SDK ou pipeline de dados. Não trate “mais cookies”, “mais atribuição” ou “bypass de bloqueios/consentimento” como benefício garantido.

Server-side processa requests recebidas em infraestrutura controlada pela organização. Para interações do navegador, um emissor Web ainda precisa coletar e enviar os eventos; a transferência de tag ao servidor não cria fatos que o produtor não emitiu. Dados recebidos só ficam sob controle operacional da organização até serem encaminhados a outros destinos, sujeitos à infraestrutura, acessos e contratos do provedor.

## Linhagem do request

Para cada fluxo, desenhe:

`produtor → transporte/URL → request → Client que reivindica → event data → trigger → Transformation → tag de saída → endpoint externo → resposta`

- Confirme método, path, headers, payload, IDs, consentimento e origem do request. Em Server Preview, o Client de maior prioridade que corresponde reivindica a requisição; valide client vencedor e dados de evento, em vez de inferir pelo nome da tag.
- Clients são adapters que interpretam requests e constroem event data. Uma requisição pode gerar evento(s); request HTTP e evento lógico não são a mesma contagem. GA4 pode agrupar múltiplos eventos em uma requisição.
- Confirme quais parâmetros adicionais o Client interpreta; campos não mapeados podem não virar event data. Algumas tags encaminham campos sem configuração adicional, então aplique transformation para minimizar ou retirar informações que não devem sair.
- Use Transformations como controles explícitos de exposição de campos por tag/tipo/contexto. Verifique prioridade e condições e confira em Preview o que cada tag efetivamente recebeu. Filtrar somente na tag final pode deixar dados disponíveis a outras tags.
- Considere reenvio, latência, timeout, respostas externas e comportamento de falha. Container GTM não é fila durável nem sistema financeiro; se confiabilidade, retry auditável, replay ou exactly-once são requisitos, implemente-os na arquitetura apropriada.

## Consentimento e privacidade

O consentimento é sinalizado no fluxo de acordo com a implementação e sinalização reconhecida pelos produtos. Para GA4 Client e Google tags server-side, confirme propagação dos parâmetros de consentimento do Web, estado visto no Preview Server e configuração do destino. A orientação do Google descreve configuração do Consent Mode no Web para esse fluxo, mas uma CMP/integração específica pode ter requisitos adicionais.

Consent Mode é mecanismo técnico, não banner ou decisão de base legal. Server-side não transforma dados identificáveis em anônimos; hashing é transformação e não anonimização automática. Defina finalidade, base aplicável, retenção, acesso, minimização, destinatários e exclusões com os responsáveis pela privacidade/segurança.

## Infraestrutura e operação

Compare hospedagem gerenciada e manual pelo conjunto real: regiões, domínio first-party/TLS, custos variáveis, escalabilidade, limites de request, cold starts/latência, disponibilidade, logs, controle de acesso, deploy, atualização e responsabilidade por incidente. Verifique valores de preço e capacidade na calculadora/documentação atual; estimativas publicadas mudam e dependem de tráfego, carga dos templates e configuração do Cloud Run ou alternativa.

Planeje e meça pelo menos:

- disponibilidade e latência por endpoint e região;
- volume recebido, reivindicado por Client, rejeitado/sem Client e enviado por destino;
- taxa e motivo de falhas/timeout, atraso de evento e sinais de saturação;
- mudança de custo de infraestrutura, transferência de rede e logging;
- teste de versão Preview e isolamento do servidor de Preview, que precisa da topologia/configuração suportada e pode exigir exatamente uma instância;
- rollback da configuração e do serviço, ownership e alertas.

Configure DNS/HTTPS, controles de origem, rede e autenticação segundo a arquitetura e documentação do provedor. Evite logar corpos completos de request, PII e headers sensíveis. A URL pública de tagging não deve ser confundida com interface de administração.

## Validação e corte

Antes da migração, enumere emissores atuais e destinos para evitar manter o caminho antigo e adicionar outro em paralelo. Teste eventos não financeiros e negativos, consentimento aceito/negado, IDs, moeda, campos removidos, client correto, múltiplos eventos por request, resposta de erro e indisponibilidade. Compare Web e Server para provar transformação e endpoint por cenário.

Faça rollout por ambiente ou coorte quando possível, defina denominadores comparáveis e critérios de reversão antes do corte. Após ativar, verifique requests, diagnósticos do destino e conciliação separadamente. Não conclua sucesso por aumento de requests ou por HTTP 2xx.
