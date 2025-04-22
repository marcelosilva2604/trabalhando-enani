import pandas as pd

# Lê o arquivo CSV original
print("Lendo arquivo CSV...")
file_path = '../Banco de dados CSV/data_crianca_calib_anon.csv'
df = pd.read_csv(file_path, low_memory=False)
print(f"Total de registros no banco de dados original: {len(df)}")

# Extrai os valores numéricos da coluna de idade em meses e filtra
print("Filtrando crianças menores de 6 meses...")
idade_em_meses = pd.to_numeric(df['b05a_idade_em_meses'].astype(str).str.extract(r'(\d+)', expand=False), errors='coerce')
menores_6_meses = idade_em_meses <= 5
df_menores_6m = df[menores_6_meses]
print(f"Total de crianças menores de 6 meses: {len(df_menores_6m)}")

# Salva o dataframe filtrado em um novo arquivo CSV
output_file = 'criancas_menores_6meses.csv'
print(f"Salvando arquivo filtrado: {output_file}")
df_menores_6m.to_csv(output_file, index=False)
print(f"Concluído!") 