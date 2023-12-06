# Especificação Técnica

O framework exp é desenvolvido em Python, seguindo uma abordagem orientada a objetos. Foi feito um esforço para que todas os parâmetros de todos os métodos fossem devidamente anotados com seus respectivos tipos, gerando, assim, dependência explícita entre as classes e os módulos do framework.

Neste documento iremos descrever como o código do framework exp é organizado, seus módulos e classes, com as seguintes exceções:
- Por uma questão de brevidade, documentaremos aqui apenas as classes públicas dos módulos. 
- O diretório `src/helpers` contém arquivos auxiliares que não compõe um módulo do framework.
- O diretório `src/examples` contém os exemplos de uso do framework. Cada exemplo é documentado em seu próprio arquivo fonte e portanto omitido.

## Arquitetura

O framework é organizado em 5 módulos principais: `arch`, `generators`, `loaders`, `models` e `preprocessing_steps`, descritos a seguir:

- `arch`: é o módulo que contém as classes básicas, fundamentais do framework, isso é, as classes abstratas, prefixadas com `Base`, a classe `Hasher`, e a própria classe `Experiment`.

- `generators`: contém as classes responsáveis por gerenciar as *epochs* do treinamento, implementações de `arch.BaseDatasetGenerator`.

- `loaders`: contém as classes responsáveis por carregar as imagens do sistema de arquivos e aplicar uma transformação nelas. São as implementações de `arch.BaseLoader`.

- `models`: contém os modelos de redes neurais que podem ser treinadas pelo framework. São as implementações de `arch.BaseModel`.

- `preprocessing_steps`: contém as etapas de pré-processamento do *dataset*. São as implementações de `arch.BaseStep`.

![](images/module_diagram.png)

Não existem muitas dependências entre módulos pois cada classe possui uma responsabilidade bem definida e independente. Todos os módulos dependem do módulo `arch` pois este contém as classes abstratas implementadas nos módulos. A única exceção é a dependência do que o módulo `arch` tem do `generators`. 

Isso acontece porque a classe `generators.DatasetGenerator` é o gerenciador de *epoch* padrão do framework, e precisa ser instanciado automaticamente quanto um gerador não é informado. Essa situação pode ser claramente visualizada no diagrama de classes abaixo:

![](images/class_diagram.png)

## Referência de Classes

### Arch

#### Base

Classe abstrata, base de todas as classes do framework. Facilita a geração dos relatórios textuais dos experimentos e o cálculo do seu *hash*.

##### `Base.__str__() -> str`

> Abstrato. Retorna, de maneira textual, o código contendo a chamada ao construtor desta classe, com todos os parâmetros necessários para reconstruir esta instância.

##### `Base.description() -> str`

> Abstrato. Retorna uma descrição legível do que essa instância faz.

##### `Base.add_hash(hasher: Hasher)`

> Abstrato. Adiciona o estado configurável desta instância ao [Hasher](#hasher) fornecido.

#### BaseDatasetGenerator(Base)

Classe abstrata de todos os gerenciadores de *epoch*.

##### `BaseDatasetGenerator.__len__() -> int`
        
> Abstrato. Returna quantos *batches* existem neste *dataset*.
    
##### `BaseDatasetGenerator.__getitem__(index: int) -> (np.array, np.array)`

> Abstrato. Retorna o conteúdo do i-ésimo *batch*, na forma de uma tupla contendo a lista das imagens e a lista das classes codificadas.

##### `BaseDatasetGenerator.on_epoch_end():`

> Abstrato. Esse método é chamado pela classe [Experiment](#experiment) ao final de cada *epoch*.

#### BaseLoader(Base)

Classe abstrata de todos os carregadores de imagens.

##### `BaseLoader.load(file: str) -> np.ndarray`

> Abstrato. Carrega uma image do disco.

#### BaseModel(Base)

Classe abstrata de todos os modelos de rede neural.

##### `BaseModel.get()`

> Abstrato. Retorna a instância do modelo Keras de rede neural a ser treinada.

##### `BaseModel.compile(classes: int)`

> Abstrato. A classe [Experiment](#experiment) chamará esse método informando o número de classes presentes no *dataset*.

#### BaseStep(Base)

Classe abstrata de todas as etapas de pré-processamento.

##### `BaseStep.process(data: pandas.DataFrame) -> pandas.DataFrame:`

Aplica esta etapa de pré-processamento à tabela provida e retorna o resultado.

#### Experiment

Classe central do framework, que organiza e executa um experimento de treinamento de redes neurais.

##### `Experiment.__init__(name: str)`

> Cria um novo experimento, fornecendo o nome do experimento.

##### `Experiment.base_images_path: str`

> Define de qual diretório as imagens do *dataset* devem ser carregadas.

##### `Experiment.base_report_path: str`

> Define em qual diretório os relatórios serão gravados. Default: reports/

##### `Experiment.input: str`

> Define o nome do arquivo Excel contendo o *dataset*.

##### `Experiment.image_column: str`

> Define qual é o nome da coluna do *dataset* contendo os nomes dos arquivos de imagem.

##### `Experiment.label_column: str`

> Define qual é o nome da coluna do *dataset* contendo as classificações (ou *labels*).

##### `Experiment.preprocessing_steps: List[BaseStep]`

> Vetor contendo todas as etapas de pré-processamento global. Default: []

##### `Experiment.model: BaseModel`

> Instância do modelo de rede neural a ser treinada neste experimento.

##### `Experiment.epochs: int`

> Número de *epochs* de treinamento. Default: 20.

#### Hasher

Classe responsável por calcular e agregar *hashes*.

##### `Hasher.__init__(*args)`

> Cria uma nova instância de Hasher. \
> `*args` : Lista de elementos a agregar ao *hash*, já na construção. Os parâmetros são *hasheados* de maneira ordenada, vide [Hasher.ordered](#hasherorderedargs-hasher)

##### `Hasher.__str__()`

> Retorna o *hash* agregado em texto, em hexadecimal. Exemplo: "%xABCDEF00"

##### `Hasher.__eq__(other)`

> Compara o valor do *hash* acumulado com outro valor. \
> `other` : Pode ser um `int` ou outra instância de [Hasher](#hasher).

##### `Hasher.ordered(*args): Hasher`

> Calcula e agrega o *hash* dos parâmetros passados. Os parâmetros são entendidos como uma lista, ou seja, a ordem dos parâmetros passados influencia o valor do *hash* calculado. \
> `*args` : Pode ser qualquer um dos tipos básicos ou uma instância de [Base](#base). \
> Retorna : a própria instância.

##### `Hasher.unordered(*args): Hasher`

> Calcula e agrega o *hash* dos parâmetros passados. Os parâmetros são entendidos como um conjunto, ou seja, a ordem dos parâmetros passados NÃO influencia o valor do *hash* calculado. \
> `*args` : Pode ser qualquer um dos tipos básicos ou uma instância de [Base](#base). \
> Retorna : a própria instância.

#### Preprocessing(Base)

Representa uma lista de etapas de pré-processamento (classes derivadas de [BaseStep](#basestepbase)). Facilita a geração textual dessas etapas e o processamento de *dataset*.

##### `Preprocessing.add_step(step: BaseStep)`

> Adiciona uma etapa de pré-processamento a esta lista. \
> `step` : Instância de classe derivada de [BaseStep](#basestepbase)

##### `Preprocessing.process(data: pandas.DataFrame) -> pandas.DataFrame`

> Processa um *dataset* por todas as etapas de pré-processamento que foram adicionadas à esta instância, na mesma ordem. \
> `data` : Uma tabela. \
> Retorna : A tabela processada.

---

### Models

#### EfficientNetB0Model

#### EfficientNetB4Model

#### OneHot

---

### Loaders

#### BaseLoader

#### BrightLoader

#### RotationLoader

---

### Preprocessing Steps

#### ChangeColumn

#### FilterColumn

#### FirstCount

#### FirstPercent

#### LastCount

#### LastPercent

#### Shuffle