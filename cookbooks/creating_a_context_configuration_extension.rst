Creating a Behat extension to provide custom configuration for Contexts
=======================================================================

Extensions are particularly useful when configuration becomes a necessity.

In this cookbook, we will create a simple extension named ``HelloWorld`` that will display some text and cover:

#. Setting up the context
#. Creating the extension
#. Initializing the context
#. Using the extension

Setting Up the Context
----------------------

First, we create a ``Context`` class that will throw a ``PendingException`` with a configurable text.
The configuration will also control whether the behaviour is enabled or not.

The example directory structure and file locations in this cookbook assume you have configured
composer to autoload the ``HelloWorld`` namespace from the ``src`` directory.

.. code-block::

  src/
      Context/
          HelloWorldContext.php   # This is where we'll implement our step

.. code-block:: php

  <?php

  namespace HelloWorld\Context;

  use Behat\Behat\Context\Context as BehatContext;
  use Behat\Behat\Tester\Exception\PendingException;
  use Behat\Step\Given;

  class HelloWorldContext implements BehatContext
  {
      private bool $enable = false;
      private string $text;

      /*
       * Will be used by the extension to initialise the context with configuration values.
       */
      public function initializeConfig(bool $enable, string $text)
      {
          $this->enable = $enable;
          $this->text = $text;
      }

      #[Given('I say Hello World')]
      public function helloWorld()
      {
          if ($this->enable) {
            throw new PendingException($this->text);
          }
      }
  }

Creating the Extension
----------------------

Next, we need to create the entry point for our Hello World, the extension itself.

.. code-block::

  src/
      Context/
          HelloWorldContext.php
      ServiceContainer/
          HelloWorldExtension.php   # This is where we'll define our extension

The ``getConfigKey`` method below is used to identify our extension in the configuration.
The ``configure`` method is used to define the configuration tree.

.. code-block:: php

  <?php

  namespace HelloWorld\ServiceContainer;

  use Behat\Behat\Context\ServiceContainer\ContextExtension;
  use Behat\Testwork\ServiceContainer\Extension;
  use Behat\Testwork\ServiceContainer\ExtensionManager;
  use Symfony\Component\Config\Definition\Builder\ArrayNodeDefinition;
  use Symfony\Component\DependencyInjection\ContainerBuilder;
  use Symfony\Component\DependencyInjection\Definition;
  use HelloWorld\Context\Initializer\HelloWorldInitializer;

  class HelloWorldExtension implements Extension
  {
      public function getConfigKey()
      {
          return 'helloworld_extension';
      }

      /**
       * Called after extensions activation, but before `configure()`.
       * Used to hook into other extensions' configuration.
       */
      public function initialize(ExtensionManager $extensionManager)
      {
          // empty for our case
      }

      public function configure(ArrayNodeDefinition $builder)
      {
          $builder
              ->addDefaultsIfNotSet()
                  ->children()
                      ->booleanNode('enable')->defaultFalse()->end()
                      ->scalarNode('text')->defaultValue('Hello World!')->end()
                  ->end()
              ->end();
      }

      public function load(ContainerBuilder $container, array $config)
      {
          // ... we'll load our configuration here
      }

      // needed as Extension interface implements CompilerPassInterface
      public function process(ContainerBuilder $container)
      {
      }
  }

.. note::

  The ``initialize`` and ``process`` methods are empty in our case but are
  useful when you need to interact with other extensions or process the
  container after it has been compiled.

Initializing the Context
------------------------

To pass configuration values to our ``HelloWorldContext``, we need to create an initializer.

.. code-block::

  src/
      Context/
          Initializer/
              HelloWorldInitializer.php   # This will handle context initialization
            HelloWorldContext.php
      ServiceContainer/
        HelloWorldExtension.php

The code for ``HelloWorldInitializer.php``:

.. code-block:: php

  <?php

  namespace HelloWorld\Context\Initializer;

  use HelloWorld\Context\HelloWorldContext;
  use Behat\Behat\Context\Context;
  use Behat\Behat\Context\Initializer\ContextInitializer;

  class HelloWorldInitializer implements ContextInitializer
  {
      private string $text;
      private bool $enable;

      public function __construct(string $text, bool $enable)
      {
          $this->text = $text;
          $this->enable = $enable;
      }

      public function initializeContext(Context $context)
      {
          /*
           * At the start of every scenario, behat will create a new instance of every `Context`
           * registered in your project. It will then call this method with each new `Context` in
           * turn. If you want to initialise multiple contexts, you can of course give them an
           * interface and check for that here.
           */
          if (!$context instanceof HelloWorldContext) {
              return;
          }

          $context->initializeConfig($this->enable, $this->text);
      }
  }

We need to register the initializer definition within the Behat container
through the ``HelloWorldExtension``, ensuring it gets loaded:

.. code-block:: php

  <?php

  // ...

  use Symfony\Component\DependencyInjection\Definition;
  use Behat\Behat\Context\ServiceContainer\ContextExtension;

  class HelloWorldExtension implements Extension
  {
      // ...

      public function load(ContainerBuilder $container, array $config)
      {
          $definition = new Definition(HelloWorldInitializer::class, [
              $config['text'],
              $config['enable'],
          ]);
          $definition->addTag(ContextExtension::INITIALIZER_TAG);
          $container->setDefinition('helloworld_extension.context_initializer', $definition);
      }

      // ...
  }

Finally, we can define a custom configuration object for use in a project's ``behat.php``.
This step is optional - users can also register your extension with the generic
``Behat\Config\Extension`` class. However, providing a custom class will make it easier
for users to discover and configure the correct settings for your extension.

.. code-block:: php

  <?php

  namespace HelloWorld\Config;

  use Behat\Config\ExtensionConfigInterface;
  use HelloWorld\ServiceContainer\HelloWorldExtension;

  final class HelloWorldExtensionConfig implements ExtensionConfigInterface
  {

      // You don't need to set defaults here, they are defined along with the config structure in
      // HelloWorld\ServiceContainer\HelloWorldExtension::configure(). It is important that this
      // object only returns settings that the user has explicitly configured.
      private array $settings = [];

      // The following methods must be provided for Behat to read the configuration object

      public function name(): string
      {
          // This should return the fully qualified name of your entrypoint class
          return HelloWorldExtension::class;
      }

      public function toArray(): array
      {
          return $this->settings;
      }

      // The following methods provide the mechanism for users to customise your
      // extension's configuration.
      // We recommend using setters rather than constructor properties, for
      // consistency with Behat's own config objects.

      public function enable(): self
      {
          $this->settings['enable'] = true;

          return $this;
      }

      public function disable(): self
      {
          $this->settings['enable'] = false;

          return $this;
      }

      public function withText(string $text): self
      {
          $this->settings['text'] = $text;

          return $this;
      }
  }


Using the extension
-------------------

Now that the extension is ready and will inject values into context, we just
need to configure it into a project.

We'll set up an instance of our custom ``HelloWorldExtensionConfig`` configuration
object, and use the ``withExtension()`` method of a profile (``default`` in our
case) to register it.

Finally, we need to load the ``HelloWorld\Context\HelloWorldContext`` into our suite.

Here's the ``behat.php``:

.. code-block:: php

    <?php

    use Behat\Config\Config;
    use Behat\Config\Extension;
    use Behat\Config\Profile;
    use Behat\Config\Suite;
    use FeatureContext;
    use HelloWorld\Context\HelloWorldContext;
    use HelloWorld\Config\HelloWorldExtensionConfig;

    return new Config()
        ->withProfile(new Profile('default')
            ->withExtension(new HelloWorldExtensionConfig()
                ->withText('Hi there!')
                ->enable()
            )
            ->withSuite(new Suite('default')
                ->withContexts(
                    FeatureContext::class,
                    HelloWorldContext::class
                )));

And now a scenario like this one:

.. code-block::

  Feature: Test

    Scenario: Test
      Given I say Hello World

Will display our text ``Hi there!`` as a pending exception.

Conclusion
----------

Congratulations! You have just created a simple Behat extension.
This extension demonstrates three of the common steps to building a Behat
extension: defining an extension, creating an initializer, and configuring contexts.

Feel free to experiment with this extension and expand its functionality.

Happy testing!
