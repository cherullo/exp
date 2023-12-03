# exp

O exp é um framework modular de apoio aos experimentos em treinamento de redes neurais convolucionais. Seu objetivo é fornecer documentação e reproducibilidade aos experimentos realizados.

Com ele é possível descrever de maneira sucinta as etapas de pré-processamento dos dados e os parâmetros de configuração da rede, e executar o treinamento, gerando um relatório que descreve todas as configurações do experimento e os resultados obtidos.

Para começar a utilizar o framework, recomendamos realizar as etapas de instalação abaixo e experimentar com os exemplos disponíveis.

## Instalação

O framework requer Python 3 com Tensorflow 2 ou superior. Recomendamos a utilização de um *[virtual environment](https://docs.python.org/3/library/venv.html)* e a instalação das dependências através do arquivo [requirements.txt](requirements.txt):

```
pip install -r requirements.txt
```

Como existem diversas maneiras de se instalar o Tensorflow, não incluímos essa dependência diretamente no requirements.txt.

## Exemplos

A fim de resolver questões de path e imports, é preciso utilizar a seguinte linha de comandos para executar os exemplos:

```
python src/run_sample.py [ARQUIVO PYTHON]
```

 - Selecionar as primeiras linhas de um dataset: [examples/filtering/first_count.py]()

- Selecionar as linhas onde uma coluna possui determinado valor: [examples/filtering/filter_by_column.py]()

- Como trocar o valor de uma coluna: [examples/filtering/change_column.py]()

- Como treinar uma rede para classificar vacas e ovelhas: [examples/training/animal_classification.py]()

## Documentação

 - [Documentação](docs/documentacao.md)
 - [Referência de Classes](docs/referencia.md)

## Licença

Licenciado sobre a [licença MIT](LICENSE).

## Convenções

Seguimos as convenções de código descritas em https://peps.python.org/pep-0008/