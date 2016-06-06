Escrevendo Features
===================

Behat é uma ferramenta para testar o o comportamento
de seua aplicação, escrito em uma linguagem especial
chamada Gherkin. Gherkin é uma `Business Readable, Domain Specific Language <http://martinfowler.com/bliki/BusinessReadableDSL.html>`_ creada especificamente
para a descrição de comportamentos. Isto lhe dá a habilidade
de remover detalhes lógicos dos testes de comportamento.

Gherkin serve como documentação do seu projeto, bem como
para testes automatizados. Behat também tem uma característica
bonus: Ele fala para você usando linguagem verdadeira, humana 
dizendo a você o código que você deve escrever.

    Dica:

    Se você ainda é novo no Behat, vá para :doc:`/quick_intro_pt1` 
    primeiro,então retorne aqui para aprender mais sobre Gherkin.

Sintaxe Gherkin
---------------

Bem como UAML e Python, Gherkin é uma linguagem orientada a espaços, ela
usa identação para definir a estrutura. Os fins de linha encerram as 
declarações (denominados steps) e espaços ou tabs também podem ser usados
para identação (nós sugerimos a você usar espaços para portabilidade).
Finalmente, a maioria das linhas em Gherkin iniciam com uma palavra
chave especial:

.. code-block:: gherkin

    # language: pt
    Funcionalidade: Algum texto descritivo conciso do que é desejado
      A fim de realizar um valor de negócio
      Como ator explicito do sistema
      Eu quero ganhar algum resultado benéfico que promova a meta 

     Texto adicional...
 
      Cenário: Uma determinada situação de negócios
        Dado uma pré condição
        E uma outra pŕe condição
        Quando uma ação feita pelo ator
        E uma outra ação
        E outra ação diferente
        Então um resultado testável é alcançado
        E outra coisa que possamos verificar também acontece
 
      Cenário: Uma situação diferente
        ...

O analizador divide a entrada em funcionalidades, cenários e etapas.
Vamos analizar o exemplo:

.# ``Funcionalidade: Algum texto descritivo conciso do que é desejado`` 
    inicia a feature e lhe dá um título. Aprenda mais sobre funcionalidades
    na seção "`Features`_".

.# As próximas três linhas (``A fim de ...``, ``Como um ...``, ``Eu quero...``)
    dão um contexto fornecem um contexto para as pessoas que lêem o seu recurso 
    e descreve o valor do negócio derivada da inclusão do recurso em seu software.
    Estas linhas não são analisadas pelo Behat e não requerem uma estrutura.
    
.# ``Cenário: Uma determinada situação de negócios`` inicia o cenário e
    contêm uma descrição do cenário. Aprenda mais sobre cenários na seção 
    "`Scenarios`_" 
    
.# As próximas 7 linhas são etapas do cenário, cada um dos quais é comparado
    com um padrão definido em outro lugar. Aprenda mais sobre etapas na
    seção "`Steps`_"

.# ``Cenário: Uma situação diferente`` inicia o próximo e cenário assim por diante.

Quando você está executando a funcionalidade, a porção da direita de cada passo
(após as palavras chaves como ``Dado``, ``E``, ``Quando``, etc) coincide com 
um padrão, que executa uma função callback do PHP. Você pode ler mais sobre 
etapas de coincidencias e execução em :doc:`/guides/2.definitions`.

Funcionalidades
---------------

Todos arquivos ``*.feature`` convencionalmente consistem em uma funcionalidade 
única. Linhas iniciando com a palavra chave ``Funcionalidade:`` (ou o seu 
equivalente) seguido de três linhas identadas iniciam uma funcionalidade. 
Usualmente uma feature contém uma lista de cenários. Você pode escrever 
qualquer coisa que você precise até o primeiro cenário, que inicia com 
``Cenário:`` (ou o seu equivalente) em uma nova linha. Você pode usar
`tags`_ para agrupar funcionalidades e cenários, independente da estrutura
do seu arquivo e diretório.

Todos cenários consistem em uma lista de `etapas`_, que devem iniciar com
uma das palvras chaves ``Dado``, ``Quando``, ``Então``, ``Mas`` ou ``E``
(ou o equivalente de um destes). O Behat trata eles do mesmo modo, mas
você não deve fazer isto.
Aqui temos um exemplo:

.. code-block:: gherkin

    # language: pt
    Funcionalidade: Servir café
        A fim de ganhar dinheiro
        Os clientes devem ser capazes de
        comprar café a todo momento

      Cenário: Compra último café
        Dado que tenha 1 café sobrando na máuqina
        E eu tenha depositado 1 real
        Quando eu pressionar o botão de café
        Então eu deveria ser servido de um café

Além do básico `Cenário`_, uma feature pode conter `Esquema do Cenário`_
e `Contexto`_.

Cenário
-------

Cenários são uma das principais estruturas do Gherkin. Todo cenário deve 
iniciar com a palavra chave ``Cenário:`` (ou palavra chave equivalente),
opcionalmente seguido de um título de cenário. Cada funcionalidade pode 
ter um ou mais cenários e todo cenário consiste em um ou mais `etapa`_.

Os cenários seguintes tem cada um 3 etapas:

.. code-block:: gherkin

    Cenário: Wilson posta em seu blog
      Dado que eu estou logado como Wilson
      Quando eu tento postar "A terapia cara"
      Então eu devo ver "Seu artigo foi publicado."

    Cenário: Wilson falha ao postar algo no blog de outra pessoa
      Dado que eu estou logado como Wilson
      Quando eu tento postar "Greg esbraveja contra impostos"
      Então eu devo ver "Hey! Este não é o seu blog!"

    Cenário: Greg posta em blog cliente
      Dado que eu estou logado como Greg
      Quando eu tento postar "Terapia Cara"
      Então eu devo ver "Seu artigo foi publicado."

Esquema do Cenário
------------------

Copiar e colar cenários para usar diferentes valores pode ser muito 
tedioso e repetitivo:

.. code-block:: gherkin

    Cenário: Comer 5 em cada 12
      Dado que tenho 12 pepinos
      Quando eu comer 5 peninos
      Então eu devo ter 7 pepinos

    Cenário: Comer 5 em cada 20
      Dado que tenho 20 pepinos
      Quando eu comer 5 peninos
      Então eu devo ter 15 pepinos    

Os `Esquemas do Cenários` nos permitem formular estes exemplos com maior precisão 
através da utilização de um modelo com espaços reservados:

.. code-block:: gherkin

    Esquema do Cenário: Comendo
      Dado que tenho <antes> pepinos
      Quando eu comer <come> pepinos
      Então eu devo ter <depois> pepinos

      Exemplos:
        | antes | come | depois |
        |  12   |  5   |   7    |
        |  20   |  5   |   15   |

As etapas do Esquema do Cenário fornecem um modelo que nunca é executado
diretamente. Um Esquema do Cenário é executado uma vez para cada linha 
na seção de exemplos abaixo dela (exceto para a primeira linha 
que é o cabeçalho).

O Esquema do Cenário utiliza espaços reservados, que estão
contidos ``< >`` nas etapas de saída do Cenário. Por exemplo:

.. code-block:: gherkin

    Dado <Eu sou um espaço reservado e estou ok>

Pense em um espaço reservado como uma variável. Isto pode ser substituido
por um valor real das linhas da tabela de ``Exemplos:``, onde o texto 
entre o ângulo de espaço em reservado corresponde ao que o cabeçalho da
coluna da tabela. O valor substituido pelo espaço reservado muda a cada 
execução subsequente do Esquema do Cenário, até que o fim da tabela de
``Exemplos`` seja alcançado.

.. tip::

    Vocẽ também pode usar os espaços reservados em `Argumentos 
    Multilineos`_.

.. note::

    Sua etapa de definições nunca terá que coincidir com o próprio texto 
    do espaço reservado, mas sim os valores terão que substituir o 
    espaço reservado.

Então quando executamos a primeira linha do nosso exemplo:

.. code-block:: gherkin

    Esquema do Cenário: Comer
      Dado que temos <antes> pepinos
      Quando eu comer <come> pepino
      Então teremos <depois> pepinos

      Exemplos:
        | antes | come | depois |
        |  12   |   5  |   7    |

O cenário que realmente é executado é:

.. code-block:: gherkin

    Cenário: Comer
      # <antes> é substituido por 12:
      Dado que temos 12 pepinos
      # <come> é substituido por 5:
      Quando eu comer 5 pepino
      # <depois> é substituido por 7:
      Então teremos 7 pepinos

Contexto
--------

Contexto permite a você adicionar algum contexto a todos os cenários em 
um único recurso. Um Contexto é como um Cenário sem título, que contém
uma série de etapas. A diferença ocorre quando ele é executado: o 
contexto está executando *antes de cada* um de seus cenários, mas depois 
dos seus hooks ``BeforeScenario`` (:doc:`/guides/3.hooks`).

.. code-block:: gherkin

    # language: pt
    Funcionalidade: Suporte a múltiplos sites
    
    Contexto: 
        Dado um administrador global chamado "Greg"
        E um blog chamado "Greg esbraveja contra impostos"
        E um cliente chamado "Wilson"
        E um blog chamado "Terapia Cara" de própriedade de "Wilson"
    
    Cenário: Wilson posta em seu próprio blog
        Dado que eu esteja logado como Wilson
        Quando eu tentar postar em "Terapia Cara"
        Então eu devo ver "Seu artigo foi publicado."

    Cenário: Greg posta no blog de um cliente
        Dado que eu esteja logado como Greg
        Quando eu tentar postar em "Terapia Cara"
        Então eu devo ver "Seu artigo foi publicado"


Etapas
------

`Funcionalidades`_ consiste em etapas, também conhecido como `Dado`_, 
`Quando`_ e ``Então_.

O Behat não tem uma distinção técnica entre estes três tipos de etapas.
Contudo, nós recomendamos fortemente que você faça! Estas palavras
foram cuidadosamente selecionadas para o seus propósito e você deve
saber que o objetivo é entrar na mentalidade BDD.

Robert C. Martin escreveu um 
`ótimo post <https://sites.google.com/site/unclebobconsultingllc/the-truth-about-bdd>`_ 
sobre o conceito de BDD Dado-Quando-Então onde ele pensa neles como uma 
máquina de estados finitos.

Dado
~~~~

O propósito da etapa **Dado** é **colocar o sistema em um estado conhecido** 
antes do usuário (ou sistema externo) iniciar a interalção com o sistema
(na etapa Quando). Evite falar sobre a interação em Dado. Se você trabalhou
com casos de uso, Dado é a sua pré condição.

.. sidebar:: Exemplos de Dado

    Dois bons exemplos do uso de **Dado** são:

    * Crear 

    * Para criar registros (instâncias de modelo) ou de configuração do 
    banco de dados:

      .. code-block:: gherkin

          Dado que não tenha usuários no site
          Dado que o banco de dados esteja limpo

    * Autenticar um usuário (uma exceção para )

    * Autenticar um usuário (uma exceção a recomendação não-interação 
    Coisas que "aconteceram antes" estão ok.):

      .. code-block:: gherkin

          Dado que eu esteja logado como "Everzet"

.. tip::

    Tudo bem chamar a camada de "dentro" da camada de interface do 
    usuário aqui (em Symfony: falar com os modelos).

.. sidebar:: Usando Dado como massa de dados:

    Se você usa ORMs como Doctrine ou Propel, nós recomendamos a utilização
    de uma etapa Dado com o argumento `tabela`_ para configurar registros 
    em vez de objetos. Neste caminho você pode ler todos os cenários em um
    único lugar e fazer sentido fora dele sem ter que saltar entre arquivos: 

    .. code-block:: gherkin

        Dado estes usuários:
        | username | password | email               |
        | everzet  | 123456   | everzet@knplabs.com |
        | fabpot   | 22@222   | fabpot@symfony.com  |

Quando
~~~~~~

O propósito da etapa **Quando** é **descrever a ação chave** que o 
usuário executa (ou, usando a metáfora de Robert C. Martin, a transição
de estado).

.. sidebar:: Exemplos de Quando

    Dois bons exemplos do uso de **Quando** são:
    
    * Interagir com uma página web (a biblioteca Mink lhe dá muitas etapas
    ``Quando`` web-amigáveis fora da caixa):

      .. code-block:: gherkin

          Quando eu estiver em "/alguma/pagina"
          Quando eu preencho o campo "username" com "everzet"
          Quando eu preencho o campo "password" com "123456"
          Quando eu clico em "login"

    * Interagir com alguma biblioteca CLI (chama comandos e grava saída):

      .. code-block:: gherkin

          Quando eu chamo "ls -la"

Então
~~~~~

O propósito da etapa **Então** é **observar saídas**. As observações 
devem estar relacionadas com o valor/benefício de negócios na sua 
descrição da funcionalidade. As observações devem inspecionar a saída 
do sistema (um relatório, interface de usuário, mensagem, saída de 
comando) e não alguma coisa profundamente enterrado dentro dela 
(que não tem valor de negócios e ao invés disso faz parte da 
implementação).

.. sidebar:: Exemplos de Então

    Dois bons exemplos do uso de **Então** são:

    * Verificar algo relacionado ao Dado + Quando está (ou não) na saída:

      .. code-block:: gherkin

          Quando eu chamo "echo hello"
          Então a saída deve ser "hello"

    * Checar se algum sistema externo recebeu a mensagem esperada:

      .. code-block:: gherkin

          Quando eu enviar um email com:
            """
            ...
            """
          Então o cliente deve receber um email com:
            """
            ...
            """

.. caution::

    Embora possa ser tentador implementar etapas Então para apenas 
    olhar no banco de dados - resista à tentação. Você deve verificar
    somente saídas que podem ser observadas pelo usuário (ou sistema 
    externo). Se a base de dados somente é visível internamente por 
    sua aplicação, mas é finalmente exposta pela saída do seu sistema
    em um navegador web, na linha de comando ou uma mensagem de email.

E, Mas
~~~~~~

Se você tem várias etapas Dado, Quando ou Então vocẽ pode escrever:

.. code-block:: gherkin

    Cenário: Múltiplos Dado
      Dado uma coisa
      Dado outra coisa
      Dado mais outra coisa
      Quando eu abrir meus olhos
      Então eu verei qualquer coisa
      Então eu não verei qualquer outra coisa

Ou você pode usar etapas **E** ou **Mas**, permitindo uma leitura mais 
fluente do seu Cenário:

.. code-block:: gherkin

    Cenário: Múltiplos Dado
      Dado uma coisa
      E outra coisa
      E mais outra coisa
      Quando eu abrir meus olhos
      Então eu verei qualquer coisa
      Mas eu não verei qualquer outra coisa

O Behat interpreta as etapas iniciando com E ou Mas exatamente como 
as outras etapas; que não faz distinção entre eles - Mas você deve!

Argumentos Multilineos
----------------------

A linha um `etapa`_

A única linha `etapas`_ permite ao Behat extrair pequenas strings de 
suas etapas e recebê-los em suas step definitions. No entanto, há 
momentos em que você quer passar uma estrutura de dados mais rica a 
partir de uma step definition.

Para isto foram porjetados os Argumentos Multilineos. Eles são 
escritos nas linhas que seguem imediatamente uma etapa e são passadas 
para o método step definition como um último argumento.

Etapas de Argumentos Multilineos vem em dois modos: `tabelas`_ ou `pystrings`_.

Tabelas
~~~~~~~

As tabelas são etapas de argumentos são úteis para a especificação de
um grande conjunto de dados - normalmente como entrada para uma saída 
de Dado ou como espera de um Então.

.. code-block:: gherkin

    Cenário:
      Dado que as seguintes pessoas existem:
        | nome  | email           | fone  |
        | Aslak | aslak@email.com | 123   |
        | Joe   | joe@email.com   | 234   |
        | Bryan | bryan@email.org | 456   |

.. attention::

    Não confunda tabelas com `Esquemas do cenário`_  - sintaticamente 
    eles são identicos, mas eles tem propósitos diferentes. Esquemas
    declaram diferentes valores múltiplos ao mesmo cenário, enquanto
    tabelas são usadas para esperar um conjunto de dados.

.. sidebar:: Tabelas correspondentes em sua Step Definition

    Uma definição correspondente para esta etapa se parece com isso:

    .. code-block:: php

        use Behat\Gherkin\Node\TableNode;

        // ...

        /**
         * @Given as seguintes pessoas existem:
         */
        public function asSeguintesPessoasExistem(TableNode $tabela)
        {
            foreach ($tabela as $linha) {
                // $linha['nome'], $linha['email'], $linha['fone']
            }
        }

    Uma tabela é injetada na definição do objeto ``TableNode``, com 
    o qual vocẽ pode obter um hash de colunas (método 
    ``TableNode::getHast()``) ou por linhas 
    (``TableNode::getRowsHash()``).

PyStrings
~~~~~~~~~

Strings multilineas (também conhecidas como PyStrings) são úteis 
para a especificação de um grande pedaço de texto. O texto deve 
ser compensado por delimitadores que consistem em três marcas de 
aspas duplas (`` """ ``), colocadas em linha:

.. code-block:: gherkin

    Cenário:
      Dado uma postagem em um blog chamado "Random" com:
        """
        Algum título, Eh?
        =================
        Aqui está o primeiro parágrafo do meu post.
        Lorem ipsum dolor sit amet, consectetur adipiscing
        elit.
        """

.. note::

    A inspiração para o PyString vem do Python onde ``"""`` é
    usado para delimitar docstrings, mais ou menos como 
    ``/** ... */`` é usado para docblocks em PHP.

.. sidebar:: PyStrings correspondentes em sua step definitions

    Em sua step definition, não precisa procurar por este texto 
    e corresponder com o seu padrão. O texto vai automaticamente 
    passar pelo último argumento no método step definition. 
    Por exemplo:

    .. code-block:: php

        use Behat\Gherkin\Node\PyStringNode;

        // ...

        /**
         * @Given um post em um blog chamado :titulo com:
         */
        public function umPostEmUmBlogChamado($titulo, PyStringNode $texto)
        {
            $this->criarPost($titulo, $texto->getRaw());
        }

    PyStrings são armazenadas em uma instancia ``PyStringNode``, que você 
    pode simplesmente converter a uma string com ``(string) $pystring``
    ou ``$pystring->getRaw()`` como no exemplo acima.

.. note::

    A identação para abrir ``"""`` não é importante, apesar de ser uma 
    prática comum deixar dois espaços da etapa de fechamento. A identação
    dentro das aspas triplas, entretanto, é significante. Cada linha da
    string passa pela chamada da step definition será re-identada de 
    acordo com a abertura ``"""``. A identação além da coluna de abertura 
    ``"""`` por conseguinte, será preservada.

Tags
----

Tags são uma ótima forma de organizar suas funcionalidades e cenários. 
Considere este exemplo:

.. code-block:: gherkin

    @faturamento
    Feature: Verifica o faturamento

      @importante
      Cenário: Falta da descrição do produto

      Cenário: Vários produtos

Um Cenário ou Funcionalidade pode ter quantas tags você quiser, basta 
apenas separá-los com espaços:

.. code-block:: gherkin

    @faturamento @brigar @incomodar
    Funcionalidade: Verificar o faturamento

.. note::

    Se uma tag existe em uma ``Funcionalidade``, o Behat irá atribuir essa 
    tag para todos os ``Cenários`` filhos e ``Esquemas do Cenário`` também.

Gherkin em Muitas Linguagens
----------------------------

O Gherkin está disponível em muitas linguagens, permitindo você escrever 
histórias usando as palavras chave de sua linguagem. Em outras palavras, 
se você fala Francês, você pode usar a palavra ``Fonctionnalité`` ao invés 
de ``Funcionalidade``.

Para checar se o Behat e o Gherkin suportam a sua lingua (Francês, por exemplo),
execute:

.. code-block:: bash

    behat --story-syntax --lang=fr

.. note::

    Guarde em sua mente que qualquer linguagem diferente de ``en`` precisa 
    ser explicitada com um comentário ``#language: ...`` no início de seu 
    arquivo ``*.feature``:

    .. code-block:: gherkin

        # language: fr
        Fonctionnalité: ...ta
          ...

    Desta forma, suas funcionalidades vão realizar todas as informações sobre 
    seu tipo de conteúdo, o que é muito importante para metodologias como BDD 
    e também dá ao Behat a capacidade de ter recursos de vários idiomas em 
    uma suíte.    
