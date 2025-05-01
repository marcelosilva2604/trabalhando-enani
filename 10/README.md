# Otimização do Modelo e Melhoria do AUC

Este diretório contém o código e os resultados de otimização do nosso modelo preditivo para aleitamento materno exclusivo (AME) utilizando técnicas de boosting.

## Resumo da Otimização

Nesta etapa, implementamos melhorias significativas em nosso modelo preditivo através de:

1. **Ajuste fino de hiperparâmetros**: Utilizamos técnicas de otimização para encontrar a melhor configuração do modelo XGBoost.

2. **Técnicas avançadas de boosting**: Implementamos algoritmos de boosting que melhoraram a capacidade preditiva do modelo.

3. **Validação cruzada robusta**: Garantimos que os resultados fossem consistentes através de múltiplas divisões dos dados.

## Resultados Alcançados

A otimização do modelo resultou em uma melhoria significativa no desempenho:

- **AUC (Area Under Curve) superior**: Conseguimos aumentar o valor do AUC em comparação com os modelos anteriores.
- **Melhor equilíbrio entre sensibilidade e especificidade**: O modelo otimizado apresenta uma capacidade superior de identificar corretamente tanto os casos positivos quanto negativos.
- **Maior robustez**: O modelo demonstrou menor variância entre diferentes subconjuntos de dados.

## Estrutura do Diretório

- `xgboost.py`: Script principal contendo o código de otimização do modelo XGBoost
- `resultados_xgboost_otimizado/`: Diretório com os resultados detalhados do modelo otimizado
- `resultados_boosting_otimizado/`: Diretório com análises adicionais do modelo de boosting

## Próximos Passos

Com base nesse modelo otimizado, podemos:

1. Implementar o modelo em ambientes de produção
2. Realizar análises de importância de features para entender melhor os fatores que influenciam o AME
3. Desenvolver ferramentas de suporte à decisão para profissionais de saúde 