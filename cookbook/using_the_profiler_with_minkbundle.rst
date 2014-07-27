Using the Symfony2 Profiler with Behat and Symfony2Extension
============================================================

Accessing the Symfony2 profiler can be useful to test some parts of your
web application that does not hit the browser. Assuming it is supposed to
send an email, you can use the profiler to test that the email is sent correctly.

Your goal here will be to implement a step like this:

.. code-block:: gherkin

     Then I should get an email on "stof@example.org" with:
        """
        To finish validating your account - please visit
        """

Bootstrapping the Email Step
----------------------------

First, let's implement a profiler retrieving function which will check that the
current driver is the profilable one (useful when you let someone else write
the features with this step to avoid misuses) and that the profiler is enabled:

.. code-block:: php

    <?php

    namespace Acme\DemoBundle\Features\Context;

    use Behat\Gherkin\Node\PyStringNode;
    use Behat\Behat\Exception\PendingException;
    use Behat\BehatBundle\Context\MinkContext;

    use Behat\Mink\Exception\UnsupportedDriverActionException,
        Behat\Mink\Exception\ExpectationException;
    use Behat\Symfony2Extension\Driver\KernelDriver;;

    use PHPUnit_Framework_ExpectationFailedException as AssertException;

    /**
     * Feature context.
     */
    class FeatureContext extends MinkContext
    {
        public function getSymfonyProfile()
        {
            $driver = $this->getSession()->getDriver();
            if (!$driver instanceof KernelDriver) {
                throw new UnsupportedDriverActionException(
                    'You need to tag the scenario with '.
                    '"@mink:symfony2". Using the profiler is not '.
                    'supported by %s', $driver
                );
            }

            $profile = $driver->getClient()->getProfile();
            if (false === $profile) {
                throw new \RuntimeException(
                    'The profiler is disabled. Activate it by setting '.
                    'framework.profiler.only_exceptions to false in '.
                    'your config'
                );
            }

            return $profile;
        }
    }

.. note::

    You can only access the profiler when using the KernelDriver which gives
    you access to the kernel handling the request. You will need to tag your
    scenario so that the `symfony2` session is used.

    .. code-block:: gherkin

        @mink:symfony2
        Scenario: I should receive an email

Implementing Email Step Logic
-----------------------------

It is now time to use the profiler to implement our email checking step:

.. code-block:: php

    /**
     * @Given /^I should get an email on "(?P<email>[^"]+)" with:$/
     */
    public function iShouldGetAnEmail($email, PyStringNode $text)
    {
        $error     = sprintf('No message sent to "%s"', $email);
        $profile   = $this->getSymfonyProfile();
        $collector = $profile->getCollector('swiftmailer');

        foreach ($collector->getMessages() as $message) {
            // Checking the recipient email and the X-Swift-To
            // header to handle the RedirectingPlugin.
            // If the recipient is not the expected one, check
            // the next mail.
            $correctRecipient = array_key_exists(
                $email, $message->getTo()
            );
            $headers = $message->getHeaders();
            $correctXToHeader = false;
            if ($headers->has('X-Swift-To')) {
                $correctXToHeader = array_key_exists($email,
                    $headers->get('X-Swift-To')->getFieldBodyModel()
                );
            }

            if (!$correctRecipient && !$correctXToHeader) {
                continue;
            }

            try {
                // checking the content
                return assertContains(
                    $text->getRaw(), $message->getBody()
                );
            } catch (AssertException $e) {
                $error = sprintf(
                    'An email has been found for "%s" but without '.
                    'the text "%s".', $email, $text->getRaw()
                );
            }
        }

        throw new ExpectationException($error, $this->getSession());
    }
