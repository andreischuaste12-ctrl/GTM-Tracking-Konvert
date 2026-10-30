# Governança, acesso e release de containers

Use quando a tarefa altera estrutura de container, organiza trabalho entre pessoas/ambientes, usa a API, prepara publicação ou precisa explicar quem pode mudar o quê.

## Modelo mental e escopo

- A hierarquia de configuração é **conta → container → workspace → entidades**. Uma alteração no workspace ainda não é uma versão publicada; `create_version` e `publish` são operações distintas na API.
- Web, Server e containers para outros produtos/plataformas têm IDs, runtimes e ciclo de vida próprios. Um ambiente GTM encaminha configuração de versão a um alvo de implantação; ele não substitui ambiente de QA da aplicação, feature flag nem estratégia de rollout do site.
- Confirme account/container ID, tipo de container, workspace ativo, base da comparação, versão live e ambiente/destino antes de interpretar nomes ou propor mudança. Não inferir produção pelo nome do workspace.
- Papéis e permissões variam por conta/container e podem permitir editar sem publicar, ou publicar sem administrar usuários. Confira acesso efetivo e ownership no produto/API; nunca solicite ou exponha credenciais em texto.

## Revisão de mudança

Antes de editar, fixe um snapshot identificável (export/hash, container, workspace e horário) e inventarie objetos e referências envolvidos. No diff, explique mudanças semânticas e dependências: tags, triggers e exceções, variáveis, sequenciamento, templates/permissões, consentimento, clients e transformations conforme aplicável.

Avalie conflito ou alteração concorrente no workspace antes de sincronizar ou importar. Não escolha substituir/combinar apenas pelo nome da opção: verifique base de comparação, itens existentes, itens removidos/renomeados e efeitos de duplicação. Preserve o estado ativo/pausado e dependências fora do escopo. Se a base mudou desde o snapshot, reavalie o diff em vez de assumir que continua válido.

## Preparação e publicação

1. Descreva intenção, escopo, risco, objetos impactados e critérios de validação antes da mudança.
2. Faça a mudança no workspace apropriado; rode validação/Preview que corresponda ao cenário e examine erros, warnings, dependências e código de template relevante.
3. Revise o diff completo contra a base correta. Não trate a lista de erros como substituta de review de comportamento.
4. Crie versão com nome e descrição que expressem o escopo real. Registre o ID/número da versão e quem aprovou quando isso fizer parte do processo do cliente.
5. Publique/envie para o ambiente somente com autorização explícita para essa ação. Confirme o alvo e a versão antes de executar. Após publicar, leia o estado live e valide um sinal seguro de produção; não dispare compra ou evento financeiro artificialmente.
6. Documente caminho de reversão, versão anterior e condições que justificariam rollback. Rollback também é publicação e deve seguir a autorização aplicável.

Relate o estado exato: **alterado no workspace**, **Preview observado**, **versão criada**, **enviado ao ambiente**, **publicado/live**, **request recebido** ou **contabilizado**. Nunca use “implantado” como sinônimo ambíguo de salvo.

## Uso programático da GTM API

Use API somente quando ela realmente reduz trabalho repetitivo ou permite inventário/diff reproduzível. Prefira leitura para auditoria. Para mutações, confirme IDs e workspace alvo, preserve o snapshot inicial e gere diff legível. Evite scripts que sincronizem ou publiquem automaticamente com base apenas em nomes.

- Use OAuth e o menor escopo/permissão compatível; armazene tokens fora do código e dos logs.
- Descubra entidades e IDs por chamadas de leitura. IDs numéricos, paths da API e nomes de usuário não são intercambiáveis.
- Antes de `sync`, `resolve_conflict`, `create_version`, `publish`, `delete` ou import equivalente, revise precondições e consequência para o workspace/versão/ambiente exato.
- Respeite quota e QPS documentados; faça chamadas limitadas, trate `403` distinguindo quota de autorização, e use retry com backoff apenas em erros transitórios. Não repita operação não idempotente sem descobrir se a primeira foi concluída.
- Registre resultado e erro sem capturar secrets ou payloads pessoais. Verifique estado após cada mutação em vez de confiar somente no HTTP de resposta.

Consulte as páginas da GTM API em [fontes oficiais](fontes-oficiais.md); quotas e métodos podem mudar.
