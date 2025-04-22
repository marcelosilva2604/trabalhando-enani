# Arquivo Final Sem Bloco E

Esta pasta contém o resultado final do processamento dos dados do ENANI-2019, com a remoção das variáveis brutas do bloco E (consumo alimentar) e a manutenção apenas da classificação de Aleitamento Materno Exclusivo (AME) que foi criada na etapa anterior.

## Objetivo

O objetivo deste processamento é simplificar o conjunto de dados, removendo as variáveis brutas de consumo alimentar (bloco E) que já foram utilizadas para criar a classificação AME. Esta limpeza:

1. Reduz o tamanho do arquivo de dados
2. Simplifica a análise futura, mantendo apenas a classificação final
3. Facilita o compartilhamento dos dados com outros pesquisadores
4. Torna o conjunto de dados mais focado e organizado

## Arquivos

- **remover_bloco_e.py**: Script que remove as colunas do bloco E do conjunto de dados e mantém a classificação AME
- **criancas_menores_6_meses_classificadas_sem_bloco_e.csv**: Arquivo final com a remoção do bloco E e a manutenção da classificação AME

## Como Executar

Para executar o script e gerar o arquivo sem o bloco E, utilize:

```
python remover_bloco_e.py
```

## Resultados Esperados

O script irá:
1. Carregar o arquivo completo da pasta anterior
2. Identificar e remover todas as colunas que começam com 'e' seguido de números (bloco E)
3. Manter a coluna 'aleitamento_materno_exclusivo' criada anteriormente
4. Salvar um novo arquivo CSV sem as colunas do bloco E

## Próximos Passos

Com esta versão simplificada do conjunto de dados, você pode proceder com:

1. Análises estatísticas da prevalência de AME
2. Cruzamentos com outras variáveis socioeconômicas e demográficas
3. Visualizações gráficas dos resultados
4. Modelagem estatística para identificar determinantes do AME 