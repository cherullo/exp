# Oportunidades de Melhoria

Neste documento, listamos algumas oportunidades de melhorias que vislumbramos.

## Controlar o embaralhamento do DatasetGenerator

A opção de embaralhamento do `generator.DatasetGenerator` (`shuffle = True`) não realiza um controle adequado da semente de aleatoriedade utilizada, isso é, não há garantia de que uma mesma semente será utilizada quando o experimento for repetido no futuro. Esse controle é essencial para garantir a reproducibilidade dos experimentos.

Curiosamente esse controle é corretamente implementado na classe `generators.StratifiedDatasetGenerator`, e pode servir como referência de implementação.

## Refatoração da classe BaseLoader

Cada classe derivada da `arch.BaseLoader` implementa uma transformação diferente na imagem carregada. Além disso, a carga é realizada pela `loaders.SimpleLoader`, da qual todas as outras derivam, dificultando a alteração na forma de carregar as imagens.

Desse modo, as classes derivadas de `arch.BaseLoader` deveriam ser refatoradas, separando-se a carga do arquivo das transformações realizadas, de modo a contemplar, inclusive, o caso do pesquisador precisar combinar essas técnicas.

## Refatorar a geração de relatórios

Hoje a classe `arch.Experiment` é responsável por muitas coisas. Uma forma relativamente fácil de mitigar esse problema seria refatorar a geração do relatório, extraindo esse código para outras classes, potencialmente permitindo melhor personalização.

## Criar exemplo de treinamento desbalanceado

A documentação descreve como o framework serve para o treinamento com *datasets* desbalanceados. Seria interessante criar um experimento de exemplo contemplando esse caso.

## Referência bidirecional entre Base e Hasher

A classe `arch.Hasher` conhece a classe abstrata `arch.Base`, pois precisa saber chamar seu método `add_hash`. Em contrapartida, a classe `arch.Base` conhece a classe `arch.Hasher` por conta da assinatura do método `add_hash`. Isso gera uma referência circular, que é um problema de arquitetura que causa problemas de compilação, definição de módulos, etc.

## Referência bidirecional entre o módulo arch e generators

A classe `arch.Experiment` possui uma referência explícita à classe `generators.DatasetGenerator`, que por sua fez referencia à classe `arch.BaseDatasetGenerator`, criando uma referência bidirecional entre estes módulos. Esse problema é melhor explicado na [Especificação Técnica](especificacao_tecnica.md#arquitetura).