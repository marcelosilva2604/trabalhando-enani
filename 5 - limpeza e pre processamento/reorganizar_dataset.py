import pandas as pd
import os

# Definir caminhos
input_path = 'dataset_limpo.csv'
output_path = 'dataset_final.csv'

print(f"Carregando o dataset limpo: {input_path}")
df = pd.read_csv(input_path)
print(f"Total de registros: {len(df)}")
print(f"Total de colunas: {len(df.columns)}")

# Verificar se a coluna de AME existe
if 'aleitamento_materno_exclusivo' in df.columns:
    posicao_atual = list(df.columns).index('aleitamento_materno_exclusivo') + 1
    print(f"Coluna 'aleitamento_materno_exclusivo' encontrada na posição {posicao_atual}")
    
    # Reordenar as colunas: AME primeiro, depois as demais
    colunas_reordenadas = ['aleitamento_materno_exclusivo'] + [col for col in df.columns if col != 'aleitamento_materno_exclusivo']
    df_reorganizado = df[colunas_reordenadas]
    
    # Salvar o dataset reorganizado
    df_reorganizado.to_csv(output_path, index=False)
    print(f"Dataset reorganizado salvo em: {output_path}")
    print(f"A coluna 'aleitamento_materno_exclusivo' agora é a primeira coluna!")
    
    # Verificar as primeiras colunas do novo dataset
    print("\nPrimeiras 10 colunas do dataset reorganizado:")
    for i, col in enumerate(list(df_reorganizado.columns)[:10], 1):
        print(f"{i}. {col}")
    
    # Mostrar a distribuição de AME
    print("\nDistribuição de Aleitamento Materno Exclusivo:")
    print(df_reorganizado['aleitamento_materno_exclusivo'].value_counts())
    print(f"Percentual AME: {(df_reorganizado['aleitamento_materno_exclusivo'] == 1).mean()*100:.1f}%")
    
else:
    print("ERRO: A coluna 'aleitamento_materno_exclusivo' não foi encontrada no dataset!")
    print("Colunas disponíveis:")
    for i, col in enumerate(df.columns[:20], 1):
        print(f"{i}. {col}")
    print("..." if len(df.columns) > 20 else "") 