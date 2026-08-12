# Mini-Projeto Avaliativo — Machine Learning e Visão Computacional [T3]
### Módulo 1 - Semana 07

## Descrição do Projeto

A Olist, empresa líder em e-commerce, extraiu lotes de dados brutos (olist_products_dataset.csv e olist_orders_dataset.csv) que apresentam inconsistências: valores nulos, categorias de produto mal formatadas e datas em formatos não padronizados. O objetivo deste projeto é construir, em Python puro (sem uso de bibliotecas externas como Pandas), um pipeline de sanitização que trate esses problemas.

## Guia de Execução

1. Coloque os arquivos olist_products_dataset.csv e olist_orders_dataset.csv na mesma pasta dos scripts.
2. Certifique-se de ter o Python 3 instalado.
3. Execute:
python main.py
4. O relatório de sanitização será exibido no terminal.

## Reflexão Teórica sobre Machine Learning

Um modelo de Machine Learning só é bom se os dados usados para treiná-lo forem bons — é o famoso Garbage In, Garbage Out: se os dados de entrada forem ruins, o resultado também será. Se deixarmos valores nulos, categorias mal escritas ou datas em formatos diferentes na base, o modelo pode aprender coisas erradas e passar a errar quando for usado com dados reais (isso é o overfitting, quando o modelo "decora" o que viu, em vez de aprender de verdade).

Por isso, a limpeza feita neste projeto — preencher categorias vazias, padronizar textos, corrigir datas e conferir se os pedidos cancelados realmente batem com as entregas nulas — ajuda a deixar a base mais confiável. Com dados organizados e consistentes, um futuro modelo de Machine Learning tem mais chance de aprender padrões reais do negócio, em vez de erros que vieram da própria bagunça dos dados.