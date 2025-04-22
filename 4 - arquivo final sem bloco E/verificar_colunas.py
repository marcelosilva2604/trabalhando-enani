import pandas as pd

# Carregar o arquivo CSV
df = pd.read_csv('criancas_menores_6_meses_classificadas_sem_bloco_e.csv', low_memory=False)

# Verificar se a coluna 'vd_dummy_gravida' existe
if 'vd_dummy_gravida' in df.columns:
    index = list(df.columns).index('vd_dummy_gravida')
    print(f"A coluna 'vd_dummy_gravida' existe e está na posição {index+1} de {len(df.columns)}")
else:
    print("A coluna 'vd_dummy_gravida' NÃO existe no arquivo!")

# Mostrar as últimas 15 colunas
print("\nÚltimas 15 colunas do arquivo:")
for i, coluna in enumerate(list(df.columns)[-15:], 1):
    print(f"{len(df.columns)-15+i}. {coluna}")

# Mostrar as colunas que começam com 'vd_'
vd_colunas = [col for col in df.columns if col.startswith('vd_')]
print(f"\nColunas que começam com 'vd_': {len(vd_colunas)} colunas")
for i, coluna in enumerate(vd_colunas, 1):
    print(f"{i}. {coluna}") 