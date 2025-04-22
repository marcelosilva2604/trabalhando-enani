import pandas as pd

# Carregar o dataset classificado
df = pd.read_csv('criancas_menores_6_meses_classificadas.csv', low_memory=False)

# Verificar as 5 primeiras classificadas como AME
ame = df[df['aleitamento_materno_exclusivo'] == 1].head(5)
print('CRIANÇAS EM AME:')
print(ame[['e01_leite_peito', 'e02_agua', 'e04_agua_com_acucar', 'e05_cha', 'e10_formula_infantil', 'aleitamento_materno_exclusivo']])

# Verificar as 5 primeiras classificadas como não AME
nao_ame = df[df['aleitamento_materno_exclusivo'] == 2].head(5)
print('\nCRIANÇAS NÃO EM AME:')
print(nao_ame[['e01_leite_peito', 'e02_agua', 'e04_agua_com_acucar', 'e05_cha', 'e10_formula_infantil', 'aleitamento_materno_exclusivo']])

# Contar quantas crianças em cada categoria
print(f"\nTotal de crianças: {len(df)}")
print(f"Crianças em AME: {(df['aleitamento_materno_exclusivo'] == 1).sum()}")
print(f"Crianças não em AME: {(df['aleitamento_materno_exclusivo'] == 2).sum()}")
print(f"Percentual de AME: {(df['aleitamento_materno_exclusivo'] == 1).mean()*100:.1f}%") 