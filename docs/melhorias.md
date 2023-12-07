# Oportunidades de Melhoria

Neste documento, listamos algumas oportunidades de melhorias que vislumbramos.

## Controlar o embaralhamento do DatasetGenerator

A opção de embaralhamento do `generator.DatasetGenerator` (`shuffle = True`) não realiza um controle adequado da semente de aleatoriedade utilizada, isso é, não há garantia de que uma mesma semente será utilizada quando o experimento for repetido no futuro. Esse controle é essencial para garantir a reproducibilidade dos experimentos.

Curiosamente esse controle é corretamente implementado na classe `generators.StratifiedDatasetGenerator`, e pode servir como referência de implementação.

## Refatoração da classe BaseLoader

Cada classe derivada da `arch.BaseLoader` implementa uma transformação diferente na imagem carregada. Além disso, a carga é realizada pela `loaders.SimpleLoader`, da qual todas as outras derivam, dificultando a alteração na forma de carregar as imagens.

Desse modo, as classes derivadas de `arch.BaseLoader` deveriam ser refatoradas, separando-se a carga do arquivo das transformações realizadas, de modo a contemplar, inclusive, o caso do pesquisador precisar combinar essas técnicas.

## Controlar a aleatoriedade na classe RotationLoader

O parâmetro `spread` no da classe [RotationLoader](especificacao_tecnica.md#classe-rotationloadersimpleloader) possui uma influência aleatória no resultado do `augmentation` realizado. Em prol da reproducibilidade dos experimentos, é importante que esse processo aleatório seja controlado por uma semente, devidamente documentada no experimento e preservada no relatório.

## Refatorar a geração de relatórios

Hoje a classe `arch.Experiment` é responsável por muitas coisas. Uma forma relativamente fácil de mitigar esse problema seria refatorar a geração do relatório, extraindo esse código para outras classes, potencialmente permitindo melhor personalização.

## Referência bidirecional entre Base e Hasher

A classe `arch.Hasher` conhece a classe abstrata `arch.Base`, pois precisa saber chamar seu método `add_hash`. Em contrapartida, a classe `arch.Base` conhece a classe `arch.Hasher` por conta da assinatura do método `add_hash`. Isso gera uma referência circular, que é um problema de arquitetura que causa problemas de compilação, definição de módulos, etc.

## Referência bidirecional entre o módulo arch e generators

A classe `arch.Experiment` possui uma referência explícita à classe `generators.DatasetGenerator`, que por sua fez referencia à classe `arch.BaseDatasetGenerator`, criando uma referência bidirecional entre estes módulos. Esse problema é melhor explicado na [Especificação Técnica](especificacao_tecnica.md#arquitetura).

## Implementar suporte à *dataset* de testes

A boa prática do desenvolvimento de redes neurais recomenda que após o treinamento, a rede deve ser avaliada utilizando-se um outro *dataset* diferente do de treinamento e do de validação, a fim de efetivamente avaliar a capacidade de generalização da rede, isso é, sua performance em imagens que nunca foram alimentadas à rede durante o treinamento e que não tiveram nenhuma influência no processo de treinamento.

De modo geral essa implementação deve ser bem fácil diante do que o *framework* já faz, mas talvez seja interessante rever como estamos dividindo os *datasets* nas etapas de pré-processamento. Como hoje estamos dividindo os dados em apenas dois conjuntos, as etapas do tipo `First*` e `Last*` nos bastam. É possível utilizá-las para dividir o *dataset* em três partes, mas é bastante inconveniente.

## Formalizar o papel da classe OneHot

A classe [OneHot](especificacao_tecnica.md#classe-onehotbase) realiza *one-hot encoding* das classes para utilização no treinamento. Esta classe não implementa uma classe básica ou abstrata. Não é trivial fazer isso porque a maneira de codificar classes, ou melhor, as saídas da rede neural, depende do tipo de rede neural que está sendo treinada. Se quisermos estender o *framework* para permitir o treinamento de outros tipos de redes, precisaremos abstrair melhor esse procedimento.