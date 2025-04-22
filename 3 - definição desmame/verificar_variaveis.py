import pandas as pd

# Carregar o dataset original
print("Carregando dados...")
df = pd.read_csv('/Users/marcelosilva/Desktop/artigo_novo/2 - menores de 6 meses/criancas_menores_6meses.csv', low_memory=False)
print(f"Total de registros: {len(df)}")

# Verificar os valores da variável de aleitamento materno
print("\nValores únicos em e01_leite_peito (leite materno):")
print(df['e01_leite_peito'].value_counts(dropna=False))

# Verificar o tipo de dados
print(f"\nTipo de dados da coluna e01_leite_peito: {df['e01_leite_peito'].dtype}")

# Verificar algumas variáveis-chave de outros alimentos
variaveis_para_verificar = [
    'e02_agua',             # Água
    'e06_leite_vaca_po',    # Leite de vaca em pó
    'e07_leite_vaca_liquido', # Leite de vaca líquido
    'e10_formula_infantil',  # Fórmula infantil
]

for var in variaveis_para_verificar:
    print(f"\nValores únicos em {var}:")
    print(df[var].value_counts(dropna=False))

# Verificar se existem crianças que atendem aos critérios de AME
leite_materno = df['e01_leite_peito'] == 1
outros_alimentos = pd.Series(False, index=df.index)

variaveis_alimentos = [
    'e02_agua', 'e04_agua_com_acucar', 'e05_cha', 'e06_leite_vaca_po',
    'e07_leite_vaca_liquido', 'e08_leite_soja_po', 'e09_leite_soja_liquido',
    'e10_formula_infantil', 'e11_suco', 'e12_fruta_inteira', 'e14_manga',
    'e16_comida_sal', 'e19_mingau', 'e20_iogurte', 'e21_arroz', 'e21a_pao',
    'e22_legumes', 'e23_cenoura', 'e24_couve', 'e25_verduras', 'e26_feijao',
    'e27_carne', 'e28_figado', 'e29_ovo', 'e30_hamburger', 'e31_salgadinhos',
    'e32_suco_industrializado', 'e33_refrigerante', 'e34_macarrao',
    'e35_biscoito', 'e36_bala', 'e37_tempero', 'e38_farinhas', 'e40_adocado'
]

for var in variaveis_alimentos:
    if var in df.columns:
        outros_alimentos |= (df[var] == 1)

ame_potencial = leite_materno & ~outros_alimentos
print(f"\nCrianças que receberam leite materno: {leite_materno.sum()}")
print(f"Crianças que receberam outros alimentos: {outros_alimentos.sum()}")
print(f"Crianças potencialmente em AME: {ame_potencial.sum()}")

# Ver alguns exemplos de registros
if ame_potencial.sum() > 0:
    print("\nExemplos de registros de crianças em AME:")
    print(df[ame_potencial].head(3)[['b05a_idade_em_meses', 'e01_leite_peito'] + variaveis_para_verificar])
else:
    print("\nExemplos de registros de crianças que tomam leite materno:")
    if leite_materno.sum() > 0:
        print(df[leite_materno].head(3)[['b05a_idade_em_meses', 'e01_leite_peito'] + variaveis_para_verificar])
    else:
        print("Nenhuma criança registrada como tendo recebido leite materno.") 