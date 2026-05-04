# **Descrição do funcionamento do estado actual do projecto**



**Hierarquia de ficheiros:**

Denotar que neste repositório existem pastas e módulos que de momento não estão a ser usados, estão apenas indicados para referência futura do que será acrescentado. O esquema hierarquico abaixo demonstra os módulos que estão activos.

AMORGOUSMULT_INTERMEDIO

├── client

│   ├── clientChoice.py     # Inicialização de clientes

│   ├── host.py             # Lógica principal do cliente e de renderização

├── information

│   └── generic.py          # Constantes, protocolos e configurações de rede estáticas

├── pygame_calls

│   └── game

│         └──── gameLogic.py    # Lógica do movimento de cada jogador, através de Pygame

├── server

│   ├── clientList.py       # Gestão dos clientes ligados

│   ├── connectionHandler.py# Gestão de novas ligações

│   ├── gameState.py        # Gestão do estado global do jogo

│   ├── positionBroadcast.py# Thread para partilhar dados de posição

│   └── serverLogic.py      # Lógica para permitir ligações entre jogadores

└── main.py                 # Inicialização de threads do servidor

# **main.py**

Chama as threads para realizar a comunicação entre cliente e servidor, presentes em server/serverLogic.py e server/connectionHandler.py e a thread responsável por transmitir informação para todos os clientes ligados ao servidor, através de server/positionBroadcast


# **server**

Pasta que contém todos os aspectos da lógica responsável por permitir a comunicação entre clientes, e a ligação de clientes ao servidor

**server/serverLogic.py**

Além das funções que lidam com a transmissão de dados por sockets, introduzidas nos laboratórios anteriores com a calculadora (receive_str, send_str, send_int, send_object, receive_object), existem as funções de serverToClientThread, para criação da thread
e instructionHandler, responsável pela lógica de como lidar com os clientes.

Deve-se notar que na refactorização do código desta entrega, o dicionário de "positions" deixa de ser relevante porque a lógica presente em server/gameState é que permite manter e manipular a informação sobre a posição de cada cliente.
A forma de como o servidor então consegue actualizar a lista, é através de mensagens recebidas através dos clientes. Sempre que um cliente envia uma mensagem ao servidor para a operação de mover (MOVE_OP em generic.py), o servidor prepara-se para receber a mensagem
para a posição actualizada desse mesmo cliente, actualizando o dicionário de posições. Em caso de falha por quebra de ligação, o cliente será removido da lista de clientes.

**server/positionBroadcast.py**

Contém a lógica para a criação de uma thread que realiza o broadcast das posições actuais de cada jogador, para cada cliente na lista, de forma a actualizar a parte gráfica corretamente.
Itera através do dicionário de clientes, e envia o dicionário contendo todas as posições dos jogadores para cada um dos clientes.

**server/connectionHandler.py**

Contém a lógica para a criação da thread responsável para aceitar as ligações por parte dos clientes, abrindo o socket em modo de listening e chamar as funções de clientList.py através da instância clientList de forma a adicionar novos clientes ao dicionário de clientes
e verificar o número actual de clientes.
Adicionalmente, também é responsável por definir o número de cada jogador de forma a definir o esquema de controlo que os jogadores usarão. Isto foi feito devido à parte gráfica ainda não conter um menu, e ser preciso alguma forma para distinguir os jogadores.
Na implementação completa de , o esquema de controlo será definido pelo jogador em si através de um menu e não pela ordem em que os clientes se ligam ao servidor.

**server/clientList.py**

Lida com todos os clientes que estão actualmente ligados ao servidor. Contém as funções de adicionar, remover, obter_lista e obterclient_total.

adicionar permite colocar um novo cliente no dicionário e incrementar o total de clientes

remover retira um cliente do dicionário e decrementa o total de clientes

obter_lista devolve uma cópia do dicionário.

obterclient_total devolve o número total de clientes presentes no dicionário



**server/gameState.py**

Contém a classe de GameState, que contém as funções de startFlag, que lida com a inicialização de um atributo que permite definir se o jogo está em execução, e resetFlag, que volta a colocar o valor do atributo game_active como falso, de forma a definir que o jogo não
está a ser executado. De momento é apenas utilizada a função de startFlag de forma a definir que o jogo começou, no futuro serão utilizadas de forma a validar certas ações que não deverão ocorrer (ou que apenas deverão ocorrer) enquanto o jogo está a ser executado.

Adicionalmente possui as funções de update_player_position, remove_player e get_broadcast_dict.
update_player_position adiciona um jogador ao dicionário se ainda não estiver presente, ou actualiza a sua posição actual

remove_player retira um jogador que esteja actualmente presente no dicionário

get_broadcast_dict devolve o dicionário contendo as posições dos jogadores e dos inimigos. De momento os inimigos ainda não foram adicionados no jogo devido à parte gráfica não estar completamente implementada, por isso o dicionário respectivo aos inimigos é um dicionário
vazio.

# **pygame_calls/game**

Contém os módulos necessários para as ações que um jogador poderá fazer e a lógica dos inimigos e obstáculos que o jogador terá de enfrentar enquanto o jogo decorre.

**game/gameLogic.py**

Classe dedicada às ações que um jogador consegue fazer enquanto está a jogar. De momento o único método relevante é movement, que permite um jogador utilizar as teclas WASD ou setas de forma a controlar o seu movimento no ecrã


# **client**

Contém os módulos que lidam com a lógica do cliente.

**client/clientChoice.py**

Chama o módulo de host.py de forma a criar um cliente, sempre que este programa é iniciado, declarando a posição inicial do jogador.

**client/host.py**

Contém a classe de Host, que define os atributos usados para definir a ligação ao servidor, e os atributos que controlam a posição / velocidade do jogador.

Como indicado antes, de momento a ordem pela qual os jogadores se ligam é que define o esquema de controlo. O esquema de controlo é definido no atributo de self.controls e é utilizado quando se chama os métodos de GameOperations, em gameLogic.py, que lidam 
com a translação de inputs do jogador para movimento no ecrã, actualizando a posição do jogador de acordo com o valor de velocidade associado.

O loop principal encontra-se na função de execute.
Quando chamada é inicializado o relógio de Pygame (de forma a controlar a framerate e garantir que o host está sincronizado com os restantes elementos do jogo) e é também inicializada a janela de Pygame, onde o ambiente gráfico será colocado.

Por cada iteração no loop é actualizada a posição do jogador. Se o jogador tiver mudado de posição desde a última iteração, é enviada uma mensagem com a operação de MOVE_OP, de forma a identificar que o jogador está a realizar uma ação de movimento, e é enviada para o
servidor a nova posição.
Adicionalmente por cada iteração, caso seja recebido uma mensagem de "pos", significa que está-se a receber uma mensagem de positionBroadcast, e nesse caso actualiza-se o dicionário de positions, que permite ao cliente definir onde deverá colocar os objectos gráficos
representativos dos jogadores.

Seguidamente é verificada a posição para ambos os clientes, actualizando o ambiente gráfico de forma a colocar o círculo na posição actual de cada cliente.



# **information**

Contém informação fixa utilizada para a operação dos outros módulos


**information/generic.py**

Contém informação relevante para o tamanho das mensagens a enviar pela ligação, as mensagens específicas a serem enviadas, o port do socket e o endereço do servidor.
Como de momento o desenvolvimento e os testes desta aplicação estão a ocorrer numa única máquina, o servidor aponta para localhost.












