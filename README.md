# exp

O exp é um framework modular de apoio ao treinamento de redes neurais convolucionais. Com ele é possível descrever de maneira sucinta as etapas de pré-processamento dos dados e os parâmetros de configuração da rede para treinamento.
Em contrapartida, o framework executa o treinamento e gera um relatório único, descrevendo as etapas de pré-processamento, a rede utilizada e os resultados obtidos.

[//]: # ( Pré-processamento de dados, incluindo leitura, normalização, seleção e distribuição nos conjuntos de treinamento, avaliação e testes. 
A configuração da rede neural, incluindo dos parâmetros de treinamento e o do otimizador.
A gravação dos resultados e geração de relatórios. )

## Instalação

O framework requer Python 3 com Tensorflow 2 ou superior. Recomendamos a utilização de um *[virtual environment](https://docs.python.org/3/library/venv.html)* e a instalação das dependências através do arquivo [requirements.txt](requirements.txt):

```
pip install -r requirements.txt
```

Como existem diversas maneiras de se instalar o Tensorflow, não incluímos essa dependência diretamente no requirements.txt.

## Documentação

 - [Requisitos](docs/requisitos.md)
 - [Arquitetura](docs/arquitetura.md)
 - [Referência de Classes](docs/referencia.md)

## Exemplos

 - [Filtragem de dados](examples/filtering)
 - [Carregamento de imagens](examples/imageLoading)

## Licença

Licenciado sobre a [licença MIT](LICENSE).

## Convenções

Seguimos as convenções de código descritas em https://peps.python.org/pep-0008/