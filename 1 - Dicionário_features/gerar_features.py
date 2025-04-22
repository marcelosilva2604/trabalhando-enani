import pandas as pd
import os

# Lê o dicionário (agora com caminho relativo atualizado)
df = pd.read_excel("../4-Dicionario-ENANI-2019 (1).xlsx")

# Cria um DataFrame para armazenar o resultado
result = []

# Itera por cada variável única
for variavel in df["variavel"].unique():
    # Filtra o DataFrame para a variável atual
    var_df = df[df["variavel"] == variavel]
    
    # Pega a descrição da variável (é a mesma para todos os valores da mesma variável)
    descricao = var_df["descricao"].iloc[0]
    
    # Cria uma lista para armazenar os valores possíveis e suas descrições
    valores_possiveis = []
    
    # Adiciona cada valor possível e sua descrição à lista
    for _, row in var_df.iterrows():
        if pd.notna(row["valor"]) and pd.notna(row["descricao_labels"]):
            valores_possiveis.append(f"{row['valor']} - {row['descricao_labels']}")
    
    # Converte a lista em uma string, com cada valor em uma linha
    valores_str = "\n      ".join(valores_possiveis) if valores_possiveis else "N/A"
    
    # Adiciona a variável, sua descrição e valores possíveis ao resultado
    result.append({
        "variavel": variavel,
        "descricao": descricao,
        "valores_possiveis": valores_str
    })

# Cria um DataFrame com o resultado
result_df = pd.DataFrame(result)

# Ordena o DataFrame pelo nome da variável
result_df = result_df.sort_values("variavel")

# Cria o conteúdo do arquivo
conteudo = ""
for _, row in result_df.iterrows():
    conteudo += f"Variável: {row['variavel']}\n"
    conteudo += f"Significado: {row['descricao']}\n"
    conteudo += f"Valores possíveis:\n      {row['valores_possiveis']}\n\n"

# Escreve o conteúdo no arquivo (mantendo o caminho para a pasta atual)
with open("features_enani.txt", "w") as f:
    f.write(conteudo)

print("Arquivo criado com sucesso: features_enani.txt")
print(f"Total de variáveis: {len(result_df)}") 