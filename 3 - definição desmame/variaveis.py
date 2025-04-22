# Lista das variáveis que indicam consumo de outros alimentos
# SCRIPT PARA CLASSIFICAÇÃO DE ALEITAMENTO MATERNO EXCLUSIVO EM CRIANÇAS MENORES DE 6 MESES

"""
Este script processa dados do ENANI-2019 para classificar crianças menores de 6 meses 
quanto ao aleitamento materno exclusivo, seguindo os critérios da OMS.

CRITÉRIOS:
- Aleitamento materno exclusivo (valor 1): Criança que recebeu APENAS leite materno, sem nenhum outro alimento ou líquido
- Sem aleitamento materno exclusivo (valor 2): Criança que NÃO recebeu leite materno OU recebeu qualquer outro alimento/líquido

INPUTS:
- Arquivo CSV com dados do ENANI-2019 contendo crianças menores de 6 meses
- Variáveis do bloco E (consumo alimentar)

OUTPUT:
- Novo arquivo CSV com variável adicional 'aleitamento_materno_exclusivo' (1 = Sim, 2 = Não)
"""

import pandas as pd
import os

# Definir caminho para salvar o arquivo de saída na pasta atual
output_path = os.path.join(os.path.dirname(__file__), 'criancas_menores_6_meses_classificadas.csv')

# Carregar o dataset original
print("Carregando dados...")
df = pd.read_csv('/Users/marcelosilva/Desktop/artigo_novo/2 - menores de 6 meses/criancas_menores_6meses.csv', low_memory=False)
print(f"Total de crianças < 6 meses: {len(df)}")

variaveis_alimentos_desmame = [
        'e02_agua',             # Água
        'e04_agua_com_acucar',  # Água com açúcar
        'e05_cha',              # Chá
        'e06_leite_vaca_po',    # Leite de vaca em pó
        'e07_leite_vaca_liquido', # Leite de vaca líquido
        'e08_leite_soja_po',    # Leite de soja em pó
        'e09_leite_soja_liquido', # Leite de soja líquido
        'e10_formula_infantil',  # Fórmula infantil
        'e11_suco',             # Suco natural
        'e12_fruta_inteira',    # Fruta
        'e14_manga',            # Manga, mamão ou goiaba
        'e16_comida_sal',       # Comida de sal
        'e19_mingau',           # Mingau ou papa com leite
        'e20_iogurte',          # Iogurte
        'e21_arroz',            # Arroz, batata, etc.
        'e21a_pao',             # Pão
        'e22_legumes',          # Legumes
        'e23_cenoura',          # Cenoura, abóbora, batata doce
        'e24_couve',            # Couve, espinafre, etc.
        'e25_verduras',         # Outras verduras
        'e26_feijao',           # Feijão ou outros grãos
        'e27_carne',            # Carne
        'e28_figado',           # Fígado
        'e29_ovo',              # Ovo
        'e30_hamburger',        # Hambúrguer, presunto, etc.
        'e31_salgadinhos',      # Salgadinhos de pacote
        'e32_suco_industrializado', # Suco industrializado
        'e33_refrigerante',     # Refrigerante
        'e34_macarrao',         # Macarrão instantâneo
        'e35_biscoito',         # Biscoito/bolacha
        'e36_bala',             # Bala, pirulito
        'e37_tempero',          # Tempero pronto industrializado
        'e38_farinhas',         # Farinhas instantâneas
        'e40_adocado'           # Alimento adoçado
    ]

# Corrigir o nome da variável de aleitamento materno
variavel_aleitamento = 'e01_leite_peito'  # Nome correto da variável no ENANI-2019

# Função para classificar aleitamento materno exclusivo
def classificar_aleitamento_exclusivo(row):
    # Verificar se tomou leite materno (no dataset, "Sim" representa que a criança recebeu leite materno)
    if row[variavel_aleitamento] != "Sim":  # Se NÃO tomou leite materno
        return 2  # Não em AME
    
    # Verificar se consumiu qualquer outro alimento/líquido
    for var in variaveis_alimentos_desmame:
        if var in row.index and row[var] == "Sim":  # Se consumiu outro alimento/líquido
            return 2  # Não em AME
    
    # Se chegou até aqui: tomou leite materno E não consumiu nenhum outro alimento/líquido
    return 1  # Sim, está em AME

# Aplicar a classificação a cada linha do dataframe
df['aleitamento_materno_exclusivo'] = df.apply(classificar_aleitamento_exclusivo, axis=1)

# Salvar o novo dataset com a classificação
df.to_csv(output_path, index=False)

print(f"Processamento concluído! Resultados:")
print(f"Total de crianças < 6 meses: {len(df)}")
print(f"Crianças em AME (aleitamento_materno_exclusivo=1): {df['aleitamento_materno_exclusivo'].value_counts().get(1, 0)}")
print(f"Crianças sem AME (aleitamento_materno_exclusivo=2): {df['aleitamento_materno_exclusivo'].value_counts().get(2, 0)}")
print(f"Percentual de aleitamento materno exclusivo: {(df['aleitamento_materno_exclusivo'] == 1).mean()*100:.1f}%")
print(f"Arquivo salvo em: {output_path}")