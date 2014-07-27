BDD in Symfony2 with Behat, Mink and Zombie.js
==============================================

Description
-----------

This guide will show how to set up a new web application project with:

* ``git``, a distributed version control system.
* ``Symfony2`` framework
* ``Behat``, a tool for behavior driven development.
* ``Mink``, a tool unifying access to browser emulators wrapping them into one API.
* ``Zombie.js``, a browser emulator.
* ``PHPUnit``, the de-facto standard test suite in the PHP world.

.. note::

    You can find a repository with each commit mentioned on github: https://github.com/havvg/BDD-Experiment

Requirements
~~~~~~~~~~~~

The requirements before getting along with this guide:

* PHP 5.3 installed
* `git installed`_
* `PHPUnit installed`_
* `node.js installed`_ and `npm installed`_
* `Zombie.js installed`_
* UNIX based operation system (or knowledge on how to get things done on your system)

Getting started
---------------

We create a folder where the project will live in and initialize a new git repository within it.

.. code-block:: bash

    $ git init

Installing ``Symfony2``
~~~~~~~~~~~~~~~~~~~~~~~

We are going to use the standard edition of Symfony2. The following steps will download and extract the files into the current directory.

.. code-block:: bash

    $ wget http://symfony.com/download?v=Symfony_Standard_2.0.1.tgz
    $ tar -xzf Symfony_Standard_2.0.1.tgz -s /^Symfony\//
    $ rm Symfony_Standard_2.0.1.tgz

Issuing the list command ``ls`` should result into this list:

:: 

    LICENSE   README.md app       bin       deps      deps.lock src       web

Now we install the dependencies defined in the ``deps`` file for Symfony2 using the following command line.

.. code-block:: bash

    $ ./bin/vendors install

Afterwards we setup the web server to point to the ``web/`` directory of our project.
In addition we have to grant the web server access to the ``app/cache/`` and ``app/logs/`` directories.

.. note::

    If you are running the command line ``php app/console ...`` under a different user as your web server, please make sure, you have set up access rights correctly!

If you access your host at ``/app_dev.php``, you will now see the shiny Symfony2 welcome page!

Before creating our first commit, we create the project's ``.gitignore`` and insert those three lines for now.

::

    app/cache/*
    app/logs/*
    !*.gitkeep

As git won't add empty folders to the repository, but we want to have the cache and logs directory in it, we add the two ``.gitkeep`` files there:

.. code-block:: bash

    $ touch app/cache/.gitkeep app/logs/.gitkeep

So, this is our first commit. We have installed Symfony2!

Installing ``Behat`` and ``BehatBundle``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now, that we have a working development environment, we can start to setup the required tools.
We start with ``Behat`` and the ``BehatBundle``. This is pretty easy, if you follow :doc:`the steps for the installation </bundle/index>`.
We are following the second method using the git approach.

**The changes at a glance as follows.**

Add those lines to the ``deps`` file.

.. code-block:: ini

    [gherkin]
        git=https://github.com/Behat/Gherkin.git
        target=/behat/gherkin
    
    [behat]
        git=https://github.com/Behat/Behat.git
        target=/behat/behat
    
    [BehatBundle]
        git=https://github.com/Behat/BehatBundle.git
        target=/bundles/Behat/BehatBundle

In ``app/autoload.php`` add these namespaces to be registered:

.. code-block:: php

    $loader->registerNamespaces(array(
        // ...

        'Behat\Gherkin' => __DIR__.'/../vendor/behat/gherkin/src',
        'Behat\Behat' => __DIR__.'/../vendor/behat/behat/src',
        'Behat\BehatBundle' => __DIR__.'/../vendor/bundles',
    ));

Finally, tell the ``AppKernel``, to register the ``BehatBundle`` to the test environment.

.. code-block:: php

    public function registerBundles()
    {
        // ...

        if ('test' === $this->getEnvironment()) {
            $bundles[] = new Behat\BehatBundle\BehatBundle();
        }
    }

Now we can install our newly added dependencies by running ``./bin/vendors install`` again.
For now, we do not lock the new dependencies to a specific version. We will do this, as soon as the setup is completed.

Setting up ``Behat`` for the DemoBundle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The standard edition of Symfony2 comes with the ``Acme\DemoBundle``. We will use this for our first tries.
This makes it very easy, because we can now focus on setting up Behat and the following tools.

By issuing ``php app/console -e=test behat --init @AcmeDemoBundle`` we are done!

This command created the bundle's ``FeatureContext`` where everything regarding Behat will be defined, such as ``step definitions``.
The newly created folder ``Features`` within the bundle will contain our feature definitions.

Tryout ``Behat``
----------------

Now that we have Behat available, we will give it a try.
We will add two entities to the bundle, a ``Product`` and a ``Category``. They will represent some kind of catalog, e.g. for an online shop.

* A product is something we keep in stock.
* A category groups products.
* A product may be part of one or more categories.

Actually, by reading the last three lines again, we figure out, that those are features already!
So, let's get to ``Gherkin``. What is Gherkin? Well, it's a language to describe features with scenarios - in other words (from `Gherkin wiki`_):

    It is a Business Readable, Domain Specific Language that lets you describe software’s behaviour without detailing how that behaviour is implemented.

Define a ``Feature``
~~~~~~~~~~~~~~~~~~~~

Ok, we are now aware, that we have already three definitions for our relation. Let's re-word them in the correct way and save them into a feature file Behat will look for.
The file will be ``ProductCategoryRelation.feature`` and will be saved into the previously mentioned ``Features`` folder within the DemoBundle.

We are now testing the behavior of our model, so we are writing a feature definition for developer or the system itself. Using Gherkin as a language, this is one possible result:

.. code-block:: gherkin

    Feature: Product Category Relationship
      In order to setup a valid catalog
      As a developer
      I need a working relationship

This being the feature, we now need the scenarios to be defined.

.. code-block:: gherkin

    Scenario: A category contains a product
      Given I have a category "Underwear"
        And I have a product "Calvin Klein Black, 5"
       When I add product "Calvin Klein Black, 5" to category "Underwear"
       Then I should find product "Calvin Klein Black, 5" in category "Underwear"
    
    Scenario: A category contains more than 1 product
      Given I have a category "Underwear"
        And I have a product "Calvin Klein Black, 5"
        And I have a product "Calvin Klein White, 5"
       When I add product "Calvin Klein Black, 5" to category "Underwear"
        And I add product "Calvin Klein White, 5" to category "Underwear"
       Then I should find product "Calvin Klein Black, 5" in category "Underwear"
        And I should find product "Calvin Klein White, 5" in category "Underwear"
    
    Scenario: A product is part of more than 1 category
      Given I have a product "Calvin Klein Black, 5"
        And I have a category "Underwear"
        And I have a category "Men"
       When I add product "Calvin Klein Black, 5" to category "Underwear"
        And I add product "Calvin Klein Black, 5" to category "Men"
       Then I should find product "Calvin Klein Black, 5" in category "Underwear"
        And I should find product "Calvin Klein Black, 5" in category "Men"

Well, we defined three scenarios - exactly the same we came up with before.
Also, we created some ``step definitions`` the ``FeatureContext`` has to provide and "translate" into actual code.

Implement ``Step Definitions``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's start implementing the step definitions into the feature context. According to our feature, our first step definition reads

.. code-block:: gherkin

    Given I have a category "Underwear"

The category name will be a parameter, so we make up a regular expression out of this definition. That could be ``/I have a category "([^"]*)"/``.
Behat will pass the matches in their respective order to the method defining the step. Adding this to our feature context results into this empty method so far.

.. code-block:: php

    /**
     * @Given /I have a category "([^"]*)"/
     */
    public function iHaveACategory($name)
    {
    }

The ``@Given`` (``@When`` and ``@Then``) annotations are recognized by Behat, for more information on this topic, review the `more about steps`_ section of the quick intro.
An ``And`` will be considered an extra ``Given``, ``When`` or ``Then`` when used after one, respectively.

Now we have a small problem. We didn't set up any entities by now. So, we could do this now, but in `Test Driven Development`_, we won't.
``Doctrine2`` is available, but we have nothing set up. However, we can use it right away - we will implement everything we need, after we have got our tests.

The step will only save a category with a given name.

.. code-block:: php

    /**
     * @Given /I have a category "([^"]*)"/
     */
    public function iHaveACategory($name)
    {
        $em = $this->getContainer()->get('doctrine')->getEntityManager();
    
        $entity = new \Acme\DemoBundle\Entity\Category();
        $entity->setName($name);
    
        $em->persist($entity);
        $em->flush();
    }

The next step is the same, but for a new product.

.. code-block:: gherkin

    And I have a product "Calvin Klein Black, 5"

The step definition is quite the same, too.

.. code-block:: php

    /**
     * @Given /I have a product "([^"]*)"/
     */
    public function iHaveAProduct($name)
    {
        $em = $this->getContainer()->get('doctrine')->getEntityManager();
    
        $entity = new \Acme\DemoBundle\Entity\Product();
        $entity->setName($name);
    
        $em->persist($entity);
        $em->flush();
    }

Retrieving the ``EntityManager`` of ``Doctrine`` has become a common task, so we add a method wrapping this call and change the methods a bit.
Afterwards, the feature context so far, will be this.

.. code-block:: php

    <?php
    
    namespace Acme\DemoBundle\Features\Context;
    
    use Behat\BehatBundle\Context\BehatContext,
        Behat\BehatBundle\Context\MinkContext;
    use Behat\Behat\Context\ClosuredContextInterface,
        Behat\Behat\Context\TranslatedContextInterface,
        Behat\Behat\Exception\PendingException;
    use Behat\Gherkin\Node\PyStringNode,
        Behat\Gherkin\Node\TableNode;
    
    require_once 'PHPUnit/Autoload.php';
    require_once 'PHPUnit/Framework/Assert/Functions.php';
    
    /**
     * Feature context.
     */
    class FeatureContext extends BehatContext
    {
        /**
         * @Given /I have a category "([^"]*)"/
         */
        public function iHaveACategory($name)
        {
            $category = new \Acme\DemoBundle\Entity\Category();
            $category->setName($name);
    
            $this->getEntityManager()->persist($category);
            $this->getEntityManager()->flush();
        }
    
        /**
         * @Given /I have a product "([^"]*)"/
         */
        public function iHaveAProduct($name)
        {
            $product = new \Acme\DemoBundle\Entity\Product();
            $product->setName($name);
    
            $this->getEntityManager()->persist($product);
            $this->getEntityManager()->flush();
        }
    
        /**
         * Returns the Doctrine entity manager.
         *
         * @return Doctrine\ORM\EntityManager
         */
        protected function getEntityManager()
        {
            return $this->getContainer()->get('doctrine')->getEntityManager();
        }
    }

Let's check, whether Behat recognizes our new definitions with ``php app/console behat -e test @AcmeDemoBundle -dl``. The output should be.

* ``Given /I have a category "([^"]*)"/``
* ``Given /I have a product "([^"]*)"/``

Well, there are only two additional step definitions left.

* ``@When /I add product "([^"]*)" to category "([^"]*)"/``
* ``@Then /I should find product "([^"]*)" in category "([^"]*)"/``

After adding these, we will have this feature context:

.. code-block:: php

    <?php
    
    namespace Acme\DemoBundle\Features\Context;
    
    use Behat\BehatBundle\Context\BehatContext,
        Behat\BehatBundle\Context\MinkContext;
    use Behat\Behat\Context\ClosuredContextInterface,
        Behat\Behat\Context\TranslatedContextInterface,
        Behat\Behat\Exception\PendingException;
    use Behat\Gherkin\Node\PyStringNode,
        Behat\Gherkin\Node\TableNode;
    
    require_once 'PHPUnit/Autoload.php';
    require_once 'PHPUnit/Framework/Assert/Functions.php';
    
    /**
     * Feature context.
     */
    class FeatureContext extends BehatContext
    {
        /**
         * @Given /I have a category "([^"]*)"/
         */
        public function iHaveACategory($name)
        {
            $category = new \Acme\DemoBundle\Entity\Category();
            $category->setName($name);
    
            $this->getEntityManager()->persist($category);
            $this->getEntityManager()->flush();
        }
    
        /**
         * @Given /I have a product "([^"]*)"/
         */
        public function iHaveAProduct($name)
        {
            $product = new \Acme\DemoBundle\Entity\Product();
            $product->setName($name);
    
            $this->getEntityManager()->persist($product);
            $this->getEntityManager()->flush();
        }
    
        /**
         * @When /I add product "([^"]*)" to category "([^"]*)"/
         */
        public function iAddProductToCategory($productName, $categoryName)
        {
            $product = $this->getRepository('AcmeDemoBundle:Product')->findOneByName($productName);
            $category = $this->getRepository('AcmeDemoBundle:Category')->findOneByName($categoryName);
    
            $category->addProduct($product);
    
            $this->getEntityManager()->persist($category);
            $this->getEntityManager()->flush();
        }
    
        /**
         * @Then /I should find product "([^"]*)" in category "([^"]*)"/
         */
        public function iShouldFindProductInCategory($productName, $categoryName)
        {
            $category = $this->getRepository('AcmeDemoBundle:Category')->findOneByName($categoryName);
    
            $found = false;
            foreach ($category->getProducts() as $product) {
                if ($productName === $product->getName()) {
                    $found = true;
                    break;
                }
            }
    
            assertTrue($found);
        }
    
        /**
         * Returns the Doctrine entity manager.
         *
         * @return Doctrine\ORM\EntityManager
         */
        protected function getEntityManager()
        {
            return $this->getContainer()->get('doctrine')->getEntityManager();
        }
    
        /**
         * Returns the Doctrine repository manager for a given entity.
         *
         * @param string $entityName The name of the entity.
         *
         * @return Doctrine\ORM\EntityRepository
         */
        protected function getRepository($entityName)
        {
            return $this->getEntityManager()->getRepository($entityName);
        }
    }

Issuing the test command ``php app/console behat -e test @AcmeDemoBundle`` will result in every single scenario failing. This is ok for now, because we didn't set up anything!

Creating the model
~~~~~~~~~~~~~~~~~~

Creating the schema
+++++++++++++++++++

First, we need to define our data model. As by our scenarios, we have a ``Product`` and a ``Category``, both sharing a Many-To-Many relationship.
``Doctrine`` is able to read YAML schema files. We need two of them: one for each model, respectively. They will be saved in the bundles directory under ``Resources/config/doctrine/``.
Their names are ``Product.orm.yml`` and ``Category.orm.yml``.

The category is described by this schema.

.. code-block:: yaml

    # Category.orm.yml
    Acme\DemoBundle\Entity\Category:
        type: entity
        table: categories
        id:
            id:
                type: integer
                generator: { strategy: AUTO }
        manyToMany:
            products:
                targetEntity: Product
                joinTable:
                    name: products_categories
                    joinColumns:
                        category_id:
                            referencedColumnName: id
                    inverseJoinColumns:
                        product_id:
                            referencedColumnName: id
        fields:
            name:
                type: string
                length: 100
                unique: true

The product will re-use the relationship and thus will result into a quite shorter schema.

.. code-block:: yaml

    # Product.orm.yml
    Acme\DemoBundle\Entity\Product:
        type: entity
        table: products
        id:
            id:
                type: integer
                generator: { strategy: AUTO }
        manyToMany:
            categories:
                targetEntity: Category
                mappedBy: products
        fields:
            name:
                type: string
                length: 100
                unique: true

Now we can create our entities using ``php app/console doctrine:generate:entities AcmeDemoBundle``.

::

    Generating entities for bundle "AcmeDemoBundle"
      > backing up Category.php to Category.php~
      > generating Acme\DemoBundle\Entity\Category
      > backing up Product.php to Product.php~
      > generating Acme\DemoBundle\Entity\Product

Setting up the database
+++++++++++++++++++++++

Before we can work with those models, we need to set up the databases correctly.
By default, Symfony2 imports the ``app/config/parameters.ini`` where your database is configured.

But you *should always* separate the databases for each environment (production, development and test).
To get this done in a simple manner, we make use of the placeholder capabilities of the configuration.
We only change the ``app/config/config.yml``. In section ``doctrine.dbal.dbname`` we change the value to ``%database_name%_%kernel.environment%``.
The complete section should read.

::

    # app/config/config.yml
    doctrine:
        dbal:
            driver:   %database_driver%
            host:     %database_host%
            port:     %database_port%
            dbname:   %database_name%_%kernel.environment%
            user:     %database_user%
            password: %database_password%
            charset:  UTF8
        orm:
            auto_mapping: true

Issuing the database:create task ``php app/console doctrine:database:create -e test`` will result in.

::

    Created database for connection named symfony_test

Now, we create the defined schema in this database by issuing ``php app/console doctrine:schema:create -e test``.

::

    ATTENTION: This operation should not be executed in a production environment.
    
    Creating database schema...
    Database schema created successfully!

Backgrounds
~~~~~~~~~~~

Now, that we have our model set up and have created a database, we are good to go!
By issuing ``php app/console behat -e test @AcmeDemoBundle``, we will see that everything should be working?

::

    Feature: Product Category Relationship
      In order to setup a valid catalog
      As a developer
      I need a working relationship
    
      Scenario: A category contains a product                                      # src/Acme/DemoBundle/Features/ProductCategoryRelation.feature:10
        Given I have a category "Underwear"                                        # Acme\DemoBundle\Features\Context\FeatureContext::iHaveACategory()
        And I have a product "Calvin Klein Black, 5"                               # Acme\DemoBundle\Features\Context\FeatureContext::iHaveAProduct()
        When I add product "Calvin Klein Black, 5" to category "Underwear"         # Acme\DemoBundle\Features\Context\FeatureContext::iAddProductToCategory()
        Then I should find product "Calvin Klein Black, 5" in category "Underwear" # Acme\DemoBundle\Features\Context\FeatureContext::iShouldFindProductInCategory()
    
      Scenario: A category contains more than 1 product                            # src/Acme/DemoBundle/Features/ProductCategoryRelation.feature:16
        Given I have a category "Underwear"                                        # Acme\DemoBundle\Features\Context\FeatureContext::iHaveACategory()
          SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry 'Underwear' for key 'UNIQ_3AF346685E237E06'
        And I have a product "Calvin Klein Black, 5"                               # Acme\DemoBundle\Features\Context\FeatureContext::iHaveAProduct()
        And I have a product "Calvin Klein White, 5"                               # Acme\DemoBundle\Features\Context\FeatureContext::iHaveAProduct()
        When I add product "Calvin Klein Black, 5" to category "Underwear"         # Acme\DemoBundle\Features\Context\FeatureContext::iAddProductToCategory()
        And I add product "Calvin Klein White, 5" to category "Underwear"          # Acme\DemoBundle\Features\Context\FeatureContext::iAddProductToCategory()
        Then I should find product "Calvin Klein Black, 5" in category "Underwear" # Acme\DemoBundle\Features\Context\FeatureContext::iShouldFindProductInCategory()
        And I should find product "Calvin Klein White, 5" in category "Underwear"  # Acme\DemoBundle\Features\Context\FeatureContext::iShouldFindProductInCategory()
    
      Scenario: A product is part of more than 1 category                          # src/Acme/DemoBundle/Features/ProductCategoryRelation.feature:25
        Given I have a product "Calvin Klein Black, 5"                             # Acme\DemoBundle\Features\Context\FeatureContext::iHaveAProduct()
          The EntityManager is closed.
        And I have a category "Underwear"                                          # Acme\DemoBundle\Features\Context\FeatureContext::iHaveACategory()
        And I have a category "Men"                                                # Acme\DemoBundle\Features\Context\FeatureContext::iHaveACategory()
        When I add product "Calvin Klein Black, 5" to category "Underwear"         # Acme\DemoBundle\Features\Context\FeatureContext::iAddProductToCategory()
        And I add product "Calvin Klein Black, 5" to category "Men"                # Acme\DemoBundle\Features\Context\FeatureContext::iAddProductToCategory()
        Then I should find product "Calvin Klein Black, 5" in category "Underwear" # Acme\DemoBundle\Features\Context\FeatureContext::iShouldFindProductInCategory()
        And I should find product "Calvin Klein Black, 5" in category "Men"        # Acme\DemoBundle\Features\Context\FeatureContext::iShouldFindProductInCategory()

    3 scenarios (1 passed, 2 failed)
    18 steps (4 passed, 12 skipped, 2 failed)
    0m0.119s

Well, not really! - Why that?
The answer is quite simple, if you take a look to the error messages. The database is not cleared between the scenarios. This is where ``Backgrounds`` join the party.
In Behat a background describes pre-scenario conditions. The steps defined in a background will be executed **before each scenario** is run.

Let's add a background, that is clearing the database according to our scenarios. We need to remove every product and category.

.. code-block:: gherkin

    Background:
      Given There is no "Product" in database
        And There is no "Category" in database

Then we need to add this new step to our feature context:

.. code-block:: php

    /**
     * @Given /There is no "([^"]*)" in database/
     */
    public function thereIsNoRecordInDatabase($entityName)
    {
        $entities = $this->getEntityManager()->getRepository('AcmeDemoBundle:'.$entityName)->findAll();
        foreach ($entities as $eachEntity) {
            $this->getEntityManager()->remove($eachEntity);
        }
    
        $this->getEntityManager()->flush();
    }

As you can see here, the name of the method implementing the step definition is not required to be in relation with the step itself. However naming them meaningful, makes life easier!

Running the tests again, will now result into our expected success.

::

    Feature: Product Category Relationship
      In order to setup a valid catalog
      As a developer
      I need a working relationship
    
      Background:                               # src/Acme/DemoBundle/Features/ProductCategoryRelation.feature:6
        Given There is no "Product" in database # Acme\DemoBundle\Features\Context\FeatureContext::thereIsNoRecordInDatabase()
        And There is no "Category" in database  # Acme\DemoBundle\Features\Context\FeatureContext::thereIsNoRecordInDatabase()
    
      Scenario: A category contains a product                                      # src/Acme/DemoBundle/Features/ProductCategoryRelation.feature:10
        Given I have a category "Underwear"                                        # Acme\DemoBundle\Features\Context\FeatureContext::iHaveACategory()
        And I have a product "Calvin Klein Black, 5"                               # Acme\DemoBundle\Features\Context\FeatureContext::iHaveAProduct()
        When I add product "Calvin Klein Black, 5" to category "Underwear"         # Acme\DemoBundle\Features\Context\FeatureContext::iAddProductToCategory()
        Then I should find product "Calvin Klein Black, 5" in category "Underwear" # Acme\DemoBundle\Features\Context\FeatureContext::iShouldFindProductInCategory()
    
      Scenario: A category contains more than 1 product                            # src/Acme/DemoBundle/Features/ProductCategoryRelation.feature:16
        Given I have a category "Underwear"                                        # Acme\DemoBundle\Features\Context\FeatureContext::iHaveACategory()
        And I have a product "Calvin Klein Black, 5"                               # Acme\DemoBundle\Features\Context\FeatureContext::iHaveAProduct()
        And I have a product "Calvin Klein White, 5"                               # Acme\DemoBundle\Features\Context\FeatureContext::iHaveAProduct()
        When I add product "Calvin Klein Black, 5" to category "Underwear"         # Acme\DemoBundle\Features\Context\FeatureContext::iAddProductToCategory()
        And I add product "Calvin Klein White, 5" to category "Underwear"          # Acme\DemoBundle\Features\Context\FeatureContext::iAddProductToCategory()
        Then I should find product "Calvin Klein Black, 5" in category "Underwear" # Acme\DemoBundle\Features\Context\FeatureContext::iShouldFindProductInCategory()
        And I should find product "Calvin Klein White, 5" in category "Underwear"  # Acme\DemoBundle\Features\Context\FeatureContext::iShouldFindProductInCategory()
    
      Scenario: A product is part of more than 1 category                          # src/Acme/DemoBundle/Features/ProductCategoryRelation.feature:25
        Given I have a product "Calvin Klein Black, 5"                             # Acme\DemoBundle\Features\Context\FeatureContext::iHaveAProduct()
        And I have a category "Underwear"                                          # Acme\DemoBundle\Features\Context\FeatureContext::iHaveACategory()
        And I have a category "Men"                                                # Acme\DemoBundle\Features\Context\FeatureContext::iHaveACategory()
        When I add product "Calvin Klein Black, 5" to category "Underwear"         # Acme\DemoBundle\Features\Context\FeatureContext::iAddProductToCategory()
        And I add product "Calvin Klein Black, 5" to category "Men"                # Acme\DemoBundle\Features\Context\FeatureContext::iAddProductToCategory()
        Then I should find product "Calvin Klein Black, 5" in category "Underwear" # Acme\DemoBundle\Features\Context\FeatureContext::iShouldFindProductInCategory()
        And I should find product "Calvin Klein Black, 5" in category "Men"        # Acme\DemoBundle\Features\Context\FeatureContext::iShouldFindProductInCategory()
    
    3 scenarios (3 passed)
    24 steps (24 passed)
    0m0.182s

Summary
~~~~~~~

What do we have by now?

* A running Symfony2 installation with all vendors.
* A test database with our schema.
* A model containing our two entities.
* A feature describing the relationship between the two entities as behaviors of those two.

So this a lot for one commit. Let's see, what we got in a commit's perspective.

* Behat, the BehatBundle and its configuration and vendors

  ``git add app/AppKernel.php deps app/autoload.php vendor/behat/ vendor/bundles/Behat/ && git commit``

* database configuration, entities and feature description

  ``git add app/config/config.yml src/Acme/ && git commit``

Adding ``Mink``
---------------

We have Behat running, a feature describing the model relationship between our two entities and a working data storage.
Now let's add a web interface to it. Testing web interfaces - as a GUI - often results in acceptance tests. This is where Mink comes in.

Installing ``Mink`` and ``MinkBundle``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Like Behat, we add Mink and the MinkBundle to our dependency file ``deps``.

.. code-block:: ini

    [mink]
        git=https://github.com/Behat/Mink.git
        target=/behat/mink
    
    [MinkBundle]
        git=https://github.com/Behat/MinkBundle.git
        target=/bundles/Behat/MinkBundle

After running the ``./bin/vendors install`` command line, we register the new namespaces in ``app/autoload.php``.

.. code-block:: php

    $loader->registerNamespaces(array(
        // ..

        // previously added
        'Behat\Gherkin' => __DIR__.'/../vendor/behat/gherkin/src',
        'Behat\Behat' => __DIR__.'/../vendor/behat/behat/src',
        'Behat\BehatBundle' => __DIR__.'/../vendor/bundles',
        'Behat\Mink' => __DIR__.'/../vendor/behat/mink/src',
        'Behat\MinkBundle' => __DIR__.'/../vendor/bundles',
    ));

The MinkBundle, like the BehatBundle will only be loaded in test environment in ``app/AppKernel.php``.

.. code-block:: php

    public function registerBundles()
    {
        // ...

        if ('test' === $this->getEnvironment()) {
            $bundles[] = new Behat\BehatBundle\BehatBundle();
            $bundles[] = new Behat\MinkBundle\MinkBundle();
        }
    }

Configure ``MinkBundle``
~~~~~~~~~~~~~~~~~~~~~~~~

Everything is in place, now a little configuration needs to be done in our test environment ``app/config/config_test.yml``.

.. code-block:: yaml

    mink:
        base_url:   http://your-virtualhost.local/app_test.php

As we are joining the web now, we need to change our feature context to be inherited from ``MinkContext`` instead of ``BehatContext``.

.. code-block:: php

    class FeatureContext extends MinkContext { }

The ``MinkContext`` is inherited from the ``BehatContext``, so all previous tests should run unchanged!

Creating the application
------------------------

Defining the application
~~~~~~~~~~~~~~~~~~~~~~~~

Now it's time to define our acceptance to the web application, we are going to create.

* We want a list of all categories.
* We want a list of all products in a selected category.
* In categories list there should be a link to the products list of this category.

Those are the requirements for the new ``CatalogController`` to be created in ``src/Acme/DemoBundle/Controller/CatalogController.php``.

Now, we will re-write them into a feature file describing the behaviors of the interface.
At first, let's take a look into available definitions ``php app/console behat -e test @AcmeDemoBundle -dl``.
There are some more now, because we are now using the MinkContext. This context provides definitions for navigating a web page.

The feature definition may look like this one in ``src/Acme/DemoBundle/Features/CatalogNavigation.feature``.

.. code-block:: gherkin

    Feature: Navigating the categories within the catalog
      In order to view the products within the catalog
      As a visitor
      I want to browse the categories
    
      Background:
        Given There is no "Product" in database
          And There is no "Category" in database
          And I have a category "Underwear"
          And I have a category "Shoes"
    
      Scenario: The categories are being listed
        Given I am on "/categories"
         Then I should see a "ul#category-list" element
          And I should see "Shoes" in the "#category-list" element
          And I should see "Underwear" in the "#category-list" element
    
      Scenario: The categories link to their products list
        Given I am on "/categories"
          And I have a product "Calvin Klein Black, 5"
          And I add product "Calvin Klein Black, 5" to category "Underwear"
          And I have a product "Converse All Star, 8"
          And I add product "Converse All Star, 8" to category "Shoes"
         When I follow "Underwear"
         Then I should see "Calvin Klein Black, 5" in the "#product-list li" element
          And I should not see "Converse All Star, 8"
         When I move backward one page
          And I follow "Shoes"
         Then I should see "Converse All Star, 8" in the "#product-list li" element
          And I should not see "Calvin Klein Black, 5"

As you can see, ``Behat`` does not care, whether we are using ``@When`` step definitions in a ``@Given`` context. 
However, *be careful when doing this*, there might be steps that will behave differently depending on what they are meant to be!

Running these scenarios will fail, so let's make a list of things, we need to do.

* We need to add routing information for our new controller.
* We need to add view templates for the visual representation of the results.
* We need to add the actions of the controller.

Adding the routing
~~~~~~~~~~~~~~~~~~

To make things easy, we will use annotations to add the routing information for our controller.
This is useful, because you have the definition in the very same place where the action is defined.

To enable this, we add those lines to our ``app/config/routing_dev.yml``:

.. code-block:: yaml

    _catalog:
        resource: "@AcmeDemoBundle/Controller/CatalogController.php"
        type:     annotation

In order to have our new routing available in the test environment, we add a file ``app/config/routing_test.yml`` importing the dev one.

.. code-block:: yaml

    _main:
        resource: routing_dev.yml

Any new route we will add in the controller file using the annotations will now be recognized.

The view basics
~~~~~~~~~~~~~~~

Our view templates using the ``Twig`` template engine will be placed under the directory ``src/Acme/DemoBundle/Resources/views/Catalog/``.
The template file names will default to ``action-name.response-format.twig``. As we are going to create a web page, we are using the format ``html``.
The files would be named like ``categories.html.twig`` for a ``CatalogController::categoriesAction()`` method.

Creating the controller
~~~~~~~~~~~~~~~~~~~~~~~

Let's start with the list of categories.
At first, we need the data, we want to be displayed: the categories. Those will be retrieved from the ``EntityRepository`` of ``Doctrine``.

.. code-block:: php

    $categories = $this->getDoctrine()
        ->getRepository('AcmeDemoBundle:Category')
        ->findAll()
    ;

Now, we need a template, to display the data at ``src/Acme/DemoBundle/Resources/views/Catalog/categories.html.twig``.
Our scenario defines a container with the id ``category-list`` containing the category names.

.. code-block:: jinja

    {% extends "AcmeDemoBundle::layout.html.twig" %}
    
    {% block title "Catalog - Category List" %}
    
    {% block content_header '' %}
    
    {% block content %}
        <h1>Category List</h1>
        <ul id="category-list">
        {% for category in categories %}
            <li>{{ category.name }}</li>
        {% endfor %}
        </ul>
    {% endblock %}

Those two snippets are now bound by `the contract pattern`_. We expect a ``categories`` to be available in the view, containing a list of items that have a ``name`` property readable.
Unfortunately the retrieved data fulfills this contract, so we can pass it to the view. Doing so completes the controller action itself.
In addition we add the routing information as defined by the scenario ``/categories``. Now our ``CatalogController`` contains the following code.

.. code-block:: php

    <?php
    
    namespace Acme\DemoBundle\Controller;
    
    use Symfony\Bundle\FrameworkBundle\Controller\Controller;
    
    use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
    use Sensio\Bundle\FrameworkExtraBundle\Configuration\Template;
    
    class CatalogController extends Controller
    {
        /**
         * @Route("/categories", name="_catalog_categories")
         * @Template()
         */
        public function categoriesAction()
        {
            $categories = $this->getDoctrine()
                ->getRepository('AcmeDemoBundle:Category')
                ->findAll();
    
            return array(
                'categories' => $categories,
            );
        }
    }

Running the acceptance tests again will make some of them pass. We are getting closer!

::

    5 scenarios (4 passed, 1 failed)
    48 steps (41 passed, 6 skipped, 1 failed)

What failed, was a condition on links to the products list of a specific category.
Let's add the controller and view for this listing.

The view file ``src/Acme/DemoBundle/Resources/Catalog/view/categoryContent.html.twig``.

.. code-block:: jinja

    {% extends "AcmeDemoBundle::layout.html.twig" %}
    
    {% block title "Catalog - Product List" %}
    
    {% block content_header '' %}
    
    {% block content %}
        <h1>Product List</h1>
        <ul id="product-list">
        {% for product in products %}
            <li>{{ product.name }}</li>
        {% endfor %}
        </ul>
    {% endblock %}

The controller will gain a new method.

.. code-block:: php

    <?php
    
    namespace Acme\DemoBundle\Controller;
    
    use Symfony\Bundle\FrameworkBundle\Controller\Controller;
    
    use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
    use Sensio\Bundle\FrameworkExtraBundle\Configuration\Template;
    
    use Acme\DemoBundle\Entity\Category;
    
    use \Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
    
    class CatalogController extends Controller
    {
        /**
         * @Route("/categories", name="_catalog_categories")
         * @Template()
         */
        public function categoriesAction()
        {
            $categories = $this->getDoctrine()
                ->getRepository('AcmeDemoBundle:Category')
                ->findAll();
    
            return array(
                'categories' => $categories,
            );
        }
    
        /**
         * @Route("/categories/{name}", name="_catalog_category_content")
         * @Template()
         */
        public function categoryContentAction($name)
        {
            $category = $this->getDoctrine()
                ->getRepository('AcmeDemoBundle:Category')
                ->findOneByName($name);
    
            if (!$category instanceof Category) {
                throw new NotFoundHttpException(sprintf('The category "%s" could not be found.', $name));
            }
    
            return array(
                'products' => $category->getProducts(),
            );
        }
    }

Now that we have the new route and its content available, we can link the categories in the category list template.

.. code-block:: jinja

    <li><a href="{{ path('_catalog_category_content', {'name': category.name}) }}">{{ category.name }}</a></li>

By issuing the test again ``php app/console behat -e test @AcmeDemoBundle``, we now can see, **we are done**!
Everything a stakeholder gave us in its feature definitions is fulfilled and working correctly.


.. note::

    Did you ever see the web page, we created? No? - Well, take a look, you deserve it!

So let's take those changes into our repository and commit them.

* Mink, the MinkBundle and its configuration

  ``git add app/AppKernel.php app/autoload.php deps src/Acme/DemoBundle/Features/Context/ app/config/config_test.yml vendor/ && git commit``

* catalog with category list and category content

  ``git add app/config/routing_dev.yml app/config/routing_test.yml src/Acme/DemoBundle/ && git commit``

Ok, now we have Mink running, doing acceptance tests against .. well? The Symfony2 bundled http crawler for functional testing.

But we want to have this done in a "real" browser! So, let's add Zombie.js to the game.
Please, view http://zombie.labnotes.org/ for installation of Zombie.js itself - it's very easy!

.. note::

    Zombie.js is a lightweight framework for testing client-side JavaScript code in a simulated environment.

Infecting the tests
-------------------

Ok, you got `Zombie.js installed`_, right?
Then let's head on. We need to configure Mink to use Zombie.js in the ``app/config/config_test_.yml``.
This will initialize the ``ZombieDriver`` for ``Mink``, but leave the default session to the default one (``symfony``). If you want to have everything run using zombie, simply change the default session to ``zombie``.

.. code-block:: yaml

    mink:
        base_url: http://your-app.dev/app_test.php
        default_session: symfony
        zombie: ~

If you don't have set the default session to ``zombie``, you can use the ``mink:zombie`` tag on any scenario, to run this one with the ``ZombieDriver``.

.. code-block:: gherkin

    @mink:zombie
    Scenario: The categories link to their products list

This is also valid for a feature definition running every scenario with Zombie.js.

.. code-block:: gherkin

    @mink:zombie
    Feature: Navigating the categories within the catalog

Well, now that we actually visit this web page, we also need that index file at ``web/app_test.php``, derived from the ``app_dev.php``.

.. code-block:: php

    <?php
    
    // this check prevents access to debug front controllers that are deployed by accident to production servers.
    // feel free to remove this, extend it, or make something more sophisticated.
    if (!in_array(@$_SERVER['REMOTE_ADDR'], array(
        '127.0.0.1',
        '::1',
    ))) {
        header('HTTP/1.0 403 Forbidden');
        exit('You are not allowed to access this file. Check '.basename(__FILE__).' for more information.');
    }
    
    require_once __DIR__.'/../app/bootstrap.php.cache';
    require_once __DIR__.'/../app/AppKernel.php';
    
    use Symfony\Component\HttpFoundation\Request;
    
    $kernel = new AppKernel('test', true);
    $kernel->loadClassCache();
    $kernel->handle(Request::createFromGlobals())->send();

Now, we have set up Zombie.js to be used by Mink. 

.. note::

    Please remember, by now we only check plain HTML, so the default symfony driver is faster and does the job!
    When interacting with the web interface in an asynchronous way using Javascript (AJAX), that's the time you want to use Zombie.js for sure.

.. _`git installed`: http://book.git-scm.com/2_installing_git.html
.. _`node.js installed`: https://github.com/joyent/node/wiki/Installation
.. _`npm installed`: https://github.com/isaacs/npm/blob/master/README.md
.. _`PHPUnit installed`: http://www.phpunit.de/manual/3.6/en/installation.html
.. _`Gherkin wiki`: https://github.com/cucumber/cucumber/wiki/Gherkin
.. _`more about steps`: http://docs.behat.org/quick_intro.html#more-about-steps
.. _`Test Driven Development`: http://en.wikipedia.org/wiki/Test-driven_development
.. _`the contract pattern`: http://en.wikipedia.org/wiki/Design_by_contract
.. _`Zombie.js installed`: http://zombie.labnotes.org/#Infection
