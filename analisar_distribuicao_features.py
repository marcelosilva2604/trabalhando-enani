import pandas as pd
import os

# Definir o caminho para o arquivo
caminho_arquivo = '/Users/marcelosilva/Desktop/artigo_novo/8/dataset.csv'

# Verificar se o arquivo existe
if not os.path.exists(caminho_arquivo):
    print(f"Arquivo não encontrado: {caminho_arquivo}")
    exit(1)

# Carregar o dataset
print(f"Carregando o dataset {caminho_arquivo}...")
try:
    df = pd.read_csv(caminho_arquivo, low_memory=False)
    print(f"Dataset carregado com sucesso. Dimensões: {df.shape}")
except Exception as e:
    print(f"Erro ao carregar o arquivo: {e}")
    exit(1)

# Criar arquivo de saída
output_file = '/Users/marcelosilva/Desktop/artigo_novo/distribuicao_features.txt'
with open(output_file, 'w') as f:
    f.write(f"Análise de Distribuição de Features no Dataset\n")
    f.write(f"Dataset: {caminho_arquivo}\n")
    f.write(f"Total de registros: {len(df)}\n")
    f.write(f"Total de features: {len(df.columns)}\n\n")
    
    # Analisar cada coluna
    for coluna in df.columns:
        f.write(f"\n{'='*80}\n")
        f.write(f"FEATURE: {coluna}\n")
        f.write(f"{'='*80}\n")
        
        # Calcular contagem e percentagem
        contagem = df[coluna].value_counts(dropna=False)
        percentagem = df[coluna].value_counts(dropna=False, normalize=True) * 100
        
        # Combinar contagem e percentagem
        resultado = pd.DataFrame({
            'Contagem': contagem,
            'Porcentagem': percentagem
        }).sort_values(by='Porcentagem', ascending=False)
        
        # Formatar e salvar no arquivo
        for valor, row in resultado.iterrows():
            valor_str = str(valor)
            if pd.isna(valor):
                valor_str = "MISSING"
            f.write(f"{valor_str}: {row['Contagem']} ({row['Porcentagem']:.2f}%)\n")

print(f"Análise concluída. Resultados salvos em: {output_file}")

# Também vamos criar um script específico para a análise de idades em meses (b05a_idade_em_meses)
if 'b05a_idade_em_meses' in df.columns:
    idade_output_file = '/Users/marcelosilva/Desktop/artigo_novo/distribuicao_idades.txt'
    with open(idade_output_file, 'w') as f:
        f.write("Análise de Distribuição de Idades em Meses\n")
        f.write("="*50 + "\n\n")
        
        idade_contagem = df['b05a_idade_em_meses'].value_counts(dropna=False)
        idade_percentagem = df['b05a_idade_em_meses'].value_counts(dropna=False, normalize=True) * 100
        
        idade_resultado = pd.DataFrame({
            'Contagem': idade_contagem,
            'Porcentagem': idade_percentagem
        }).sort_values(by='Porcentagem', ascending=False)
        
        f.write("Distribuição de Idades em Meses:\n")
        for idade, row in idade_resultado.iterrows():
            idade_str = str(idade)
            if pd.isna(idade):
                idade_str = "MISSING"
            f.write(f"{idade_str}: {row['Contagem']} ({row['Porcentagem']:.2f}%)\n")
    
    print(f"Análise de idades concluída. Resultados salvos em: {idade_output_file}") 