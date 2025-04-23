# ENANI-2019: Análise de Aleitamento Materno Exclusivo

Este repositório contém scripts e análises dos dados do Estudo Nacional de Alimentação e Nutrição Infantil (ENANI-2019), com foco na classificação de crianças menores de 6 meses quanto ao aleitamento materno exclusivo (AME), seguindo os critérios da Organização Mundial da Saúde (OMS).

## Estrutura do Projeto

O projeto está organizado em etapas sequenciais, cada uma em seu próprio diretório:

1. **2 - menores de 6 meses**: Scripts para selecionar apenas crianças menores de 6 meses do dataset original do ENANI-2019.

2. **3 - definição desmame**: Scripts para classificar as crianças segundo o critério AME (Aleitamento Materno Exclusivo).
   - Classifica como AME (valor 1) crianças que recebem APENAS leite materno
   - Classifica como não-AME (valor 2) crianças que não recebem leite materno OU recebem outros alimentos/líquidos

3. **4 - arquivo final sem bloco E**: Scripts para simplificar o dataset, removendo as variáveis brutas do bloco E (consumo alimentar) e mantendo apenas a classificação AME.

4. **5 - limpeza e pre processamento**: Scripts para limpeza do dataset, removendo variáveis com alta proporção de dados faltantes (>30%) e variáveis com near-zero variance.

## Resultados Principais

A análise dos dados de 1.960 crianças menores de 6 meses revelou:

- **Total de crianças**: 1.960
- **Crianças em AME**: 920 (46,9%)
- **Crianças sem AME**: 1.040 (53,1%)

A coluna `aleitamento_materno_exclusivo` (AME) está na posição 691 do dataset final.

## Fluxo de Processamento

1. Seleção de crianças menores de 6 meses
2. Classificação quanto ao AME
3. Remoção das variáveis brutas de consumo alimentar
4. Limpeza para remover variáveis com muitos dados faltantes e baixa variabilidade
5. Geração do dataset final para análises estatísticas

## Como Utilizar

Cada diretório contém seu próprio README com instruções detalhadas sobre os scripts e como executá-los.

## Requisitos

- Python 3.6+
- Pandas
- NumPy
- Os datasets originais do ENANI-2019

## Autores

- Marcelo Silva 