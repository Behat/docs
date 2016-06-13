Funcionalidades de teste
========================

Nós já usamos esta estranha classe ``FeatureContext`` como uma casa para nossa 
:doc:`definição de etapas </guides/2.definitions>` e :doc:`hooks </guides/3.hooks>`,
mas nós não temos feito muito para explicar o que realmente é.

Classes de contexto são uma pedra angular do meio ambiente de testes em Behat. 
A classe de contexto é uma simples POPO - Plain Old PHP Object (Ou traduzido 
literalmente: Objeto PHP Simples Velho) que diz ao Behat como testar as suas 
funcionalidades. Se todos arquivos ``*.feature`` descrevem *como* sua 
aplicação se comporta, então a classe de contexto é sobre como testar isso.

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;

    class FeatureContext implements Context
    {
        public function __construct($parametro)
        {
            // instanciar contexto
        }

        /** @BeforeFeature */
        public static function prepararParaAFuncionalidade()
        {
            // limpar o banco de dados ou fazer outras preparações
        }

        /** @Given nós temos algum contexto */
        public function prepararContexto()
        {
            // fazer algo
        }

        /** @When ocorrer um evento */
        public function fazerAlgumaAcao()
        {
            // fazer algo
        }

        /** @Then algo deve ser feito */
        public function checar()
        {
            // fazer algo
        }
    }

Um mnemônico simples para classes de contexto é "testar funcionalidades *em um contexto*".
Descrições de funcionalidades tendem ser muito alto nível. Isto siginifca que 
não há muito detalhe técnico exposto neles, então o caminho para você testar 
essa linda funcionalidade depende do contexto em que seu teste está contido. 
Isso é o que as classes de contexto são.

Requerimentos de Classe de Contexto
-----------------------------------

A fim de ser usado pelo Behat, sua classe de contexto deve seguir as seguintes regras:

#. A classe de contexto deve implementar a interface ``Behat\Behat\Context\Context``.

#. A classe de contexto deve ser chamada ``FeatureContext``. É uma simples 
   convenção dentro da infraestrutura do Behat. ``FeatureContext`` é o nome da 
   sua classe de contexto para uma suite padrão. Isto pode ser facilmente 
   alterado através da configuração da suite dentro de ``behat.yml``.

#. A classe de contexto deve ser detectável e carregável pelo Behat. Isso 
   significa que você deve de alguma forma dizer ao Behat sobre o arquivo 
   de classe. O Behat vem com uma PSR-0 carregamento automático fora e o 
   carregamento automático de diretório padrão é ``features/bootstrap``. 
   É por isso que é carregado o padrão ``FeatureContext`` tão fácil pelo Behat. 
   Você pode colocar suas próprias classes sob ``features/bootstrap`` seguindo 
   a convenção PSR-0 ou você pode até definir seu próprio arquivo auto 
   carregável em ``behat.yml``.

.. note::

    ``Behat\Behat\Context\SnippetAcceptingContext`` e 
    ``Behat\Behat\Context\CustomSnippetAcceptingContext`` são versões
    especiais da interface ``Behat\Behat\Context\Context`` que dizem 
    ao Behat neste contexto, espera fragmentos a ser gerado por ele.

A forma mais fácil de começar a utilizar o Behat em seu projeto é chamar 
o ``behat`` com a opção ``--init`` dentro do diretório do seu projeto:

.. code-block:: bash

    $ vendor/bin/behat --init

O Behat irá criar um alguns diretórios e uma classe esqueleto ``FeatureContext``
dentro do seu projeto.

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


Tempo de vida do Contexto
-------------------------

Sua classe de contexto é inicializada antes de cada cenário ser executado, e 
todos os cenários tem a sua própria instância do contexto. Isto significa 2 
coisas:

#. Todos os cenários são isolados de cada um dos outros cenários de contexto. 
   Você pode fazer quase qualquer coisa dentro da instância do seu cenário de 
   contexto sem medo de afetar outros cenários - todos os cenários tem a sua 
   própria instância do contexto.

#. Todas as etapas em um único cenário são executados dentro de uma instância
   de contexto comum . Isto significa que você pode colocar instâncias ``privadas`` 
   variáveis dentro de sua etapa ``@Given`` e você será capaz de ler seus novos 
   valores dentro de suas etapas ``@When`` e ``@Then``.

Contextos Multiplos
-------------------

Em algum momento, manter tudo em uma única classe :doc:`step definitions </guides/2.definitions>`
e :doc:`hooks </guides/3.hooks>` poderia se tornar muito difícil. Você poderia 
utilizar herança de classes e dividir as definições em múltiplas classes, mas 
fazer isto poderia tornar muito difícil de seguir o seu código e utilizá-lo.

À luz destas questões, o Behat provê um caminho mais flexivel para ajudar a 
fazer um código mais estruturado, permitindo que você utilize múltiplos 
contextos em uma única suite de teste.

A fim de personalizar a lista de contextos que sua suíte de teste requer, 
você precisa ajustar a configuração da suite dentro de `` behat.yml``:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            default:
                contexts:
                    - FeatureContext
                    - SecondContext
                    - ThirdContext

A primeira ``default`` nesta configuração é um nome do perfil. Nós vamos 
discutir em :doc:`profiles </guides/6.profiles>` um pouco mais tarde. 
Sobre o perfil específico, nós temos uma seção especial ``suites``, 
que configura suites dentro deste perfil. Nós vamos falar sobre suites 
de teste com mais detalhes no :doc:`próximo capítulo </guides/5.suites>`, 
por hora basta tem em sua mente que uma suite é uma forma de dizer ao Behat 
onde encontrar suas funcionalidades e como as testar. A parte interessante 
para nós agora é a seção ``contextos`` - esta é uma matriz de nomes de 
classes de contexto. O Behat utilizará as classes especificadas em 
seu contexto de funcionalidades. Isto significa que a cada vez que o 
Behat ver um cenário em sua suite de testes, ele irá:

#. Pegar a lista de todas as classes de contexto da opção ``contexts``.

#. Tentará inicializar todas estas classes de contexto em Objetos.

#. Buscará por :doc:`step definitions </guides/2.definitions>` e 
   :doc:`hooks </guides/3.hooks>` em todos eles.

.. note::

    Não se esqueça que cada uma destas classes de contexto deve seguir 
    todos os requerimentos de uma classe de contexto. Especificamente - 
    todos eles devem implementar a interface ``Behat\Behat\Context\Context`` 
    e ser autocarregadas pelo Behat.

Basicamente, todos os contextos sob a seção ``contexts`` em seu ``behat.yml`` 
são os mesmos para o Behat. Ele vai encontrar e utilizar os métodos da 
mesma forma que faz na ``FeatureContext`` padrão. E se você estiver feliz 
com uma única classe de contexto, mas você não gosta do nome ``FeatureContext``,
aqui está como você muda isto:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            default:
                contexts:
                    - MyAwesomeContext

Esta configuração irá dizer ao Behat para olhar para ``MyAwesomeContext`` 
ao invés da padrão ``FeatureContext``.

.. note::

    Ao contrário de :doc:`profiles </guides/6.profiles>`, o Behat não irá 
    herdar qualquer configuração de sua suite ``default``. O nome ``default`` 
    é utilizado somente para demonstração neste guia. Se você tem múltiplas 
    suites que todas devem utilizar o mesmo contexto, você deverá definir este 
    contexto específico para cada suite específica:

    .. code-block:: yaml

        # behat.yml

        default:
            suites:
                default:
                    contexts:
                        - MyAwesomeContext
                        - MyWickedContext
                suite_a:
                    contexts:
                        - MyAwesomeContext
                        - MyWickedContext
                suite_b:
                    contexts:
                        - MyAwesomeContext

    Esta configuração irá dizer ao Behat para olhar para ``MyAwesomeContext`` 
    e ``MyWickedContext`` quando testar ``suite_a`` e ``MyAwesomeContext`` 
    quando testar ``suite_b``. Neste exemplo, ``suite_b`` não será capaz de 
    chamar etapas estão definidas em ``MyWickedContext``. Como você pode ver, 
    mesmo se você utilizar o nome ``defaukt`` como o nome de uma suite, o Behat 
    não irá herdar qualquer configuração desta suite.

Parâmetros de Contexto
----------------------

Classes de contexto podem ser muito flexiveis dependendo de quão longe 
você quer ir em fazê-los dinâmicos. A maioria de vai querer fazer 
nossas contextos ambiente-independente; onde deve nós colocaremos 
arquivos temporários, como URLs que serão utilizadas para acessar a 
aplicação? Estas são as opções de configuração de contexto altamente 
dependentes do ambiente que você irá testar as suas funcionalidades.

Já dissemos que classes de contexto são simplesmente velhas classes PHP.
Como você incorporaria parâmetros ambiente-dependentes em sua classe 
PHP? Utilize *argumentos no construtor*:

.. code-block:: php

    // features/bootstrap/MyAwesomeContext.php

    use Behat\Behat\Context\Context;

    class MyAwesomeContext implements Context
    {
        public function __construct($baseUrl, $tempPath)
        {
            $this->baseUrl = $baseUrl;
            $this->tempPath = $tempPath;
        }
    }

Na realidade, o Behat lhe dá a habilidade de fazer exatamente isto. 
Você pode especificar argumentos requiridos para instanciar sua classe 
de contexto através de alguma configuração ``contexts`` em seu ``behat.yml``:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            default:
                contexts:
                    - MyAwesomeContext:
                        - http://localhost:8080
                        - /var/tmp

.. note::

    Nota sobre identação para parâmetros. É significativo:

    .. code-block:: yaml

        contexts:
            - MyAwesomeContext:
                - http://localhost:8080
                - /var/tmp

    Alinhado a quatro espaços da própria classe de contexto.

Argumentos seriam passados ao construtor ``MyAwesomeContext`` na 
ordem especificada aqui. Se você não está feliz com a ideia de 
manter uma ordem de argumentos em sua cabeça, você pode utilizar 
nomes de argumentos em vez disso:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            default:
                contexts:
                    - MyAwesomeContext:
                        baseUrl: http://localhost:8080
                        tempPath: /var/tmp

Na realidade, se você o fizer, a ordem em que você especificar estes 
argumentos se torna irrelevante:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            default:
                contexts:
                    - MyAwesomeContext:
                        tempPath: /var/tmp
                        baseUrl: http://localhost:8080

Levando isso um passo adiante, se os seus argumentos de construtor 
de contexto são opcionais:

.. code-block:: php

    public function __construct($baseUrl = 'http://localhost', $tempPath = '/var/tmp')
    {
        $this->baseUrl = $baseUrl;
        $this->tempPath = $tempPath;
    }

Você então pode especificar somente o parâmetro que você precisa mudar atualmente:

.. code-block:: yaml

    # behat.yml

    default:
        suites:
            default:
                contexts:
                    - MyAwesomeContext:
                        tempPath: /var/tmp

Neste caso, o valor padrão seria utilizado para outros parâmetros.

Traços de Contexto
------------------

O PHP 5.4 trouxe uma funcionalidade interessante para a linguagem - traços.
Traços são um mecanismo para reutilização de código em linguagens de 
herança simples como o PHP. Traços são implementados em PHP como um 
copia-cola em tempo de compilação. Que significa se você colocar alguma 
definição de etapa ou hooks dentro de um traço:

.. code-block:: php

    // features/bootstrap/DicionarioDeProdutos.php

    trait DicionarioDeProdutos
    {
        /**
         * @Given que tenha uma(s) :arg1, que custe R$:arg2
         */
        public function queTenhaUmaQueCusteR($arg1, $arg2)
        {
            throw new PendingException();
        }
    }

E então utilize isto em seu contexto:

.. code-block:: php

    // features/bootstrap/MyAwesomeContext.php

    use Behat\Behat\Context\Context;

    class MyAwesomeContext implements Context
    {
        use DicionarioDeProdutos;
    }

Só irá funcionar como você espera.

Traços de contexto vem a calhar se você gostaria de ter contextos diferentes, 
mas ainda precisa utilizar a mesma etapa de definições em ambos. Ao invés de 
terem o mesmo código em ambos - você deve criar um único Traço que você 
``utiliza`` em ambas classes de contexto.

.. note::

    Dado que a etapa de definições :doc:`não pode ser duplicada dentro de um 
    Suite </guides/2.definitions>`, isso só vai funcionar para contextos utilizados 
    em suites separadas.

    Em outras palavras, se a sua Suite utiliza no mínimo dois Contextos diferentes, 
    estas classes de contexto ``usam`` o mesmo Traço, isto irá resultar em uma 
    definição de etapa duplicada e o behat irá queixar-se lançando uma exceção 
    ``Redundant``.
