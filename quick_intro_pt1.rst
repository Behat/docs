Building Domain Model
=====================

Bem vindo ao Behat! Behat é uma ferramenta para fechar o laço de comunicação do 
`Desenvolvimento Dirigido por Comportamento`_(BDD). BDD é uma metodologia de 
desenvolvimento de software por meio de comunicação baseado em exemplo contínuo 
entre desenvolvedores e a área de negócios, que esta aplicação suporta. Esta 
comunicação acontece em uma forma que a área de negócios e os desenvolvedores 
podem claramente entender - exemplos. Exemplos são estruturados entorno do padrão
``Contexto-Ação-Resultado`` e são escritos em um formato especial chamado *Gherkin*.
O fato do Guerkin ser muito estrutural torna muito fácil automatizar e automatizar 
seus testes de comportamento contra uma aplicação em desenvolvimento. Exemplos 
automatizados são utilizados atualmente para guiar o desenvolvimento de aplicações TDD-style.

Exemplo
-------

Vamos imaginar que você está construindo uma plataforma totalmente nova de e-commerce.
Uma das características fundamentais de qualquer plataforma de compras online é a habilidade
de comprar produtos. Mas antes de comprar algo, os clientes devem poder informar ao sistema
quais produtos eles têm interesse em comprar. Vocẽ precisa de uma cesta.
Então vamos escrever sua primeira user-story:

.. code-block:: gherkin

    # language: pt
    Funcionalidade: Cesta de produtos
      A fim de comprar produtos
      Como um cliente
      Eu preciso colocar produtos do meu interesse na cesta

.. note::

    Esta é uma feature básica em Gherkin e está é uma simples descrição 
    desta história. Cada feature inicia com este mesmo formato: uma
    linha com o título da feature, seguida por três linhas que descrevem
    os benefícios, o papel e o próprio recurso com qualquer quantidade de 
    linhas de descrição adicionais seguem depois.

Before we begin to work on this feature, we must fulfil a promise of any
user-story and have a real conversation with our business stakeholders.
They might say that they want customers to see not only the combined
price of the products in the basket, but the price reflecting both the
VAT (20%) and the delivery cost (which depends on the total price of
the products):

.. code-block:: gherkin

    Feature: Product basket
      In order to buy products
      As a customer
      I need to be able to put interesting products into a basket

      Rules:
      - VAT is 20%
      - Delivery for basket under £10 is £3
      - Delivery for basket over £10 is £2

So as you can see, it already becomes tricky (ambiguous at least) to talk
about this feature in terms of *rules*. What does it mean to add VAT? What
happens when we have two products, one of which is less than £10 and another
that is more? Instead you proceed with having a back-and-forth chat with
stakeholders in form of actual examples of a *customer* adding products to
the basket. After some time, you will come up with your first behaviour
examples (in BDD these are called *scenarios*):

.. code-block:: gherkin

    Feature: Product basket
      In order to buy products
      As a customer
      I need to be able to put interesting products into a basket

      Rules:
      - VAT is 20%
      - Delivery for basket under £10 is £3
      - Delivery for basket over £10 is £2

      Scenario: Buying a single product under £10
        Given there is a "Sith Lord Lightsaber", which costs £5
        When I add the "Sith Lord Lightsaber" to the basket
        Then I should have 1 product in the basket
        And the overall basket price should be £9

      Scenario: Buying a single product over £10
        Given there is a "Sith Lord Lightsaber", which costs £15
        When I add the "Sith Lord Lightsaber" to the basket
        Then I should have 1 product in the basket
        And the overall basket price should be £20

      Scenario: Buying two products over £10
        Given there is a "Sith Lord Lightsaber", which costs £10
        And there is a "Jedi Lightsaber", which costs £5
        When I add the "Sith Lord Lightsaber" to the basket
        And I add the "Jedi Lightsaber" to the basket
        Then I should have 2 products in the basket
        And the overall basket price should be £20

.. note::

    Each scenario always follows the same basic format:

    .. code-block:: gherkin

        Scenario: Some description of the scenario
          Given some context
          When some event
          Then outcome

    Each part of the scenario - the *context*, the *event*,  and the
    *outcome* - can be extended by adding the ``And`` or ``But`` keyword:

    .. code-block:: gherkin

        Scenario: Some description of the scenario
          Given some context
          And more context
          When some event
          And second event occurs
          Then outcome
          And another outcome
          But another outcome

    There's no actual difference between, ``Then``, ``And`` ``But`` or any
    of the other words that start each line. These keywords are all made
    available so that your scenarios are natural and readable.

This is your and your stakeholders' shared understanding of the project written
in a structured format. It is all based on the clear and constructive
conversation you have had together. Now you can put this text in a simple file -
``features/basket.feature`` - under your project directory and start
implementing the feature by manually checking if it fits the defined scenarios.
No tools (Behat in our case) needed. That, in essence, is what BDD is.

If you are still reading, it means you are expecting more. Good! Because
even though tools are not the central piece of BDD puzzle, they do improve
the entire process and add a lot of benefits on top of it. For one, tools
like Behat actually do close the communication loop of the story. It means
that not only you and your stakeholder can together define how your
feature should work before going to implement it, BDD tools allow you to
automate that behaviour check after this feature is implemented. So everybody
knows when it is done and when the team can stop writing code. That, in
essence, is what Behat is.

Behat is an executable that you'll run from the command line to test that your
application behaves exactly as you described in your ``*.feature`` scenarios.

Going forward, we'll show you how Behat can be used to automate this particular
basket feature as a test verifying that the application (existing or not)
works as you and your stakeholders expect (according to your conversation) it
to.

That's it! Behat can be used to automate anything, including web-related
functionality via the `Mink`_ library.

.. note::

    If you want to learn more about the philosophy of "Behaviour Driven
    Development" of your application, see `What's in a Story?`_

.. note::

    Behat was heavily inspired by Ruby's `Cucumber`_ project. Since v3.0,
    Behat is considered an official Cucumber implementation in PHP and is part
    of one big family of BDD tools.

Installation
------------

Before you begin, ensure that you have at least PHP 5.3.3 installed.

Method #1 - Composer (the recommended one)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The official way to install Behat is through Composer. Composer is a package
manager for PHP. Not only can it install Behat for you right now, it will be
able to easily update you to the latest version later when one comes out. If
you don't have Composer already, see
`the Composer documentation <https://getcomposer.org/download/>`_ for
instructions. After that, just go into your project directory (or create a
new one) and run:

.. code-block:: bash

    $ php composer.phar require --dev behat/behat=~3.0.4

Then you will be able to check installed Behat version using:

.. code-block:: bash

    $ vendor/bin/behat -V
    
Method #2 - PHAR (an easy one)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An easier way to install Behat is to grab a latest ``behat.phar`` from
`the download page <https://github.com/Behat/Behat/releases>`_. Make sure
that you download a ``3+`` release. After downloading it, just place it in
your project folder (or create a new one) and check the installed version using:

.. code-block:: bash

    $ php behat.phar -V

Development
-----------

Now we will use our newly installed Behat to automate our previously written
feature under the ``features/basket.feature``.

Our first step after describing the feature and installing Behat is configuring
the test suite. A test suite is a key concept in Behat. Suites are a way for Behat
to know where to find and how to test your application against your features.
By default, Behat comes with a ``default`` suite, which tells Behat to search
for features under the ``features/`` folder and test them using ``FeatureContext``
class. Lets initialise this suite:

.. code-block:: bash

    $ vendor/bin/behat --init

.. note::

    If you installed Behat via PHAR, use ``php behat.phar`` instead of
    ``vendor/bin/behat`` in the rest of this article.

The ``--init`` command tells Behat to provide you with things missing
to start testing your feature. In our case - it's just a ``FeatureContext``
class under the ``features/bootstrap/FeatureContext.php`` file.

Executing Behat
~~~~~~~~~~~~~~~

I think we're ready to see Behat in action! Let's run it:

.. code-block:: bash

    $ vendor/bin/behat

You should see that Behat recognised that you have 3 scenarios. Behat should
also tell you that your ``FeatureContext`` class has missing steps and proposes
step snippets for you. ``FeatureContext`` is your test environment. It is an
object through which you will describe how you would test your application against
your features. It was generated by the ``--init`` command and now looks like this:

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

Defining Steps
~~~~~~~~~~~~~~

Finally, we got to the automation part. How does Behat know what to do
when it sees ``Given there is a "Sith Lord Lightsaber", which costs £5``? You
tell it. You write PHP code inside your context class (``FeatureContext``
in our case) and tell Behat that this code represents a specific scenario step
(via an annotation with a pattern):

.. code-block:: php

    /**
     * @Given there is a(n) :arg1, which costs £:arg2
     */
    public function thereIsAWhichCostsPs($arg1, $arg2)
    {
        throw new PendingException();
    }

.. note::

    ``/** ... */`` is a special syntax in PHP called a doc-block. It is
    discoverable at runtime and used by different PHP frameworks as a
    way to provide additional meta-information for the classes, methods and
    functions. Behat uses doc-blocks for step definitions, step
    transformations and hooks.

``@Given there is a(n) :arg1, which costs £:arg2`` above the method tells Behat
that this particular method should be executed whenever Behat sees step that
looks like ``... there is a ..., which costs £...``. This pattern will match
any of the following steps:

.. code-block:: gherkin

    Given there is a "Sith Lord Lightsaber", which costs £5
    When there is a "Sith Lord Lightsaber", which costs £10
    Then there is an 'Anakin Lightsaber', which costs £10
    And there is a Lightsaber, which costs £2
    But there is a Lightsaber, which costs £25

Not only that, but Behat will capture tokens (words starting with ``:``, e.g.
``:arg1``) from the step and pass their value to the method as arguments:

.. code-block:: php

    // Given there is a "Sith Lord Lightsaber", which costs £5
    $context->thereIsAWhichCostsPs('Sith Lord Lightsaber', '5');

    // Then there is a 'Jedi Lightsaber', which costs £10
    $context->thereIsAWhichCostsPs('Jedi Lightsaber', '10');

    // But there is a Lightsaber, which costs £25
    $context->thereIsAWhichCostsPs('Lightsaber', '25');

.. note::

    If you need to define more complex matching algorithms, you can also use regular
    expressions:

    .. code-block:: php

        /**
         * @Given /there is an? \"([^\"]+)\", which costs £([\d\.]+)/
         */
        public function thereIsAWhichCostsPs($arg1, $arg2)
        {
            throw new PendingException();
        }

Those patterns could be quite powerful, but at the same time, writing them for all
possible steps manually could become extremely tedious and boring. That's why Behat
does it for you. Remember when you previously executed ``vendor/bin/behat`` you
got:

.. code-block:: text

    --- FeatureContext has missing steps. Define them with these snippets:

        /**
         * @Given there is a :arg1, which costs £:arg2
         */
        public function thereIsAWhichCostsPs($arg1, $arg2)
        {
            throw new PendingException();
        }

Behat automatically generates snippets for missing steps and all that you need to
do is copy and paste them into your context classes. Or there is an even easier
way - just run:

.. code-block:: bash

    $ vendor/bin/behat --dry-run --append-snippets

And Behat will automatically append all the missing step methods into your
``FeatureContext`` class. How cool is that?

If you executed ``--append-snippets``, your ``FeatureContext`` should look like:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Tester\Exception\PendingException;
    use Behat\Behat\Context\SnippetAcceptingContext;
    use Behat\Gherkin\Node\PyStringNode;
    use Behat\Gherkin\Node\TableNode;

    class FeatureContext implements SnippetAcceptingContext
    {
        /**
         * @Given there is a :arg1, which costs £:arg2
         */
        public function thereIsAWhichCostsPs($arg1, $arg2)
        {
            throw new PendingException();
        }

        /**
         * @When I add the :arg1 to the basket
         */
        public function iAddTheToTheBasket($arg1)
        {
            throw new PendingException();
        }

        /**
         * @Then I should have :arg1 product(s) in the basket
         */
        public function iShouldHaveProductInTheBasket($arg1)
        {
            throw new PendingException();
        }

        /**
         * @Then the overall basket price should be £:arg1
         */
        public function theOverallBasketPriceShouldBePs($arg1)
        {
            throw new PendingException();
        }
    }

.. note::

    We have removed the constructor and grouped ``I should have :arg1 product in the basket``
    and ``I should have :arg1 products in the basket`` into one
    ``I should have :arg1 product(s) in the basket``.

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
