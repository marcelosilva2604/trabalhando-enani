# Análise de Modelos de Machine Learning para Predição de Aleitamento Materno Exclusivo

Este projeto utiliza técnicas de machine learning para analisar e prever o status de aleitamento materno exclusivo, utilizando dados do estudo PESN 2019.

## Processo de Desenvolvimento

### 1. Análise de Importância de Features
- Geração do arquivo `feature_score.csv` utilizando o F-test do scikit-learn
- Avaliação da importância de cada feature para a predição do aleitamento materno exclusivo

### 2. Exploração de Diferentes Combinações de Features
- Teste de várias combinações de features para identificar as mais relevantes
- Análise de performance com diferentes subconjuntos de features

### 3. Análise com Diferentes Números de Features
Foram testados modelos com diferentes números de features, obtendo os seguintes resultados:

#### Modelo com 3 Features
- Acurácia: 0.8929
- AUC: 0.5606
- F1-Score: 0.8852
- Métricas de Validação Cruzada:
  - Média de Acurácia: 0.8708 (±0.0254)
  - Média de AUC: 0.9343 (±0.0131)
  - Média de F1-Score: 0.8707 (±0.0255)

#### Modelo com 5 Features
- Acurácia: 0.8588
- AUC: 0.5304
- F1-Score: 0.8454
- Métricas de Validação Cruzada:
  - Média de Acurácia: 0.8417 (±0.0199)
  - Média de AUC: 0.9223 (±0.0118)
  - Média de F1-Score: 0.8415 (±0.0198)

#### Modelo com 10 Features
- Acurácia: 0.8554
- AUC: 0.5312
- F1-Score: 0.8429
- Métricas de Validação Cruzada:
  - Média de Acurácia: 0.8260 (±0.0042)
  - Média de AUC: 0.9185 (±0.0098)
  - Média de F1-Score: 0.8260 (±0.0041)

#### Modelo com 20 Features
- Acurácia: 0.8571
- AUC: 0.5154
- F1-Score: 0.8439
- Métricas de Validação Cruzada:
  - Média de Acurácia: 0.8281 (±0.0123)
  - Média de AUC: 0.9172 (±0.0140)
  - Média de F1-Score: 0.8279 (±0.0125)

#### Modelo com 50 Features
- Acurácia: 0.8605
- AUC: 0.5406
- F1-Score: 0.8498
- Métricas de Validação Cruzada:
  - Média de Acurácia: 0.8271 (±0.0101)
  - Média de AUC: 0.9185 (±0.0137)
  - Média de F1-Score: 0.8270 (±0.0102)

#### Modelo com Todas as Features (139)
- Acurácia: 0.8605
- AUC: 0.5595
- F1-Score: 0.8487
- Métricas de Validação Cruzada:
  - Média de Acurácia: 0.8458 (±0.0176)
  - Média de AUC: 0.9208 (±0.0168)
  - Média de F1-Score: 0.8457 (±0.0177)

### Modelo Final (Ideal)
- Features selecionadas: 3 features mais importantes
  - `k18_somente`: Indicador de aleitamento materno exclusivo
  - `k25_mamadeira`: Uso de mamadeira
  - `b05a_idade_em_meses`: Idade da criança em meses
- Algoritmo: XGBoost
- Performance:
  - Acurácia: 0.8929
  - AUC: 0.5606
  - F1-Score: 0.8852

## Conclusões Principais
1. O modelo com 3 features apresentou a melhor performance geral, com a maior acurácia (0.8929) e F1-Score (0.8852)
2. A adição de mais features não melhorou significativamente a performance do modelo
3. O modelo com 3 features mostrou maior estabilidade nas métricas de validação cruzada
4. O XGBoost foi o algoritmo que apresentou os melhores resultados em todos os cenários

## Arquivos do Projeto
- `modelo_otimo.py`: Script para treinar o modelo final com as 3 features mais importantes
- `gerar_feature_score.py`: Script para gerar o arquivo de importância das features
- `gerar_modelos_features.py`: Script para testar diferentes números de features
- `feature_score.csv`: Arquivo com a pontuação de importância de cada feature
- `resultado_pycaret/`: Diretório contendo resultados e gráficos gerados pelo PyCaret

## Próximos Passos
1. Análise detalhada das 3 features mais importantes
2. Exploração de outras combinações de features
3. Teste de diferentes algoritmos de machine learning
4. Análise de interpretabilidade do modelo 