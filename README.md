# exp

O exp é um *framework* modular de apoio aos experimentos em treinamento de redes neurais convolucionais. Seu objetivo é fornecer documentação e reproducibilidade aos experimentos realizados.

Com ele é possível descrever de maneira sucinta as etapas de pré-processamento dos dados e os parâmetros de configuração da rede, e executar o treinamento, gerando um relatório que descreve todas as configurações do experimento e os resultados obtidos.

Para começar a utilizar o framework, recomendamos realizar as etapas de instalação abaixo e experimentar com os exemplos disponíveis.

## Instalação

O *framework* requer Python 3 com Tensorflow 2 ou superior. Sua instalação atualmente se faz copiando o diretório [/src/exp](src/exp/) para a raiz do seu projeto, ou adicionando ele ao  [PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH) do seu ambiente.

As dependências do *framework* em si podem ser instaladas através do arquivo [requirements.txt](requirements.txt):

```
pip install -r requirements.txt
```

Recomendamos a utilização de um *[virtual environment](https://docs.python.org/3/library/venv.html)* para melhor gerenciar o ambiente de desenvolvimento. Como existem diversas maneiras de se instalar o Tensorflow, não incluímos essa dependência diretamente no requirements.txt.

## Exemplos

A fim de resolver questões de path e imports, é preciso utilizar a seguinte linha de comandos para executar os exemplos:

```
python src/run_sample.py [ARQUIVO PYTHON]
```

 - Selecionar as primeiras linhas de um dataset: [examples/filtering/first_count.py](src/examples/filtering/first_count.py)

- Selecionar as linhas onde uma coluna possui determinado valor: [examples/filtering/filter_by_column.py](src/examples/filtering/filter_by_column.py)

- Como trocar o valor de uma coluna: [examples/filtering/change_column_value.py](src/examples/filtering/change_column_value.py)

- Como treinar uma rede para classificar vacas e ovelhas: [examples/training/animal_classification_2classes.py](src/examples/training/animal_classification_2classes.py)

- Como treinar uma rede para classificar vacas, ovelhas, esquilos e borboletas: [examples/training/animal_classification_4classes.py](src/examples/training/animal_classification_4classes.py)

- Como treinar uma rede para classificar vacas, ovelhas, esquilos e borboletas, usando *loaders* para compensar a falta de imagens em uma das classes: [examples/training/animal_classification_4classes_imbalanced.py](src/examples/training/animal_classification_4classes_imbalanced.py)

## Documentação

 - [Documentação](docs/documentacao.md)
 - [Especificação Técnica](docs/especificacao_tecnica.md)
 - [Possíveis Melhorias](docs/melhorias.md)

## Observações

 - A documentação contida neste repositório foi escrita como parte da disciplina Projeto Final de Programação, do curso de Doutorado em Ciências - Informática da PUC-Rio.

 - Uma versão anterior do código contido neste repositório foi utilizada na elaboração do trabalho *Treating Dataset Imbalance in Fetal Echocardiography Classification* ([DOI](http://dx.doi.org/10.15439/2022F56)).

## Licença

Licenciado sobre a [licença MIT](LICENSE).
