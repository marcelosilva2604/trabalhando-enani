import pandas as pd
import os
import numpy as np

# Definir caminhos
input_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                         '/Users/marcelosilva/Desktop/artigo_novo/4 - arquivo final sem bloco E/criancas_menores_6_meses_reorganizado.csv')
output_path = os.path.join(os.path.dirname(__file__), 'dataset_limpo.csv')

def identificar_near_zero_var(df, freq_cut=19, unique_cut=10):
    """
    Identifica variáveis com near-zero variance segundo Kuhn & Johnson (2013).
    
    Parameters:
    -----------
    df : pandas.DataFrame
        O conjunto de dados a ser analisado
    freq_cut : float, default=19
        Limiar para a razão entre a frequência do valor mais comum e a do segundo mais comum
    unique_cut : float, default=10
        Limiar para a porcentagem de valores únicos (%)
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame com métricas e sinalizadores para variáveis com near-zero variance
    """
    resultados = pd.DataFrame(index=df.columns)
    
    for coluna in df.columns:
        # Ignorar valores missing
        dados = df[coluna].dropna()
        
        # Verificar se há dados após remover os valores nulos
        if len(dados) == 0:
            # Se a coluna tem apenas valores nulos, consideramos zero variance
            resultados.loc[coluna, 'freq_ratio'] = float('inf')
            resultados.loc[coluna, 'percent_unique'] = 0.0
            resultados.loc[coluna, 'zero_var'] = True
            resultados.loc[coluna, 'near_zero_var'] = True
            continue
            
        # Calcular tabela de frequência dos valores
        freq_tabela = dados.value_counts().sort_values(ascending=False)
        
        # Calcular razão de frequência
        if len(freq_tabela) >= 2:
            freq_ratio = freq_tabela.iloc[0] / freq_tabela.iloc[1]
        else:
            freq_ratio = float('inf')  # Para o caso de valor único
        
        # Calcular porcentagem de valores únicos
        percent_unique = (len(freq_tabela) / len(dados)) * 100
        
        # Verificar se é zero-variance (valor único)
        zero_var = len(freq_tabela) == 1
        
        # Verificar se atende aos critérios de near-zero variance
        nzv = (freq_ratio > freq_cut and percent_unique < unique_cut) or zero_var
        
        # Armazenar resultados
        resultados.loc[coluna, 'freq_ratio'] = freq_ratio
        resultados.loc[coluna, 'percent_unique'] = percent_unique
        resultados.loc[coluna, 'zero_var'] = zero_var
        resultados.loc[coluna, 'near_zero_var'] = nzv
    
    return resultados

# Carregar o dataset
print(f"Carregando o dataset: {input_path}")
try:
    df = pd.read_csv(input_path, low_memory=False)
    print(f"Total de registros: {len(df)}")
    print(f"Total de colunas antes da limpeza: {len(df.columns)}")
except FileNotFoundError:
    print(f"ERRO: O arquivo {input_path} não foi encontrado!")
    # Verificar se o arquivo existe com outro nome
    diretorio = os.path.dirname(input_path)
    arquivos = [f for f in os.listdir(diretorio) if f.endswith('.csv')]
    if arquivos:
        print(f"Arquivos CSV disponíveis no diretório: {arquivos}")
        # Tentar carregar o primeiro arquivo disponível
        input_path = os.path.join(diretorio, arquivos[0])
        print(f"Tentando carregar: {input_path}")
        df = pd.read_csv(input_path, low_memory=False)
        print(f"Arquivo carregado! Total de registros: {len(df)}")
    else:
        print("Nenhum arquivo CSV encontrado no diretório.")
        exit(1)

# 1. Remover variáveis com mais de 30% de dados faltantes
print("\n1. Identificando variáveis com mais de 30% de dados faltantes...")
percent_missing = df.isnull().sum() * 100 / len(df)
vars_missing_30 = percent_missing[percent_missing > 30].index.tolist()

print(f"Variáveis com >30% de dados faltantes: {len(vars_missing_30)}")
if len(vars_missing_30) > 0:
    print("Primeiras 10 variáveis com dados faltantes:")
    for i, var in enumerate(vars_missing_30[:10], 1):
        print(f"  {i}. {var}: {percent_missing[var]:.1f}% de dados faltantes")

# 2. Identificar variáveis com near-zero variance
print("\n2. Identificando variáveis com near-zero variance...")
nzv_resultados = identificar_near_zero_var(df)
vars_nzv = nzv_resultados[nzv_resultados['near_zero_var'] == True].index.tolist()

print(f"Variáveis com near-zero variance: {len(vars_nzv)}")
if len(vars_nzv) > 0:
    print("Primeiras 10 variáveis com near-zero variance:")
    for i, var in enumerate(vars_nzv[:10], 1):
        print(f"  {i}. {var}: ratio={nzv_resultados.loc[var, 'freq_ratio']:.1f}, unique={nzv_resultados.loc[var, 'percent_unique']:.1f}%")

# 3. Remover as variáveis identificadas
vars_para_remover = list(set(vars_missing_30 + vars_nzv))
print(f"\nTotal de variáveis a serem removidas: {len(vars_para_remover)}")

# Verificar se a coluna de AME está entre as variáveis a serem removidas
if 'aleitamento_materno_exclusivo' in vars_para_remover:
    print("ATENÇÃO: A variável 'aleitamento_materno_exclusivo' seria removida! Ela será mantida.")
    vars_para_remover.remove('aleitamento_materno_exclusivo')

# Criar o dataset limpo
df_limpo = df.drop(columns=vars_para_remover)
print(f"Total de colunas após a limpeza: {len(df_limpo.columns)}")
print(f"Colunas removidas: {len(df.columns) - len(df_limpo.columns)}")

# Verificar colunas importantes mantidas
print("\nVerificando colunas importantes mantidas:")
colunas_importantes = ['aleitamento_materno_exclusivo', 'b05a_idade_em_meses', 'b02_sexo', 'a00_regiao']
for col in colunas_importantes:
    if col in df_limpo.columns:
        print(f"  - {col}: MANTIDA")
    else:
        print(f"  - {col}: REMOVIDA")

# Salvar o dataset limpo
df_limpo.to_csv(output_path, index=False)
print(f"\nDataset limpo salvo em: {output_path}")

# Resumo final
print("\nResumo do processamento:")
print(f"Total de registros: {len(df_limpo)}")
print(f"Total de colunas original: {len(df.columns)}")
print(f"Total de colunas após limpeza: {len(df_limpo.columns)}")
print(f"Variáveis removidas por dados faltantes >30%: {len(vars_missing_30)}")
print(f"Variáveis removidas por near-zero variance: {len(vars_nzv)}")
print(f"Variáveis removidas no total (sem duplicação): {len(vars_para_remover)}")

# Exibir distribuição de AME no dataset final
if 'aleitamento_materno_exclusivo' in df_limpo.columns:
    print("\nDistribuição de Aleitamento Materno Exclusivo no dataset final:")
    print(df_limpo['aleitamento_materno_exclusivo'].value_counts())
    print(f"Percentual AME: {(df_limpo['aleitamento_materno_exclusivo'] == 1).mean()*100:.1f}%") 