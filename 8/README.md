# Análise de Variabilidade de Features

Este diretório contém scripts e análises destinados a revisar as features do dataset para avaliar respostas com baixa variabilidade.

## Objetivo

O principal objetivo desta análise é identificar features que possuem baixa variabilidade nos dados, ou seja, aquelas onde a grande maioria das respostas está concentrada em um único valor. Features com baixa variabilidade tendem a contribuir pouco para modelos preditivos e podem ser candidatas à remoção para simplificar o dataset.

## Critérios Utilizados na Pasta 5

Na etapa anterior de limpeza (pasta 5), foram utilizados os seguintes critérios para identificar e remover features com baixa variabilidade:

1. **Features com near-zero variance**: Features foram consideradas com baixa variabilidade quando:
   - A razão entre a frequência do valor mais comum e a do segundo mais comum é alta (>19)
   - A porcentagem de valores únicos em relação ao total de observações é baixa (<10%)

2. Foram removidas um total de 194 features por apresentarem baixa variabilidade, além de 301 features por terem mais de 30% de dados faltantes.

## Análise Atual (Pasta 8)

Nesta etapa, estamos realizando uma reavaliação das features restantes para identificar outras que ainda apresentam baixa variabilidade. Os principais critérios considerados são:

- Features onde mais de 90% das respostas correspondem a um único valor
- Features com distribuição extremamente desequilibrada

## Análise Realizada

- Avaliação da distribuição percentual de respostas para cada feature
- Identificação de features onde mais de 90% das respostas correspondem a um único valor
- Análise detalhada da distribuição de idades em meses (b05a_idade_em_meses)

## Resultados

A análise identificou features adicionais com baixa variabilidade que podem ser removidas do dataset para otimizar os modelos subsequentes. 