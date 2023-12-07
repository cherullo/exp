# Especificação Técnica

O *framework* exp é desenvolvido em Python, seguindo uma abordagem orientada a objetos. Foi feito um esforço para que todas os parâmetros de todos os métodos fossem devidamente anotados com seus respectivos tipos, gerando, assim, dependência explícita entre as classes e os módulos do framework.

Neste documento iremos descrever como o código do *framework* exp é organizado, seus módulos e classes, com as seguintes exceções:
- Por uma questão de brevidade, documentaremos aqui apenas as classes públicas dos módulos. 
- O diretório [`src/exp/helpers`](../src/exp/helpers/) contém arquivos auxiliares que não compõe um módulo do framework.
- O diretório [`src/examples`](../src/examples/) contém os exemplos de uso do framework. Cada exemplo é documentado em seu próprio arquivo fonte e portanto omitido.

## Arquitetura

O *framework* é organizado em 5 módulos principais: `arch`, `generators`, `loaders`, `models` e `preprocessing_steps`, descritos a seguir:

- [`arch`](#módulo-arch): é o módulo que contém as classes básicas, fundamentais do framework, isso é, as classes abstratas, prefixadas com `Base`, a classe [`Hasher`](#classe-hasher), e a própria classe [`Experiment`](#classe-experiment).

- [`generators`](#módulo-generators): contém as classes responsáveis por gerenciar as *epochs* do treinamento, implementações de [`BaseDatasetGenerator`](#classe-basedatasetgeneratorbase).

- [`loaders`](#módulo-loaders): contém as classes responsáveis por carregar as imagens do sistema de arquivos e aplicar uma transformação nelas. São as implementações de [`BaseLoader`](#classe-baseloaderbase).

- [`models`](#módulo-models): contém os modelos de redes neurais que podem ser treinadas pelo framework. São as implementações de [`BaseModel`](#classe-basemodelbase).

- [`preprocessing_steps`](#módulo-preprocessing_steps): contém as etapas de pré-processamento do *dataset*. São as implementações de [`BaseStep`](#classe-basestepbase).

<p align="center">
  <img src="images/module_diagram.png" width="50%">
</p>

Não existem muitas dependências entre módulos pois cada classe possui uma responsabilidade bem definida e independente. Todos os módulos dependem do módulo [`arch`](#módulo-arch) pois este contém as classes abstratas implementadas nos módulos. A única exceção é a dependência que o módulo [`arch`](#módulo-arch) tem do módulo [`generators`](#módulo-generators). 

Isso acontece porque a classe [`DatasetGenerator`](#classe-datasetgeneratorbasegenerator) é o gerenciador de *epoch* padrão do framework, e precisa ser instanciado automaticamente quanto um gerador não é informado. Essa situação pode ser claramente visualizada no diagrama de classes abaixo:

<p align="center">
  <img src="images/class_diagram.png" width="80%">
</p>

As principais oportunidades de extensão que o *framework* oferece consistem em implementar classes derivadas das classes abstratas [`BaseDatasetGenerator`](#classe-basedatasetgeneratorbase), [`BaseLoader`](#classe-baseloaderbase), [`BaseModel`](#classe-basemodelbase) e [`BaseStep`](#classe-basestepbase), com funcionalidades bem definidas e reusáveis.

## Referência de Classes

### Módulo arch

Este é o módulo fundamental do framework, contendo a classe [Experiment](#experiment) as classes abstratas (prefixadas com `Base`) que serão implementadas nos demais módulos.

#### Classe Base

Classe abstrata, base de todas as classes do framework. Facilita a geração dos relatórios textuais dos experimentos e o cálculo do seu *hash*.

##### `Base.__str__() -> str`

Abstrato. Retorna, de maneira textual, o código contendo a chamada ao construtor desta classe, com todos os parâmetros necessários para reconstruir esta instância.

##### `Base.description() -> str`

Abstrato. Retorna uma descrição legível do que essa instância faz.

##### `Base.add_hash(hasher: Hasher)`

Abstrato. Adiciona o estado configurável desta instância ao [Hasher](#classe-hasher) fornecido.

#### Classe BaseDatasetGenerator(Base)

Classe abstrata de todos os gerenciadores de *epoch*.

##### `BaseDatasetGenerator.encoding`

Classe que será utilizada para codificar e decodificar as classes do *dataset* para a rede neural. Não existe uma definição formal de seu tipo. Por ora a melhor referência de implementação é a classe [OneHot](#classe-onehotbase).

##### `BaseDatasetGenerator.dataset: pandas.DataFrame`

O *dataset* gerenciado por esta instância. Esse atributo existe para permitir ao *framework* informar o *dataset* processado à uma instância de *generator* configurada pelo usuário.

##### `BaseDatasetGenerator.__len__() -> int`
        
Abstrato. Returna quantos *batches* existem neste *dataset*.
    
##### `BaseDatasetGenerator.__getitem__(index: int) -> (np.array, np.array)`

Abstrato. Retorna o conteúdo do i-ésimo *batch*, na forma de uma tupla contendo a lista das imagens e a lista das classes codificadas.

##### `BaseDatasetGenerator.on_epoch_end():`

Abstrato. Esse método é chamado pela classe [Experiment](#classe-experiment) ao final de cada *epoch*.

#### Classe BaseLoader(Base)

Classe abstrata de todos os carregadores de imagens.

##### `BaseLoader.load(file: str) -> np.ndarray`

Abstrato. Carrega uma image do disco.

#### Classe BaseModel(Base)

Classe abstrata de todos os modelos de rede neural.

##### `BaseModel.get() -> tensorflow.keras.Model`

Abstrato. Retorna a instância do modelo Keras de rede neural a ser treinada.

##### `BaseModel.compile(classes: int)`

Abstrato. A classe [Experiment](#classe-experiment) chamará esse método informando o número de classes presentes no *dataset*.

#### Classe BaseStep(Base)

Classe abstrata de todas as etapas de pré-processamento.

##### `BaseStep.process(data: pandas.DataFrame) -> pandas.DataFrame:`

Aplica esta etapa de pré-processamento à tabela provida e retorna o resultado.

#### Classe Experiment

Classe central do framework, que organiza e executa um experimento de treinamento de redes neurais.

##### `Experiment.__init__(name: str)`

Cria um novo experimento, fornecendo o nome do experimento.

##### `Experiment.base_images_path: str`

Define de qual diretório as imagens do *dataset* devem ser carregadas.

##### `Experiment.base_report_path: str`

Define em qual diretório os relatórios serão gravados.
> Default: 'reports/'

##### `Experiment.input: str`

Define o nome do arquivo Excel contendo o *dataset*.

##### `Experiment.image_column: str`

Define qual é o nome da coluna do *dataset* contendo os nomes dos arquivos de imagem.

##### `Experiment.label_column: str`

Define qual é o nome da coluna do *dataset* contendo as classificações (ou *labels*).

##### `Experiment.preprocessing_steps: List[BaseStep]`

Vetor contendo todas as etapas de pré-processamento global. 
> Default: []

##### `Experiment.add_train_set(steps: List[BaseStep], *loaders: BaseLoader)`

Define uma "fatia" do *dataset* de treinamento, como descrito na seção [Descrição de um Experimento](documentacao.md#descrição-de-um-experimento), associando uma lista de etapas de pré-processamento à uma lista de carregadores de imagem.

Essas etapas de pré-processamento serão aplicadas ao *dataset* após as etapas de pré-processamento globais serem aplicadas. Os elementos resultantes farão parte do *dataset* de treinamento, sendo carregados pelos *loaders* informados, em multiplicidade. 

> `steps` : Lista de etapas de pré-processamento. \
> `loaders` : Lista de *loaders*.

##### `Experiment.add_validation_set(steps: List[BaseStep], *loaders: BaseLoader)`

Define uma "fatia" do *dataset* de validação, como descrito na seção [Descrição de um Experimento](documentacao.md#descrição-de-um-experimento), associando uma lista de etapas de pré-processamento à uma lista de carregadores de imagem.

Essas etapas de pré-processamento serão aplicadas ao *dataset* após as etapas de pré-processamento globais serem aplicadas. Os elementos resultantes farão parte do *dataset* de validação, sendo carregados pelos *loaders* informados, em multiplicidade. 

> `steps` : Lista de etapas de pré-processamento. \
> `loaders` : Lista de *loaders*.

##### `Experiment.model: BaseModel`

Instância do modelo de rede neural a ser treinada neste experimento.

##### `Experiment.epochs: int`

Número de *epochs* de treinamento.
> Default: 20.

##### `Experiment.train_set_generator: BaseDatasetGenerator`

Qual gerenciador de *epoch* será utilizado durante o treinamento. Se não for informado, uma instância classe [DatasetGenerator](#classe-datasetgeneratorbasedatasetgenerator) com os valores padrão será utilizada.

Se uma instância personalizada for atribuída, não é preciso (nem possível) definir o atributo [dataset](#basedatasetgeneratordataset-pandasdataframe). Esse atributo deve permanecer como `None` que o *framework* atribuirá o *dataset* correto durante o treinamento.

Além disso, se o *generator* informado não tiver uma valor definido no atributo [encoding](#basedatasetgeneratorencoding), o *framework* criará automaticamente uma instância da classe [OneHot](#classe-onehotbase) contemplando todas as classes únicas presentes no *dataset*.

##### `Experiment.run(dry: bool)`

Realiza o treinamento e gera o relatório do experimento.

> `dry` : Se True, realiza o pré-processamento do *dataset*, mas não realiza o treinamento propriamente dito. O relatório gerado é simplificado.  Default: False.

#### Classe Hasher

Classe responsável por calcular e agregar *hashes*.

##### `Hasher.__init__(*args)`

Cria uma nova instância de Hasher. 
> `*args` : Lista de elementos a agregar ao *hash*, já na construção. Os parâmetros são *hasheados* de maneira ordenada, vide [Hasher.ordered](#hasherorderedargs-hasher)

##### `Hasher.__str__()`

Retorna o *hash* agregado em texto, em hexadecimal. Exemplo: "%xABCDEF00"

##### `Hasher.__eq__(other)`

Compara o valor acumulado do *hash* com outro valor. 
> `other` : Pode ser um `int` ou outra instância de [Hasher](#classe-hasher).

##### `Hasher.ordered(*args): Hasher`

Calcula e agrega o *hash* dos parâmetros passados. Os parâmetros são entendidos como uma lista, ou seja, a ordem dos parâmetros passados influencia o valor do *hash* calculado. 
> `*args` : Pode ser qualquer um dos tipos básicos ou uma instância de [Base](#classe-base). \
> Retorna : a própria instância.

##### `Hasher.unordered(*args): Hasher`

 Calcula e agrega o *hash* dos parâmetros passados. Os parâmetros são entendidos como um conjunto, ou seja, a ordem dos parâmetros passados NÃO influencia o valor do *hash* calculado.
> `*args` : Pode ser qualquer um dos tipos básicos ou uma instância de [Base](#classe-base). \
> Retorna : a própria instância.

#### Classe Preprocessing(Base)

Representa uma lista de etapas de pré-processamento (classes derivadas de [BaseStep](#classe-basestepbase)). Facilita a geração textual dessas etapas e o processamento de *dataset*.

##### `Preprocessing.add_step(step: BaseStep)`

Adiciona uma etapa de pré-processamento a esta lista. 
> `step` : Instância de classe derivada de [BaseStep](#classe-basestepbase).

##### `Preprocessing.process(data: pandas.DataFrame) -> pandas.DataFrame`

Processa um *dataset* por todas as etapas de pré-processamento que foram adicionadas à esta instância, na mesma ordem.
> `data` : Uma tabela. \
> Retorna : A tabela processada.

---

### Módulo generators

Contém os gerenciadores de *epoch* padrão do framework. Os generators são classes que carregam e preparam cada entrada do *dataset* (imagem e classe) para o treinamento, de acordo com uma politica de seleção e agrupamento de linhas. Mais informações na seção [Regime de Treinamento](documentacao.md#regime-de-treinamento) da documentação.

Observe que o *dataset* aqui já está totalmente processado, e possui apenas as colunas `input`, `loader` e `label`, como explicado ao final da seção [Descrição de um Experimento](documentacao.md#descrição-de-um-experimento) da documentação.

Para personalizar o *generator* utilizado durante o treinamento, basta atribuir uma instância ao atributo [Experiment.train_set_generator](#experimenttrain_set_generator-basedatasetgenerator).

#### Classe DatasetGenerator(BaseDatasetGenerator)

É o gerenciador de *epoch* padrão do framework. Ele fornece todos os elementos do *dataset* por *epoch*, organizados em *batches* de tamanho fixo. Opcionalmente pode embaralhar o *dataset* antes de cada *epoch*.

##### `DatasetGenerator.__init__(dataset: pandas.DataFrame, encoding: OneHot, batch_size: int, shuffle: bool)`

Constrói uma nova instância da classe [DatasetGenerator](#classe-datasetgeneratorbasedatasetgenerator). 

> `dataset` : O *dataset* a ser gerenciado. Opcional, pode ser alterado posteriormente através do atributo [dataset](#basedatasetgeneratordataset-pandasdataframe). \
> `encoding` : Instância da classe [OneHot](#classe-onehotbase) configurada para codificar e decodificar as classes do *dataset*. Opcional, pode ser alterado posteriormente através do atributo [encoding](#basedatasetgeneratorencoding). \
> `batch_size` : O número de imagens por *batch*. Default: 16 \
> `shuffle` : Determina se o *dataset* deve ser embaralhado no início de cada *epoch*. Default: True

#### Classe StratifiedDatasetGenerator(BaseDatasetGenerator)

Implementa uma estratégia estratificada de montagem das *epochs*, onde dado um número *N* de elementos por classe, as *epochs* são formadas da seguinte maneira:
- *N* elementos aleatórios de cada classe são colocados em uma lista.
- Essa lista é embaralhada em ordem aleatória.
- A lista é quebrada em *batches* e submetida para treinamento.

Desta maneira, o número de imagens utilizadas para treinamento por *epoch* pode ser muito menor do que o número de elementos no *dataset* total. Além disso, a rede é treinada toda *epoch* com o mesmo número de elementos por classe, melhorando seu treinamento com *datasets* desbalanceados, isso é, *datasets* onde existe uma diferença muito grande no número de elementos em cada classe.

##### `StratifiedDatasetGenerator.__init__(dataset: pandas.DataFrame, encoding, samples_per_class: int, seed: int, batch_size: int, shuffle: bool) `

Constrói uma nova instância da classe [StratifiedDatasetGenerator](#classe-stratifieddatasetgeneratorbasedatasetgenerator).

> `dataset` : O *dataset* a ser gerenciado. Opcional, pode ser alterado posteriormente através do atributo [dataset](#basedatasetgeneratordataset-pandasdataframe). \
> `encoding` : Instância da classe [OneHot](#classe-onehotbase) configurada para codificar e decodificar as classes do *dataset*. Opcional, pode ser alterado posteriormente através do atributo [encoding](#basedatasetgeneratorencoding). \
> `samples_per_class` : O número de elementos aleatórios de cada classe a serem selecionados por *epoch*. \
> `seed`: A [semente aleatória](https://en.wikipedia.org/wiki/Random_seed) utilizada na seleção e embaralhamento das linhas. É automaticamente alterado ao final de cada *epoch*. \
> `batch_size` : O número de imagens por *batch*. Default: 16 \
> `shuffle` : Determina se o *dataset* deve ser embaralhado no início de cada *epoch*. Default: True

---

### Módulo loaders

Contém as classes responsáveis por carregar imagens do sistema de arquivos.

#### Classe BrightLoader(SimpleLoader)

Carrega uma imagem interpretando cada componente de cor dos pixels como valores no intervalo `[0, 255]`, e ajusta seu brilho, aplicando a seguinte equação à cada componente de cada pixel:

`X = alpha * X + beta`

Onde `alpha` e `beta` são coeficientes informados no construtor. Opcionalmente redimensiona a imagem ao carregá-la.

##### `BrightLoader.__init__(alpha: float, beta: float, resize: tuple[int, int])`

Constrói uma nova instância de [BrightLoader](#classe-brightloadersimpleloader).
> `alpha`: Coeficiente multiplicativo. Default: 1.0 \
> `beta`: Coeficiente aditivo. Default: 0.0 \
> `resize`: Dimensões (linhas, colunas) usados para redimensionar a image. Opcional.

#### Classe RotationLoader(SimpleLoader)

Carrega uma imagem e a rotaciona pelo ponto central, interpretando cada componente de cor dos pixels como valores no intervalo `[0, 255]`. O ângulo utilizado é aleatório, escolhido dentro do intervalo:

 `[angle - spread, angle + spread]`

 Onde `angle` e `spread` são valores informados no construtor, em graus. Opcionalmente redimensiona a imagem ao carregá-la.

##### `RotationLoader.__init__(angle: float = 0.0, spread: float = 0.0, resize: tuple[int, int])`

Constrói uma nova instância de [RotationLoader](#classe-rotationloadersimpleloader).

> `angle` : Ângulo base de rotação. Default: 0.0 \
> `spread` : Largura do intervalo aleatório em torno de `angle`. Default: 0.0 \
> `resize`: Dimensões (linhas, colunas) usados para redimensionar a image. Opcional.

#### Classe SimpleLoader(BaseLoader)

Carrega uma imagem do sistema de arquivos, interpretando cada componente de cor dos pixels como valores no intervalo `[0, 255]`. Opcionalmente redimensiona a imagem ao carregá-la.

##### `SimpleLoader.__init__(resize: tuple[int, int])`

Constrói uma nova instância de [SimpleLoader](#classe-simpleloaderbaseloader).

> `resize`: Dimensões (linhas, colunas) usados para redimensionar a image. Opcional.

---

### Módulo models

Contém as implementações padrão da classe abstrata [BaseModel](#classe-basemodelbase), ou seja, modelos de rede neural que podem ser treinados pelo framework.

#### Classe EfficientNetB0Model(BaseModel)

Encapsula o modelo de redes neurais [EfficientNetB0](https://www.tensorflow.org/api_docs/python/tf/keras/applications/efficientnet/EfficientNetB0), configurado para utilizar o otimizador [Adam](https://keras.io/api/optimizers/adam/).

##### `EfficientNetB0Model.learning_rate: float`

Define a taxa de aprendizado da rede. 
> Default: 0.001

##### `EfficientNetB0Model.loss: str`

Define qual função de perda será utilizada durante o treinamento. Para conhecer os valores possíveis, visite https://keras.io/api/losses/.
> Default: 'categorical_crossentropy'

#### Classe EfficientNetB4Model(BaseModel)

Encapsula o modelo de redes neurais [EfficientNetB4](https://www.tensorflow.org/api_docs/python/tf/keras/applications/efficientnet/EfficientNetB4), configurado para utilizar o otimizador [Adam](https://keras.io/api/optimizers/adam/).

##### `EfficientNetB4Model.learning_rate: float`

Define a taxa de aprendizado da rede. 
> Default: 0.001

##### `EfficientNetB4Model.loss: str`

Define qual função de perda será utilizada durante o treinamento. Para conhecer os valores possíveis, visite https://keras.io/api/losses/.
> Default: 'categorical_crossentropy'

#### Classe OneHot(Base)

Classe auxiliar utilizada para codificar, com a estratégia [one-hot](https://en.wikipedia.org/wiki/One-hot), a classe de uma imagem em um vetor numérico. 

Por exemplo, se as classes de um *dataset* são "gato", "taco", "cabra", "queijo", "pizza", uma possível codificação em one-hot seria:

```
 "gato"    [1, 0, 0, 0, 0]
 "taco"    [0, 1, 0, 0, 0]
 "cabra"   [0, 0, 1, 0, 0]
 "queijo"  [0, 0, 0, 1, 0]
 "pizza"   [0, 0, 0, 0, 1]
```

##### `OneHot.__init__(labels: [str])`

Cria uma nova instância capaz de codificar as classes informadas. Não é possível trocar as classes da codificação após a construção da classe.

##### `OneHot.encode(labels: str | [str]) -> [number] | [[number]]`

Codifica a classe ou classes informadas. 
> `labels` : Uma classe ou uma lista de classes. \
> Retorna : Um vetor numérico codificando a classe informada, ou um vetor de vetores numéricos codificando cada classe informada.

##### `OneHot.decode(pred: [number]) -> str`

Descodifica a predição realizada pela rede neural em uma das classes do *dataset*, no caso, retorna a classe referente ao índice com o maior valor no vetor informado.

Por exemplo, considerando-se as classes de exemplo acima, o resultado de se decodificar o vetor `[0.03, 0.52, 0.04, 0.21, 0.95]` seria "pizza", pois o último valor do vetor é o maior de todos, referente à última classe informada no construtor.

> `pred`: vetor numérico contendo a predição da rede neural, onde cada valor significa a probabilidade da imagem classificada pertencer à respectiva classe. \
> Retorna : String contendo o nome da classe predita pela rede.

---

### Módulo preprocessing_steps

Módulo contendo as implementações padrão da classe abstrata [BaseStep](#classe-basestepbase), ou seja, as etapas de pré-processamento do *dataset*. Seu uso será através do método [BaseStep.process](#basestepprocessdata-pandasdataframe---pandasdataframe).

#### Classe FilterColumn(BaseStep)

Etapa de pré-processamento que filtra as linhas em função do valor em uma determinada coluna.

##### `FilterColumn.__init__(column: str, values: List[str])`

Constrói uma nova instância da classe [FilterColumn](#classe-filtercolumnbasestep).

> `column`: Coluna a ser utilizada pelo filtro. \
> `values`: Vetor contendo os valores permitidos para a coluna `column`. Apenas linhas contendo esses valores serão preservadas.

#### Classe FirstCount(BaseStep)

Etapa de pré-processamento que preserva um número determinado das primeiras linhas do *dataset*.

##### `FirstCount.__init__(count: int)`

Constrói uma nova instância da classe [FirstCount](#classe-firstcountbasestep).

> `count` : O número de linhas do início do *dataset* a serem preservadas.

#### Classe FirstPercent(BaseStep)

Etapa de pré-processamento que preserva um certo número das primeiras linhas do *dataset*, informado como uma percentagem do número total de linhas.

##### `FirstPercent.__init__(precent: float)`

Constrói uma nova instância da classe [FirstPercent](#classe-firstpercentbasestep).

> `percent` : O número de linhas do início do *dataset* a serem preservadas, como percentual do total de linhas do *dataset*.

#### Classe LastCount(BaseStep)

Etapa de pré-processamento que preserva um número determinado das últimas linhas do *dataset*.

##### `LastCount.__init__(count: int)`

Constrói uma nova instância da classe [LastCount](#classe-lastcountbasestep).

> `count` : O número de linhas do final do *dataset* a serem preservadas.

#### Classe LastPercent(BaseStep)

Etapa de pré-processamento que preserva um certo número das últimas linhas do *dataset*, informado como uma percentagem do número total de linhas.

##### `LastPercent.__init__(precent: float)`

Constrói uma nova instância da classe [LastPercent](#classe-lastpercentbasestep).

> `percent` : O número de linhas do final do *dataset* a serem preservadas, como percentual do total de linhas do *dataset*.

#### Classe ReplaceValueInColumn(BaseStep)

Etapa de pré-processamento que substitui determinados valores em uma coluna do *dataset*.

##### `ReplaceValueInColumn.__init__(column: str, originalValue: str, newValue: str)`

Constrói uma instância da classe [ReplaceValueInColumn](#classe-replacevalueincolumnbasestep).

> `column` : Coluna do *dataset* a ser alterada. \
> `originalValue` : Valor da coluna `column` a ser substituído. \
> `newValue` : Valor a ser aplicado à coluna `column` se seu valor for igual à `originalValue`.

#### Classe Shuffle(BaseStep)

Etapa de pré-processamento que embaralha as linhas do *dataset*.

##### `Shuffle.__init__(seed: int)`

Constrói uma nova instância da classe [Shuffle](#classe-shufflebasestep).

> `seed`: A [semente aleatória](https://en.wikipedia.org/wiki/Random_seed) utilizada no embaralhamento das linhas.