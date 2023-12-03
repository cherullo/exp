# Documentação do framework exp

## Introdução

Durante o desenvolvimento de soluções envolvendo o uso de redes neurais, pesquisadores realizam diversos experimentos até convergir em uma rede treinada que cumpra os objetivos desejados. É um processo complexo, iterativo, onde os pesquisadores precisam analisar os resultados de cada etapa para saber quais parâmetros devem ser ajustados para o próximo experimento.

Assim, não basta que o resultado de cada um desses experimentos seja uma rede treinada, os pesquisadores precisam sistematicamente analisar diversos aspectos do processo de treinamento e da performance da rede obtida. Ou seja, o processo de treinamento precisa gerar também um conjunto de relatórios e gráficos de apoio, essenciais para que o pesquisador possa continuar o processo iterativo de refinamento da rede.

Nesse contexto, uma parte importante do trabalho do pesquisador está relacionado ao tratamento dos dados utilizados durante o treinamento. Dada uma massa de dados, é preciso importar, converter, tratar, selecionar e distribuir os dados nos conjuntos de treinamento, avaliação e testes. 

## Objetivos

O objetivo do framework exp é apoiar o processo iterativo de desenvolvimento de redes neurais através da estruturação dos experimentos em duas partes: sua descrição em python, e seu respectivo relatório de treinamento.

As classes do framework permitem ao pesquisador descrever as etapas de pré-processamento e os parâmetros de treinamento de uma rede neural, servindo naturalmente como documentação do experimento. 

O framework, por sua vez, deve realizar o treinamento baseado nesta descrição e gerar os respectivos relatórios, suportando o caso comum de mais de um pesquisador estar trabalhando no mesmo projeto, e mais de um experimento estar sendo realizado simultaneamente.

## Requisitos

### Requisitos Funcionais

### Requisitos Não-Funcionais

## Descrição

[Referência de classes](referencia.md)

### Descrição Funcional

## Cenários de Uso

### Cenário Adequado: Treinamento com datasets desbalanceados

### Cenário Adequado:

### Cenário Não-Adequado:

### Cenário Não-Adequado:
