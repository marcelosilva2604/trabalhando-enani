# Classificação de Aleitamento Materno Exclusivo (AME)

Este diretório contém scripts para classificação de crianças menores de 6 meses quanto ao aleitamento materno exclusivo, seguindo os critérios da Organização Mundial da Saúde (OMS).

## Visão Geral

O projeto consiste em analisar dados do ENANI-2019 (Estudo Nacional de Alimentação e Nutrição Infantil) para classificar crianças menores de 6 meses em duas categorias:

1. **Aleitamento Materno Exclusivo (AME)**: Crianças que recebem APENAS leite materno, sem nenhum outro alimento ou líquido
2. **Sem Aleitamento Materno Exclusivo**: Crianças que NÃO recebem leite materno OU recebem qualquer outro alimento/líquido

## Arquivos do Projeto

- **variaveis.py**: Script principal que realiza a classificação das crianças e gera um novo arquivo CSV com a classificação.
- **verificar_variaveis.py**: Script de análise exploratória dos dados para visualizar a distribuição das variáveis relevantes.
- **verificar_resultados.py**: Script para verificar a qualidade da classificação realizada.
- **criancas_menores_6_meses_classificadas.csv**: Arquivo de saída com a nova classificação.

## Metodologia

### Critérios de Classificação

- **AME (valor 1)**: Para ser classificada em AME, a criança deve:
  - Receber leite materno (`e01_leite_peito` = "Sim")
  - NÃO receber nenhum outro alimento ou líquido (todas as outras variáveis de alimento = "Não")

- **Não AME (valor 2)**: A criança será classificada como não estando em AME se:
  - NÃO receber leite materno (`e01_leite_peito` = "Não"), OU
  - Receber qualquer outro alimento ou líquido (qualquer variável de alimento = "Sim")

### Variáveis Utilizadas

As seguintes variáveis foram consideradas para determinar o consumo de outros alimentos:

- `e02_agua`: Água
- `e04_agua_com_acucar`: Água com açúcar
- `e05_cha`: Chá
- `e06_leite_vaca_po`: Leite de vaca em pó
- `e07_leite_vaca_liquido`: Leite de vaca líquido
- `e08_leite_soja_po`: Leite de soja em pó
- `e09_leite_soja_liquido`: Leite de soja líquido
- `e10_formula_infantil`: Fórmula infantil
- `e11_suco`: Suco natural
- `e12_fruta_inteira`: Fruta
- `e14_manga`: Manga, mamão ou goiaba
- `e16_comida_sal`: Comida de sal
- `e19_mingau`: Mingau ou papa com leite
- `e20_iogurte`: Iogurte
- `e21_arroz`: Arroz, batata, etc.
- `e21a_pao`: Pão
- `e22_legumes`: Legumes
- `e23_cenoura`: Cenoura, abóbora, batata doce
- `e24_couve`: Couve, espinafre, etc.
- `e25_verduras`: Outras verduras
- `e26_feijao`: Feijão ou outros grãos
- `e27_carne`: Carne
- `e28_figado`: Fígado
- `e29_ovo`: Ovo
- `e30_hamburger`: Hambúrguer, presunto, etc.
- `e31_salgadinhos`: Salgadinhos de pacote
- `e32_suco_industrializado`: Suco industrializado
- `e33_refrigerante`: Refrigerante
- `e34_macarrao`: Macarrão instantâneo
- `e35_biscoito`: Biscoito/bolacha
- `e36_bala`: Bala, pirulito
- `e37_tempero`: Tempero pronto industrializado
- `e38_farinhas`: Farinhas instantâneas
- `e40_adocado`: Alimento adoçado

## Resultados

A análise dos dados de 1.960 crianças menores de 6 meses revelou:

- **Total de crianças**: 1.960
- **Crianças em AME**: 920 (46,9%)
- **Crianças sem AME**: 1.040 (53,1%)

### Exemplos de Classificação

**Crianças em AME**:
- Recebem leite materno ("Sim")
- Não recebem água ("Não")
- Não recebem outros alimentos ou líquidos ("Não")

**Crianças não em AME**:
- Não recebem leite materno, OU
- Recebem leite materno mas também recebem água, fórmula infantil ou outros alimentos

## Como Executar os Scripts

1. **Para realizar a classificação**:
   ```
   python variaveis.py
   ```
   Isso criará o arquivo `criancas_menores_6_meses_classificadas.csv` com a nova classificação.

2. **Para verificar as variáveis**:
   ```
   python verificar_variaveis.py
   ```
   Este script mostra a distribuição das principais variáveis utilizadas na classificação.

3. **Para verificar os resultados da classificação**:
   ```
   python verificar_resultados.py
   ```
   Este script mostra exemplos de crianças classificadas em cada categoria e as estatísticas gerais.

## Notas Importantes

- Os dados originais estão no formato de texto ("Sim"/"Não") e não numérico (1/0)
- A análise considera apenas as variáveis do bloco E (consumo alimentar) do ENANI-2019
- A classificação segue rigorosamente as diretrizes da OMS para definição de AME 