# Contratos, dependências e nomes

## Variáveis

Para cada variável, conferir tipo, caminho/código, versão da Data Layer, valor padrão, tipos retornados, referências e disponibilidade no evento de uso. Considerar `undefined`, `null`, string vazia, zero, `false`, tipo inesperado e API/SDK VTEX ainda indisponível. Evitar que acesso ausente quebre execução da tag ou seja convertido silenciosamente em zero.

Seguir a convenção de prefixos que o usuário definiu:

- `DLV | ...` — variável da camada de dados.
- `JS | ...` — JavaScript personalizado.
- `Cookie | ...` — cookie próprio.
- `Constante | ...` — valor constante.
- `Tabela | ...` — tabela de consulta.

Completar com domínio do dado e finalidade em linguagem inequívoca. Em eventos financeiros, distinguir `Pedido | ID da transação`, `Ocorrência | ID do evento`, `Carrinho | orderFormId`, valor em reais e valor em centavos. Não inferir que `id`, `value`, `total` ou `transaction_id` significam o mesmo em produtores diferentes.

Use os caminhos realmente presentes no `dataLayer`. `transaction_id`, `transactionId`, `ecommerce.transaction_id` e `orderFormId` são campos distintos até haver evidência de igualdade e semântica. Dados de evento de uma etapa (por exemplo `add_payment_info`) não provam que o campo existe em `purchase`.

## Acionadores

Nomeie pelo papel, origem e evento, por exemplo `Evento | Ecommerce | purchase`, `Evento | Navegação | pageView | Loja`, `DOM Ready | Page view | Checkout` ou `Exceção | ...`. Use só os rótulos alinhados ao tipo real de acionador.

Confira tipo, evento exato/capitalização, regex e ancoragem, filtros, exceções, tags referenciadas, condições de página e combinações de acionadores. Vários acionadores em uma tag são geralmente alternativas de disparo; filtre exceções na tag e não presuma efeito por nomes. Prefixar regex inteira com `^` e terminar com `$` quando a intenção for evento exato. Testar caminhos com e sem `/`, subcaminhos e caminhos semelhantes.

## Tags e pastas

O nome descreve plataforma, tipo/evento e escopo. Preserve a convenção que já existe no container e não copie prefixos, anos ou identificadores de outro ambiente. Se não houver convenção, proponha um padrão curto e confirme-o antes de renomear objetos existentes.

Confirme independentemente: nome da tag; tipo/template; ID de destino; nome de evento enviado; parâmetros/event settings; objeto de ecommerce; consentimento; acionadores de disparo; exceções; sequenciamento; opção de disparo; estado pausado/ativo. Renomear uma tag não altera o evento enviado.

Pasta é organização visual e não altera coleta. Mover para pasta só é correção quando a organização foi pedida. Antes de copiar uma tag, confirmar que a original será preservada e que nome/acionador/evento da nova são distintos conforme intenção.

## Auditoria estrutural de export

Inventarie os itens e suas relações antes de corrigir: duplicatas, referências ausentes, dependências de templates, acionadores e exceções, tags de setup/teardown, ciclos de sequenciamento e código executável. Quando afirmar que código passou sintaxe, registrar método e escopo. Sintaxe JavaScript normal não prova que um template compila no sandbox do GTM, suas permissões autorizam URLs reais ou a plataforma aceite o payload.

Estrutura válida e referência existente não provam que campo de negócio, tipo, moeda, consentimento, envio ou contabilização estejam corretos. Não reportar zero itens com problema quando o parser ignorou campos ou built-ins.
