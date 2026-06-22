Writing a custom Behat formatter
================================

How to write a custom formatter for Behat?

Introduction
------------

Why a custom formatter?
~~~~~~~~~~~~~~~~~~~~~~~~

Behat has three native formatters:

-  **pretty**: the default formatter, which prints every line in green (if a test passes) or red (if it fails),
-  **progress**: print a "dot" for each test, and a recap of all failing tests at the end,
-  **junit**: outputs a `junit`_ compatible XML file.

Those are nice, and worked for most of the cases. You can use the "progress" one for the CI, and the "pretty" for
development for example.

But you might want to handle differently the output that Behat renders.
In this cookbook, we will see how to implement a custom formatter for `reviewdog`_,
a global review tool that takes input of linters or testers, and that can send "checks" on github,
bitbucket or gitlab PR.

Reviewdog can handle `two types of input`_:

-  any stdin, coupled with an "errorformat"
   (a Vim inspired format that can convert text string to machine-readable errors),
-  a `"Reviewdog Diagnostic Format"`_: a JSON with error data that reviewdog can parse.

But parsing Behat stdout with errorformat is not that easy, as Behat's output is multi-line, add dots, errorformat can
be tricky and might not handle every case (behat has different possible outputs, etc.).
So We will create a custom formatter for Behat.

This way, we will still
have Behat's human-readable stdout, and a JSON file written that reviewdog can understand.


.. _`junit`: https://junit.org/
.. _`reviewdog`: https://github.com/reviewdog/reviewdog
.. _`two types of input`: https://github.com/reviewdog/reviewdog#input-format
.. _`"Reviewdog Diagnostic Format"`: https://github.com/reviewdog/reviewdog/tree/48b25a0aafb8494e751387e16f729faee9522c46/proto/rdf

Let's dive
----------

Behat allows us to load "extensions", that can add features to the language. In fact, it is a core functionality to
implement PHP functions behind gherkin texts.
Those extensions are just classes that are loaded by Behat to register configuration and features.

Behat is powered by Symfony: if you know it, you will already know the concepts under the hood, if you don't,
that's not a problem and not required to create your extension.

Anatomy of a formatter extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A formatter extension requires three things to work:

-  a class that "defines" the extension, to make your extension work with Behat,
-  a "formatter", that can listen to Behat events, and converts Behat's tests result to anything you want,
-  an "output printer", that writes the converted data anywhere you want (mainly the stdout, a file or a directory).

Create the extension
~~~~~~~~~~~~~~~~~~~~

Any Behat extensions must implement ``Behat\Testwork\ServiceContainer\Extension``.
It is a way to inject anything you want into Behat's kernel.

In our case, we need to load the "formatter" in Behat's kernel, and tag it as an output formatter.
This way Behat will allow our extension to be configured as a formatter. You can register multiple formatters with the
same extension if you like.

.. code:: php

   <?php

   declare(strict_types=1);

   namespace HelloWorld\BehatReviewdogFormatter;

   use Behat\Testwork\Output\ServiceContainer\OutputExtension;
   use Behat\Testwork\ServiceContainer\Extension;
   use Behat\Testwork\ServiceContainer\ExtensionManager;
   use Symfony\Component\Config\Definition\Builder\ArrayNodeDefinition;
   use Symfony\Component\DependencyInjection\ContainerBuilder;

   class ReviewdogFormatterExtension implements Extension
   {
       public function getConfigKey()
       {
           return 'reviewdog_formatter';
       }

       /**
        * This is the only method that we will configure to inject our formatter
        */
       public function load(ContainerBuilder $container, array $config): void
       {
           // register the "Output printer" class
           $outputPrinterDefinition = $container->register(ReviewdogOutputPrinter::class);

           // add some arguments. In this case, it will use Behat's current working directory to write the output file, if not override
           $outputPrinterDefinition->addArgument('%paths.base%');

           // register the "ReviewdogFormatter" class in Behat's kernel
           $formatterDefinition = $container->register(ReviewdogFormatter::class);

           // add some arguments that will be called in the constructor.
           // This isn't required, but in our case we will inject Behat's base path (to remove it from the absolute file path later) and the printer.
           $formatterDefinition->addArgument('%paths.base%');
           $formatterDefinition->addArgument($outputPrinterDefinition);

           // tag the formatter as an "output.formatter", this way Behat will add it to its formatter list.
           $formatterDefinition->addTag(OutputExtension::FORMATTER_TAG, ['priority' => 100]);
       }

       public function configure(ArrayNodeDefinition $builder): void { }

       public function initialize(ExtensionManager $extensionManager): void { }

       public function process(ContainerBuilder $container): void { }
   }

Create the formatter
~~~~~~~~~~~~~~~~~~~~

The formatter will listen to Behat's events, and create output data depending on the type of event, the current state,
etc.

.. code:: php

   <?php

   namespace HelloWorld\BehatReviewdogFormatter;

   use Behat\Behat\EventDispatcher\Event\AfterStepTested;
   use Behat\Behat\EventDispatcher\Event\StepTested;
   use Behat\Behat\Tester\Result\ExecutedStepResult;
   use Behat\Testwork\EventDispatcher\Event\BeforeExerciseCompleted;
   use Behat\Testwork\Output\Formatter;
   use Behat\Testwork\Output\Printer\OutputPrinter;

   class ReviewdogFormatter implements Formatter
   {
       public function __construct(
           private readonly string $pathsBase,
           private readonly ReviewdogOutputPrinter $outputPrinter
       ) {
       }

       /**
        * setParameter will be called for each key given to the formatter in your behat.php file.
        * We will see that later in the "integration".
        * In our case, the only allowed parameter is a "file_name" that must be a string : the JSON file that we will write.
        */
       public function setParameter($name, $value): void
       {
           switch ($name) {
               case 'file_name':
                   if (!is_string($value)) {
                       throw new \InvalidArgumentException('file_name must be a string');
                   }

                   $this->outputPrinter->setFileName($value);
                   break;
               default:
                   throw new \Exception('Unknown parameter ' . $name);
           }
       }

       /**
        * We do not call this, so no need to define an implementation
        */
       public function getParameter($name) { }

       /**
        * Our formatter is a Symfony EventSubscriber.
        * This method tells Behat where we want to "hook" in the process.
        * Here we want to be called:
        *   - at start, when the test is launched with the `BeforeExerciseCompleted::BEFORE` event,
        *   - when a step has ended with the `StepTested::AFTER` event.
        *
        * There are a lot of other events that can be found here in the Behat\Testwork\EventDispatcher\Event class
        */
       public static function getSubscribedEvents(): array
       {
           return [
               // call the `onBeforeExercise` method on startup
               BeforeExerciseCompleted::BEFORE => 'onBeforeExercise',
               // call the `onAfterStepTested` method after each step
               StepTested::AFTER => 'onAfterStepTested',
           ];
       }

       /**
        * This is the name of the formatter, that will be used in the behat.php file
        */
       public function getName(): string
       {
           return 'reviewdog';
       }

       public function getDescription(): string
       {
           return 'Reviewdog formatter';
       }

       public function getOutputPrinter(): OutputPrinter
       {
           return $this->outputPrinter;
       }

       /**
        * When we launch a test, let's inform the printer that we want a fresh new file
        */
       public function onBeforeExercise(BeforeExerciseCompleted $event):void
       {
           $this->outputPrinter->removeOldFile();
       }

       public function onAfterStepTested(AfterStepTested $event):void
       {
           $testResult = $event->getTestResult();
           $step = $event->getStep();

           // In the reviewdog formatter, we just want to print errors, so ignore all steps that are not a failure executed test
           // but you might want to handle things differently here !
           if ($testResult->isPassed() || !$testResult instanceof ExecutedStepResult) {
               return;
           }

           // get the relative path
           $path = str_replace($this->pathsBase . '/', '', $event->getFeature()->getFile() ?? '');

           // prepare the data that we will send to the printer…
           $line = [
               'message' => $testResult->getException()?->getMessage() ?? 'Failed step',
               'location' => [
                   'path' => $path,
                   'range' => [
                       'start' => [
                           'line' => $step->getLine(),
                           'column' => 0,
                       ],
                   ],
               ],
               'severity' => 'ERROR',
               'source' => [
                   'name' => 'behat',
               ],
           ];

           $json = json_encode($line, \JSON_THROW_ON_ERROR);

           // …and send it
           $this->getOutputPrinter()->writeln($json);
       }

   }

Create the output printer
~~~~~~~~~~~~~~~~~~~~~~~~~

The last file that we need to implement is the printer. In our case we need a single class that can write lines to a
file.

.. code:: php

   <?php

   namespace HelloWorld\BehatReviewdogFormatter;

   use Behat\Testwork\Output\Printer\OutputPrinter;

   class ReviewdogOutputPrinter implements OutputPrinter
   {
       private ?bool $isOutputDecorated;

       /** the outputPath where we will write the output file */
       private ?string $outputPath = null;

       /** The default filename, if none is provided */
       private string $fileName = 'reviewdog-behat.json';

       public function __construct(private readonly string $pathBase) { }

       /**
        * as the formatter can inform us of the filename, we need to store that
        */
       public function setFileName(string $fileName): void
       {
           $this->fileName = $fileName;
       }

       /**
        * outputPath is a special parameter that you can give to any Behat formatter under the key `output_path`
        */
       public function setOutputPath($path): void
       {
           $this->outputPath = $path;
       }

       /**
        * The output path, defaults to Behat's base path
        */
       public function getOutputPath(): string
       {
           return $this->outputPath ?? $this->pathBase;
       }

       /** Sets output styles. */
       public function setOutputStyles(array $styles): void { }

       /** @deprecated */
       public function getOutputStyles()
       {
           return [];
       }

       /** Forces output to be decorated. */
       public function setOutputDecorated($decorated): void
       {
           $this->isOutputDecorated = (bool) $decorated;
       }

       /** @deprecated */
       public function isOutputDecorated()
       {
           return $this->isOutputDecorated;
       }

       /**
        * Behat can have multiple verbosity levels, you may want to handle this to display more information.
        * These use the Symfony\Component\Console\Output\OutputInterface::VERBOSITY_ constants.
        * For reviewdog, we do not need that.
        */
       public function setOutputVerbosity($level): void { }

       /** @deprecated */
       public function getOutputVerbosity()
       {
           return 0;
       }

       /**
        * Writes message(s) to output stream.
        *
        * @param string|array<string> $messages
        */
       public function write($messages): void
       {
           if (!is_array($messages)) {
               $messages = [$messages];
           }

           $this->doWrite($messages, false);
       }

       /**
        * Writes newlined message(s) to output stream.
        *
        * @param string|array<string> $messages
        */

       public function writeln($messages = ''): void
       {
           if (!is_array($messages)) {
               $messages = [$messages];
           }

           $this->doWrite($messages, true);
       }

       /**
        * Clear output stream, so on next write formatter will need to init (create) it again.
        * Not needed in my case.
        */
       public function flush(): void
       {
       }

       /**
        * Called by the formatter when test starts
        */
       public function removeOldFile(): void
       {
           $filePath = $this->getFilePath();

           if (file_exists($filePath)) {
               unlink($filePath);
           }
       }

       /**
        * @param array<string> $messages
        */
       private function doWrite(array $messages, bool $append): void
       {
           // create the output path if if does not exists.
           if (!is_dir($this->getOutputPath())) {
               mkdir($this->getOutputPath(), 0777, true);
           }

           // write data to the file
           file_put_contents($this->getFilePath(), implode("\n", $messages) . "\n", $append ? \FILE_APPEND : 0);
       }

       private function getFilePath(): string
       {
           return $this->getOutputPath() . '/' . $this->fileName;
       }
   }

Integration in your project
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need to add the extension in your Behat configuration file (default is ``behat.php``)
and configure it to use the formatter:

.. code:: php

    <?php

    use Behat\Config\Config;
    use Behat\Config\Extension;
    use Behat\Config\Formatter\Formatter;
    use Behat\Config\Formatter\PrettyFormatter;
    use Behat\Config\Profile;
    use HelloWorld\BehatReviewdogFormatter\ReviewdogFormatterExtension;

    return new Config()
        ->withProfile(new Profile('default')
            ->withExtension(new Extension(ReviewdogFormatterExtension::class)));
            ->withFormatter(new PrettyFormatter())
            // "reviewdog" here is the "name" given in our formatter
            ->withFormatter(new Formatter('reviewdog', [
                // 'file_name' is optional and a custom parameter that we inject into the printer
                'file_name' => 'reviewdog-behat.json',
            ])
                // outputPath is optional and handled directly by Behat
                ->withOutputPath('build/logs/behat'))

.. note::

      Remember, this formatter only produces output if scenarios fail - if your features all
      pass, the output file will not be created.

Different output per profile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can activate the extension only when you specify a profile in your command (ex: ``--profile=ci``)

For example if you want the pretty formatter by default, but both progress and reviewdog on your CI,
you can configure it like this:

.. code:: php

    <?php

    use Behat\Config\Config;
    use Behat\Config\Extension;
    use Behat\Config\Formatter\Formatter;
    use Behat\Config\Formatter\PrettyFormatter;
    use Behat\Config\Formatter\ProgressFormatter;
    use Behat\Config\Profile;
    use HelloWorld\BehatReviewdogFormatter\ReviewdogFormatterExtension;

    return new Config()
        ->withProfile(new Profile('default')
            ->withExtension(new Extension(ReviewdogFormatterExtension::class)))
            ->withFormatter(new PrettyFormatter())
        ->withProfile(new Profile('ci')
            ->disableFormatter('pretty')
            ->withFormatter(new ProgressFormatter())
            ->withFormatter(new Formatter('reviewdog', [
                'file_name' => 'reviewdog-behat.json',
            ])
                ->withOutputPath('build/logs/behat')));

Enjoy!
-------

That's how you can write a basic custom Behat formatter!

If you have much more complex logic, and you need the formatter to be more dynamic, Behat provides a
FormatterFactory interface.
You can see usage examples directly in `Behat's codebase`_,
but in a lot of cases, something like this example should work.

.. _`Behat's codebase`: https://github.com/Behat/Behat/tree/2a3832d9cb853a794af3a576f9e524ae460f3340/src/Behat/Behat/Output/ServiceContainer/Formatter

Want to use reviewdog and the custom formatter yourself?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to use the reviewdog custom formatter, you can find it on github: `jdeniau/behat-reviewdog-formatter`_

There are other Behat custom formatters in the wild, especially `BehatHtmlFormatterPlugin`_.
Reading this formatter might help you understand how the Behat formatter system works, and it can output an HTML
file that can help you understand why your CI is failing.


.. _`jdeniau/behat-reviewdog-formatter`: https://github.com/jdeniau/behat-reviewdog-formatter
.. _`BehatHtmlFormatterPlugin`: https://github.com/dutchiexl/BehatHtmlFormatterPlugin

About the author
~~~~~~~~~~~~~~~~

Written by `Julien Deniau <https://julien.deniau.me>`__,
originally posted as a blog post `on his blog <https://julien.deniau.me/posts/2024-01-24-custom-behat-formatter>`__.
