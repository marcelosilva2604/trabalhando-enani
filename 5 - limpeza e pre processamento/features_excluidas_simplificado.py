import pandas as pd
import os

# Definir caminhos
dataset_original_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                         '4 - arquivo final sem bloco E/criancas_menores_6_meses_classificadas_sem_bloco_e.csv')
dataset_limpo_path = 'dataset_final.csv'
output_txt_path = 'features_excluidas_motivo.txt'

print(f"Carregando os datasets...")

# Carregar o dataset original
df_original = pd.read_csv(dataset_original_path, low_memory=False)
print(f"Dataset original carregado: {df_original.shape[0]} linhas, {df_original.shape[1]} colunas")

# Calcular porcentagem de valores nulos para cada coluna
percent_missing = df_original.isnull().mean() * 100

# Identificar colunas com mais de 30% de valores nulos
cols_missing_30 = [(col, percent) for col, percent in percent_missing.items() if percent > 30]
print(f"Features com >30% de dados faltantes: {len(cols_missing_30)}")

# Função para identificar colunas com near-zero variance
def identificar_near_zero_var(df, freq_cut=19, unique_cut=10):
    resultado = []
    
    for coluna in df.columns:
        # Ignorar valores missing
        dados = df[coluna].dropna()
        
        # Pular colunas vazias
        if len(dados) == 0:
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
        
        if nzv:
            resultado.append((coluna, freq_ratio, percent_unique))
    
    return resultado

# Identificar colunas com near-zero variance
print("Identificando colunas com baixa variabilidade...")
cols_nzv = identificar_near_zero_var(df_original)
print(f"Features com baixa variabilidade: {len(cols_nzv)}")

# Carregar o dataset limpo
df_limpo = pd.read_csv(dataset_limpo_path)
print(f"Dataset limpo carregado: {df_limpo.shape[0]} linhas, {df_limpo.shape[1]} colunas")

# Identificar features excluídas
colunas_original = set(df_original.columns)
colunas_limpo = set(df_limpo.columns)
colunas_excluidas = colunas_original - colunas_limpo
print(f"Total de features excluídas: {len(colunas_excluidas)}")

# Criar o arquivo de texto
with open(output_txt_path, 'w') as f:
    f.write("FEATURES EXCLUÍDAS E MOTIVOS\n")
    f.write("===========================\n\n")
    f.write(f"Total de features excluídas: {len(colunas_excluidas)}\n\n")
    
    # Lista de features excluídas por terem mais de 30% de valores nulos
    f.write("FEATURES EXCLUÍDAS POR TEREM >30% DE DADOS FALTANTES\n")
    f.write("---------------------------------------------------\n")
    f.write(f"Total: {len(cols_missing_30)}\n\n")
    
    for i, (col, percent) in enumerate(sorted(cols_missing_30, key=lambda x: x[1], reverse=True), 1):
        if col in colunas_excluidas:  # Garantir que a coluna foi de fato excluída
            f.write(f"{i}. {col} - {percent:.1f}% de dados faltantes\n")
    
    # Lista de features excluídas por terem baixa variabilidade
    f.write("\n\nFEATURES EXCLUÍDAS POR TEREM BAIXA VARIABILIDADE\n")
    f.write("------------------------------------------------\n")
    f.write(f"Total: {len(cols_nzv)}\n\n")
    
    for i, (col, ratio, unique) in enumerate(sorted(cols_nzv, key=lambda x: x[1], reverse=True), 1):
        if col in colunas_excluidas:  # Garantir que a coluna foi de fato excluída
            f.write(f"{i}. {col} - ratio={ratio:.1f}, unique={unique:.1f}%\n")

print(f"Arquivo com motivos de exclusão criado: {output_txt_path}")
print(f"Features com >30% de dados faltantes: {len(cols_missing_30)}")
print(f"Features com baixa variabilidade: {len(cols_nzv)}")
print(f"Features excluídas no total: {len(colunas_excluidas)}") 