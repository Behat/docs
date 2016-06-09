Definindo Ações Reutilizáveis
=============================

:doc:`Gherkin language</guides/1.gherkin>` fornece uma maneira para descrever
o comportamento da sua aplicação em uma linguagem de negócios compreensível.
Mas como você testa se o comportamento descrito realmente é implementado?
Ou se esta aplicação satisfaz as expectativas de negócios descritas nos
cenários da funcionalidade? O Behat provê uma maneira para mapear suas
etapas de cenário (ações) 1-a-1 com o código PHP chamado na step definitions:

.. code-block:: php

    /**
     * @When eu fizer algo com :argumento
     */
    public function euFizerAlgoCom($argumento)
    {
        // fazer algo com o $argumento
    }

A Casa das Definições - A Classe ``FeatureContext``
---------------------------------------------------

As step definitions são apenas métodos normais de PHP. Eles são métodos 
de instâncias de em uma classe especial chamada :doc:`FeatureContext</guides/4.contexts>`.
Esta classe pode ser facilmente criada executando ``behat`` com o comando 
``--init`` do diretório do seu projeto:

.. code-block:: bash

    $ vendor/bin/behat --init

Depois de você executar este comando, o Behat vai configurar um diretório
``features`` dentro do seu projeto:

A recentemente criara ``features/bootstrap/FeatureContext.php`` terá
uma classe contexto inicial para você começar:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\SnippetAcceptingContext;
    use Behat\Gherkin\Node\PyStringNode;
    use Behat\Gherkin\Node\TableNode;

    class FeatureContext implements SnippetAcceptingContext
    {
        /**
         * Initializes context.
         */
        public function __construct()
        {
        }
    }

Todas step definitions e :doc:`hooks</guides/3.hooks>` necessárias 
para testar seu projeto contra suas funcionalidades serão 
representadas por métodos dentro desta classe.

Criando Sua Primeira Step Definition
------------------------------------

O principal objetivo da step definition é ser executada quando o 
Behat vê a sua etapa correspondente no cenário de execução. Contudo, 
não é apenas porque um método existe em ``FeatureContext`` que o Behat
irá encontrá-lo. O Behat precisa de uma forma de verificar se um 
método de classe concreta é adequado para uma etapa concreta em um 
cenário. O Behat corresponde os métodos do ``FeatureContext`` com a 
step definitions utilizando correspondência padrão.

Quando o Behat é executado, ele compara as linhas de etapas do Gherkin 
de cada cenário com os padrões vinculados a cada método em seu 
`` FeatureContext``. Se a linha do Gherkin satisfaz o padrão vinculado, 
a sua step definition correspondente é executada. Simples assim!

O Behat utiliza anotações php-doc para vincular padrões com os métodos
do ``FeatureContext``:

.. code-block:: php

    /**
     * @When eu fizer algo com :argumentoDoMetodo
     */
    public function algumMetodo($argumentoDoMetodo) {}

Vamos dar uma olhada neste código:

#. ``@When`` é uma palavra chave definida. Há 3 palavras-chave suportadas
   em anotações: ``@Given``/``@When``/``@Then``. Estas três palavras-chave 
   de definição atualmente são equivalentes, mas todas as três permanecem
   disponíveis para que a sua step definition permaneça legível.

#. O texto depois da palavra-chave é a etapa texto padrão(por exemplo:
   ``eu fizer algo com :argumentoDoMetodo``).

#. Todos os valores token do padrão (por exemplo ``:argumentoDoMetodo``) são 
   capturados e passados ao método argumento com o mesmo nome (``$argumentoDoMetodo``).

.. note::
    
    Note que o bloco de comentário inicia com ``/**``, e não o usual ``/*``.
    Isto é importante para o Behat ser capaz de analisar tais comentários como anotações!

Como você já deve ter notado, este padrão é bastante geral e seu método 
correspondente será chamado pelas etapas que contenham 
``...eu fizer algo com...``, incluindo:

.. code-block:: gherkin

    Given eu fizer algo com "string1"
    When eu fizer algo com 'alguma outra string'
    Then eu fizer algo com 25

A única diferença real entre essa etapa aos olhos do Behat é o 
texto token capturado. Este texto será passado para as etapas 
do método ao correspondente valor de argumento. No exemplo acima, 
``FeatureContext::algumMetodo()`` vai ser chamado três vezes,
em cada vez com um argumento diferente:

#. ``$context->algumMetodo($argumentoDoMetodo = 'string1');``.

#. ``$context->algumMetodo($argumentoDoMetodo = 'alguma outra string');``.

#. ``$context->algumMetodo($argumentoDoMetodo = '25');``.

.. note::

    Um padrão não pode determinar automaticamente o tipo de dados de 
    suas correspondências, então todos os argumentos dos métodos vem
    para o step definitions passados como strings. Até mesmo que seu 
    padrão corresponda a "500", que pode ser considerado como um 
    inteiro, '500' será passado como um argumento string para o 
    método step definitions.

    Isto não é uma funcionalidade ou limitação do Behat, mas sim
    uma forma inerente da string corresponder. É sua responsabilidade
    converter os arumentos string para inteiro, ponto flutuante ou 
    booleano onde for aplicável dado o código que você está testando. 

    A conversão de argumentos para tipos específicos pode ser
    feita usando `step argument transformations`_.

.. note::

    O Behat não diferencia palavras-chave da etapa quando corresponde 
    padrões para métodos. Assim uma etapa definida com ``@When``
    também poderia ser correspondida com ``@Given ...``, ``@Then ...``, 
    ``@And ...``, ``@But ...``, etc.

Sua step definitions também pode definir argumentos múltiplos argumentos 
para passar para o método ``FeatureContext`` correspondente:

.. code-block:: php

    /**
     * @When eu fizer algo com :argumentoString e com :argumentoNumero
     */
    public function algumMetodo($argumentoString, $argumentoNumero) {}

Você também pode especificar palavras alternativas e partes opcionais 
de palavras, como esta:

.. code-block:: php

    /**
     * @When aqui esta/estao :contador monstro(s)
     */
    public function aquiEstaoMonstros($contador) {}

Se você precisa de um algoritimo de correspondência muito mais 
complicado, você sempre pode usar a boa e velha expressão regular:

.. code-block:: php

    /**
     * @When /^aqui (?:esta|estao) (\d+) monstros?$/i
     */
    public function aquiEstaoMonstros($contador) {}

Definição de Fragmentos
-----------------------

Agora você sabe como escrever step definitions à mão, mas escrever
todos estes métodos raiz, anotações e padrões à mão é tedioso. O
Behat faz esta tarefa rotineira muito fácil e divertido com a 
geração de Definição de Fragmentos para você! Vamos fingir que 
você tenha esta funcionalidade:

.. code-block:: gherkin

    Funcionalidade:
      Cenário:
        Dado alguma etapa com um argumento "string"
        E uma etapa com número 23

Se a sua classe contexto implementa a interface 
``Behat\Behat\Context\SnippetAcceptingContext`` e você testa uma 
funcionalidade com etapas em falta no Behat:

.. code-block:: bash

    $ vendor/bin/behat features/exemplo.feature

O Behat vai providenciar fragmentos gerados automaticamente para 
sua classe contexto.

Ele não somente gera o tipo de definição adequada (``@Given``), 
mas também propõe um padrão com o token capturado (``:arg1``, 
``:arg2``), nome do método (``algumaEtapaComUmArgumento()``, 
``umaEtapaComNumero()``) e argumentos (``$arg1``, ``$arg2``), 
todos baseados no texto da etapa. não é legal?

A única coisa que falta para você fazer é copiar estes fragmentos 
de métodos para a sua classe ``FeatureContext`` e fornecer um 
corpo útil para eles. Ou melhor ainda, executar o behat com a
opção ``--append-snippets``:

.. code-block:: bash

    $ vendor/bin/behat features/exemplo.feature --dry-run --append-snippets

``--append-snippets`` diz ao behat para automaticamente adicionar
fragmentos dentro de sua classe contexto.

.. note::

    A implementação da interface ``SnippetAcceptingContext`` diz 
    ao Behat que seu contexto espera fragmentos a serem gerados 
    no seu interior. O Behat vai gerar padrões simples de fragmentos 
    para você, mas se a sua for uma expressão regular, o Behat pode
    gerar ao invés de você, se você implementar a interface 
    ``Behat\Behat\Context\CustomSnippetAcceptingContext`` e adicionar
    o método ``getAcceptedSnippetType()`` irá retornar a string ``"regex"``:

    .. code-block:: php

        public static function getAcceptedSnippetType()
        {
            return 'regex';
        }

Tipos de resultado da execução da etapa
---------------------------------------

Agora você sabe como mapear o código atual do PHP que vai ser 
executado. Mas como você pode falar exatamente o que "falhou" 
ou "passou" quando executou uma etapa? E como atualmente o 
Behat verifica se um passo é executado corretamente?

Para isto, nós temos tipos de execução de etapa . O Behat 
diferencia sete tipos de resultados de execuções de etapa: 
"`Successful Steps`_", "`Undefined Steps`_",
"`Pending Steps`_", "`Failed Steps`_", "`Skipped Steps`_", 
"`Ambiguous Steps`_" e "`Redundant Step Definitions`_".

Vamos usar nossa funcionalidade introduzida anteriormente 
para todos os exemplos a seguir:

.. code-block:: gherkin

    # features/exemplo.feature
    Funcionalidade:
      Cenário:
        Dado alguma etapa com um argumento "string"
        E uma etapa com número 23

Successful Steps
~~~~~~~~~~~~~~~~

Quando o Behat encontra uma step definition correspondente 
ele vai executá-la. Se o método definido **not** joga nenhuma 
``Exceção``, a etapa é marcada como bem sucedida (verde). 
O que você retornar de um método de definição não tem efeito 
sobre o status de aprovação ou reprovação do próprio.

Vamos simular que nossa classe contexto contenha o código abaixo:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {
        /** @Given alguma etapa com um argumento :argumento1 */
        public function algumaEtapaComUmArgumento($argumento1)
        {
        }

        /** @Given uma etapa com numero :argumento1 */
        public function umaEtapaComNumero($argumento1)
        {
        }
    }

Quando você executar sua funcionalidade, você vai ver todas as 
etapas passadas serem marcadas de verde. Isso simplesmente porque
não foram lançadas exceções durante a sua execução.

.. note::

    Etapas passadas sempre são marcadas de **verde** se o seu console
    suportar cores.


.. tip::

    Habilite a extensão PHP "posix" para ver a saída colorida do Behat.
    Dependendo do seu Linux, Mac OS ou outro sistema Unix pode fazer 
    parte da instalação padrão do PHP ou um pacote ``php5-posix`` a parte.

Etapas Indefinidas
~~~~~~~~~~~~~~~~~~

Quando o Behat não pode achar uma definição correspondente, a etapa
é marcada como **indefinida**, e todas as etapas subsequentes do cenário
são **ignoradas**.

Vamos supor que temos uma classe contexto vaiza:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {
    }

Quando você executar a sua funcionalidade, você terá 2 etapas 
indefinidas marcadas de amarelo.

.. note::

    Etapas indefinidas sempre são marcadas de **amarelo** se 
    o seu console suportar cores.

.. note::

    Todas as etapas seguintes de uma etapa indefinida não são 
    executadas, como o seguinte comportamento é imprevisível. 
    Estas etapas são marcadas como **ignoradas** (ciano).

.. tip::

    Se você usar a opção ``--strict`` com o Behat, etapas não 
    definidas vão fazer o Behat sair o código ``1``.

Etapas Pendentes
~~~~~~~~~~~~~~~~

Quando uma definição de um método lança uma exceção 
``Behat\Behat\Tester\Exception\PendingException``, a etapa
é marcada como **pendente**, lembrando que você tem trabalho a fazer.

Vamos supor que sua ``FeatureContext`` se pareça com isto:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;
    use Behat\Behat\Tester\Exception\PendingException;

    class FeatureContext implements Context
    {
        /** @Given alguma etapa com um argumento :argumento1 */
        public function algumaEtapaComUmArgumento($argumento1)
        {
            throw new PendingException('Fazer algum trabalho de string');
        }

        /** @Given uma etapa com numero :argumento1 */
        public function umaEtapaComNumero($argumento1)
        {
            throw new PendingException('Fazer algum trabalho de numero');
        }
    }

Quando você executar sua funcionalidade, você terá 1 etapa 
pendente marcada de amarelo e uma etapa seguinte que é marcada
de ciano.

.. note::

    Etapas pendentes sempre são marcadas de **amarelo** se o
    seu console suportar cores, porque são logicamente semelhante 
    aos passos **indefinidos**

.. note::

    Todas as etapas seguintes a uma etapa pendente não são 
    executadas, como o comportamento seguinte é imprevisível.
    Essas etapas são marcadas como **ignoradas**

.. tip::

    Se você usar a opção ``--strict`` com o Behat, etapas não 
    definidas vão fazer o Behat sair o código ``1``.

Etapas Falhas
~~~~~~~~~~~~~

Quando uma definição de um método lança uma ``Exceção`` (exceto 
``PendingException``) durante a execução, a etapa é marcada como
**falha**. Novamente, o que você retornar de uma definição não 
afeta a passagem ou falha da etapa. Retornando ``null`` ou 
``false`` não vai causar a falha da etapa.

Vamos supor, que sua ``FeatureContext`` possua o seguinte código:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {
        /** @Given alguma etapa com um argumento :argumento1 */
        public function algumaEtapaComUmArgumento($argumento1)
        {
            throw new Exception('alguma exceção');
        }

        /** @Given uma etapa com numero :argumento1 */
        public function umaEtapaComNumero($argumento1)
        {
        }
    }

Quando você executar sua funcionalidade, você terá 1 etapa falha
marcada de vermelho e será seguida de uma etapa ignorada marcada
de ciano.

.. note::

    Etapas falhas são marcadas de **vermelho** se o seu console suportar cores.

.. note::

    Todas as etapas seguintes a uma etapa pendente não são 
    executadas, como o comportamento seguinte é imprevisível.
    Essas etapas são marcadas como **ignoradas**

.. tip::

    Se você usar a opção ``--strict`` com o Behat, etapas não 
    definidas vão fazer o Behat sair o código ``1``.

.. tip::

    O Behat não vem com uma ferramenta própria de asserção, 
    mas você pode usar qualquer ferramenta de asserção externa.
    Uma ferramenta própria para asserção é uma biblioteca, na
    qual asserções lancem exceções em caso de falha. Por exemplo, 
    se você está familiarizado com o PHPUnit, você pode utilizar 
    suas asserções no Behat o instalando via composer:

    .. code-block:: bash

        $ php composer.phar require --dev phpunit/phpunit='~4.1.0'

    e então simplesmente utilizar asserções em suas etapas:

    .. code-block:: php

        PHPUnit_Framework_Assert::assertCount(valorInteiro($contador), $this->cesta);

.. tip::

    Você pode ter uma exceção stack trace com a opção ``-vv`` 
    fornecido pelo Behat:

    .. code-block:: bash

        $ vendor/bin/behat features/exemplo.feature -vv

Etapas Ignoradas
~~~~~~~~~~~~~~~~

Etapas que seguem etapas **indefinidas**, **pendentes** ou **falhas** 
nunca são executadas, mesmo que tenham correspondência definida. 
Essas etapas são marcadas como **ignoradas**:

.. note::

    Etapas ignoradas são marcadas de **ciano** se o seu console 
    suportar cores.

Etapas Ambiguas
~~~~~~~~~~~~~~~

Quando o Behat encontra duas ou mais definições correspondentes a 
uma única etapa, esta etapa é marcada como **ambigua**.

Considere que sua ``FeatureContext`` tenha o seguinte código:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {

        /** @Given /^.* etapa com .*$/ */
        public function algumaEtapaComUmArgumento()
        {
        }

        /** @Given /^uma etapa com .*$/ */
        public function umaEtapaComNumero($argument1)
        {
        }
    }

A execução do Behat com este contexto da funcionalidade irá 
resultar no lançamento de uma exceção ``Ambigua``.

O Behat não vai tomar uma decisão sobre qual definição irá executar. 
Este é o seu trabalho! Mas como você pode ver, o Behat vai fornecer 
informações para ajudar você a eliminar o tais problemas.

Step Definitions Redundante
~~~~~~~~~~~~~~~~~~~~~~~~~~~

O Behat não vai deixar você definir uma expressão de etapa correspondente 
a um padrão mais de uma vez. Por exemplo, olhe para dois padrões definidos 
``@Given`` em seu contexto de funcionalidade:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {
        /** @Given /^etapa com numero (\d+)$/ */
        public function trabalhandoComUmNumero($numero1)
        {
        }

        /** @Given /^etapa com numero (\d+)$/ */
        public function trabalhandoComUmNumeroDiferente($numero1)
        {
        }
    }

Executando o Behat com este contexto de funcionalidade irá resultar no 
lançamento de uma exceção ``Redundante``.

Transformações da Etapa Argumento
---------------------------------

Transformações da etapa argumento permite você abstrair operações comuns
executadas em argumentos no método de definição da etapa, em um dado mais 
específico ou em um objeto.

Cada método de transformação deve retornar um valor novo. Este valor, em 
seguida, substitui o valor original da string ele estava sendo utilizado 
como um argumento para um método de definição da etapa.

Métodos de transformação são definidos utilizando a mesmo estilo de 
anotação como métodos de definição, mas sim usar a palavra-chave ``@Transform``, 
seguido de um padrão correspondente.

Como um exemplo básico, você pode automaticamente converter todos os 
argumentos numericos para inteiro com o seguinte código na classe de contexto:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {
        /**
         * @Transform /^(\d+)$/
         */
        public function converteStringParaNumero($string)
        {
            return intval($string);
        }

        /**
         * @Then um usuario :nome, deve ter :contador seguidores
         */
        public function confirmaUsuarioTemSeguidores($nome, $contador)
        {
            if ('inteiro' !== gettype($contador)) {
                throw new Exception('Um número inteiro é esperado');
            }
        }
    }

.. note::

    Assim como em definições de etapa, você também pode usar ambos 
    os simples padrões e expressões regulares.

Vamos a uma etapa mais distante e criar um método de transformação 
que pegue um argumento string de entrada e retorne um objeto específico. 
No exemplo a seguir, nosso método de transformação vai passar um nome 
de usuário e o método vai criar e retornar um novo objeto ``Usuario``:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {
        /**
         * @Transform :usuario
         */
        public function converteNomeDeUsuarioEmUmUsuario($usuario)
        {
            return new Usuario($usuario);
        }

        /**
         * @Then um :usuario, deve ter :contador seguidores
         */
        public function confirmaUsuarioTemSeguidores(Usuario $usuario, $contador)
        {
            if ('integer' !== gettype($contador)) {
                throw new Exception('Um número inteiro é esperado');
            }
        }
    }

Transformando Tabelas
~~~~~~~~~~~~~~~~~~~~~

Vamos supor que nós escrevemos a seguinte funcionalidade:

.. code-block:: gherkin

    # features/table.feature
    Funcionalidade: Usuários

      Cenário: Criando Usuários
        Dado os seguintes usuários:
          | nome          | seguidores |
          | everzet       | 147        |
          | avalanche123  | 142        |
          | kriswallsmith | 274        |
          | dgosantos89   | 962        |

E nossa classe ``FeatureContext`` parecida com esta:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;
    use Behat\Gherkin\Node\TableNode;

    class FeatureContext implements Context
    {
        /**
         * @Given os seguintes usuarios:
         */
        public function incluiUsuarios(TableNode $tabelaUsuarios)
        {
            $users = array();
            foreach ($tabelaUsuarios as $hashUsuario) {
                $usuario = new Usuario();
                $usuario->colocaNomeUsuario($hashUsuario['nome']);
                $usuario->colocaContadorDeSeguidores($hashUsuario['seguidores']);
                $usuarios[] = $usuario;
            }

            // fazer a mesma coisa com $usuarios
        }
    }

Uma tabela como esta pode ser necessária em uma etapa que teste a criação 
dos próprios objetos ``Usuario``, e mais tarde usada novamente para validar 
outras partes de nosso código que dependa de múltiplos objetos ``Usuario`` 
que já existam. Em ambos os casos, nosso método de transformação pode usar 
nossa tabela de nomes de usuarios e contador de seguidores e construir os 
usuários fictícios. Ao usar um método de transformação nós eliminamos a 
necessidade de duplicar o código que cria nossos objetos ``Usuario``, e 
ao invés disso podemos contar com o método de transformação em cada 
momento que esta funcionalidade for necessária.

Transformações também podem ser usadas com tabelas. Uma transformação 
de tabela é correspondida por vírguas que delimitam a lista de 
cabeçalho das colunas prefixadas com ``table:``:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;
    use Behat\Gherkin\Node\TableNode;

    class FeatureContext implements Context
    {
        /**
         * @Transform table:nome,seguidores
         */
        public function converteTabelaUsuarios(TableNode $tabelaUsuarios)
        {
            $usuarios = array();
            foreach ($tabelaUsuarios->getHash() as $hashUsuario) {
                $usuario = new Usuario();
                $usuario->colocaNomeUsuario($hashUsuario['nome']);
                $usuario->colocaContadorDeSeguidores($hashUsuario['seguidores']);
                $usuarios[] = $usuario;
            }

            return $usuarios;
        }

        /**
         * @Given os seguintes usuarios:
         */
        public function incluiUsuarios(array $usuarios)
        {
            // faça alguma coisa com $usuarios
        }

        /**
         * @Then eu espero que os seguintes usuarios:
         */
        public function confirmaUsuarios(array $usuarios)
        {
            // faça alguma coisa com $usuarios
        }
    }

.. note::

    Transformações são poderosas e é importante ter cuidado como você 
    as implementa. Um erro pode frequentemente introduzir um estranho 
    e inesperado comportamento. Também, eles são por natureza difíceis 
    de serem depurados devido a sua natureza altamente dinâmica.

Procure no seu dicionário de etapas
-----------------------------------

Tal como o seu conjunto de cenários irá crescer, há uma boa chance de 
que a quantidade de etapas diferentes que você terá à sua disposição 
para escrever novos cenários também irá crescer.

O Behat provem uma opção de linha de comando ``--definitions`` ou 
simplesmente ``-d`` para navegar facilmente nas definições, a fim de 
reutilizá-los ou adaptá-los (introdução de novos espaços reservados 
por exemplo).

Por exemplo, quando utilizamos o contexto Mink provido pela extensão 
Mink, você terá acesso a este dicionário de etapas executando:

.. code-block:: console

    $ behat -di
    web_features | Given /^(?:|I )am on (?:|the )homepage$/
                 | Opens homepage.
                 | at `Behat\MinkExtension\Context\MinkContext::iAmOnHomepage()`

    web_features | When /^(?:|I )go to (?:|the )homepage$/
                 | Opens homepage.
                 | at `Behat\MinkExtension\Context\MinkContext::iAmOnHomepage()`

    web_features | Given /^(?:|I )am on "(?P<page>[^"]+)"$/
                 | Opens specified page.
                 | at `Behat\MinkExtension\Context\MinkContext::visit()`

    # ...

ou, pela saída curta:

.. code-block:: console

    $ behat -dl
    web_features | Given /^(?:|I )am on (?:|the )homepage$/
    web_features |  When /^(?:|I )go to (?:|the )homepage$/
    web_features | Given /^(?:|I )am on "(?P<page>[^"]+)"$/
    web_features |  When /^(?:|I )go to "(?P<page>[^"]+)"$/
    web_features |  When /^(?:|I )reload the page$/
    web_features |  When /^(?:|I )move backward one page$/
    web_features |  When /^(?:|I )move forward one page$/
    # ...

Você também pode procurar por um padrão específico executando:

.. code-block:: console

    $ behat --definitions="field" (ou simplesmente behat -dfield)
    web_features | When /^(?:|I )fill in "(?P<field>(?:[^"]|\\")*)" with "(?P<value>(?:[^"]|\\")*)"$/
                 | Fills in form field with specified id|name|label|value.
                 | at `Behat\MinkExtension\Context\MinkContext::fillField()`

    web_features | When /^(?:|I )fill in "(?P<field>(?:[^"]|\\")*)" with:$/
                 | Fills in form field with specified id|name|label|value.
                 | at `Behat\MinkExtension\Context\MinkContext::fillField()`

    #...

É isso aí, agora você pode procurar e navegar pelo seu dicionário de etapas inteiro.
