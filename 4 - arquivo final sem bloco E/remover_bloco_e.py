import pandas as pd
import os
import re

# Definir caminhos
input_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                          '3 - definição desmame/criancas_menores_6_meses_classificadas.csv')
output_path = os.path.join(os.path.dirname(__file__), 
                          'criancas_menores_6_meses_classificadas_sem_bloco_e.csv')

print(f"Carregando o arquivo: {input_path}")
df = pd.read_csv(input_path, low_memory=False)

# Contar colunas antes da remoção
total_colunas_antes = len(df.columns)
print(f"Total de colunas antes da remoção: {total_colunas_antes}")

# Identificar as colunas do bloco E (começam com 'e' e um número)
colunas_bloco_e = [col for col in df.columns if re.match(r'^e\d+', col)]

# Verificar a quantidade de colunas do bloco E
total_colunas_bloco_e = len(colunas_bloco_e)
print(f"Total de colunas do bloco E a serem removidas: {total_colunas_bloco_e}")
print(f"Primeiras 10 colunas a serem removidas: {colunas_bloco_e[:10]}")

# Manter apenas a coluna de classificação AME
df_sem_bloco_e = df.drop(colunas_bloco_e, axis=1)

# Contar colunas depois da remoção
total_colunas_depois = len(df_sem_bloco_e.columns)
print(f"Total de colunas após a remoção: {total_colunas_depois}")
print(f"Colunas removidas: {total_colunas_antes - total_colunas_depois}")

# Verificar se a coluna de aleitamento materno exclusivo ainda está presente
if 'aleitamento_materno_exclusivo' in df_sem_bloco_e.columns:
    print("A coluna 'aleitamento_materno_exclusivo' foi mantida no arquivo!")
    print(f"Distribuição de aleitamento_materno_exclusivo: {df_sem_bloco_e['aleitamento_materno_exclusivo'].value_counts()}")
else:
    print("ERRO: A coluna 'aleitamento_materno_exclusivo' não foi encontrada!")

# Salvar o novo arquivo sem as colunas do bloco E
df_sem_bloco_e.to_csv(output_path, index=False)
print(f"Arquivo salvo em: {output_path}")

print("\nResumo da operação:")
print(f"Arquivo original: {total_colunas_antes} colunas")
print(f"Arquivo final: {total_colunas_depois} colunas")
print(f"Colunas do bloco E removidas: {total_colunas_bloco_e}")
print(f"Dados preservados: {len(df_sem_bloco_e)} registros") 