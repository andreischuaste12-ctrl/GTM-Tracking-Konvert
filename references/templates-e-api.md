# Templates customizados e APIs do GTM

Use ao criar ou revisar template de tag/variável, avaliar template da Community Template Gallery, modificar código sandboxed ou investigar permissão/execução.

## Proveniência e review

Identifique tipo (Web ou Server), nome/ID, origem (built-in, Gallery, template interno, export ou código local), versão instalada, data e alterações locais. Compare o código efetivo e as permissões com a origem declarada. Não atualize por “latest” sem diff; mantenha cópia de segurança e conheça tags/variáveis que dependem do template.

Revise separadamente:

- metadados, campos, defaults, validação e UX de configuração;
- código executado e caminhos de sucesso/falha;
- permissões declaradas e efetivamente necessárias, com escopo mínimo;
- comportamento diante de ausências, tipos inválidos, repetição, timeout e callback;
- tratamento de dados e destinos de rede, cookies, globals, armazenamento e consentimento;
- testes, limitações deles e compatibilidade com a versão usada.

Uma permissão concedida autoriza uma capacidade, não prova que seu uso é necessário ou correto. Uma permissão ampla aumenta o impacto potencial. Restrinja URLs e recursos a destinos e dados justificados pelo contrato.

## Runtime Web sandboxed

Custom templates não executam no `window` global como JavaScript comum. Use apenas runtime/API suportados por `require()` e os tipos/métodos documentados. APIs solicitadas podem exigir permissões no template. Código que funciona no Console do navegador pode falhar no sandbox, no validador de permissões ou em produção.

Para template de consentimento, use `setDefaultConsentState` e `updateConsentState` pelas APIs do GTM. Não use `gtag('consent', ...)` dentro do template: comandos `gtag()` são enfileirados e podem não ser processados antes do evento seguinte. Não confundir essa regra com interfaces da CMP ou integração via `gtag.js`; determine qual runtime está sendo usado.

## Runtime Server sandboxed

Server templates têm APIs e permissões diferentes das Web APIs. Confira documentação específica, `require()` disponíveis, tipos de dados, leitura de event data, resposta HTTP e risco de SSRF. Não copie código de Web para Server nem trate o Server como navegador. Para chamadas externas, valide host/URL, método, dados enviados, timeout e resposta segundo as APIs permitidas e o risco real.

## Testes e limites

Use os unit tests do Template Editor para cenários positivos, entradas ausentes/malformadas, API chamada/não chamada, retorno e erro. Mocks não testam integração de rede real nem necessariamente as verificações de permissão. Execute validação de código/permissões e faça Preview em um container e ambiente não produtivos quando disponíveis.

Capture evidência sem credenciais/PII. Relate o que foi testado em sandbox, o que foi observado em Preview e o que ainda depende de request/aceite do fornecedor. A publicação do template e a adoção do template pelas tags são mudanças separadas.

Políticas `gtag('policy', ...)` podem restringir permissões do template na página; inspecione CSP e política efetiva se a falha ocorrer somente em determinadas rotas/páginas. Não remova política de segurança como correção automática: descubra qual permissão foi negada e valide com responsável pela aplicação.

Referências e links atuais em [fontes oficiais](fontes-oficiais.md).
