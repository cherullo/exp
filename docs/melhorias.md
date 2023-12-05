# Melhorias

Neste documento, listamos algumas oportunidades de melhorias que vislumbramos.

## Controlar o embaralhamento do DatasetGenerator

A opção de embaralhamento do `DatasetGenerator` (`shuffle = True`) não realiza um controle adequado da semente de aleatoriedade utilizada, isso é, não há garantia de que uma mesma semente será utilizada quando o experimento for repetido no futuro. Esse controle é essencial para garantir a reproducibilidade dos experimentos.

Curiosamente esse controle é corretamente implementado na classe `StratifiedDatasetGenerator`, e pode servir como referência de implementação.

## Refatoração da classe BaseLoader

Cada classe derivada da `BaseLoader` implementa uma transformação diferente na imagem carregada. Além disso, a carga é realizada pela própria `BaseLoader`, dificultando a alteração na forma de carregar as imagens.

Desse modo, as classes derivadas de `BaseLoader` deveriam ser refatoradas, separando-se a carga do arquivo das transformações realizadas, de modo a contemplar, inclusive, o caso do pesquisador precisar combinar essas técnicas.

## Refatorar a geração de relatórios

Hoje a classe `Experiment` é responsável por muitas coisas. Uma forma relativamente fácil de mitigar esse problema seria refatorar a geração do relatório, extraindo esse código para outras classes, potencialmente permitindo melhor personalização.

## Criar exemplo de treinamento desbalanceado

A documentação descreve como o framework serve para o treinamento com *datasets* desbalanceados. Seria interessante criar um experimento de exemplo contemplando esse caso.