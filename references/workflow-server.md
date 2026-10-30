# Container GTM Server

O Server recebe eventos e encaminha/transforma dados. Identifique o client que aceitou cada request, os dados recebidos, tags de saída, transformação, consentimento e destino. Uma tag de encaminhamento GA4 não é uma conversão Google Ads nem uma confirmação de que o evento foi contado.

## Ordem de revisão

1. Confirmar container Server, domínio de tagging, workspace/publicação e transportador Web real.
2. Inspecionar clients e precedência: qual client reivindica request; diferenciar GA4 de outros formatos.
3. Inspecionar dados de evento recebidos e client name no Preview; não inferir conteúdo a partir do nome do acionador.
4. Conferir acionadores, regex, filtros e tags dedicadas/genéricas. Excluir eventos auxiliares ou roteados por tags dedicadas de uma regra genérica quando causa sobreposição, depois de verificar impacto.
5. Conferir transformações e saídas: eventos, `event_id`, `transaction_id`, itens, moedas, valor, consentimento e configurações atuais do template.
6. Conferir as respostas externas e deduplicação separadamente.

Regex de allowlist de eventos deve ser ancorada (`^(eventA|eventB)$`) se a intenção for match exato. `purchase` dentro de `.+purchase` também pode aceitar `fake_purchase`; valide nomes auxiliares e capitalize exatamente. “Todos os eventos personalizados” é amplo; aplique filtros de client e eventos necessários.

Use o template instalado como fonte efetiva. Documentação do template GitHub ou versão upstream não prova que o template personalizado na conta é idêntico. Examine permissões, variáveis, template code, versão de API, URLs, campos e credenciais. Não expor tokens em código, logs, outputs ou exemplos. Usar constantes/cofre suportado e confirmar rotação diretamente no fornecedor quando credencial já foi exposta.

Antes de atualizar um template, comparar versão do código original, mudança local e permissões atuais. Não substituir custom template pela última versão presumida. Preservar tags pausadas, escopos de permissão e acionadores existentes até que a mudança exata seja conhecida.

Evidência de `POST` com status 200/204 indica resposta HTTP nesse teste. Para Meta, se presente, conferir `events_received` e mensagens. Isso não garante contabilização em Ads Manager, deduplicação ou persistência em relatórios GA4. Diferencie aceitação na camada Server, resposta do fornecedor, Test Events e relatório final.
