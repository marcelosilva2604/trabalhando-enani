# Limpeza e Pré-processamento dos Dados

Esta etapa do projeto realiza a limpeza e pré-processamento do dataset de crianças menores de 6 meses classificadas quanto ao Aleitamento Materno Exclusivo (AME).

## Objetivo

Esta etapa teve como objetivo simplificar o dataset através de:

1. **Remoção de variáveis com alta proporção de dados faltantes** (>30% de NA)
2. **Remoção de variáveis com near-zero variance** (variáveis com pouca ou nenhuma variabilidade)
3. **Reordenação do dataset final** para posicionar a variável 'aleitamento_materno_exclusivo' como primeira coluna

## Fluxo de Trabalho

┌───────────────────────┐
│ Dataset Original ENANI│
│ (N registros)         │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Filtro: Crianças      │
│ menores de 6 meses    │
│ Resultado: 1.960      │
│ registros             │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Criação da feature    │
│ 'aleitamento_materno_ │
│ exclusivo'            │
│ (+1 feature derivada) │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Remoção do Bloco E    │
│ (51 features removidas)│
│                       │
│ Motivo: Bloco E define│
│ desfecho e não é      │
│ fator preditivo       │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Dataset Intermediário │
│ 691 features          │
│ (742 - 51 + 0 = 691)  │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Remoção de features   │
│ com >30% dados        │
│ faltantes             │
│ (301 features)        │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Remoção de features   │
│ com near-zero variance│
│ (194 features)        │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Total features        │
│ removidas: 426        │
│ (algumas em ambos     │
│ os critérios)         │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Dataset Final         │
│ 265 features          │
│ 1.960 registros       │
│ AME: 920 (46,9%)      │
│ Não AME: 1.040 (53,1%)│
└───────────────────────┘

## Arquivos Gerados

1. **dataset_limpo.csv**: Dataset após remoção das features problemáticas
2. **dataset_final.csv**: Dataset com a variável AME posicionada como primeira coluna
3. **features_excluidas_motivo.txt**: Lista de todas as features excluídas e seus motivos

## Scripts Utilizados

### 1. limpar_dataset.py

Este script realiza a limpeza do dataset, removendo:

- Variáveis com mais de 30% de dados faltantes (301 features)
- Variáveis com near-zero variance (313 features)
- Total: 426 features únicas removidas (algumas se encaixavam em ambos os critérios)

Ele utiliza dois critérios principais:

- Percentual de dados faltantes > 30%
- Near-zero variance, quando:
  - A razão entre a frequência do valor mais comum e a do segundo mais comum é alta (>19)
  - A porcentagem de valores únicos em relação ao total de observações é baixa (<10%)

### 2. reorganizar_dataset.py

Este script reorganiza o dataset limpo, movendo a variável 'aleitamento_materno_exclusivo' para a primeira posição no dataset, para facilitar visualização e análises futuras.

### 3. features_excluidas_simplificado.py

Este script gera um relatório detalhado das features excluídas, categorizando-as por motivo de exclusão:

- Features excluídas por terem mais de 30% de dados faltantes
- Features excluídas por terem baixa variabilidade

## Resultados

O processo de limpeza resultou em:

- **Dataset original**: 691 colunas
- **Dataset final**: 265 colunas (redução de 61.6%)
- **Features removidas por dados faltantes**: 301
- **Features removidas por baixa variabilidade**: 194
- **Total de features removidas**: 426

A variável alvo 'aleitamento_materno_exclusivo' foi preservada e posicionada como primeira coluna do dataset final.

## Distribuição Final do AME

```
aleitamento_materno_exclusivo
2    1040  (53.1%)
1     920  (46.9%)
```

O percentual de crianças em Aleitamento Materno Exclusivo permaneceu em 46.9% após todo o processo de limpeza.

## Como Executar

Os scripts devem ser executados na seguinte ordem:

1. Para limpar o dataset:

   ```
   python3 limpar_dataset.py
   ```
2. Para reorganizar o dataset (mover AME para primeira coluna):

   ```
   python3 reorganizar_dataset.py
   ```
3. Para gerar relatório de features excluídas:

   ```
   python3 features_excluidas_simplificado.py
   ```

## Próximos Passos

Com o dataset limpo e organizado, é possível prosseguir para:

1. Análise exploratória de dados
2. Modelagem estatística
3. Identificação de fatores associados ao AME
