Development
===========

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

Implementing the Feature
------------------------

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

    $ vendor/bin/behat

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

Automating Steps
----------------

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

Defining Steps
--------------

Finally, we got to the automation part. How does Behat knows what to do
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

What's next?
------------

Congratulations! You now know everything you need in order to get started
with behavior driven development and Behat. From here, you can learn more
about the :doc:`Gherkin </guides/1.gherkin>` syntax or learn how to test your
web applications by using Behat with Mink.