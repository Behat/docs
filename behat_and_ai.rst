Behat and AI
============

AI coding agents can generate and modify code based on behavioural descriptions.
Behat provides a reliable way to define, verify, and preserve behaviour in these workflows.

By expressing behaviour as executable scenarios, Behat ensures that AI-generated code
satisfies a clear and objective contract.

Using Behat as a Behavioural Contract
-------------------------------------

Behat scenarios define observable behaviour in a precise and executable form:

.. code-block:: gherkin

   Feature: Refund processing

     Scenario: Refunding a paid order
       Given there is a paid order
       When I refund the order
       Then the order should be marked as refunded

     Scenario: Prevent duplicate refunds
       Given an order has already been refunded
       When I refund the order
       Then the refund should be rejected

AI agents can implement features and use Behat to verify that the expected behaviour is satisfied.
When scenarios pass, the behavioural contract is fulfilled.

Executable and Verifiable Behaviour
-----------------------------------

Behat scenarios serve as executable specifications. They can be used by AI agents to:

* verify correctness after implementing a feature
* detect behavioural regressions
* ensure behaviour remains consistent during refactoring

Because scenarios are executable, they remain accurate as the system evolves.

Generating Scenarios with AI
----------------------------

AI agents can generate Behat scenarios from behavioural descriptions.
These scenarios can then be reviewed, refined, and executed.

This allows behaviour to be defined before or alongside implementation.

Behat provides a structured and executable representation of behaviour
that can be used directly by AI tooling.

Human Review and Iteration
--------------------------

As with any specification or testing tool, generated scenarios and assertions should be reviewed carefully.
It is critical to ensure that both the human-readable scenarios and the executable step definitions
accurately represent the intended behaviour. They also need to be robust enough to prove that
the actual behaviour matches the expectations, even if the implementation changes.

Once validated, scenarios serve as the authoritative definition of the feature. AI agents can implement
or modify the system until all scenarios pass.

This creates a reliable feedback loop where behaviour is defined, verified, and preserved.

Maintaining Behaviour Over Time
-------------------------------

With well-designed scenarios and step definitions, Behat ensures that behaviour remains stable as code changes.
AI agents can safely modify or refactor code, and Behat will detect any unintended behavioural changes.

As long as scenarios pass, the defined behaviour is preserved.

Behat MCP Server
----------------

Behat provides an `MCP (Model Context Protocol) server`_ that allows AI agents to interact
directly with Behat projects.

The MCP server enables agents to discover scenarios, execute Behat,
and integrate behavioural verification into automated workflows.

.. _`MCP (Model Context Protocol) server`: https://github.com/Behat/mcp-server
