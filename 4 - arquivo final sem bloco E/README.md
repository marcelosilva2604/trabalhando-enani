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
- **reorganizar_csv.py**: Script que reorganiza o CSV movendo a coluna 'aleitamento_materno_exclusivo' para a primeira posição (coluna A)
- **criancas_menores_6_meses_reorganizado.csv**: Arquivo final reorganizado com a coluna AME na primeira posição

## Fluxograma de Transformação de Features

```
┌───────────────────────┐
│ Conjunto Original     │
│ Total: 742 features   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Remoção do Bloco E    │
│ (51 features removidas)│
│                       │
│ Motivo: Bloco E define│
│ aleitamento materno e │
│ não é fator preditivo │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Adição da feature     │
│ 'aleitamento_materno_ │
│ exclusivo'            │
│ (+1 feature derivada) │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Conjunto Final        │
│ Total: 691 features   │
│ (742 - 51 + 0 = 691)  │
└───────────────────────┘
```

**Observações:**
- Foram retiradas 51 features do bloco E, que representavam informações brutas de consumo alimentar
- A feature "aleitamento_materno_exclusivo" já havia sido criada na etapa anterior a partir do bloco E
- O bloco E foi removido pois seus dados já foram utilizados para criar a classificação AME, que é o objetivo principal da análise
- As 51 features do bloco E não são fatores preditivos neste caso, mas sim as variáveis que definem o desfecho (AME)
- O conjunto final possui 691 features, com a coluna de AME reorganizada para a primeira posição para facilitar a análise

## Como Executar

Para executar o script e gerar o arquivo sem o bloco E, utilize:

```
python remover_bloco_e.py
```

Para reorganizar o arquivo e mover a coluna AME para a primeira posição:

```
python reorganizar_csv.py
```

## Resultados Esperados

O script de remoção irá:
1. Carregar o arquivo completo da pasta anterior
2. Identificar e remover todas as colunas que começam com 'e' seguido de números (bloco E)
3. Manter a coluna 'aleitamento_materno_exclusivo' criada anteriormente
4. Salvar um novo arquivo CSV sem as colunas do bloco E

O script de reorganização irá:
1. Carregar o arquivo sem o bloco E
2. Identificar a posição da coluna 'aleitamento_materno_exclusivo'
3. Mover essa coluna para a primeira posição (coluna A) no CSV
4. Salvar um novo arquivo reorganizado para facilitar a análise

## Próximos Passos

Com esta versão simplificada e reorganizada do conjunto de dados, você pode proceder com:

1. Análises estatísticas da prevalência de AME
2. Cruzamentos com outras variáveis socioeconômicas e demográficas
3. Visualizações gráficas dos resultados
4. Modelagem estatística para identificar determinantes do AME 