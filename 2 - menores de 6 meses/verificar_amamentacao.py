import pandas as pd
import numpy as np

def main():
    print("Verificando informações sobre amamentação no banco de dados ENANI...")
    
    # Lê o arquivo CSV das crianças
    file_path = '../Banco de dados CSV/data_crianca_calib_anon.csv'
    df = pd.read_csv(file_path, low_memory=False)
    
    # Extrai os valores numéricos da coluna de idade em meses
    idade_em_meses = pd.to_numeric(df['b05a_idade_em_meses'].astype(str).str.extract(r'(\d+)', expand=False), errors='coerce')
    menores_6_meses = idade_em_meses <= 5
    df_menores_6m = df[menores_6_meses]
    
    # Verifica valores únicos e contagem em e01_leite_peito
    print("\nValores únicos em e01_leite_peito (banco completo):")
    valores_leite = df['e01_leite_peito'].value_counts().to_dict()
    for valor, contagem in valores_leite.items():
        print(f"  '{valor}': {contagem} ocorrências")
    
    print("\nValores únicos em e01_leite_peito (crianças < 6 meses):")
    valores_leite_menores = df_menores_6m['e01_leite_peito'].value_counts().to_dict()
    for valor, contagem in valores_leite_menores.items():
        print(f"  '{valor}': {contagem} ocorrências")
    
    # Verifica o tipo dos dados
    print(f"\nTipo de dados da coluna e01_leite_peito: {df['e01_leite_peito'].dtype}")
    
    # Tenta converter para numérico e verificar novamente
    df['e01_leite_peito_num'] = pd.to_numeric(df['e01_leite_peito'], errors='coerce')
    print("\nApós tentativa de conversão para numérico:")
    print(df['e01_leite_peito_num'].value_counts().sort_index())
    
    # Verifica outras variáveis relacionadas à alimentação
    colunas_alimentacao = [col for col in df.columns if col.startswith('e0')]
    print(f"\nColunas relacionadas à alimentação (prefixo 'e0'): {len(colunas_alimentacao)}")
    for col in colunas_alimentacao[:10]:  # Primeiras 10 colunas como exemplo
        print(f"\nDistribuição da variável {col}:")
        print(df[col].value_counts().head())
    
    # Verifica especificamente variáveis importantes para aleitamento
    variaveis_importantes = ['e01_leite_peito', 'e06_leite_vaca_po', 'e07_leite_vaca_liquido', 
                           'e10_formula_infantil', 'e39_mamadeira']
    
    print("\nDetalhamento das variáveis importantes para análise de aleitamento:")
    for var in variaveis_importantes:
        print(f"\n{var}:")
        valores = df_menores_6m[var].value_counts()
        valores_proporcionais = df_menores_6m[var].value_counts(normalize=True) * 100
        for val in valores.index:
            print(f"  '{val}': {valores[val]} crianças ({valores_proporcionais[val]:.1f}%)")

if __name__ == "__main__":
    main() 