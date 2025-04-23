import pandas as pd
import os

# Definir caminhos
dataset_original_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                         '4 - arquivo final sem bloco E/criancas_menores_6_meses_classificadas_sem_bloco_e.csv')
dataset_limpo_path = 'dataset_final.csv'
output_txt_path = 'features_excluidas.txt'

print(f"Carregando os datasets...")
try:
    # Carregar o dataset original e o dataset limpo
    df_original = pd.read_csv(dataset_original_path, low_memory=False)
    df_limpo = pd.read_csv(dataset_limpo_path)
    
    # Identificar as colunas que estavam no original mas não estão no limpo
    colunas_original = set(df_original.columns)
    colunas_limpo = set(df_limpo.columns)
    colunas_excluidas = colunas_original - colunas_limpo
    
    print(f"Total de colunas no dataset original: {len(colunas_original)}")
    print(f"Total de colunas no dataset limpo: {len(colunas_limpo)}")
    print(f"Total de colunas excluídas: {len(colunas_excluidas)}")
    
    # Organizar as colunas excluídas em categorias
    # 1. Identificar colunas do bloco E (já foram removidas anteriormente, mas vamos verificar)
    colunas_bloco_e = [col for col in colunas_excluidas if col.startswith('e') and any(c.isdigit() for c in col)]
    
    # 2. Identificar outras categorias de colunas excluídas
    colunas_vd = [col for col in colunas_excluidas if col.startswith('vd_')]
    colunas_i = [col for col in colunas_excluidas if col.startswith('i') and any(c.isdigit() for c in col)]
    colunas_h = [col for col in colunas_excluidas if col.startswith('h') and any(c.isdigit() for c in col)]
    colunas_d = [col for col in colunas_excluidas if col.startswith('d') and any(c.isdigit() for c in col)]
    
    # Outras colunas que não se encaixam nas categorias acima
    outras_colunas = colunas_excluidas - set(colunas_bloco_e) - set(colunas_vd) - set(colunas_i) - set(colunas_h) - set(colunas_d)
    
    # Criar o arquivo de texto
    with open(output_txt_path, 'w') as f:
        f.write(f"FEATURES EXCLUÍDAS DO DATASET\n")
        f.write(f"===============================\n\n")
        f.write(f"Total de features excluídas: {len(colunas_excluidas)}\n\n")
        
        # Escrever as colunas por categoria
        categories = [
            ("Variáveis do Bloco E (Consumo Alimentar)", colunas_bloco_e),
            ("Variáveis Derivadas (VD)", colunas_vd),
            ("Variáveis de Desenvolvimento Infantil (I)", colunas_i),
            ("Variáveis de Saúde (H)", colunas_h),
            ("Variáveis de Alimentação/Dieta (D)", colunas_d),
            ("Outras Variáveis", outras_colunas)
        ]
        
        for category_name, cols in categories:
            if cols:
                f.write(f"\n{category_name} ({len(cols)} variáveis):\n")
                f.write("-" * 50 + "\n")
                for i, col in enumerate(sorted(cols), 1):
                    # Se possível, usar dados originais para ver porcentagem de valores faltantes
                    if col in df_original.columns:
                        percent_missing = df_original[col].isnull().mean() * 100
                        f.write(f"{i}. {col} - {percent_missing:.1f}% de dados faltantes\n")
                    else:
                        f.write(f"{i}. {col}\n")
    
    print(f"Arquivo com features excluídas criado em: {output_txt_path}")
    
    # Mostrar resumo das categorias
    print("\nResumo das features excluídas por categoria:")
    for category_name, cols in categories:
        print(f"{category_name}: {len(cols)} variáveis")
    
except FileNotFoundError as e:
    print(f"ERRO: Um dos arquivos não foi encontrado - {e}")
    # Verificar se os arquivos existem
    print("\nVerificando arquivos disponíveis:")
    pasta_original = os.path.dirname(dataset_original_path)
    if os.path.exists(pasta_original):
        arquivos = [f for f in os.listdir(pasta_original) if f.endswith('.csv')]
        print(f"Arquivos CSV em {pasta_original}:")
        for a in arquivos:
            print(f"  - {a}")
    
    pasta_atual = os.getcwd()
    arquivos = [f for f in os.listdir(pasta_atual) if f.endswith('.csv')]
    print(f"Arquivos CSV na pasta atual:")
    for a in arquivos:
        print(f"  - {a}")
except Exception as e:
    print(f"ERRO: {e}") 