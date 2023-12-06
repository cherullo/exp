# Especificação Técnica

O framework exp é desenvolvido em Python, seguindo uma abordagem orientada a objetos. Foi feito um esforço para que todas os parâmetros de todos os métodos fossem devidamente anotados com seus respectivos tipos, gerando dependência explícita entre as classes e módulos do framework.

Neste documento iremos descrever como o código do framework exp é organizado, seus módulos e classes, com as seguintes exceções:
- Por uma questão de brevidade, documentaremos aqui apenas as classes públicas dos módulos. 
- O diretório `src/helpers` contém arquivos auxiliares que não compõe um módulo do framework.
- O diretório `src/examples` contém os exemplos de uso do framework. Cada exemplo é documentado em seu próprio arquivo fonte e portanto omitidos.

## Arquitetura

O framework é organizado em 5 módulos principais: `arch`, `generators`, `loaders`, `models` e `preprocessing_steps`, descritos a seguir:

- `arch`: é o módulo que contém as classes básicas, fundamentais do framework, isso é, as classes abstratas, prefixadas com `Base`, a classe `Hasher`, e a própria classe `Experiment`.

- `generators`: contém as classes responsáveis por gerenciar as *epochs* do treinamento, derivadas de `arch.BaseDatasetGenerator`.

- `loaders`: contém as classes responsáveis por carregar as imagens do sistema de arquivos e aplicar uma transformação nelas. São as classes derivadas de `loaders.BaseLoader`.

- `models`: contém os modelos de redes neurais que podem ser treinadas pelo framework. São as classes derivadas de `arch.BaseModel`.

- `preprocessing_steps`: contém as etapas de pré-processamento do *dataset*. São as classes derivadas de `arch.BaseStep`.

![](images/module_diagram.png)

Como cada classe possui uma responsabilidade única, é bem natural que o diagrama de módulos seja

from .Base import Base
from .BaseModel import BaseModel
from .BaseStep import BaseStep
from .BaseDatasetGenerator import BaseDatasetGenerator

from .Hasher import Hasher
from .Experiment import Experiment
from .Preprocessing import Preprocessing

## Referência de Classes

### Arch

#### Base

```
def __str__():
```

```
description() -> str
```

```
add_hash(hasher)
```

#### DatasetGenerator

#### Experiment

#### Hasher

#### Preprocessing

#### Step

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