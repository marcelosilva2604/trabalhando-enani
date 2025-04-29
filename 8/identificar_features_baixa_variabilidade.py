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

# Lista de níveis de variabilidade para análise (%)
thresholds = [99.0, 95.0, 90.0, 80.0, 70.0]

# Criar arquivo de saída
output_file = '/Users/marcelosilva/Desktop/artigo_novo/8/features_para_remocao.txt'

with open(output_file, 'w') as f:
    f.write("Análise de Features com Baixa Variabilidade\n")
    f.write("="*80 + "\n\n")
    f.write(f"Dataset: {caminho_arquivo}\n")
    f.write(f"Total de registros: {len(df)}\n")
    f.write(f"Total de features: {len(df.columns)}\n\n")
    
    for threshold in thresholds:
        features_threshold = []
        
        print(f"Analisando features com variabilidade < {100-threshold:.1f}%...")
        
        for coluna in df.columns:
            # Calcular percentagem de cada valor
            contagem = df[coluna].value_counts(dropna=False)
            percentagem = df[coluna].value_counts(dropna=False, normalize=True) * 100
            
            # Verificar se o valor mais frequente ultrapassa o threshold
            if percentagem.max() >= threshold:
                valor_dominante = percentagem.idxmax()
                valor_str = "MISSING" if pd.isna(valor_dominante) else str(valor_dominante)
                
                # Calcular número de valores únicos
                num_valores_unicos = len(contagem)
                
                features_threshold.append({
                    'feature': coluna,
                    'valor_dominante': valor_str,
                    'percentagem': percentagem.max(),
                    'num_valores_unicos': num_valores_unicos
                })
        
        # Ordenar por percentagem (descendente)
        features_threshold = sorted(features_threshold, key=lambda x: x['percentagem'], reverse=True)
        
        # Escrever no arquivo
        f.write(f"\n{'='*80}\n")
        f.write(f"Features com {threshold}% ou mais em um único valor (variabilidade < {100-threshold:.1f}%)\n")
        f.write(f"Total de features identificadas: {len(features_threshold)}\n")
        f.write(f"{'='*80}\n\n")
        
        if features_threshold:
            f.write(f"{'FEATURE':<40} {'VALOR DOMINANTE':<30} {'%':<6} {'#VALORES':<8}\n")
            f.write(f"{'-'*85}\n")
            
            for item in features_threshold:
                valor_mostrado = item['valor_dominante']
                # Limitar tamanho do valor dominante para exibição
                if len(valor_mostrado) > 28:
                    valor_mostrado = valor_mostrado[:25] + "..."
                
                f.write(f"{item['feature']:<40} {valor_mostrado:<30} {item['percentagem']:.1f}% {item['num_valores_unicos']:<8}\n")
        else:
            f.write("Nenhuma feature identificada para este threshold.\n")

print(f"Análise concluída. Resultados salvos em: {output_file}")

# Também criar uma saída separada para os valores percentuais de cada feature
print("Gerando detalhamento da distribuição percentual de valores...")
detalhe_file = '/Users/marcelosilva/Desktop/artigo_novo/8/detalhamento_percentual_valores.txt'

with open(detalhe_file, 'w') as f:
    f.write("Detalhamento de Distribuição Percentual de Valores por Feature\n")
    f.write("="*80 + "\n\n")
    
    # Selecionar algumas features interessantes para análise detalhada
    features_interesse = ['aleitamento_materno_exclusivo', 'b05a_idade_em_meses', 'a00_regiao']
    
    # Adicionar algumas features com baixa variabilidade (top 10)
    baixa_var_features = []
    for coluna in df.columns:
        percentagem = df[coluna].value_counts(dropna=False, normalize=True) * 100
        if percentagem.max() >= 80.0:  # 80% ou mais no valor dominante
            baixa_var_features.append((coluna, percentagem.max()))
    
    # Ordenar por percentagem e pegar os top 10
    baixa_var_features = sorted(baixa_var_features, key=lambda x: x[1], reverse=True)[:10]
    
    # Adicionar à lista de features de interesse
    for feat, _ in baixa_var_features:
        if feat not in features_interesse:
            features_interesse.append(feat)
    
    # Analisar cada feature de interesse
    for coluna in features_interesse:
        if coluna not in df.columns:
            continue
            
        f.write(f"\n{'='*80}\n")
        f.write(f"FEATURE: {coluna}\n")
        f.write(f"{'='*80}\n\n")
        
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

print(f"Detalhamento concluído. Resultados salvos em: {detalhe_file}") 