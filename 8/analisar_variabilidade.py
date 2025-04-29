import pandas as pd
import os

# Carregar dataset
print("Carregando dataset...")
caminho_arquivo = '/Users/marcelosilva/Desktop/artigo_novo/8/dataset.csv'
try:
    df = pd.read_csv(caminho_arquivo, low_memory=False)
    print(f"Dataset carregado com sucesso. Dimensões: {df.shape}")
except Exception as e:
    print(f"Erro ao carregar o arquivo: {e}")
    exit(1)

# Arquivo de saída
output_file = '/Users/marcelosilva/Desktop/artigo_novo/8/analise_variabilidade.txt'

# Ordenar features por variabilidade
print("Analisando variabilidade...")
features_info = []

for coluna in df.columns:
    # Calcular valor mais frequente e sua percentagem
    contagem = df[coluna].value_counts(dropna=False)
    percentagem = df[coluna].value_counts(dropna=False, normalize=True) * 100
    
    valor_dominante = percentagem.idxmax()
    valor_str = "MISSING" if pd.isna(valor_dominante) else str(valor_dominante)
    
    # Adicionar à lista
    features_info.append({
        'feature': coluna,
        'valor_dominante': valor_str,
        'percentagem': percentagem.max(),
        'valores_unicos': len(contagem)
    })

# Ordenar por percentagem (variabilidade crescente)
features_info_sorted = sorted(features_info, key=lambda x: x['percentagem'], reverse=True)

# Salvar resultados
with open(output_file, 'w') as f:
    f.write("Análise de Variabilidade das Features\n")
    f.write("="*80 + "\n\n")
    f.write(f"Dataset: {caminho_arquivo}\n")
    f.write(f"Total de registros: {len(df)}\n")
    f.write(f"Total de features: {len(df.columns)}\n\n")
    
    f.write(f"{'FEATURE':<40} {'VALOR DOMINANTE':<30} {'%':<10} {'#VALORES':<10}\n")
    f.write(f"{'-'*90}\n")
    
    for item in features_info_sorted:
        valor_mostrado = item['valor_dominante']
        # Limitar tamanho do valor dominante para exibição
        if len(valor_mostrado) > 28:
            valor_mostrado = valor_mostrado[:25] + "..."
        
        f.write(f"{item['feature']:<40} {valor_mostrado:<30} {item['percentagem']:.2f}% {item['valores_unicos']:<10}\n")

    # Adicionar sugestões de features para remover (alta concentração em um valor)
    f.write("\n\n")
    f.write("="*80 + "\n")
    f.write("SUGESTÕES DE FEATURES PARA REMOVER (> 90% em um único valor)\n")
    f.write("="*80 + "\n\n")
    
    for item in features_info_sorted:
        if item['percentagem'] >= 90.0:
            f.write(f"{item['feature']:<40} {item['percentagem']:.2f}%\n")

print(f"Análise concluída. Resultados salvos em: {output_file}")

# Análise específica da distribuição de idades
if 'b05a_idade_em_meses' in df.columns:
    idade_output_file = '/Users/marcelosilva/Desktop/artigo_novo/8/distribuicao_idades_detalhada.txt'
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