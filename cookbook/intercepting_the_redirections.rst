Intercepting the redirection with Behat and Mink
================================================

Intercepting a redirection to execute some steps before following it can
be useful in some cases, for instance when you are redirecting after sending
an email and want to test it :doc:`using the profiler </cookbook/using_the_profiler_with_minkbundle>`.
This is possible for drivers based on the Symfony BrowserKit component.

Adding the Needed Steps
-----------------------

To intercept the redirections, you will need two new steps: one to enable
the interception (allowing you to intercept the redirection for a step), and
another one to follow the redirection manually when you are ready and disable
the interception.

A scenario using them will look like this:

.. code-block:: gherkin

    When I submit the form without redirection
    # At this place, the redirection is not followed automatically
    # This allows using the profiler for this request
    Then I should receive an email
    # The redirection can then be followed manually
     And I should be redirected
    # The driver uses the normal behavior again after this

Bootstrapping the Interception Steps:
-------------------------------------

First, let's implement a function which will check that the current driver
is able to intercept the redirections (useful when you let someone else write
the features with this step to avoid misuses):

.. code-block:: php

    <?php

    namespace Acme\DemoBundle\Features\Context;

    use Behat\BehatBundle\Context\MinkContext;
    use Behat\Behat\Context\Step;
    use Behat\Mink\Exception\UnsupportedDriverActionException;
    use Behat\Mink\Driver\GoutteDriver;

    /**
     * Feature context.
     */
    class FeatureContext extends MinkContext
    {
        public function canIntercept()
        {
            $driver = $this->getSession()->getDriver();
            if (!$driver instanceof GoutteDriver) {
                throw new UnsupportedDriverActionException(
                    'You need to tag the scenario with '.
                    '"@mink:goutte" or "@mink:symfony". '.
                    'Intercepting the redirections is not '.
                    'supported by %s', $driver
                );
            }
        }
    }

.. note::

    You can only intercept the redirections when using the GoutteDriver or
    the SymfonyDriver which are based on the Symfony BrowserKit component.
    You will need to tag your scenario so that the `goutte` or the `symfony`
    session is used.

    .. code-block:: gherkin

        @mink:symfony
        Scenario: I should receive an email

Implementing Interception Steps Logic
-------------------------------------

It is now time to use the client to configure the interception:

.. code-block:: php

    /**
     * @Given /^(.*) without redirection$/
     */
    public function theRedirectionsAreIntercepted($step)
    {
        $this->canIntercept();
        $this->getSession()->getDriver()->getClient()->followRedirects(false);

        return new Step\Given($step);
    }

    /**
     * @When /^I follow the redirection$/
     * @Then /^I should be redirected$/
     */
    public function iFollowTheRedirection()
    {
        $this->canIntercept();
        $client = $this->getSession()->getDriver()->getClient();
        $client->followRedirects(true);
        $client->followRedirect();
    }
