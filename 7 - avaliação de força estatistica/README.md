# Análise Estatística Avançada - Aleitamento Materno Exclusivo

Esta pasta contém scripts e resultados da análise estatística avançada realizada para identificar a força e significância da associação entre a variável "aleitamento_materno_exclusivo" e as demais variáveis do estudo ENANI-2019. A análise busca determinar quais fatores estão mais fortemente associados ao aleitamento materno exclusivo em crianças menores de 6 meses.

## Scripts Disponíveis

- `gerar_significado_variaveis.py`: Script principal que:
  - Extrai significados das variáveis do dicionário do ENANI-2019
  - Gera um dicionário completo das variáveis presentes no dataset
  - Cria um resumo detalhado da análise estatística
  - Aprimora o resumo adicionando significados das variáveis mais importantes

- `resumo_resultados.py`: Script auxiliar que gera um resumo da análise estatística com:
  - Visão geral dos resultados
  - Distribuição por classificação de força
  - Top 20 variáveis mais fortemente associadas
  - Métodos estatísticos utilizados
  - Distribuição por tipo de variável
  - Conclusões principais

## Arquivos Gerados

- `dicionario_variaveis.txt`: Dicionário completo de todas as variáveis presentes no dataset, incluindo:
  - Significado de cada variável conforme o dicionário ENANI-2019
  - Valores possíveis para variáveis categóricas

- `resumo_analise.txt`: Resumo básico da análise estatística com resultados

- `resumo_analise_completo.txt`: Versão aprimorada do resumo que adiciona:
  - Significados detalhados das variáveis mais importantes
  - Valores possíveis para cada variável categórica relevante
  - Melhor interpretação dos resultados estatísticos

- `analise_associacoes.csv`: Arquivo CSV com resultados completos da análise para todas as variáveis

## Metodologia Estatística

A análise utiliza métodos estatísticos específicos para cada tipo de variável, garantindo uma avaliação precisa da associação com aleitamento materno exclusivo:

### Tipos de Variáveis Identificadas Automaticamente

- **Categórica nominal**: Variáveis qualitativas sem ordem natural (ex: região geográfica)
- **Categórica ordinal**: Variáveis qualitativas com ordem natural (ex: nível de escolaridade)
- **Numérica discreta**: Variáveis quantitativas com valores inteiros (ex: idade em meses)
- **Numérica contínua**: Variáveis quantitativas com valores decimais (ex: peso em kg)

### Métodos Estatísticos Aplicados

- **Para variáveis categóricas**: Chi-quadrado com V de Cramer para mensurar força de associação
- **Para variáveis numéricas vs categóricas binárias**: Correlação Point-Biserial
- **Para variáveis numéricas vs categóricas múltiplas**: ANOVA com Eta-squared
- **Para distribuições não-normais**: Testes não-paramétricos (Kruskal-Wallis)
- **Para relacionamentos ordinais**: Correlações de Spearman ou Kendall's Tau

### Classificação da Força de Associação

A força da associação é classificada conforme padrões estabelecidos na literatura científica:

- **Para V de Cramer**:
  - < 0.1: Negligenciável
  - 0.1 - 0.2: Fraca
  - 0.2 - 0.3: Moderada
  - 0.3 - 0.4: Relativamente forte
  - > 0.4: Forte

- **Para Correlações** (Pearson, Spearman, Point-Biserial):
  - < 0.1: Negligenciável
  - 0.1 - 0.3: Fraca
  - 0.3 - 0.5: Moderada
  - 0.5 - 0.7: Relativamente forte
  - > 0.7: Forte

- **Para Eta-squared (ANOVA)**:
  - < 0.01: Negligenciável
  - 0.01 - 0.06: Fraca
  - 0.06 - 0.14: Moderada
  - > 0.14: Forte

## Principais Resultados

A análise identificou 5 variáveis com associação forte ou relativamente forte ao aleitamento materno exclusivo:

1. **k25_mamadeira** (Forte, 0.6815): Uso de mamadeira pela criança
2. **k18_somente** (Relativamente forte, 0.6177): Tempo de aleitamento materno exclusivo
3. **b05a_idade_em_meses** (Relativamente forte, 0.3489): Idade da criança em meses
4. **i000c_idade_em_meses** (Relativamente forte, 0.3231): Idade recalculada em meses
5. **k14_ainda** (Relativamente forte, 0.3060): Continuidade do aleitamento materno

Estas variáveis são prioritárias para análises mais aprofundadas e potenciais intervenções relacionadas ao aleitamento materno exclusivo.

## Como Utilizar

Para gerar novamente a análise completa com o dicionário de variáveis e resumos:

```bash
python gerar_significado_variaveis.py
```

O script utilizará o arquivo de dicionário do ENANI localizado em `./1 - Dicionário_features/features_enani.txt` e os resultados da análise estatística em `./7 - avaliação de força estatistica/analise_associacoes.csv` para gerar os arquivos.

## Referências Metodológicas

- Cohen, J. (1988). Statistical power analysis for the behavioral sciences (2nd ed.). Lawrence Erlbaum Associates.
- Cramér, H. (1946). Mathematical Methods of Statistics. Princeton University Press.
- Lakens, D. (2013). Calculating and reporting effect sizes to facilitate cumulative science: A practical primer for t-tests and ANOVAs. Frontiers in Psychology, 4, 863. 