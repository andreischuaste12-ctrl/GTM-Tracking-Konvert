# Contratos de eventos e arquitetura de tracking

## O que faz um contrato confiável

Descreva eventos em vocabulário de negócio, não em termos do botão ou da tag. Por evento, registre:

- **Nome e definição:** fato observável, momento exato e condição para ocorrer.
- **Grão:** o que uma linha/evento representa (ação, sessão, item, pedido, pagamento, remessa, reembolso). Não misture grãos no mesmo parâmetro.
- **Produtor e fonte de verdade:** aplicação, backend, checkout, webhook ou integração que originou o fato; dono técnico e responsável pelo dado.
- **Identidade:** ID do evento lógico e IDs de entidade necessários (pedido, pagamento, usuário, item/variante). Explique escopo, estabilidade, unicidade e se o identificador sobrevive a retries e aos fluxos browser/server.
- **Tempo:** hora do evento versus hora de envio/ingestão, timezone e política para atraso/replay quando isso muda análise.
- **Campos:** chave, descrição, tipo, formato/unidade, nulabilidade, enumerações, regra de validação, sensibilidade e destinos autorizados.
- **Semântica monetária:** moeda ISO 4217, major/minor units, inclusões de frete/imposto/desconto, regra de arredondamento e total esperado. Não converta por heurística.
- **Operação:** política de repetição, idempotência/deduplicação, correções, cancelamento/reembolso, versão compatível e contato responsável.

Mantenha um catálogo ou especificação versionada fora de tags dispersas. Uma tabela ou JSON Schema é útil quando automatiza validação; não crie schema cerimonial sem consumidores. Alterações incompatíveis (nome, grão, tipo, semântica, unidade, identidade) precisam de migração coordenada e compatibilidade explícita.

## Arquitetura por camadas

Pense nas camadas separadamente:

1. **Produção do fato:** aplicação ou backend emite fato correto, uma vez por condição de negócio; preservar identificação e dados autoritativos.
2. **Coleta:** dataLayer/GTM Web recebe evento estruturado ou requisição; não depende de texto visual/DOM se existe contrato confiável.
3. **Interpretação:** variáveis, trigger ou Client identificam a mensagem e resolvem dados sem misturar mensagens ou eventos diferentes.
4. **Transformação e roteamento:** validar, normalizar apenas por regra explícita, aplicar consentimento/minimização e mapear a destinos.
5. **Entrega:** browser ou Server envia payload conforme contrato do destino. GTM Server não deve ser tratado como fila durável, sistema transacional, garantia de exactly-once ou warehouse; valide garantias reais do provedor e da infraestrutura.
6. **Consumo e controle:** plataforma, warehouse/BI e fonte financeira podem ter regras distintas. Reconcilie com definição, janela e grão compatíveis.

Documente fluxo e propriedade por evento crítico. Uma matriz simples reduz divergência:

| Evento | Produtor/source of truth | Grão/ID | Web | Server | Destinos | Dono |
|---|---|---|---|---|---|---|

## dataLayer e SPA

- Inicialize o objeto antes do container, se eventos pré-carregamento precisarem estar disponíveis; use o mesmo nome de dataLayer configurado.
- Cada evento deve carregar snapshot coerente dos campos usados naquele fato sempre que possível. O data layer mantém estado; campos antigos podem permanecer após push parcial. Trate explicitamente ausência, estado antigo e limpeza para ecommerce conforme documentação e contrato.
- Não associe `visitorType`, moeda, carrinho ou frete de um push anterior ao pedido atual sem chave que prove a relação.
- Em SPA, observe a navegação real, a política de `page_view` automático/manual e qual sistema dispara a mudança de rota. Não deduza pageview por All Pages ou DOM Ready em toda navegação.
- Conte ocorrências do produtor e avalie reentrância/repetição. Uma regra temporal de GTM não substitui identidade idempotente para pagamentos/pedidos.
- Prefira uma fonte responsável por cada evento. Se browser, checkout, backend e Server enviam o mesmo evento, documente por que e como ocorre deduplicação no destino.

## Nomes e contratos por destino

Mantenha um nome de negócio estável e traduza para nomes/parâmetros de destino em uma tabela de mapeamento. Não force todos os destinos a partilhar um payload incompatível.

- Use nomes recomendados por GA4 quando os semânticos coincidirem e envie os parâmetros exigidos pelo schema oficial para relatórios de ecommerce.
- Preserve IDs de evento/pedido no formato e no escopo definidos pelo destino; a existência do campo não comprova deduplicação.
- Diferencie ID de usuário, ID de sessão, ID de pedido e ID de evento. Não substitua um pelo outro.
- Para itens, mantenha identificador de catálogo, variante, quantidade e preço segundo o catálogo e o destino; confirme compatibilidade entre SKU/variant e feed de anúncio.

## Testes de contrato

Use fixtures sintéticas sem PII, cobrindo payload válido, campos omitidos, valor inválido, moeda distinta, quantidade decimal quando não permitida, array de itens vazio, pedidos e reembolsos parciais, retry e evento duplicado, consentimento negado e alteração de schema. Automatize validações locais quando viável; GTM Preview complementa, não substitui, esses testes.
