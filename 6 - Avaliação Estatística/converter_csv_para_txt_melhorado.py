import pandas as pd
import os

# Ler o arquivo CSV
df = pd.read_csv('resultados/features_excluidas.csv')

# Formatar dados para o arquivo TXT
linhas = []
linhas.append('Lista de features excluídas por não apresentarem relação estatisticamente significativa com aleitamento_materno_exclusivo (p≥0.05)\n')
linhas.append('=' * 100 + '\n\n')
linhas.append(f'Total de features excluídas: {len(df)}\n\n')

# Contar tipos de testes aplicados nas features excluídas
contagem_testes = df['teste'].value_counts()
linhas.append('Testes aplicados nas features excluídas:\n')
for teste, contagem in contagem_testes.items():
    linhas.append(f'- {teste}: {contagem}\n')
linhas.append('\n')

linhas.append('Feature                                  | Classificação | Teste Aplicado                  | p-valor\n')
linhas.append('-' * 100 + '\n')

# Formatar cada linha
for idx, row in df.iterrows():
    feature = row['feature']
    classificacao = row['classificacao']
    teste = row['teste']
    p_valor = row['p_valor']
    
    linha = f'{feature:<40} | {classificacao:<13} | {teste:<30} | {p_valor:.5f}\n'
    linhas.append(linha)

# Escrever no arquivo TXT na pasta 6 (não na subpasta)
with open('features_excluidas.txt', 'w') as f:
    f.writelines(linhas)

print('Arquivo features_excluidas.txt atualizado com sucesso!') 