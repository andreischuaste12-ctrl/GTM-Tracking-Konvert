# Armadilhas técnicas e como comprová-las

Estas situações são riscos de investigação, não regras universais. Confirme no código do produtor, documentação atual e cenário real antes de escolher uma correção.

## Estado da mensagem e avaliação de variáveis

- `dataLayer` acumula estado. Um push parcial pode deixar valores anteriores disponíveis. Confirme se o evento carrega um snapshot coerente e se as variáveis são avaliadas no contexto e momento esperados.
- Tags HTML customizadas, callbacks, sequenciamento e processamento assíncrono podem mudar o momento da leitura. Não use evento ou ID de uma mensagem seguinte para preencher a atual. Compare os campos com a mensagem e ocorrência observadas no Preview.
- Prefira ler a mensagem de negócio que originou o evento por uma interface suportada. Se o contrato exige uma técnica específica para capturar snapshot, prove-a com casos de execução síncrona e tardia antes de generalizar.
- Não use um identificador constante como fallback para `event_id`: isso pode colapsar eventos distintos. Se não há ID confiável, sinalize a lacuna; não invente estabilidade.

## Estado de compilação e Preview

- Erros de referência, formato de export e permissão de template podem impedir salvar, Preview ou publicar. Valide no workspace e confira que a prévia está associada à versão/código esperado.
- Um Preview aparentemente sem mudança pode estar usando outro workspace/container ou uma build anterior. Confira IDs, workspace, hora, evento selecionado, variáveis e versão.
- JavaScript de template GTM é sandboxed e tem APIs/permissões próprias. Sintaxe válida no console do navegador não prova compilação nem permissão de execução do template.
- Valores de variáveis devem ser vistos no evento real. A configuração de uma variável não prova que o valor existe, tem tipo esperado ou pertence àquela ocorrência.

## Repetição e deduplicação

- SPA e widgets podem emitir a mesma navegação ou ação várias vezes; observe a sequência do produtor antes de alterar triggers.
- Identidade idempotente precisa vir do evento/pedido e respeitar o contrato de destino. Timer, URL, SKU ou ID de sessão raramente identificam por si só uma ocorrência financeira.
- Pixel + API server-side só deve ser chamado de deduplicado quando o destino confirma o mesmo nome e chave conforme suas regras vigentes. A presença de `event_id` nos exports não é essa confirmação.
- Diferencie evento duplicado no navegador, duas requisições, dois registros recebidos e duas conversões contadas.

## Export e importação

- Exports são snapshots; nomes de arquivo como `final` e contagens em tela não garantem que se trata de versão publicada ou do workspace atual. Fixe hash, container, versão e origem.
- Antes de importar, examine a prévia e os efeitos de merge/substituição no workspace escolhido; após ação autorizada, confira o conteúdo do workspace e o diff. Uma prévia de import pode comparar com outra base que a equipe imaginava.
- Preserve templates, tags pausadas e dependências até entender os usos. Mudança de nome/pasta não é correção de comportamento.

## Provas mínimas por tipo de afirmação

- “Disparou”: tag e acionador no evento correto do Preview.
- “Enviou”: request e payload de saída observados.
- “Aceito”: confirmação aplicável do produto, sem inferir apenas pelo nome da tag ou status HTTP.
- “Deduplicado”: diagnóstico do destino para os eventos de mesma ocorrência.
- “Compra reconciliada”: ID do pedido, itens e valores comparados à fonte financeira e à definição documentada.

Registre apenas metadados necessários para reproduzir o cenário. Use fixtures sintéticas; não copie PII ou credenciais para logs e relatórios.
