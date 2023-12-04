# Introdução

Durante o desenvolvimento de soluções envolvendo o uso de redes neurais, pesquisadores realizam diversos experimentos até convergir em uma rede treinada que cumpra os objetivos desejados. É um processo complexo, iterativo, onde os pesquisadores precisam analisar os resultados de cada etapa para saber quais parâmetros devem ser ajustados para o próximo experimento.

Assim, não basta que o resultado de cada um desses experimentos seja uma rede treinada, os pesquisadores precisam sistematicamente analisar diversos aspectos do processo de treinamento e da performance da rede obtida. Ou seja, o processo de treinamento precisa gerar também um conjunto de relatórios e gráficos de apoio, essenciais para que o pesquisador possa continuar o processo iterativo de refinamento da rede.

Nesse contexto, uma parte importante do trabalho do pesquisador está relacionado ao tratamento dos dados utilizados durante o treinamento. Dada uma massa de dados, é preciso importar, converter, tratar, selecionar e distribuir os dados nos conjuntos de treinamento, avaliação e testes. 

# Objetivos

O objetivo do framework exp é apoiar o processo iterativo de desenvolvimento de redes neurais através da estruturação dos experimentos em duas partes: sua descrição em python, e seu respectivo relatório de treinamento.

As classes do framework permitem ao pesquisador descrever as etapas de pré-processamento e os parâmetros de treinamento de uma rede neural, servindo naturalmente como documentação do experimento. 

O framework, por sua vez, deve realizar o treinamento baseado nesta descrição e gerar os respectivos relatórios, suportando o caso comum de mais de um pesquisador estar trabalhando no mesmo projeto, e mais de um experimento estar sendo realizado simultaneamente.

# Requisitos

A fim de alcançar os objetivos definidos acima e considerando-se o contexto da prática de desenvolvimento de redes neurais, o framework foi desenvolvido observando-se os seguintes requisitos funcionais e não funcionais.

## Requisitos Funcionais

**[RF]** O framework deve permitir a descrição de todas as etapas de pré-processamento de dados do experimento.

**[RF]** O framework deve suportar que o treinamento seja realizado utilizando-se técnicas de *data augmentation*, isso é, transformações nos dados realizadas a fim de aumentar a quantidade de dados disponíveis.

**[RF]** O framework deve permitir que o pesquisador defina qual rede neural será treinada, bem como os parâmetros pertinentes ao processo de treinamento.

**[RF]** Guiado pela descrição do experimento, o framework deve realizar as etapas de pré-processamento de dados e o treinamento da rede neural.

**[RF]** Ao término de cada experimento, o framework deve gerar um relatório legível contendo tudo o que foi realizado, como todas as etapas de pré-processamento, as caracterísicas da rede, a evolução do treinamento e seu resultado.

## Requisitos Não-Funcionais

**[RNF]** O framework será escrito em Python 3.

**[RNF]** Durante as etapas de pré-processamento, os dados tabulares serão manipulados utilizando a biblioteca [pandas](https://pandas.pydata.org/).

**[RNF]** As imagens são manipuladas utilizando matrizes [numpy](https://numpy.org).

**[RNF]** O framework deve ser extensível, para permitir que o desenvolvedor o adapte às especificidades de seu projeto.

**[RNF]** O framework deve permitir que diversos experimentos sejam especificados e executados simultaneamente.

**[RNF]** Os experimentos criados utilizando o framework devem ser reproduzíveis, isso é, deve ser possível repetir um experimento futuramente mesmo que este contenha etapas aleatórias.

# Visão Geral de Uso

Ao se utilizar o framework, cada experimento é representado por uma instância da classe Experiment. Essa classe permite configurar todos os aspectos do experimento, e depois executá-lo. Por questões de organização, entendemos que cada experimento deve ser definido em um arquivo fonte Python separado. A execução do experimento é realizada executando-se o método `Experiment.run`.

Durante a execução de um experimento, o framework calcula o *hash* do experimento, isso é, o *hash* de todos os parâmetros e configurações realizadas no objeto `Experiment`. Para viabilizar esse cálculo, todas as classes do framework herdam da classe `Base`, que define o método `Base.add_hash`, utilizado para calcular e agregar o hash do cada objeto.

Após a execução do experimento, um relatório é criado no seguinte diretório (configurável):
```
 reports/[NOME DO FONTE PYTHON]_[HASH DO EXPERIMENTO]/
```

Como o nome do relatório remete ao fonte do experimento, e como o relatório contém todas as configurações de um experimento, é fácil relacionar qual fonte gerou qual experimento, mesmo se o fonte for alterado posteriormente. Entretanto, não recomendamos que um arquivo de experimento seja alterado após sua execução. Para a próxima iteração do desenvolvimento, recomendamos que o experimento seja duplicado e então alterado.

Esse esquema permite que um ou mais pesquisadores criem e executem seus experimentos simultaneamente, incluindo todos os experimentos e seus respectivos relatórios em um mesmo sistema de versionamento, sem que haja a preocupação de que os resultados de um experimento sejam perdidos, sobrescritos, ou necessitem de uma operação de *merge* no sistema de versionamento.

## Descrição de um Experimento

Em linhas gerais, um experimento é composto pelos seguintes itens, todos definidos pelo usuário:

1. Um arquivo Excel de *dataset*, onde cada linha representa um *sample* de dados para treinamento.
1. Uma sequência de etapas de pré-processamento global a ser aplicada em todo do *dataset*.
1. Um subconjunto do *dataset* para treinamento.
1. Um subconjunto do *dataset* para validação.
1. Um modelo básico de rede neural a ser treinada.

Para definir o arquivo Excel de entrada, o usuário do framework só precisa fornecer o nome do arquivo em disco. Isso é feito através do atributo `Experiment.input`. Neste instante, as colunas desta tabela são arbitrárias.

Para definir a sequência de etapas de pré-processamento global, o usuário deve fornecer uma lista de instâncias de classes derivadas da classe `Step` através do atributo `Experiment.preprocessing_steps`. Cada instância realizará uma alteração simples à tabela (como renomear uma coluna, trocar valores, selecionar linhas, etc), e elas serão aplicadas sucessivamente ao dataset carregado, na ordem em que aparecem na lista. Em Python:

```python
def _process_steps(dataset: pandas.DataFrame, steps: List[Step]) -> pandas.DataFrame:
    for step in steps:
        dataset = step.process(dataset)

    return dataset
```

O pré-processamento global irá gerar um *dataset* pré-processado, que será utilizado na geração dos subconjuntos de treinamento e validação. Tanto o *dataset* de treinamento quanto de validação são formados por diversas "fatias". Cada fatia é composta por uma sequência de etapas de pré-processamento (novamente uma lista instâncias de classes derivadas de `Step`) associadas a um *loader*. *Loaders* são classes derivadas da classe `BaseLoader` e encarregadas de ler uma imagem do disco e aplicar uma transformação nelas. 


Essas fatias são definidas pelo usuário através de sucessivas chamadas aos métodos `Experiment.add_train_set` e `Experiment.add_validation_set`, com a assinatura abaixo:

```python
    def add_train_set(steps:List[Step], *loaders: BaseLoader) -> None

    def add_validation_set(steps:List[Step], *loaders: BaseLoader) -> None
``` 

Observe que vários *loaders* podem ser passados em cada chamada. Isso é equivalente à chamar o método uma vez para cada *loader*, passando a mesma lista de etapas. Podemos entender esta organização graficamente abaixo:

![](images/Experimento.png)

Quando um treinamento é executado, as etapas de pré-processamento são aplicadas ao *dataset* inicial, gerando o *dataset* pré-processado. Os *datasets* de treinamento e validação são gerados concatenando-se o resultado do processamento de cada uma de suas fatias, que consiste simplesmente em aplicar as respectivas etapas de processamento ao *dataset* pré-processado e anexar uma coluna contendo o respectivo loader.

A geração do *dataset* de treinamento pode ser simplificadamente entendida pelo seguinte código Python:

```python
# Carrega o dataset do disco
dataset = pandas.read_excel(self.input)

# Aplica as etapas de pré-processamento globais
ds_pre = _process_steps(dataset, self.preprocessing_steps)

# Inicia com um dataset de treinamento vazio
training_set = []

# Para cada "fatia" do dataset de treinamento:
for steps, loaders in training_slices:
    for loader in loaders:
        # Aplica as etapas de pré-processamento da fatia após o pré-processamento global
        slice_set = _process_steps(ds_pre, steps) 

        # Adiciona uma coluna ao dataset com o loader
        slice_set.loc[:, 'loader'] = loader

        # Concatena o resultado desta fatia ao dataset de treinamento
        training_set.append (slice_set)
```

O mesmo processo é realizado para gerar o subconjunto de validação. Finalmente, para iniciar o treinamento, os datasets de treinamento e validação precisam são transformados em tabelas consolidadas, com formato padronizado, contendo apenas três colunas: 

- `input`: contém o nome do arquivo de imagem;
- `loader`: contém o *loader* a ser utilizado para carregar a referida imagem;
- `label`: contém o *label*, ou classe a que esta imagem pertence.

A coluna `loader` é adicionada automaticamente, já as colunas `input` e `label` precisam ser fornecidas pelo usuário. O nome da coluna contendo o nome dos arquivos de imagem precisa ser informada pelo usuário através do atributo `Experiment.image_column`, e o nome da coluna contendo os *labels* (ou classe da imagem) precisa ser informado através do atributo `Experiment.label_column`. A transformação consiste então em: renomear essas colunas respectivamente para `input` e `label`, manter a coluna `loader` e descartar as demais.

O treinamento é realizado utilizando esse formato padronizado de dados. O modelo da rede neural a ser treinada deve ser informada através do atributo `Experiment.model`, e deve ser uma instância de classe derivada de `BaseModel`.

## Composição do Relatório

Quais os arquivos gerados no relatório

# Especificação Técnica

## Descrição Funcional

Quais são as etapas de execução de um experimento

## Arquitetura

Diagrama de classes

## Documentação de Classes

[Documentação de classes](referencia.md)

# Cenários de Uso

## Cenário Adequado: Treinamento com datasets desbalanceados

## Cenário Adequado:

## Cenário Não-Adequado:

## Cenário Não-Adequado:
