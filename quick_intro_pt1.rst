Construindo Modelo de Domínio
=============================

Bem vindo ao Behat! Behat é uma ferramenta para fechar o laço de comunicação do 
`Desenvolvimento Dirigido por Comportamento-BDD`. BDD é uma metodologia de 
desenvolvimento de software baseado em exemplo por meio da comunicação contínua 
entre desenvolvedores e a área de negócios que esta aplicação suporta. Esta 
comunicação acontece de uma forma que a área de negócios e os desenvolvedores 
podem claramente entender - exemplos. Exemplos são estruturados entorno do padrão
``Contexto-Ação-Resultado`` e são escritos em um formato especial chamado *Gherkin*.
O fato do Guerkin ser muito estrutural torna muito fácil automatizar testes de 
comportamento contra uma aplicação em desenvolvimento. Exemplos 
automatizados são utilizados atualmente para guiar o desenvolvimento de aplicações TDD-style.

Exemplo
-------

Vamos imaginar que você está construindo uma plataforma totalmente nova de e-commerce.
Uma das características fundamentais de qualquer plataforma de compras online é a habilidade
de comprar produtos. Mas antes de comprar algo, os clientes devem poder informar ao sistema
quais produtos eles têm interesse de comprar. Vocẽ precisa de um carrinho de produtos.
Então vamos escrever sua primeira user-story:

.. code-block:: gherkin

    # language: pt
    Funcionalidade: Carrinho de produtos
      A fim de comprar produtos
      Como um cliente
      Eu preciso colocar produtos do meu interesse no carrinho

.. nota::

    Esta é uma feature básica em Gherkin e esta é uma simples descrição 
    desta história. Cada feature inicia com este mesmo formato: uma
    linha com o título da feature, seguida por três linhas que descrevem
    os benefícios, o papel e o próprio recurso com qualquer quantidade de 
    linhas de descrição adicionais seguem depois.

Antes de nós começarmos a trabalhar nesta feature, nós precisamos preencher 
uma promessa de user-story e ter uma conversa de verdade com nossos stakeholders 
da área de negócios. Eles podem dizer que eles querem que os clientes vejam 
o preço combinado do produto no carrinho, mas que o preço reflita o imposto (20%) 
e o valor do frete (que depende da soma total dos produtos):

.. code-block:: gherkin

    # language: pt
    Funcionalidade: Carrinho de produtos
      A fim de comprar produtos
      Como um cliente
      Eu preciso colocar produtos do meu interesse no carrinho

      Regras:
      - O imposto é de 20%
      - O frete para um carrinho de compras até R$10 é R$3
      - O frete para um carrinho de compras maior que R$10 é R$2

Então como você pode ver, está ficando complicado (ambíguo, pelo menos)
falar sobre está feature, em termos de *regras*. O que você entende por 
adicionar imposto? O que acontece quando nós tivermos dois produtos, 
um com valor menor que R$10 e outro de maior valor? Ao invés de você
prosseguir em ter um leva e traz de conversas entre os stakeholders na forma
dos exemplos atuais de um *cliente* adicionando produtos ao carrinho. Depois
de algum tempo, você vai levantar seus primeiros exemplos de comportamentos (no BDD 
isto é chamado de *Cenários*):

.. code-block:: gherkin

    # language: pt
    Funcionalidade: Carrinho de produtos
      A fim de comprar produtos
      Como um cliente
      Eu preciso colocar produtos do meu interesse no carrinho

      Regras:
      - O imposto é de 20%
      - O frete para um carrinho de compras até R$10 é R$3
      - O frete para um carrinho de compras maior que R$10 é R$2

      Cenário: Comprando um único produto que custe menos que R$10
        Dado que exista um "Sabre de luz do Lorde Sith", que custe R$5
        Quando Eu adicionar o "Sabre de luz do Lorde Sith" ao carrinho
        Então Eu devo ter 1 produto no carrinho
        E o valor total do carrinho deve ser de R$9

      Cenário: Comprando um único produto que custe mais que R$10
        Dado que exista um "Sabre de luz do Lorde Sith", que custe R$15
        Quando Eu adicionar o "Sabre de luz do Lorde Sith" ao carrinho
        Então Eu devo ter 1 produto no carrinho
        E o valor total do carrinho deve ser de R$20

      Cenário: Comprando dois produtos que custem mais que R$10
        Dado que exista um "Sabre de luz do Lorde Sith", que custe R$10
        E que exista um "Sabre de luz Jedi", que custe R$5
        Quando Eu adicionar o "Sabre de luz do Lorde Sith" ao carrinho
        E Eu adicionar o "Sabre de luz Jedi" ao carrinho
        Então Eu devo ter 2 products no carrinho
        E o valor total do carrinho deve ser de R$20

.. nota::

    Cada cenário sempre segue o mesmo formato básico:

    .. code-block:: gherkin

        Cenário: Alguma descrição do cenário
          Dado algum contexto
          Quando algum evento
          Então resultado

    Cada parte do cenário - o *contexto*, o *evento*,  e o
    *resultado* - pode ser extendido pelo adicional da palavra chave ``E`` 
    ou ``Mas``:

    .. code-block:: gherkin

        Cenário: Alguma descrição do cenário
          Dado algum contexto
          E mais outro contexto
          Quando algum evento
          E um segundo evento ocorra
          Então o resultado
          E outro resultado
          Mas outro resultado

    Não há uma real diferença entre ``Então``, ``E`` ``Mas`` ou qualquer 
    outra palavra que inicie cada linha. Estas palavras chave são 
    disponibilizadas para que os cenários sejam naturais e legíveis.
    
Isto é seu e seus stakeholders compartilham da mesma escrita em um formato 
estruturado do projeto. Tudo é baseado na clara e construtiva conversa que 
vocês tiveram juntos. Agora você pode colocar este texto em um arquivo 
simples - ``features/carrinho.feature`` - dentro do diretório do seu projeto e 
começar a implementar a funcionalidade checando manualmente se se encaixa no 
cenário definido. Não é necessário nenhuma ferramenta (Behat em seu caso). 
Isto é, na essência, o que o BDD é.

Se você ainda está lendo,  significa que você ainda espera mais. Ótimo! 
Porque  apesar das ferramentas não serem a peça central do quebra-cabeça do BDD, 
elas melhoram todo o processo e adicionam muitos benefícios ao topo disto.
Para isso, ferramentas como o Behat atualmente fecham o ciclo de comunicação da história.
Isto significa que não somente você e seu stakeholder podem juntos definir como sua 
feature deveria trabalhar após ser implementada, ferramentas de BDD permitem a você
automatizar a checagem do comportamento após a funcionalidade ser implementada. Então
todo mundo sabe quando isto está feito e quando o time pode parar de escrever código.
Isto, na essência, é oque o Behat é.

*Behat é um executável que quando você o executa da linha de comando ele irá testar como 
a sua aplicação se comporta exatamente como você descreveu nos seus ``*.feature`` cenários.*

Indo adiante, nós vamos mostrar a você como o Behat pode ser usado para automatizar em 
particular esta feature do carrinho de compras como um teste verificando se aquela 
aplicação (existindo ou não) trabalha como você e seus stakeholders esperam (de acordo 
com a conversa de vocês) também.

É isso ai! O Behat pode ser usado para automatizar qualquer coisa, inclusive relacionadas a
funcionalidades web via `Mink`_ library.

.. nota::

    Se você quer aprender mais sobre a filosofia do "Desenvolvimento 
    Dirigido por comportamento" sobre a sua aplicação, veja `What's in a Story?`_

.. nota::

    Behat estava profundamente inspirado pelo projeto em Ruby `Cucumber`_. Desde a v3.0,
    Behat é considerado uma implementação oficial do Cucumber em PHP e faz parte da grande
    família de ferramentas BDD.

Instalação
----------

Antes de você começar, garanta que você tem uma versão superior a 5.3.3 do PHP instalada.

Método #1 - Composer (o recomendado)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

O caminho oficial para instalar o Behat é através do Composer. Composer é um
gerenciador de pacotes para PHP. Ele não irá lhe ser útil somente para instalar o Behat para 
você agora, ele será capaz de atualizar facilmente para a última versão mais tarde, quando 
for lançada. Se você ainda não tem o Composer, veja `a documentação do Composer <https://getcomposer.org/download/>`_ 
para instruções. Depois disto, basta ir ao diretório do projeto (ou criar um novo) e rodar:

.. code-block:: bash

    $ php composer.phar require --dev behat/behat=~3.0.4

Então vocẽ estará apto a checar a versão instalada do Behat:

.. code-block:: bash

    $ vendor/bin/behat -V
    
Método #2 - PHAR (um caminho fácil)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Um caminho fácil para instalar o Behat é pegar a última ``behat.phar`` na 
`página de download <https://github.com/Behat/Behat/releases>`_. Certifique-se
de fazer o download de uma versão ``3+``. Depois de baixar isto, basta colocá-lo 
no diretório do seu projeto (ou criar um novo) e checar a versão instalada usando:

.. code-block:: bash

    $ php behat.phar -V

Desenvolvendo
-------------

Agora nós vamos usar nosso recém instalado Behat para automatizar a feature escrita 
anteriormente em ``features/carrinho.feature``.

Nosso primeiro passo após descrever a feature e instalar o Behat é configurar a suite 
de teste. Uma suite de teste é um conceito chave em Behat. Suites são uma forma do Behat 
saber onde achar e como testar sua aplicação com as suas features.
Por padrão, Behat vem com uma suite ``default``, que diz ao Behat para procurar por 
features no diretório ``features/`` e os teste usando a classe ``FeatureContext``.
Vamos inicializar esta suite:

.. code-block:: bash

    $ vendor/bin/behat --init

.. nota::

    Se você instalou o Behat via PHAR, use ``php behat.phar`` ao invés de
    ``vendor/bin/behat`` no resto deste artigo.

O comando ``--init`` diz ao Behat para prover para você com coisas faltando 
para começar a testar sua feature. Em nosso caso - é apenas uma classe ``FeatureContext`` 
no arquivo ``features/bootstrap/FeatureContext.php``.

Executando o Behat
~~~~~~~~~~~~~~~~~~

Eu acho que nós estamos prontos para ver o Behat em ação! Vamos rodar isto:

.. code-block:: bash

    $ vendor/bin/behat

Vocẽ deve ver que o Behat reconheceu que você tem 3 cenários. o Behat deve também
contar a você que na sua classe ``FeatureContext`` faltam passos e propor trechos 
para etapas para você. ``FeatureContext`` é seu ambiente de teste. É um objeto 
através do qual você descreve como você deve testar sua aplicação através de suas 
features. Isso foi gerado através do comando ``--init`` e agora se parece com isso:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Context\SnippetAcceptingContext;
    use Behat\Gherkin\Node\PyStringNode;
    use Behat\Gherkin\Node\TableNode;

    class FeatureContext implements SnippetAcceptingContext
    {
        /**
         * Initializes context.
         */
        public function __construct()
        {
        }
    }

Definindo Steps
~~~~~~~~~~~~~~~

Finalmente, nós chegamos a parte de automação. Como é que o Behat sabe o que fazer 
quando vê  ``Dado que exista um "Sabre de luz do Lorde Sith", que custe R$5``? 
Diga a ele. Você escreve em PHP dentro da sua classe de contexto (``FeatureContext`` 
no seu caso) e diz ao Behat que este código representa um passo específico do cenário 
(através de uma anotação com um padrão):

.. code-block:: php

    /**
     * @Given que exista um :arg1, que custe R$:arg2
     */
    public function queExistaUmQueCusteR($arg1, $arg2)
    {
        throw new PendingException();
    }


.. nota::

    ``/** ... */`` é uma sintaxe especial em PHP chamada de doc-block.
    Isto é detectável em tempo de execução e usado por diferentes frameworks 
    de PHP como um caminho para prover meta-informação adicionais para as 
    classes, métodos e funções. Behat usa doc-blocks para step definitions, 
    step transformations e hooks.

``@Given que exista um :arg1, que custe R$:arg2`` sobre o método diz ao Behat
que este método em particular deve ser executado sempre que o Behat ver um step 
que se pareça com ``... que exista um ..., que custe R$...``. Este padrão 
combina qualquer um dos seguintes steps:

.. code-block:: gherkin

    Dado que exista um "Sabre de luz do Lorde Sith", que custe R$5
    Quando que exista um "Sabre de luz do Lorde Sith", que custe R$10
    Então que exista um "Sabre de luz do Anakin", que custe R$10
    E que exista um "Sabre de luz", que custe R$2
    Mas que exista um "Sabre de luz", que custe R$25

Não somente estes, mas o Behat irá capturar tokens (palavras iniciadas com ``:``, 
por exemplo ``:arg1``) a partir do step e passar seu valor para o método como argumentos:

.. code-block:: php

    // Dado que exista um "Sabre de luz do Lorde Sith", que custe R$5
    $context->queExistaUmQueCusteR('Sabre de luz do Lorde Sith', '5');

    // Então que exista um "Sabre de luz Jedi", que custe R$10
    $context->queExistaUmQueCusteR('Sabre de luz Jedi', '10');

    // Mas que exista um "Sabre de luz", que custe R$25
    $context->queExistaUmQueCusteR('Sabre de luz', '25');

.. nota::

    Se você precisa definir algoritmos de correspondência mais complexos, 
    você também pode usar expressões regulares:

    .. code-block:: php

        /**
         * @Given /que exista um? \"([^\"]+)\", que custe R$([\d\.]+)/
         */
        public function queExistaUmQueCusteR($arg1, $arg2)
        {
            throw new PendingException();
        }

Estes padrões podem ser muito poderosos, mas ao mesmo tempo, escreve-los por todos steps 
possíveis manualmente pode ser extremamente tedioso e chato. É por isso que o Behat faz
isto para você. Relembre quando você executou anteriormente ``vendor/bin/behat`` você teve:

.. code-block:: text

    --- FeatureContext has missing steps. Define them with these snippets:

        /**
         * @Given que exista um :arg1, que custe R$:arg2
         */
        public function queExistaUmQueCusteR($arg1, $arg2)
        {
            throw new PendingException();
        }

O Behat gera automaticamente trechos para etapas que faltam e tudo que você precisa 
para os copiar e colar em sua classe context. Ou há ainda um caminho mais fácil - pasta rodar:

.. code-block:: bash

    $ vendor/bin/behat --dry-run --append-snippets

E o Behat vai automaticamente acrescentar todos os métodos das etapas que faltam em
sua classe ``FeatureContext``. Como isso é legal?

Se vocẽ executou `--append-snippets``, sua ``FeatureContext`` deve se parecer com:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Tester\Exception\PendingException;
    use Behat\Behat\Context\SnippetAcceptingContext;
    use Behat\Gherkin\Node\PyStringNode;
    use Behat\Gherkin\Node\TableNode;

    class FeatureContext implements SnippetAcceptingContext
    {
        /**
         * @Given que exista um :arg1, que custe R$:arg2
         */
        public function queExistaUmQueCusteR($arg1, $arg2)
        {
            throw new PendingException();
        }

        /**
         * @When Eu adicionar o :arg1 ao carrinho
         */
        public function euAdicionarOAoCarrinho($arg1)
        {
            throw new PendingException();
        }

        /**
         * @Then Eu devo ter :arg1 produto(s) no carrinho
         */
        public function euDevoTerProdutoNoCarrinho($arg1)
        {
            throw new PendingException();
        }

        /**
         * @Then o valor total do carrinho deve ser de R$:arg1
         */
        public function oValorTotalDoCarrinhoDeveSerDeR($arg1)
        {
            throw new PendingException();
        }
    }

.. nota::

    Nós removemos o construtor e agrupamos ``Eu devo ter :arg1 produto no carrinho`` e
    ``Eu devo ter :arg1 produtos no carrinho`` em um ``Eu devo ter :arg1 produto(s) no carrinho``

Automating Steps
~~~~~~~~~~~~~~~~

Agora finalmente é o tempo de começar a implementar nossa feature do carrinho de compras.
A abordagem quando você usa testes para dirigir o desenvolvimento da sua aplicação é chamada 
de Test-Driven Development (ou simplesmente TDD). Com o TDD você inicia definindo casos de 
testes para a funcionalidade que você vai desenvolver, em seguida você preenche estes casos 
de teste com o melhor código da aplicação que você poderia chegar (use suas habilidades 
de design e imaginação).

No caso do Behat, você já tem casos de teste definidos (step definitions em sua ``FeatureContext``) 
e a unica coisa que está faltando é o melhor código da aplicação que poderíamos chegar para cumprir 
o nosso cenário. Algo assim:

.. code-block:: php

    // features/bootstrap/FeatureContext.php

    use Behat\Behat\Tester\Exception\PendingException;
    use Behat\Behat\Context\SnippetAcceptingContext;
    use Behat\Gherkin\Node\PyStringNode;
    use Behat\Gherkin\Node\TableNode;

    class FeatureContext implements SnippetAcceptingContext
    {
        private $prateleira;
        private $carrinho;

        public function __construct()
        {
            $this->prateleira = new Prateleira();
            $this->carrinho = new Carrinho($this->prateleira);
        }

        /**
         * @Given que exista um :produto, que custe R$:valor
         */
        public function queExistaUmQueCuste($produto, $valor)
        {
            $this->prateleira->colocaValorProduto($produto, floatval($valor));
        }

        /**
         * @When Eu adicionar o :produto ao carrinho
         */
        public function euAdicionarOAoCarrinho($produto)
        {
            $this->carrinho->adicionaProduto($produto);
        }

        /**
         * @Then Eu devo ter :quantidade produto(s) no carrinho
         */
        public function euDevoTerProdutoNoCarrinho($quantidade)
        {
            PHPUnit_Framework_Assert::assertCount(
                intval($quantidade),
                $this->carrinho
            );
        }

        /**
         * @Then o valor total do carrinho deve ser de R$:valor
         */
        public function oValorTotalDoCarrinhoDeveSerDeR($valor)
        {
            PHPUnit_Framework_Assert::assertSame(
                floatval($valor),
                $this->carrinho->pegaValorTotal()
            );
        }
    }

Como você pode ver, afim de implementar e testar nossa aplicação, nós introduzimos 2 objetos - 
``Prateleira`` and ``Carrinho``. O primeiro responsavel por armazenar produtos e seus preços, 
o segundo é responsável pela representação do carrinho do nosso cliente. Através do step definitions
apropriado nós declaramos produtos' preços e adicionamos ao carrinho. Nós então comparamos o estado 
de nosso objeto ``Carrinho`` com a nossa expectativa usando asserções do PHPUnit.

.. nota::

    O Behat não vem com uma ferramenta própria de asserção, mas você pode usar qualquer 
    outra ferramenta correta de asserção. Uma ferramenta de asserção correta é uma biblioteca 
    cujas afirmações lançam excessões em caso de falha. Por exemplo, se você está familiarizado 
    com o PHPUnit você pode usar as asserções dele no Behat instalando via composer:

    .. code-block:: bash

        $ php composer.phar require --dev phpunit/phpunit='~4.1.0'

    E então simplesmente usar as asserções em seus steps:

    .. code-block:: php

        PHPUnit_Framework_Assert::assertCount(
            intval($count),
            $this->carrinho
        );

Agora vamos tentar executar seu teste funcional:

.. code-block:: bash

    $ vendor/bin/behat

Você deve ver o início da feature e em seguida um erro dizendo que a classe 
``Prateleira`` não existe. Isso significa que estamos prontos para começar a 
efetivamente escrever código da aplicação!

Implementando a Feature
~~~~~~~~~~~~~~~~~~~~~~~

Então agora nós temos 2 coisas muito importantes:

1. Uma concreta descrição da funcionalidade que estamos tentando entregar.
2. Ao falhar, o teste nos diz o que fazer a seguir.

Agora a parte mais fácil do desenvolvimento da aplicação - implementação da feature.
Sim, com TDD e BDD a implementação se torna uma rotina, devido você já ter a maioria 
do trabalho nas fases anteriores - você escreveu os testes, vocẽ veio com uma solução
elegante (tanto quanto você poderia dar no contexto atual) e você escolhe os atores (objetos) 
e ações (métodos) que estão envolvidos. Agora é a hora de escrever um punhado de palavras 
chave em PHP para colar tudo junto. Ferramentas como o Behat, quando usadas da forma correta, 
vão ajudar vocẽ a escrever esta fase, lhe dando um simples conjunto de instruções que você
precisa para seguir. Você fez seu pensamento e projeto,agora está na hora de sentar, rodar 
a ferramenta e seguir as instruções na ordem para escrever seu código de produção.

Vamos começar! Rode:

.. code-block:: bash

    $ vendor/bin/behat

O Behat vai tentar testar a sua aplicação com o ``FeatureContext`` mas vai falhar 
logo, exibindo algum evento como este em sua tela:

.. code-block:: text

    Fatal error: Class 'Prateleira' not found

Agora nosso trabalho é reinterpretar esta frase em uma instrução executável. Como 
"Criar a classe ``Prateleira``". Vamos criar isto em ``features/bootstrap``:

.. code-block:: php

    // features/bootstrap/Shelf.php

    final class Prateleira
    {
    }

.. nota::

    Nós colocamos a classe ``Prateleira`` em ``features/bootstrap/Prateleira.php`` pois 
    ``features/bootstrap`` é um diretório de carregamento automático para o Behat. O Behat
    tem um carregador automário em PSR-0, que olha para ``features/bootstrap``. Se você
    está desenvolvendo sua própria aplicação, vocẽ provavelmente vai precisar colocar 
    classes dentro da pasta apropriada para a sua aplicação.

Vamos executar o Behat novamente:

.. code-block:: bash

    $ vendor/bin/behat

Nós vamos ter uma mensagem diferente em nossa tela:

.. code-block:: text

    Fatal error: Class 'Carrinho' not found

Ótimo, nós estamos progredindo! Reinterpretando a mensagem como "Criar a classe ``Carrinho``".
Vamos seguir nossa nova instrução:

.. code-block:: php

    // features/bootstrap/Carrinho.php

    final class Carrinho
    {
    }

Rode o Behat novamente:

.. code-block:: bash

    $> vendor/bin/behat

Maravilha! Outra "instrução":

.. code-block:: text

    Call to undefined method Prateleira::colocaValorProduto()

Seguindo estas instruções passo-a-passo você vai terminar com uma classe ``Prateleira`` 
parecida com esta:

.. code-block:: php

    // features/bootstrap/Prateleira.php

    final class Prateleira
    {
        private $valores = array();

        public function colocaValorProduto($produto, $valor)
        {
            $this->valores[$produto] = $valor;
        }

        public function pegaValorProduto($produto)
        {
            return $this->valores[$produto];
        }
    }

E uma classe ``Carrinho`` parecida com esta:

.. code-block:: php

    // features/bootstrap/Carrinho.php

    final class Carrinho implements \Countable
    {
        private $prateleira;
        private $produtos;
        private $valoresProdutos = 0.0;

        public function __construct(Prateleira $prateleira)
        {
            $this->prateleira = $prateleira;
        }

        public function adicionaProduto($produto)
        {
            $this->produtos[] = $produto;
            $this->valoresProdutos += $this->prateleira->pegaValorProduto($produto);
        }

        public function pegaValorTotal()
        {
            return $this->valoresProdutos
                + ($this->valoresProdutos * 0.2)
                + ($this->valoresProdutos > 10 ? 2.0 : 3.0);
        }

        public function contador()
        {
            return contador($this->produtos);
        }
    }

Execute o Behat novamente:

.. code-block:: bash

    $ vendor/bin/behat

Todos os cenários devem passar agora! Parabéns, você quase terminou a sua primeira feature. 
O último passo é *refatorar*. Olhe para as classes ``Carrinho`` e ``Prateleira`` e tente 
achar um caminho para fazer um código mais limpo, fácil de ler e conciso.

.. dica::
    
    Eu recomendaria iniciar pelo método ``Carrinho::pegarValorTotal()`` e
    extrair o calculo do imposto e do frete para métodos privados.

Depois da refatoração pronta, vocẽ terá:

#. Um código óbvio e claramente concebido que faz exatamente o que deveria fazer 
   sem funcionalidades que não foram solicitadas pelos usuários.

#. Um conjunto de testes de regressão que irá ajudá-lo a ter confiança em seu código daqui para frente.

#. Uma documentação viva do comportaento do seu código, 

#. Documentação viva do comportamento do seu código que vai viver, evoluir e morrer em conjunto com o seu código.

#. Um incrível nível de confiança em seu código. Não só você está confiante agora que ele faz exatamente o que é 
   suposto fazer, você está confiante de que ele faz isso por entregar valor para os usuários finais (clientes, 
   no nosso caso).

Existem muitos outros beneficios no BDD, mas estes são as razões chaves porque 
a maioria dos praticantes de BDD fazem BDD em Ruby, .Net, Java, Python e JS.
Bem vindo a família!

What's Next?
------------

Parabéns! Você agora conhece tudo o que precisa para começar com o desenvolvimento
dirigido por testes e Behat. Daqui, vocẽ pode aprender mais sobre a sintaxe :doc: `Gherkin </guides/1.gherkin>`
ou aprender como testar suas aplicações web usando Behat com Mink.

.. _`Behavior Driven Development`: https://pt.wikipedia.org/wiki/Behavior_Driven_Development
.. _`Mink`: https://github.com/behat/mink
.. _`What's in a Story?`: http://blog.dannorth.net/whats-in-a-story/
.. _`Cucumber`: http://cukes.info/
.. _`Goutte`: https://github.com/fabpot/goutte
.. _`PHPUnit`: http://phpunit.de
.. _`Testando Aplicações Web com Mink`: https://github.com/behat/mink
