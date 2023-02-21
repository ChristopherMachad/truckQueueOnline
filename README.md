# truckQueueOnline
FUNCIONAAAAAAAAAAAAAA!!!!!!

OK, esse foi desafiador. Depois de semanas pesquisando, usando stackoverflow e Chatgpt, descobri o defeito na função Delete.
Consistia em uma falha na formatação do link que era pedido pra deletar.
Adicionei alguns prints na função delete do programa Main, para entender oque estava acontecendo. a formatação estava colocando o link /pedido.json
e o correto era link/pedido/ID.json (prestar atenção para projetos futuros)

Bom, pra caso por algum milagra alguém cair aqui, tudo acontece da seguinte maneira:
- O programa Main tem acesso as funções CRUD para o link do Realtime Firebase que for aberto. (crie o seu)
- O programa janela tem acesso apenas a leitura, no meu caso servirá pra motoristas ficarem longes do escritório porém acompanhando a placa e status dele.
- Para gerar um executavel, é importante que a imagem esteja na mesma pasta que o executavel. Também é importante que o caminho não seja o relativo, mas sim o curto.
