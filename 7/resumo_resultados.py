import pandas as pd

# Carregar os resultados da análise
print("Carregando resultados da análise estatística...")
resultados = pd.read_csv('./7/analise_associacoes.csv')

# Filtrar resultados significativos
resultados_significativos = resultados[resultados['significancia'] == 'Significativa']

# Contar o número de variáveis por classificação de força
contagem_classificacao = resultados_significativos['classificacao_forca'].value_counts().to_dict()

# Ordenar variáveis por força de associação
resultados_ordenados = resultados_significativos.sort_values(by='forca_associacao', ascending=False)

# Obter top 20 variáveis mais importantes
top_20 = resultados_ordenados.head(20)

# Criar arquivo de resumo
with open('./7/resumo_analise.txt', 'w') as f:
    f.write("RESUMO DA ANÁLISE ESTATÍSTICA - ASSOCIAÇÃO COM ALEITAMENTO MATERNO EXCLUSIVO\n")
    f.write("="*80 + "\n\n")
    
    # 1. Visão geral
    f.write("1. VISÃO GERAL\n")
    f.write("-"*50 + "\n\n")
    f.write(f"Total de variáveis analisadas: {len(resultados)}\n")
    f.write(f"Variáveis com associação significativa (p<0.05): {len(resultados_significativos)}\n")
    f.write(f"Porcentagem de variáveis significativas: {len(resultados_significativos)/len(resultados)*100:.1f}%\n\n")
    
    # 2. Distribuição por classificação de força
    f.write("2. DISTRIBUIÇÃO POR CLASSIFICAÇÃO DE FORÇA\n")
    f.write("-"*50 + "\n\n")
    
    # Ordem personalizada para exibição
    ordem_classificacao = ['Forte', 'Relativamente forte', 'Moderada', 'Fraca', 'Negligenciável', 'Não calculável']
    
    for classificacao in ordem_classificacao:
        contagem = contagem_classificacao.get(classificacao, 0)
        percentual = contagem / len(resultados_significativos) * 100
        f.write(f"{classificacao}: {contagem} variáveis ({percentual:.1f}%)\n")
    
    f.write("\n")
    
    # 3. Top 20 variáveis mais fortemente associadas
    f.write("3. TOP 20 VARIÁVEIS MAIS FORTEMENTE ASSOCIADAS\n")
    f.write("-"*50 + "\n\n")
    
    for i, (_, row) in enumerate(top_20.iterrows(), 1):
        f.write(f"{i}. {row['feature']}\n")
        f.write(f"   Tipo: {row['tipo_variavel']}\n")
        f.write(f"   Valor p: {row['valor_p']:.8f}\n")
        f.write(f"   Força de associação: {row['forca_associacao']:.4f}\n")
        f.write(f"   Classificação: {row['classificacao_forca']}\n")
        f.write(f"   Método utilizado: {row['metodo_utilizado']}\n\n")
    
    # 4. Métodos estatísticos utilizados
    metodos_contagem = resultados_significativos['metodo_utilizado'].value_counts()
    
    f.write("4. MÉTODOS ESTATÍSTICOS UTILIZADOS\n")
    f.write("-"*50 + "\n\n")
    
    for metodo, contagem in metodos_contagem.items():
        percentual = contagem / len(resultados_significativos) * 100
        f.write(f"{metodo}: {contagem} variáveis ({percentual:.1f}%)\n")
    
    f.write("\n")
    
    # 5. Análise por tipo de variável
    tipos_contagem = resultados['tipo_variavel'].value_counts()
    
    f.write("5. DISTRIBUIÇÃO POR TIPO DE VARIÁVEL\n")
    f.write("-"*50 + "\n\n")
    
    for tipo, contagem in tipos_contagem.items():
        percentual = contagem / len(resultados) * 100
        f.write(f"{tipo}: {contagem} variáveis ({percentual:.1f}%)\n")
    
    f.write("\n")
    
    # 6. Conclusões
    f.write("6. CONCLUSÕES PRINCIPAIS\n")
    f.write("-"*50 + "\n\n")
    
    # Variáveis com força forte ou relativamente forte
    variaveis_fortes = resultados_significativos[
        (resultados_significativos['classificacao_forca'] == 'Forte') | 
        (resultados_significativos['classificacao_forca'] == 'Relativamente forte')
    ]
    
    f.write(f"Foram identificadas {len(variaveis_fortes)} variáveis com associação forte ou relativamente forte.\n\n")
    
    f.write("As principais variáveis associadas ao aleitamento materno exclusivo são:\n")
    for i, (_, row) in enumerate(variaveis_fortes.iterrows(), 1):
        f.write(f"{i}. {row['feature']} ({row['classificacao_forca']}, força = {row['forca_associacao']:.4f})\n")
    
    f.write("\nEstas variáveis devem ser consideradas prioritárias para análise e intervenções relacionadas ao aleitamento materno exclusivo.\n")

print(f"Resumo dos resultados gerado com sucesso em './7/resumo_analise.txt'") 