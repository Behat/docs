Acessando contexto de outro
===========================

Quando dividimos as definições em múltiplos contextos, pode ser útil acessar 
um contexto de um outro. Isto é particularmente útil ao migrar do Behat 2.x 
para substituir sub contextos.

O Behat permite acessar o ambiente em :doc:`hooks </guides/3.hooks>`, 
então outros contextos podem ser recuperados utilizando a hook ``BeforeScenario``:

.. code-block:: php

    use Behat\Behat\Context\Context;
    use Behat\Behat\Hook\Scope\BeforeScenarioScope;

    class FeatureContext implements Context
    {
        /** @var \Behat\MinkExtension\Context\MinkContext */
        private $minkContext;

        /** @BeforeScenario */
        public function reunirContextos(BeforeScenarioScope $scope)
        {
            $environment = $scope->getEnvironment();

            $this->minkContext = $environment->getContext('Behat\MinkExtension\Context\MinkContext');
        }
    }

.. caution::

    Referências circulares em objetos de contexto impediriam a referência PHP 
    contagem da recolha de contextos até o fim de cada cenário, forçando a 
    aguardar o garbage colleector ser executado. Isso aumentaria o uso de 
    memória utilizada pela execução do Behat. Para previnir isto, é melhor 
    evitar o armazenamento do ambiente em suas classes de contexto. Também 
    é melhor evitar a criação de referências circulares entre diferentes 
    contextos.
