Step Argument Transformations
=============================

Step argument transformations allow you to abstract common operations performed
on step definition arguments into reusable methods. In addition, these methods
can be used to transform a normal string argument that was going to be used
as an argument to a step definition method, into a more specific data type
or an object.

Each transformation method must return a new value. This value then replaces
the original string value that was going to be used as an argument to a step
definition method.

Transformation methods are defined using the same attribute style as step
definition methods, but instead use the ``Transform`` attribute with
a matching pattern as argument.

As a basic example, you can automatically cast all numeric arguments to
integers with the following context class code:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;
    use Behat\Step\Then;
    use Behat\Transformation\Transform;

    class FeatureContext implements Context
    {
        #[Transform('/^(\d+)$/')]
        public function castStringToNumber(string $string): int
        {
            return intval($string);
        }

        #[Then('a user :name, should have :count followers')]
        public function checkFollowers($name, $count): void
        {
            if ('integer' !== gettype($count)) {
                throw new Exception('Integer expected');
            }
        }
    }

.. note::

    In the same way as with step definitions, you can use both simple patterns and
    regular expressions.

Let's go a step further and create a transformation method that takes an
incoming string argument and returns a specific object. In the following
example, our transformation method will be passed a username, and the method
will create and return a new ``User`` object:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;
    use Behat\Step\Then;
    use Behat\Transformation\Transform;

    class FeatureContext implements Context
    {
        #[Transform(':user')]
        public function castUsernameToUser($user): User
        {
            return new User($user);
        }

        #[Then('a :user, should have :count followers')]
        public function checkFollowers(User $user, $count): void
        {
            if ('integer' !== gettype($count)) {
                throw new Exception('Integer expected');
            }
        }
    }

Table Transformation
~~~~~~~~~~~~~~~~~~~~

Let's pretend we have written the following feature:

.. code-block:: gherkin

    # features/table.feature
    Feature: Users

      Scenario: Creating Users
        Given the following users:
          | name          | followers |
          | everzet       | 147       |
          | avalanche123  | 142       |
          | kriswallsmith | 274       |
          | fabpot        | 962       |

And our ``FeatureContext`` class looks like this:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;
    use Behat\Gherkin\Node\TableNode;
    use Behat\Step\Given;

    class FeatureContext implements Context
    {
        #[Given('the following users:')]
        public function pushUsers(TableNode $usersTable): void
        {
            $users = array();
            foreach ($usersTable as $userHash) {
                $user = new User();
                $user->setUsername($userHash['name']);
                $user->setFollowersCount($userHash['followers']);
                $users[] = $user;
            }

            // do something with $users
        }
    }

Instead of having to transform the data in the step definition, we can define a transformation that transforms a whole
table. A table transformation is matched via the prefix ``table:`` followed by the list of table headers:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\Context;
    use Behat\Gherkin\Node\TableNode;
    use Behat\Step\Given;
    use Behat\Step\Then;
    use Behat\Transformation\Transform;

    class FeatureContext implements Context
    {
        #[Transform('table:name,followers')]
        public function castUsers(TableNode $usersTable): array
        {
            $users = array();
            foreach ($usersTable->getHash() as $userHash) {
                $user = new User();
                $user->setUsername($userHash['name']);
                $user->setFollowersCount($userHash['followers']);
                $users[] = $user;
            }

            return $users;
        }

        #[Given('the following users:')]
        public function pushUsers(array $users): void
        {
            // do something with $users
        }

        #[Then('I expect the following users:')]
        public function assertUsers(array $users): void
        {
            // do something with $users
        }
    }

The function that performs the transformation receives as an argument a ``TableNode`` with the table data and it should
return an array with one or more transformed values (one for each row in the table).

You can also transform each row individually instead of transforming the table as a whole. In this case you should use
the ``row:`` prefix followed by a list of column headers:

.. code-block:: php

        #[Transform('row:name,followers')]
        public function castUserRow(array $row): User
        {
            $user = new User();
            $user->setUsername($row['name']);
            $user->setFollowersCount($row['followers']);
            return $user;
        }

In this case, the function that performs the transformation receives as an argument an array with the data for each
individual row and should return the transformed value.

If you prefer, you can pass the data in columns instead of rows, for example with this feature file:

.. code-block:: gherkin

    # features/row-table.feature
    Feature: Users

      Scenario: Creating Users
        Given the following users:
          | name      | everzet | avalanche123 | kriswallsmith |
          | followers | 147     | 142          | 274           |

You should then modify your transformation function to use the ``rowtable:`` prefix with a list of row headers:

.. code-block:: php

        #[Transform('rowtable:name,followers')]
        public function castUsersTable(TableNode $usersTable)
        {
            $users = array();
            foreach ($usersTable->getRowsHash() as $userHash) {
                $user = new User();
                $user->setUsername($userHash['name']);
                $user->setFollowersCount($userHash['followers']);
                $users[] = $user;
            }

            return $users;
        }

Again the function that performs the transformation receives as an argument a ``TableNode`` with the table data and it
should return an array with one or more transformed values (one for each column in the table). Notice that we are
using ``getRowsHash()`` instead of ``getHash()`` to get the data from the table.

One final possibility is to transform one or more columns in a table into a different value. For example you might
have this feature:

.. code-block:: gherkin

    # features/table-column.feature
    Feature: Users

      Scenario: Assigning followers to users
        When I assign this number of followers to users:
          | user          | followers |
          | everzet       | 147       |
          | avalanche123  | 142       |
          | kriswallsmith | 274       |
          | fabpot        | 962       |

In your transformation you should use the ``column:`` prefix with a list of the column names that can be matched:

.. code-block:: php

        #[Transform('column:user')]
        public function castUserName(string $name): User
        {
            $user = new User();
            $user->setUsername($name);
            return $user;
        }

        #[Given('I assign this number of followers to users:')]
        public function assignFollowers(array $data): void
        {
            foreach ($data as $row) {
                $user = $row['user'];
                $user->setFollowersCount($row['followers']);
            }
        }

As you can see, the transformation function receives a string with the value of the corresponding column in each row
and should return a transformed value. This is used to build an array where the corresponding columns will have the
transformed values and this is what is passed to the step definition.

.. note::

    Transformations are powerful and it is important to take care how you
    implement them. A mistake can often introduce strange and unexpected
    behavior. Also, they are inherently hard to debug because of their
    highly dynamic nature.
