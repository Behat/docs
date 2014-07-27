Using Spin Functions for Slow Tests
===================================

Often, especially when using Mink to test web applications, you will find that
Behat goes faster than your web application can keep up - it will try and click
links or perform actions before the page has had chance to load, and therefore
result in a failing test, that would have otherwise passed.

To alleviate this problem, we can use spin functions, to repeatedly try and
action or test a condition, until it works. This article looks at applying it
to Mink, but the technique is applicable to any test using Behat.

Using closures
--------------

PHP 5.3 introduced closures - anonymous functions (functions without a name)
that can be passed as function arguments. This is very useful for our purpose
as it allows us to pass a function that tests a certain condition, or tries
to perform a certain action.

You can read more about closures in the `PHP documentation <http://php.net/manual/en/functions.anonymous.php>`.

Spin method
-----------

Lets start by implementing a spin method in our FeatureContext.php.

.. code-block:: php

    public function spin ($lambda)
    {
        while (true)
        {
            try {
                if ($lambda($this)) {
                    return true;
                }
            } catch (Exception $e) {
                // do nothing
            }
            
            sleep(1);
        }
    }

This will create a loop, calling our anonymous function every second, until it
returns true. To allow us to access the FeatureContext object, we'll pass it
into the function as a parameter.

Using the method
----------------

Now we have implemented it, we can make use of it in our step definitions. For
our first example, lets say we're using Mink, and we want to wait until a
specific element becomes visible.

The method expects us to pass it a function that returns true when the conditions
are satisfied. So lets implement that.

.. code-block:: php

    $this->spin(function($context) {
        return ($context->getSession()->getPage()->findById('example')->isVisible());
    });

This function will return whether #example element is visible or not. Our
spin method will taken try to run this function every second until
the function returns true.

Because our spin method will also catch exceptions, we can also try
actions that would normally throw an exception and cause the test to fail.

.. code-block:: php

    $this->spin(function($context) {
        $context->getSession()->getPage()->findById('example')->click();
        return true;
    });

If the #example element isn't available to click yet, the function will throw
an exception, and this will be caught by the try catch block in our spin
method, and tried again in one second.

If no exception is thrown, the method will continue to run through and return
true at the end.

.. note::

    It is important to remember to return true at the end of the function,
    otherwise our spin method will continue to try running the function.

Adding a timeout
----------------

This works well when we just need to wait a while for some action to become
available, but what if things have actually gone wrong? The method would just
sit spinning forever. To resolve this, we can add a timeout.

.. code-block:: php

    public function spin ($lambda, $wait = 60)
    {
        for ($i = 0; $i < $wait; $i++)
        {
            try {
                if ($lambda($this)) {
                    return true;
                }
            } catch (Exception $e) {
                // do nothing
            }
            
            sleep(1);
        }
        
        $backtrace = debug_backtrace();
        
        throw new Exception(
            "Timeout thrown by " . $backtrace[1]['class'] . "::" . $backtrace[1]['function'] . "()\n" .
            $backtrace[1]['file'] . ", line " . $backtrace[1]['line']
        );
    }

Now, if the function still isn't returning true after a minute, we will throw
an exception stating where the test timed out.

Further reading
---------------

* `How to Lose Races and Win at Selenium <http://sauceio.com/index.php/2011/04/how-to-lose-races-and-win-at-selenium/>`