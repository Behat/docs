Construindo Modelo de Domínio
=============================

Bem vindo ao Behat! Behat é uma ferramenta para fechar o laço de comunicação do 
`Desenvolvimento Dirigido por Comportamento-BDD`. BDD é uma metodologia de 
desenvolvimento de software baseado em exemplo por meio da comunicação contínua 
entre desenvolvedores e a área de negócios que esta aplicação suporta. Esta 
comunicação acontece de uma forma que a área de negócios e os desenvolvedores 
podem claramente entender - exemplos. Exemplos são estruturados entorno do padrão
``Contexto-Ação-Resultado`` e são escritos em um formato especial chamado *Gherkin*.
O fato do Guerkin ser muito estrutural torna muito fácil automatizar testes de 
comportamento contra uma aplicação em desenvolvimento. Exemplos 
automatizados são utilizados atualmente para guiar o desenvolvimento de aplicações TDD-style.

Exemplo
-------

Vamos imaginar que você está construindo uma plataforma totalmente nova de e-commerce.
Uma das características fundamentais de qualquer plataforma de compras online é a habilidade
de comprar produtos. Mas antes de comprar algo, os clientes devem poder informar ao sistema
quais produtos eles têm interesse de comprar. Vocẽ precisa de um carrinho de produtos.
Então vamos escrever sua primeira user-story:

.. code-block:: gherkin

    # language: pt
    Funcionalidade: Carrinho de produtos
      A fim de comprar produtos
      Como um cliente
      Eu preciso colocar produtos do meu interesse no carrinho

.. note::

    Esta é uma feature básica em Gherkin e esta é uma simples descrição 
    desta história. Cada feature inicia com este mesmo formato: uma
    linha com o título da feature, seguida por três linhas que descrevem
    os benefícios, o papel e o próprio recurso com qualquer quantidade de 
    linhas de descrição adicionais seguem depois.

Antes de nós começarmos a trabalhar nesta feature, nós precisamos preencher 
uma promessa de user-story e ter uma conversa de verdade com nossos stakeholders 
da área de negócios. Eles podem dizer que eles querem que os clientes vejam 
o preço combinado do produto no carrinho, mas que o preço reflita o imposto (20%) 
e o valor do frete (que depende da soma total dos produtos):

.. code-block:: gherkin

    # language: pt
    Funcionalidade: Carrinho de produtos
      A fim de comprar produtos
      Como um cliente
      Eu preciso colocar produtos do meu interesse no carrinho

      Regras:
      - O imposto é de 20%
      - O frete para um carrinho de compras até R$10 é R$3
      - O frete para um carrinho de compras maior que R$10 é R$2

Então como você pode ver, está ficando complicado (ambíguo, pelo menos)
falar sobre está feature, em termos de *regras*. O que você entende por 
adicionar imposto? O que acontece quando nós tivermos dois produtos, 
um com valor menor que R$10 e outro de maior valor? Ao invés de você
prosseguir em ter um leva e traz de conversas entre os stakeholders na forma
dos exemplos atuais de um *cliente* adicionando produtos ao carrinho. Depois
de algum tempo, você vai levantar seus primeiros exemplos de comportamentos (no BDD 
isto é chamado de *Cenários*):

.. code-block:: gherkin

    # language: pt
    Funcionalidade: Carrinho de produtos
      A fim de comprar produtos
      Como um cliente
      Eu preciso colocar produtos do meu interesse no carrinho

      Regras:
      - O imposto é de 20%
      - O frete para um carrinho de compras até R$10 é R$3
      - O frete para um carrinho de compras maior que R$10 é R$2

      Cenário: Comprando um único produto que custe menos que R$10
        Dado que exista um "Sabre de luz do Lorde Sith", que custe R$5
        Quando Eu adicionar o "Sabre de luz do Lorde Sith" ao carrinho
        Então Eu devo ter 1 produto no carrinho
        E o valor total do carrinho deve ser de R$9

      Cenário: Comprando um único produto que custe mais que R$10
        Dado que exista um "Sabre de luz do Lorde Sith", que custe R$15
        Quando Eu adicionar o "Sabre de luz do Lorde Sith" ao carrinho
        Então Eu devo ter 1 produto no carrinho
        E o valor total do carrinho deve ser de R$20

      Cenário: Comprando dois produtos que custem mais que R$10
        Dado que exista um "Sabre de luz do Lorde Sith", que custe R$10
        E que exista um "Sabre de luz Jedi", que custe R$5
        Quando Eu adicionar o "Sabre de luz do Lorde Sith" ao carrinho
        E Eu adicionar o "Sabre de luz Jedi" ao carrinho
        Então Eu devo ter 2 products no carrinho
        E o valor total do carrinho deve ser de R$20

.. note::

    Cada cenário sempre segue o mesmo formato básico:

    .. code-block:: gherkin

        Cenário: Alguma descrição do cenário
          Dado algum contexto
          Quando algum evento
          Então resultado

    Cada parte do cenário - o *contexto*, o *evento*,  e o
    *resultado* - pode ser extendido pelo adicional da palavra chave ``E`` 
    ou ``Mas``:

    .. code-block:: gherkin

        Cenário: Alguma descrição do cenário
          Dado algum contexto
          E mais outro contexto
          Quando algum evento
          E um segundo evento ocorra
          Então o resultado
          E outro resultado
          Mas outro resultado

    Não há uma real diferença entre ``Então``, ``E`` ``Mas`` ou qualquer 
    outra palavra que inicie cada linha. Estas palavras chave são 
    disponibilizadas para que os cenários sejam naturais e legíveis.
    
Isto é seu e seus stakeholders compartilham da mesma escrita em um formato 
estruturado do projeto. Tudo é baseado na clara e construtiva conversa que 
vocês tiveram juntos. Agora você pode colocar este texto em um arquivo 
simples - ``features/carrinho.feature`` - dentro do diretório do seu projeto e 
começar a implementar a funcionalidade checando manualmente se se encaixa no 
cenário definido. Não é necessário nenhuma ferramenta (Behat em seu caso). 
Isto é, na essência, o que o BDD é.

Se você ainda está lendo,  significa que você ainda espera mais. Ótimo! 
Porque  apesar das ferramentas não serem a peça central do quebra-cabeça do BDD, 
elas melhoram todo o processo e adicionam muitos benefícios ao topo disto.
Para isso, ferramentas como o Behat atualmente fecham o ciclo de comunicação da história.
Isto significa que não somente você e seu stakeholder podem juntos definir como sua 
feature deveria trabalhar após ser implementada, ferramentas de BDD permitem a você
automatizar a checagem do comportamento após a funcionalidade ser implementada. Então
todo mundo sabe quando isto está feito e quando o time pode parar de escrever código.
Isto, na essência, é oque o Behat é.

*Behat é um executável que quando você o executa da linha de comando ele irá testar como 
a sua aplicação se comporta exatamente como você descreveu nos seus ``*.feature`` cenários.*

Indo adiante, nós vamos mostrar a você como o Behat pode ser usado para automatizar em 
particular esta feature do carrinho de compras como um teste verificando se aquela 
aplicação (existindo ou não) trabalha como você e seus stakeholders esperam (de acordo 
com a conversa de vocês) também.

É isso ai! O Behat pode ser usado para automatizar qualquer coisa, inclusive relacionadas a
funcionalidades web via `Mink`_ library.

.. note::

    Se você quer aprender mais sobre a filosofia do "Desenvolvimento 
    Dirigido por comportamento" sobre a sua aplicação, veja `What's in a Story?`_

.. note::

    Behat estava profundamente inspirado pelo projeto em Ruby `Cucumber`_. Desde a v3.0,
    Behat é considerado uma implementação oficial do Cucumber em PHP e faz parte da grande
    família de ferramentas BDD.

Instalação
----------

Antes de você começar, garanta que você tem uma versão superior a 5.3.3 do PHP instalada.

Método #1 - Composer (o recomendado)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

O caminho oficial para instalar o Behat é através do Composer. Composer é um
gerenciador de pacotes para PHP. Ele não irá lhe ser útil somente para instalar o Behat para 
você agora, ele será capaz de atualizar facilmente para a última versão mais tarde, quando 
for lançada. Se você ainda não tem o Composer, veja `a documentação do Composer <https://getcomposer.org/download/>`_ 
para instruções. Depois disto, basta ir ao diretório do projeto (ou criar um novo) e rodar:

.. code-block:: bash

    $ php composer.phar require --dev behat/behat=~3.0.4

Então vocẽ estará apto a checar a versão instalada do Behat:

.. code-block:: bash

    $ vendor/bin/behat -V
    
Método #2 - PHAR (um caminho fácil)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Um caminho fácil para instalar o Behat é pegar a última ``behat.phar`` na 
`página de download <https://github.com/Behat/Behat/releases>`_. Certifique-se
de fazer o download de uma versão ``3+``. Depois de baixar isto, basta colocá-lo 
no diretório do seu projeto (ou criar um novo) e checar a versão instalada usando:

.. code-block:: bash

    $ php behat.phar -V

Desenvolvendo
-------------

Agora nós vamos usar nosso recém instalado Behat para automatizar a feature escrita 
anteriormente em ``features/carrinho.feature``.

Nosso primeiro passo após descrever a feature e instalar o Behat é configurar a suite 
de teste. Uma suite de teste é um conceito chave em Behat. Suites são uma forma do Behat 
saber onde achar e como testar sua aplicação com as suas features.
Por padrão, Behat vem com uma suite ``default``, que diz ao Behat para procurar por 
features no diretório ``features/`` e os teste usando a classe ``FeatureContext``.
Vamos inicializar esta suite:

.. code-block:: bash

    $ vendor/bin/behat --init

.. note::

    Se você instalou o Behat via PHAR, use ``php behat.phar`` ao invés de
    ``vendor/bin/behat`` no resto deste artigo.

O comando ``--init`` diz ao Behat para prover para você com coisas faltando 
para começar a testar sua feature. Em nosso caso - é apenas uma classe ``FeatureContext`` 
no arquivo ``features/bootstrap/FeatureContext.php``.

Executando o Behat
~~~~~~~~~~~~~~~~~~

Eu acho que nós estamos prontos para ver o Behat em ação! Vamos rodar isto:

.. code-block:: bash

    $ vendor/bin/behat

Vocẽ deve ver que o Behat reconheceu que você tem 3 cenários. o Behat deve também
contar a você que na sua classe ``FeatureContext`` faltam passos e propor trechos 
para etapas para você. ``FeatureContext`` é seu ambiente de teste. É um objeto 
através do qual você descreve como você deve testar sua aplicação através de suas 
features. Isso foi gerado através do comando ``--init`` e agora se parece com isso:

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

Definindo Steps
~~~~~~~~~~~~~~~

Finalmente, nós chegamos a parte de automação. Como é que o Behat sabe o que fazer 
quando vê  ``Dado que exista um "Sabre de luz do Lorde Sith", que custe R$5``? 
Diga a ele. Você escreve em PHP dentro da sua classe de contexto (``FeatureContext`` 
no seu caso) e diz ao Behat que este código representa um passo específico do cenário 
(através de uma anotação com um padrão):

.. code-block:: php

    /**
     * @Given que exista um :arg1, que custe R$:arg2
     */
    public function queExistaUmQueCusteR($arg1, $arg2)
    {
        throw new PendingException();
    }


.. note::

    ``/** ... */`` é uma sintaxe especial em PHP chamada de doc-block.
    Isto é detectável em tempo de execução e usado por diferentes frameworks 
    de PHP como um caminho para prover meta-informação adicionais para as 
    classes, métodos e funções. Behat usa doc-blocks para step definitions, 
    step transformations e hooks.

``@Given que exista um :arg1, que custe R$:arg2`` sobre o método diz ao Behat
que este método em particular deve ser executado sempre que o Behat ver um step 
que se pareça com ``... que exista um ..., que custe R$...``. Este padrão 
combina qualquer um dos seguintes steps:

.. code-block:: gherkin

    Dado que exista um "Sabre de luz do Lorde Sith", que custe R$5
    Quando que exista um "Sabre de luz do Lorde Sith", que custe R$10
    Então que exista um "Sabre de luz do Anakin", que custe R$10
    E que exista um "Sabre de luz", que custe R$2
    Mas que exista um "Sabre de luz", que custe R$25

Não somente estes, mas o Behat irá capturar tokens (palavras iniciadas com ``:``, 
por exemplo ``:arg1``) a partir do step e passar seu valor para o método como argumentos:

.. code-block:: php

    // Dado que exista um "Sabre de luz do Lorde Sith", que custe R$5
    $context->queExistaUmQueCusteR('Sabre de luz do Lorde Sith', '5');

    // Então que exista um "Sabre de luz Jedi", que custe R$10
    $context->queExistaUmQueCusteR('Sabre de luz Jedi', '10');

    // Mas que exista um "Sabre de luz", que custe R$25
    $context->queExistaUmQueCusteR('Sabre de luz', '25');

.. note::

    Se você precisa definir algoritmos de correspondência mais complexos, 
    você também pode usar expressões regulares:

    .. code-block:: php

        /**
         * @Given /que exista um? \"([^\"]+)\", que custe R$([\d\.]+)/
         */
        public function queExistaUmQueCusteR($arg1, $arg2)
        {
            throw new PendingException();
        }

Estes padrões podem ser muito poderosos, mas ao mesmo tempo, escreve-los por todos steps 
possíveis manualmente pode ser extremamente tedioso e chato. É por isso que o Behat faz
isto para você. Relembre quando você executou anteriormente ``vendor/bin/behat`` você teve:

.. code-block:: text

    --- FeatureContext has missing steps. Define them with these snippets:

        /**
         * @Given que exista um :arg1, que custe R$:arg2
         */
        public function queExistaUmQueCusteR($arg1, $arg2)
        {
            throw new PendingException();
        }

O Behat gera automaticamente trechos para etapas que faltam e tudo que você precisa 
para os copiar e colar em sua classe context. Ou há ainda um caminho mais fácil - pasta rodar:

.. code-block:: bash

    $ vendor/bin/behat --dry-run --append-snippets

E o Behat vai automaticamente acrescentar todos os métodos das etapas que faltam em
sua classe ``FeatureContext``. Como isso é legal?

Se vocẽ executou `--append-snippets``, sua ``FeatureContext`` deve se parecer com:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Tester\Exception\PendingException;
    use Behat\Behat\Context\SnippetAcceptingContext;
    use Behat\Gherkin\Node\PyStringNode;
    use Behat\Gherkin\Node\TableNode;

    class FeatureContext implements SnippetAcceptingContext
    {
        /**
         * @Given que exista um :arg1, que custe R$:arg2
         */
        public function queExistaUmQueCusteR($arg1, $arg2)
        {
            throw new PendingException();
        }

        /**
         * @When Eu adicionar o :arg1 ao carrinho
         */
        public function euAdicionarOAoCarrinho($arg1)
        {
            throw new PendingException();
        }

        /**
         * @Then Eu devo ter :arg1 produto(s) no carrinho
         */
        public function euDevoTerProdutoNoCarrinho($arg1)
        {
            throw new PendingException();
        }

        /**
         * @Then o valor total do carrinho deve ser de R$:arg1
         */
        public function oValorTotalDoCarrinhoDeveSerDeR($arg1)
        {
            throw new PendingException();
        }
    }

.. note::

    Nós removemos o construtor e agrupamos ``Eu devo ter :arg1 produto no carrinho`` e
    ``Eu devo ter :arg1 produtos no carrinho`` em um ``Eu devo ter :arg1 produto(s) no carrinho``

Automating Steps
~~~~~~~~~~~~~~~~

Now it is finally time to start implementing our basket feature. The approach when
you use tests to drive your application development is called a Test-Driven Development
(or simply TDD). With TDD you start by defining test cases for the functionality you
develop, then you fill these test cases with the best-looking application code you could
come up with (use your design skills and imagination).

In the case of Behat, you already have defined test cases (step definitions in your
``FeatureContext``) and the only thing that is missing is that best-looking application
code we could come up with to fulfil our scenario. Something like this:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Tester\Exception\PendingException;
    use Behat\Behat\Context\SnippetAcceptingContext;
    use Behat\Gherkin\Node\PyStringNode;
    use Behat\Gherkin\Node\TableNode;

    class FeatureContext implements SnippetAcceptingContext
    {
        private $shelf;
        private $basket;

        public function __construct()
        {
            $this->shelf = new Shelf();
            $this->basket = new Basket($this->shelf);
        }

        /**
         * @Given there is a :product, which costs £:price
         */
        public function thereIsAWhichCostsPs($product, $price)
        {
            $this->shelf->setProductPrice($product, floatval($price));
        }

        /**
         * @When I add the :product to the basket
         */
        public function iAddTheToTheBasket($product)
        {
            $this->basket->addProduct($product);
        }

        /**
         * @Then I should have :count product(s) in the basket
         */
        public function iShouldHaveProductInTheBasket($count)
        {
            PHPUnit_Framework_Assert::assertCount(
                intval($count),
                $this->basket
            );
        }

        /**
         * @Then the overall basket price should be £:price
         */
        public function theOverallBasketPriceShouldBePs($price)
        {
            PHPUnit_Framework_Assert::assertSame(
                floatval($price),
                $this->basket->getTotalPrice()
            );
        }
    }

As you can see, in order to test and implement our application, we introduced 2 objects -
``Shelf`` and ``Basket``. The first is responsible for storing products and their prices,
the second is responsible for the representation of our customer basket. Through appropriate step
definitions we declare products' prices and add products to the basket. We then compare the
state of our ``Basket`` object with our expectations using PHPUnit assertions.

.. note::

    Behat doesn't come with its own assertion tool, but you can use any proper assertion
    tool out there. A proper assertion tool is a library whose assertions throw
    exceptions on failure. For example, if you're familiar with PHPUnit you can use
    its assertions in Behat by installing it via composer:

    .. code-block:: bash

        $ php composer.phar require --dev phpunit/phpunit='~4.1.0'

    and then by simply using assertions in your steps:

    .. code-block:: php

        PHPUnit_Framework_Assert::assertCount(
            intval($count),
            $this->basket
        );

Now try to execute your feature tests:

.. code-block:: bash

    $ vendor/bin/behat

You should see a beginning of the feature and then an error saying that class ``Shelf``
does not exist. It means we're ready to start writing actual application code!

Implementing the Feature
~~~~~~~~~~~~~~~~~~~~~~~~

So now we have 2 very important things:

1. A concrete user-aimed description of functionality we're trying to deliver.
2. Set of failing tests that tell us what to do next.

Now is the easiest part of application development - feature implementation. Yes, with
TDD and BDD implementation becomes a routine task, because you already did most of the
job in the previous phases - you wrote tests, you came up with an elegant solution (as far
as you could go in current context) and you chose the actors (objects) and actions
(methods) that are involved. Now it's time to write a bunch of PHP keywords to glue it
all together. Tools like Behat, when used in the right way, will help you to write this
phase by giving you a simple set of instructions that you need to follow. You
did your thinking and design, now it's time to sit back, run the tool and follow its
instructions in order to write your production code.

Lets start! Run:

.. code-block:: bash

    $ vendor/bin/behat

Behat will try to test your application with ``FeatureContext`` but will fail soon,
producing something like this onto your screen:

.. code-block:: text

    Fatal error: Class 'Shelf' not found

Now our job is to reinterpret this phrase into an actionable instruction. Like
"Create the ``Shelf`` class". Let's go and create it inside ``features/bootstrap``:

.. code-block:: php

    // features/bootstrap/Shelf.php

    final class Shelf
    {
    }

.. note::

    We put the ``Shelf`` class into ``features/bootstrap/Shelf.php`` because
    ``features/bootstrap`` is an autoloading folder for Behat. Behat has a built-in
    PSR-0 autoloader, which looks into ``features/bootstrap``. If you're developing
    your own application, you probably would want to put classes into a place
    appropriate for your app.

Let's run Behat again:

.. code-block:: bash

    $ vendor/bin/behat

We will get different message on our screen:

.. code-block:: text

    Fatal error: Class 'Basket' not found

Good, we are progressing! Reinterpreting the message as, "Create the ``Basket`` class".
Let's follow our new instruction:

.. code-block:: php

    // features/bootstrap/Basket.php

    final class Basket
    {
    }

Run Behat again:

.. code-block:: bash

    $> vendor/bin/behat

Great! Another "instruction":

.. code-block:: text

    Call to undefined method Shelf::setProductPrice()

Follow these instructions step-by-step and you will end up with ``Shelf``
class looking like this:

.. code-block:: php

    // features/bootstrap/Shelf.php

    final class Shelf
    {
        private $priceMap = array();

        public function setProductPrice($product, $price)
        {
            $this->priceMap[$product] = $price;
        }

        public function getProductPrice($product)
        {
            return $this->priceMap[$product];
        }
    }

and ``Basket`` class looking like this:

.. code-block:: php

    // features/bootstrap/Basket.php

    final class Basket implements \Countable
    {
        private $shelf;
        private $products;
        private $productsPrice = 0.0;

        public function __construct(Shelf $shelf)
        {
            $this->shelf = $shelf;
        }

        public function addProduct($product)
        {
            $this->products[] = $product;
            $this->productsPrice += $this->shelf->getProductPrice($product);
        }

        public function getTotalPrice()
        {
            return $this->productsPrice
                + ($this->productsPrice * 0.2)
                + ($this->productsPrice > 10 ? 2.0 : 3.0);
        }

        public function count()
        {
            return count($this->products);
        }
    }

Run Behat again:

.. code-block:: bash

    $ vendor/bin/behat

All scenarios should pass now! Congratulations, you almost finished your first
feature. The last step is to *refactor*. Look at the ``Basket`` and ``Shelf``
classes and try to find a way to make their code even more cleaner, easier to
read and concise.

.. tip::

    I would recommend starting from ``Basket::getTotalPrice()`` method and
    extracting VAT and delivery cost calculation in private methods.

After refactoring is done, you will have:

#. Clearly designed and obvious code that does exactly the thing it should do
   without any gold plating.

#. A regression test suite that will help you to be confident in your code going
   forward.

#. Living documentation for the behaviour of your code that will live, evolve and
   die together with your code.

#. An incredible level of confidence in your code. Not only are you confident now
   that it does exactly what it's supposed to do, you are confident that it does
   so by delivering value to the final users (customers in our case).

There are many more benefits to BDD but those are the key reasons why most BDD
practitioners do BDD in Ruby, .Net, Java, Python and JS. Welcome to the family!

What's Next?
------------

Congratulations! You now know everything you need in order to get started
with behavior driven development and Behat. From here, you can learn more
about the :doc:`Gherkin </guides/1.gherkin>` syntax or learn how to test your
web applications by using Behat with Mink.

.. _`Behavior Driven Development`: http://en.wikipedia.org/wiki/Behavior_Driven_Development
.. _`Mink`: https://github.com/behat/mink
.. _`What's in a Story?`: http://blog.dannorth.net/whats-in-a-story/
.. _`Cucumber`: http://cukes.info/
.. _`Goutte`: https://github.com/fabpot/goutte
.. _`PHPUnit`: http://phpunit.de
.. _`Testing Web Applications with Mink`: https://github.com/behat/mink
