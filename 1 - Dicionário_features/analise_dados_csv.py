#!/usr/bin/env python
# coding: utf-8

"""
Análise de Dados ENANI-2019

Este script analisa os arquivos CSV do banco de dados ENANI-2019 para determinar:
1. Quantos usuários (crianças) estão cadastrados 
2. Quantas features (variáveis) existem no conjunto de dados
"""

import pandas as pd
import os
import glob
import numpy as np

# Caminho para a pasta com os arquivos CSV
data_dir = '/Users/marcelosilva/Desktop/artigo_novo/Banco de dados CSV'

# Obter lista de todos os arquivos CSV na pasta
csv_files = glob.glob(os.path.join(data_dir, '*.csv'))
print(f"Total de arquivos CSV encontrados: {len(csv_files)}")

# Mostrar os primeiros 5 arquivos para verificação
for file in csv_files[:5]:
    print(f"- {os.path.basename(file)}")

print("\n" + "="*50)
print("ANÁLISE DO ARQUIVO PRINCIPAL DE CRIANÇAS")
print("="*50)

# Vamos primeiro analisar o arquivo principal de crianças
crianca_file = os.path.join(data_dir, 'data_crianca_calib_anon.csv')

# Verificar se o arquivo existe
if os.path.exists(crianca_file):
    # Ler apenas as primeiras linhas para entender a estrutura
    crianca_sample = pd.read_csv(crianca_file, nrows=5)
    print("Amostra do arquivo de crianças (primeiras 5 linhas, primeiras 5 colunas):")
    print(crianca_sample.iloc[:, :5])
    
    # Contar número total de registros (crianças)
    # Usando pandas para contar linhas
    num_criancas = len(pd.read_csv(crianca_file))
    print(f"\nTotal de crianças no dataset: {num_criancas}")
    
    # Contar número de colunas (features)
    num_features_crianca = len(crianca_sample.columns)
    print(f"Total de features no arquivo de crianças: {num_features_crianca}")
    
    # Listar as primeiras 10 features para verificação
    print("\nPrimeiras 10 features:")
    for i, col in enumerate(crianca_sample.columns[:10]):
        print(f"{i+1}. {col}")
else:
    print(f"Arquivo {crianca_file} não encontrado!")

print("\n" + "="*50)
print("ANÁLISE DE TODOS OS ARQUIVOS CSV")
print("="*50)

# Vamos analisar todos os arquivos para identificar o número total de features
file_info = []
all_columns = set()

# Para cada arquivo CSV, vamos extrair informações básicas
for csv_file in csv_files:
    filename = os.path.basename(csv_file)
    try:
        # Ler apenas as primeiras linhas para economizar memória
        df_sample = pd.read_csv(csv_file, nrows=5)
        num_rows = len(pd.read_csv(csv_file))
        num_cols = len(df_sample.columns)
        
        # Adicionar colunas ao conjunto total
        all_columns.update(df_sample.columns)
        
        # Armazenar informações
        file_info.append({
            'arquivo': filename,
            'num_registros': num_rows,
            'num_colunas': num_cols
        })
        
        print(f"Processado: {filename} - {num_rows} registros, {num_cols} colunas")
    except Exception as e:
        print(f"Erro ao processar {filename}: {e}")

# Criar DataFrame com as informações coletadas
info_df = pd.DataFrame(file_info)
print("\nInformações sobre os arquivos CSV:")
print(info_df)

# Mostrar estatísticas
print(f"\nTotal de arquivos processados: {len(info_df)}")
print(f"Total de features únicas em todos os arquivos: {len(all_columns)}")
print(f"Média de registros por arquivo: {info_df['num_registros'].mean():.1f}")
print(f"Média de colunas por arquivo: {info_df['num_colunas'].mean():.1f}")

print("\n" + "="*50)
print("VERIFICAÇÃO DE IDs ÚNICOS")
print("="*50)

# Vamos verificar se há uma coluna de ID que pode ser usada para contar usuários únicos
# Primeiro, verificamos o arquivo de crianças
if os.path.exists(crianca_file):
    df_crianca = pd.read_csv(crianca_file)
    
    # Verificar colunas que podem conter IDs
    id_columns = [col for col in df_crianca.columns if 'id' in col.lower()]
    print(f"Possíveis colunas de ID: {id_columns}")
    
    # Para cada possível coluna de ID, contar valores únicos
    if id_columns:
        print("\nContagem de IDs únicos:")
        for id_col in id_columns:
            num_unique = df_crianca[id_col].nunique()
            print(f"Coluna {id_col}: {num_unique} valores únicos")
    else:
        print("Nenhuma coluna de ID identificada")

print("\n" + "="*50)
print("RESUMO DA ANÁLISE DO BANCO DE DADOS ENANI-2019")
print("="*50)

if 'df_crianca' in locals():
    print(f"Total de crianças (registros no arquivo principal): {len(df_crianca)}")
    
    # Se encontramos colunas de ID, usar a que tem mais valores únicos
    if 'id_columns' in locals() and id_columns:
        id_counts = {col: df_crianca[col].nunique() for col in id_columns}
        main_id_col = max(id_counts, key=id_counts.get)
        print(f"Coluna de ID principal: {main_id_col} com {id_counts[main_id_col]} valores únicos")

print(f"\nTotal de arquivos CSV analisados: {len(csv_files)}")
print(f"Total de features únicas em todos os arquivos: {len(all_columns)}")

# Exibir os 5 arquivos com mais colunas
top_files = info_df.sort_values('num_colunas', ascending=False).head(5)
print("\n5 arquivos com mais features:")
for i, (idx, row) in enumerate(top_files.iterrows()):
    print(f"{i+1}. {row['arquivo']} - {row['num_colunas']} features")

print("\n" + "="*50)
print("FIM DA ANÁLISE")
print("="*50) 