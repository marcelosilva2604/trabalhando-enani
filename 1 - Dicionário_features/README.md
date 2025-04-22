# Dicionário de Features ENANI / ENANI Features Dictionary

## Português

### Passo 1: Criação do Dicionário de Features

Neste primeiro passo, extraímos todas as variáveis (features) presentes no banco de dados CSV do estudo ENANI-2019 e as organizamos em um formato estruturado e de fácil consulta. O processo envolveu:

1. **Extração das variáveis**: Identificamos 742 variáveis únicas do arquivo "4-Dicionario-ENANI-2019 (1).xlsx".
2. **Estruturação dos dados**: Para cada variável, documentamos:
   - Nome da variável (ex: a00_regiao)
   - Significado/descrição da variável (ex: a00_regiao - Macrorregião)
   - Todos os valores possíveis e seus significados (ex: 1 - Norte, 2 - Nordeste, etc.)
3. **Organização**: As variáveis foram organizadas em ordem alfabética para facilitar a consulta.

Os arquivos nesta pasta incluem:
- **features_enani.txt**: Dicionário completo com todas as variáveis e seus valores possíveis
- **gerar_features.py**: Script que extrai as informações do arquivo original e gera o dicionário
- **contar_variaveis.py**: Script que analisa e exibe estatísticas sobre o dicionário gerado

Este dicionário serve como referência fundamental para entender as variáveis presentes nos arquivos CSV do estudo ENANI-2019, facilitando análises futuras.

## English

### Step 1: Creation of the Features Dictionary

In this first step, we extracted all variables (features) present in the ENANI-2019 study CSV database and organized them in a structured, easy-to-consult format. The process involved:

1. **Variable extraction**: We identified 742 unique variables from the "4-Dicionario-ENANI-2019 (1).xlsx" file.
2. **Data structuring**: For each variable, we documented:
   - Variable name (e.g., a00_regiao)
   - Meaning/description of the variable (e.g., a00_regiao - Macroregion)
   - All possible values and their meanings (e.g., 1 - North, 2 - Northeast, etc.)
3. **Organization**: The variables were organized in alphabetical order to facilitate consultation.

The files in this folder include:
- **features_enani.txt**: Complete dictionary with all variables and their possible values
- **gerar_features.py**: Script that extracts information from the original file and generates the dictionary
- **contar_variaveis.py**: Script that analyzes and displays statistics about the generated dictionary

This dictionary serves as a fundamental reference for understanding the variables present in the ENANI-2019 study CSV files, facilitating future analyses. 