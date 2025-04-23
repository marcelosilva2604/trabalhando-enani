import pandas as pd
import re
import os

def extrair_dicionario_variaveis(arquivo_dicionario):
    """
    Extrai o dicionário de variáveis do arquivo de texto do ENANI
    """
    print(f"Extraindo significados do arquivo: {arquivo_dicionario}")
    dicionario = {}
    
    with open(arquivo_dicionario, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Padrão para encontrar blocos de variáveis
    padrao = r'Variável:\s+(.+?)\nSignificado:\s+(.+?)\nValores possíveis:([\s\S]+?)(?=\n\nVariável:|$)'
    
    matches = re.finditer(padrao, conteudo)
    
    for match in matches:
        variavel = match.group(1).strip()
        significado = match.group(2).strip()
        valores = match.group(3).strip()
        
        # Limpar o nome da variável (remover possíveis descrições)
        if ' - ' in variavel:
            nome_var = variavel.split(' - ')[0].strip()
        else:
            nome_var = variavel
        
        # Limpar o significado (remover o código da variável se estiver repetido)
        if significado.startswith(nome_var):
            significado = significado[len(nome_var):].strip()
            if significado.startswith('- '):
                significado = significado[2:].strip()
            if significado.startswith('-'):
                significado = significado[1:].strip()
        
        # Extrair valores possíveis de maneira formatada
        valores_formatados = []
        for linha in valores.split('\n'):
            linha = linha.strip()
            if ' - ' in linha:
                codigo, desc = linha.split(' - ', 1)
                valores_formatados.append(f"{codigo.strip()}: {desc.strip()}")
        
        # Armazenar no dicionário
        dicionario[nome_var] = {
            'significado': significado,
            'valores': valores_formatados if valores_formatados else ['Valores não especificados']
        }
    
    print(f"Total de variáveis extraídas do dicionário: {len(dicionario)}")
    return dicionario

def obter_variaveis_dataset(arquivo_dataset):
    """
    Obtém a lista de variáveis presentes no dataset
    """
    print(f"Obtendo variáveis do dataset: {arquivo_dataset}")
    df = pd.read_csv(arquivo_dataset, nrows=1)
    variaveis = list(df.columns)
    return variaveis

def gerar_dicionario_significados(dicionario_enani, variaveis_dataset):
    """
    Gera um dicionário apenas com as variáveis do dataset
    """
    dicionario_filtrado = {}
    
    for var in variaveis_dataset:
        if var in dicionario_enani:
            dicionario_filtrado[var] = dicionario_enani[var]
        else:
            dicionario_filtrado[var] = {
                'significado': 'Significado não encontrado no dicionário ENANI',
                'valores': ['Valores não especificados']
            }
    
    return dicionario_filtrado

def escrever_arquivo_significados(dicionario_filtrado, arquivo_saida):
    """
    Escreve o arquivo de saída com os significados das variáveis
    """
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write("DICIONÁRIO DE VARIÁVEIS DO DATASET - ENANI 2019\n")
        f.write("="*80 + "\n\n")
        
        for var, info in dicionario_filtrado.items():
            f.write(f"Variável: {var}\n")
            f.write(f"Significado: {info['significado']}\n")
            
            if info['valores'][0] != 'Valores não especificados':
                f.write("Valores possíveis:\n")
                for valor in info['valores']:
                    f.write(f"  {valor}\n")
            else:
                f.write("Valores possíveis: Não especificados\n")
            
            f.write("\n" + "-"*50 + "\n\n")

def gerar_resumo_analise(arquivo_analise, arquivo_resumo):
    """
    Gera o resumo da análise estatística
    """
    print("Gerando resumo da análise estatística...")
    resultados = pd.read_csv(arquivo_analise)
    
    # Filtrar resultados significativos
    resultados_significativos = resultados[resultados['significancia'] == 'Significativa']
    
    # Contar o número de variáveis por classificação de força
    contagem_classificacao = resultados_significativos['classificacao_forca'].value_counts().to_dict()
    
    # Ordenar variáveis por força de associação
    resultados_ordenados = resultados_significativos.sort_values(by='forca_associacao', ascending=False)
    
    # Obter top 20 variáveis mais importantes
    top_20 = resultados_ordenados.head(20)
    
    # Criar arquivo de resumo
    with open(arquivo_resumo, 'w') as f:
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
    
    print(f"Resumo da análise gerado em: {arquivo_resumo}")

def aprimorar_resumo_analise(arquivo_resumo, dicionario_filtrado, arquivo_saida):
    """
    Aprimora o resumo da análise adicionando os significados das variáveis
    """
    with open(arquivo_resumo, 'r', encoding='utf-8') as f:
        conteudo_resumo = f.read()
    
    # Procurar por todas as variáveis mencionadas
    variavel_pattern = r'(\w+_\w+)'
    variaveis_mencionadas = re.findall(variavel_pattern, conteudo_resumo)
    variaveis_unicas = set(variaveis_mencionadas)
    
    # Seção de variáveis importantes (encontradas na seção 3 e 6)
    padrao_sec3 = r'3\. TOP 20 VARIÁVEIS MAIS FORTEMENTE ASSOCIADAS[\s\S]+?4\. MÉTODOS ESTATÍSTICOS UTILIZADOS'
    padrao_sec6 = r'6\. CONCLUSÕES PRINCIPAIS[\s\S]+?As principais variáveis associadas ao aleitamento materno exclusivo são:([\s\S]+?)$'
    
    sec3_match = re.search(padrao_sec3, conteudo_resumo)
    sec6_match = re.search(padrao_sec6, conteudo_resumo)
    
    variaveis_importantes = set()
    
    if sec3_match:
        variaveis_sec3 = re.findall(r'(\w+_\w+)', sec3_match.group(0))
        variaveis_importantes.update(variaveis_sec3)
    
    if sec6_match:
        variaveis_sec6 = re.findall(r'(\w+_\w+)', sec6_match.group(0))
        variaveis_importantes.update(variaveis_sec6)
    
    # Criar novo conteúdo
    novo_conteudo = conteudo_resumo.strip()
    
    # Adicionar seção com significados das variáveis importantes
    novo_conteudo += "\n\n" + "="*80 + "\n\n"
    novo_conteudo += "7. SIGNIFICADO DAS VARIÁVEIS IMPORTANTES\n"
    novo_conteudo += "-"*50 + "\n\n"
    
    # Adicionar significados das variáveis mais importantes
    for var in variaveis_importantes:
        if var in dicionario_filtrado:
            significado = dicionario_filtrado[var]['significado']
            novo_conteudo += f"Variável: {var}\n"
            novo_conteudo += f"Significado: {significado}\n"
            
            # Adicionar valores possíveis apenas para variáveis categóricas
            if dicionario_filtrado[var]['valores'][0] != 'Valores não especificados':
                novo_conteudo += "Valores possíveis:\n"
                for valor in dicionario_filtrado[var]['valores'][:5]:  # Limitar a 5 valores para não ficar muito extenso
                    novo_conteudo += f"  {valor}\n"
                
                if len(dicionario_filtrado[var]['valores']) > 5:
                    novo_conteudo += "  (mais valores...)\n"
            
            novo_conteudo += "\n"
    
    # Salvar novo arquivo
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(novo_conteudo)

    print(f"Resumo aprimorado salvo em: {arquivo_saida}")

def main():
    # Definir caminhos
    arquivo_dicionario = './1 - Dicionário_features/features_enani.txt'
    arquivo_dataset = './6 - Avaliação Estatística/dataset_f_est.csv'
    arquivo_analise = './7 - avaliação de força estatistica/analise_associacoes.csv'
    arquivo_saida_dicionario = './7/dicionario_variaveis.txt'
    arquivo_resumo = './7/resumo_analise.txt'
    arquivo_saida_resumo = './7/resumo_analise_completo.txt'
    
    # Gerar o resumo da análise
    gerar_resumo_analise(arquivo_analise, arquivo_resumo)
    
    # Extrair dicionário de variáveis do ENANI
    dicionario_enani = extrair_dicionario_variaveis(arquivo_dicionario)
    
    # Obter variáveis presentes no dataset
    variaveis_dataset = obter_variaveis_dataset(arquivo_dataset)
    
    # Gerar dicionário filtrado com as variáveis do dataset
    dicionario_filtrado = gerar_dicionario_significados(dicionario_enani, variaveis_dataset)
    
    # Escrever arquivo com os significados das variáveis
    escrever_arquivo_significados(dicionario_filtrado, arquivo_saida_dicionario)
    print(f"Dicionário de variáveis salvo em: {arquivo_saida_dicionario}")
    
    # Aprimorar o resumo da análise
    aprimorar_resumo_analise(arquivo_resumo, dicionario_filtrado, arquivo_saida_resumo)

if __name__ == "__main__":
    main() 