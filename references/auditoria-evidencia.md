# Evidência, auditoria e qualidade de dados

## Identifique a fonte examinada

Para export GTM, registre arquivo, SHA-256, container ID, data de obtenção, versão/workspace declarado e contagens de tags, variáveis, triggers, templates e pastas. Preserve cópia original. Um export não indica por si só o que está publicado. Para UI, anote container, workspace/versão, tela e momento da observação. Reconfirme hash/versão ao final se arquivos puderem mudar durante análise.

Faça inventário estrutural (IDs e nomes duplicados, referências ausentes, triggers órfãos, tags pausadas, sequenciamento, permissões de template) como pista para investigação, não como prova de execução ou bug. Inspecione os campos de configuração e dependências para cada caminho de evento.

## Escada de evidência

Use o rótulo mais alto sustentado pela fonte, com timestamp/cenário e limites:

1. **Declarado no contrato/código de origem** — o produtor pretende emitir o evento.
2. **Configurado no export/workspace** — objeto e regra presentes, sem provar execução.
3. **Observado no navegador/dataLayer** — evento e payload ocorreram naquele cenário.
4. **Resolvido no GTM/Preview** — variáveis, triggers, tags e consentimento se comportaram no cenário testado.
5. **Request de saída observado** — destino, endpoint e payload enviados no browser ou Server.
6. **Recebido/aceito pelo destino** — diagnóstico próprio do destino ou log confiável confirma recebimento; HTTP 2xx sozinho prova resposta de transporte.
7. **Contabilizado** — evento aparece na interface/relatório/API com processamento aplicável e intervalo de latência esperado.
8. **Conciliado** — identidade e valores correspondem à fonte financeira/operacional usando mesma definição, grão, fuso, moeda, período, filtros e janela.

Deduplicação é uma evidência separada: exigir o diagnóstico do destino para o par de eventos e IDs que deveriam ser deduplicados. Não inferir a partir de nomes de tag, IDs presentes ou totais agregados.

## Diagnóstico por caminho

Para cada evento crítico, caminhe em ordem e guarde apenas evidências necessárias, com payload minimizado:

`ação/fato → produtor → dataLayer/request → variável/Client → trigger e exceções → tag → transformação → request de saída → confirmação do destino → consumo/financeiro`

Compare origem e destino por evento lógico, ID, timestamp, parâmetros tipados, moeda/unidade e consentimento. Em Server, confira client vencedor, event data, consentimento, transformations aplicadas, tag de saída e request. Em Web, confira número/momento da mensagem e valores resolvidos nela.

## Métricas de qualidade

Escolha controles que correspondam ao risco e denominador: volume/coverage por evento e etapa; percentual de IDs nulos/inválidos; valores fora de faixa; moeda/tipo/unidade; itens sem ID/preço; taxa de duplicação por identidade; atraso entre fato e recebimento; divergência por destino; proporção reconciliada; falhas por consentimento/sessão/rota. Defina janela, segmento, fonte e limite de alerta antes de interpretar variação.

Não trate contagens iguais como qualidade: eventos podem faltar e duplicar em proporções compensatórias; payload, grão e valor podem divergir mantendo total igual. Não compare usuários/sessões/eventos/pedidos como se fossem a mesma entidade. Separe perda, atraso, valor errado, duplicação, atribuição e divergência de definição de receita.

## Classificação e relatório

Priorize impacto (receita, otimização, privacidade, decisão) e força da evidência. Para cada achado: observação, fonte, cenário, consequência provável, hipótese/alternativas, confiança, recomendação e como verificar. Preserve itens corretos e explique riscos de correção. Nunca use nota percentual subjetiva como confiança ou garantia.
