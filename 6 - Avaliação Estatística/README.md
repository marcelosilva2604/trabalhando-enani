# Avaliação Estatística

Esta etapa do projeto realiza a avaliação estatística das features em relação à variável alvo "aleitamento_materno_exclusivo", com o objetivo de identificar quais features possuem relação estatística significativa (p<0,05) com o desfecho.

## Objetivo

Os objetivos desta etapa são:

1. **Classificar as features** em qualitativas ou quantitativas
2. **Aplicar testes estatísticos apropriados** para cada tipo de feature:
   - Teste Chi-quadrado ou Teste Exato de Fisher para features qualitativas
   - Teste t ou Mann-Whitney U para features quantitativas
3. **Identificar features estatisticamente significativas** (p<0,05)
4. **Criar um novo dataset** apenas com as features significativas

## Metodologia

### Classificação das Features

As features foram classificadas em:

- **Qualitativas**: Features categóricas ou numéricas com baixa cardinalidade (≤10 valores únicos)
- **Quantitativas**: Features numéricas contínuas ou com alta cardinalidade

### Fluxograma da Análise Estatística

```
┌─────────────────────┐
│ Dataset Final       │
│ (265 features)      │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Classificação das   │
│ features:           │
│ • Qualitativas (186)│
│ • Quantitativas (78)│
└─────────┬───────────┘
          │
          ▼
┌───────────────────────────┐
│ Features Qualitativas     │
│ • Chi-quadrado: 186       │
│ • Teste Exato Fisher: 0   │
└────────────┬──────────────┘
             │
             │    ┌───────────────────────┐
             │    │ Teste de Normalidade  │
             │    │ para Quantitativas    │
             │    └───────────┬───────────┘
             │                │
             │    ┌───────────┴───────────┐
             │    │ Distribuição Normal?  │
             │    └───────────┬───────────┘
             │                │
┌────────────┴─────┐  ┌───────┴──────┐ ┌────────────┐
│ Features         │  │ Sim (1)      │ │ Não (77)   │
│ Qualitativas     │  └───────┬──────┘ └─────┬──────┘
└────────────┬─────┘          │              │
             │        ┌───────┴──────┐ ┌─────┴──────┐
             │        │ t-test       │ │ Mann-      │
             │        └───────┬──────┘ │ Whitney U  │
             │                │        └─────┬──────┘
             ▼                ▼              ▼
┌────────────────────────────────────────────────────┐
│ Seleção de features com p<0.05                     │
│ (139 features)                                     │
└────────────────────────────┬───────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────┐
│ Dataset Final Estatisticamente Significativo       │
│ (139 features)                                     │
└────────────────────────────────────────────────────┘
```

### Testes Estatísticos Aplicados

Para cada tipo de feature, foram aplicados testes apropriados:

1. **Features Qualitativas**:
   - **Teste Chi-quadrado**: Para tabelas de contingência com valores esperados adequados
   - **Teste Exato de Fisher**: Para tabelas 2x2 com valores esperados pequenos (<5)

2. **Features Quantitativas**:
   - **Teste t (t-test)**: Para dados com distribuição normal
   - **Teste Mann-Whitney U**: Para dados sem distribuição normal

### Critério de Significância

Foi adotado o nível de significância estatística de 5% (p<0,05) para selecionar as features relevantes para a variável alvo.

## Arquivos Gerados

1. **dataset_f_est.csv**: Dataset contendo apenas as features estatisticamente significativas
2. **resultados/relatorio_estatistico_completo.csv**: Relatório completo com todas as features, classificação, teste aplicado e p-valor
3. **resultados/features_excluidas.csv**: Lista de features que não apresentaram relação estatisticamente significativa

## Script Utilizado

### analise_estatistica_melhorado.py

Este script:
1. Carrega o dataset final da etapa anterior
2. Verifica a disponibilidade da biblioteca SciPy e implementa alternativas se necessário
3. Classifica cada feature como qualitativa ou quantitativa
4. Verifica a normalidade das distribuições das variáveis quantitativas
5. Aplica o teste estatístico apropriado para cada feature:
   - Chi-quadrado ou Teste Exato de Fisher para features qualitativas
   - t-test (para distribuições normais) ou Mann-Whitney U (para distribuições não normais)
6. Identifica features com relação estatisticamente significativa (p<0,05)
7. Gera um novo dataset apenas com as features significativas
8. Cria relatórios detalhados sobre a análise

## Como Executar

Para executar a análise estatística:

```
python analise_estatistica_melhorado.py
```

Para gerar o arquivo de features excluídas:

```
python converter_csv_para_txt_melhorado.py
```

## Resultados

Os resultados obtidos incluem:

- **Total de features analisadas**: 264
- **Features estatisticamente significativas**: 139 (52,7%)
- **Features não significativas**: 125 (47,3%)

### Testes Aplicados

A análise estatística verificou com sucesso a normalidade das distribuições das variáveis quantitativas e aplicou os testes apropriados:

1. **Features Qualitativas**:
   - Chi-quadrado: 186 features
   - Teste Exato de Fisher: 0 features (nenhuma tabela 2x2 com valores esperados pequenos)

2. **Features Quantitativas**:
   - t-test: 1 feature (com distribuição normal verificada)
   - Mann-Whitney U: 77 features (sem distribuição normal)

### Aplicação Correta dos Testes

A nova análise demonstrou a importância de verificar a normalidade das distribuições:
- Para as variáveis quantitativas, 77 features foram testadas com Mann-Whitney U (98,7% das features quantitativas)
- Apenas 1 feature quantitativa apresentou distribuição normal suficiente para aplicação do t-test

As 5 features com maior significância estatística (menores p-valores) foram:

1. **k25_mamadeira** (p ≈ 6.1e-159)
2. **h05_chupeta_usou** (p ≈ 2.8e-32)
3. **b05a_idade_em_meses** (p ≈ 1.9e-28)
4. **i000c_idade_em_meses** (p ≈ 1.9e-28)
5. **k24_utilizou** (p ≈ 6.8e-23)

Estes resultados demonstram que há associações estatisticamente significativas entre várias características materno-infantis e a prática de aleitamento materno exclusivo.

## Próximos Passos

Com as features estatisticamente significativas identificadas, os próximos passos podem incluir:

1. Análise mais detalhada das features significativas
2. Modelagem preditiva usando apenas as features selecionadas
3. Análise de importância relativa das features significativas 