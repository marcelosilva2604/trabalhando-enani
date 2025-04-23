# Análise Estatística Avançada

Esta pasta contém scripts e resultados da análise estatística avançada realizada para identificar a força e significância da associação entre a variável "aleitamento_materno_exclusivo" e outras variáveis do estudo.

## Scripts

- `analise_estatistica_avancada.py`: Script que analisa cada variável do dataset em relação ao aleitamento materno exclusivo, calculando:
  - Tipo de variável (categórica nominal, categórica ordinal, numérica discreta, numérica contínua)
  - Valor p para determinar significância estatística
  - Força da associação utilizando métodos apropriados ao tipo de variável
  - Classificação da força da associação
  - Método estatístico utilizado para cada análise

## Resultados Gerados

- `analise_associacoes.txt`: Arquivo de texto formatado com os resultados detalhados
- `analise_associacoes.csv`: Arquivo CSV com os mesmos resultados para facilitar análise em outros softwares

## Métodos Estatísticos Utilizados

Dependendo do tipo de variável, o script seleciona automaticamente o método estatístico mais apropriado:

- Para variáveis categóricas vs categóricas: Chi-quadrado e V de Cramer
- Para variáveis numéricas vs categóricas binárias: Correlação Point-Biserial
- Para variáveis numéricas vs categóricas com múltiplas categorias: ANOVA com Eta-squared
- Para variáveis com distribuições não normais: Testes não-paramétricos como Kruskal-Wallis
- Para relacionamentos ordinais: Correlação de Spearman ou Kendall's Tau

## Classificação da Força de Associação

A força da associação é classificada de acordo com o método utilizado, seguindo padrões estabelecidos na literatura estatística:

- Para V de Cramer:
  - < 0.1: Negligenciável
  - 0.1 - 0.2: Fraca
  - 0.2 - 0.3: Moderada
  - 0.3 - 0.4: Relativamente forte
  - > 0.4: Forte

- Para Correlações (Pearson, Spearman, Point-Biserial):
  - < 0.1: Negligenciável
  - 0.1 - 0.3: Fraca
  - 0.3 - 0.5: Moderada
  - 0.5 - 0.7: Relativamente forte
  - > 0.7: Forte

- Para Eta-squared (ANOVA):
  - < 0.01: Negligenciável
  - 0.01 - 0.06: Fraca
  - 0.06 - 0.14: Moderada
  - > 0.14: Forte 