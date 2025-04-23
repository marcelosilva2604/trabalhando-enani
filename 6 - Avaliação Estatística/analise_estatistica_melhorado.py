import pandas as pd
import numpy as np
import os
import importlib
import sys

# Verificar se scipy está instalado corretamente
try:
    from scipy import stats
    print("Biblioteca scipy importada com sucesso!")
except ImportError:
    print("Erro ao importar scipy. Tentando instalar...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "--break-system-packages", "scipy"])
    try:
        from scipy import stats
        print("Scipy instalado e importado com sucesso!")
    except ImportError:
        print("Falha ao instalar scipy. Usando implementação simplificada.")
        stats = None

# Criar diretório de saída se não existir
os.makedirs('resultados', exist_ok=True)

# Carregar o dataset com a feature aleitamento_materno_exclusivo na primeira coluna
print("Carregando dataset...")
df = pd.read_csv('../5 - limpeza e pre processamento/dataset_final.csv')
print(f"Dataset carregado com {df.shape[0]} linhas e {df.shape[1]} colunas.")

# Verificar se a primeira coluna é aleitamento_materno_exclusivo
target_col = 'aleitamento_materno_exclusivo'
if df.columns[0] != target_col:
    print(f"ATENÇÃO: A primeira coluna não é {target_col}. Verificando se existe no dataset...")
    if target_col in df.columns:
        print(f"Coluna {target_col} encontrada. Movendo para primeira posição...")
        cols = df.columns.tolist()
        cols.remove(target_col)
        cols = [target_col] + cols
        df = df[cols]
    else:
        raise ValueError(f"Coluna {target_col} não encontrada no dataset!")

print(f"Valores na coluna alvo: {df[target_col].value_counts().to_dict()}")

# Separar a variável alvo
target = df[target_col]
features = df.drop(columns=[target_col])

# Funções simplificadas para usar caso o scipy falhe
def chi2_simplified(contingency_table):
    """Implementação simplificada do teste Chi-quadrado"""
    rows, cols = contingency_table.shape
    total = contingency_table.sum().sum()
    
    # Se alguma linha ou coluna tem soma zero, não podemos calcular
    if (contingency_table.sum(axis=0) == 0).any() or (contingency_table.sum(axis=1) == 0).any():
        return 1.0
    
    chi2 = 0
    for i in range(rows):
        for j in range(cols):
            observed = contingency_table.iloc[i, j]
            row_sum = contingency_table.iloc[i, :].sum()
            col_sum = contingency_table.iloc[:, j].sum()
            expected = row_sum * col_sum / total
            
            # Evitar divisão por zero
            if expected > 0:
                chi2 += ((observed - expected) ** 2) / expected
    
    # Graus de liberdade
    df = (rows - 1) * (cols - 1)
    
    import math
    # Aproximação para p-valor (simplificada)
    if df == 1:
        # Correção de Yates para 2x2
        p_valor = math.exp(-0.5 * chi2) if chi2 < 10 else 0.0001
    else:
        p_valor = math.exp(-0.5 * (chi2 - df)) if chi2 > df else 0.5
    
    return min(p_valor, 1.0)

def fisher_exact_simplified(table):
    """Implementação simplificada do teste exato de Fisher para tabelas 2x2"""
    if table.shape != (2, 2):
        return 1.0  # Não é uma tabela 2x2
    
    a = table.iloc[0, 0]
    b = table.iloc[0, 1]
    c = table.iloc[1, 0]
    d = table.iloc[1, 1]
    
    import math
    
    # Calcular fatorial de forma simplificada
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        return n * factorial(n-1)
    
    # Evitar overflow em fatoriais grandes
    try:
        p = (factorial(a+b) * factorial(c+d) * factorial(a+c) * factorial(b+d)) / (factorial(a) * factorial(b) * factorial(c) * factorial(d) * factorial(a+b+c+d))
    except OverflowError:
        # Aproximação para tabelas com valores grandes
        p = 0.1
    
    return min(p, 1.0)

def ttest_simplified(group1, group2):
    """Implementação simplificada do teste t"""
    n1, n2 = len(group1), len(group2)
    
    # Se algum grupo tem menos de 2 elementos, não podemos calcular
    if n1 < 2 or n2 < 2:
        return 1.0
    
    # Calcular médias e variâncias
    mean1, mean2 = group1.mean(), group2.mean()
    var1, var2 = group1.var(), group2.var()
    
    # Evitar divisão por zero
    if var1 <= 0 or var2 <= 0:
        return 1.0 if mean1 == mean2 else 0.0001
    
    import math
    # t-statistic (assumindo variâncias desiguais)
    pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
    t_stat = abs(mean1 - mean2) / math.sqrt(pooled_var * (1/n1 + 1/n2))
    
    # Graus de liberdade
    df = n1 + n2 - 2
    
    # Aproximação para p-valor (simplificada)
    p_valor = 1.0 / (1.0 + t_stat * math.sqrt(0.5))
    
    return min(p_valor, 1.0)

def mannwhitneyu_simplified(x, y):
    """Implementação simplificada do teste Mann-Whitney U"""
    # Concatenar os dados e preservar a origem
    all_data = [(val, 0) for val in x] + [(val, 1) for val in y]
    
    # Ordenar por valor
    all_data.sort(key=lambda x: x[0])
    
    # Atribuir ranks (posições)
    n = len(all_data)
    ranks = [0] * n
    
    # Lidar com empates
    i = 0
    while i < n:
        j = i
        while j < n and all_data[j][0] == all_data[i][0]:
            j += 1
        
        # Média dos ranks para valores empatados
        rank = (i + j - 1) / 2
        for k in range(i, j):
            ranks[k] = rank
        
        i = j
    
    # Somar ranks do primeiro grupo
    r1 = sum(ranks[i] for i in range(n) if all_data[i][1] == 0)
    
    # Calcular estatística U
    n1, n2 = len(x), len(y)
    u1 = r1 - n1 * (n1 + 1) / 2
    
    # Aproximação para p-valor usando distribuição normal
    import math
    mean_u = n1 * n2 / 2
    std_u = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    
    if std_u == 0:
        return 0.5
    
    z = abs(u1 - mean_u) / std_u
    # Aproximação para função de distribuição normal
    p_valor = 1 - 0.5 * (1 + math.erf(z / math.sqrt(2)))
    
    return min(p_valor * 2, 1.0)  # Multiplicar por 2 para teste bilateral

def check_normality(data, alpha=0.05):
    """Verifica normalidade de uma distribuição usando teste de Shapiro-Wilk"""
    if len(data) < 3:
        return True  # Poucos dados para testar normalidade
    
    if len(data) > 5000:
        # Amostra para conjuntos grandes
        data = data.sample(5000, random_state=42)
    
    if stats is not None:
        try:
            _, p_valor = stats.shapiro(data)
            is_normal = p_valor > alpha
            return is_normal
        except Exception as e:
            print(f"Erro no teste de normalidade: {str(e)}")
            return True  # Em caso de erro, assume normalidade
    else:
        # Se scipy não estiver disponível, verificar assimetria e curtose (simplificado)
        skewness = data.skew()
        kurtosis = data.kurtosis()
        return abs(skewness) < 1 and abs(kurtosis) < 3  # Valores aproximados

# Inicializar contadores para monitorar testes
testes_aplicados = {
    'Chi-quadrado': 0,
    'Teste Exato de Fisher': 0,
    't-test': 0,
    'Mann-Whitney U': 0,
    'Outros': 0
}

# Inicializar listas para armazenar resultados
resultados = []
features_significativas = []

# Analisar cada feature
print(f"Analisando relações estatísticas para {features.shape[1]} features...")

for col in features.columns:
    # Obter dados da feature atual
    feature_data = features[col]
    
    # Verificar se a feature tem dados
    if feature_data.isna().all():
        resultado = {
            'feature': col,
            'classificacao': 'Indeterminada',
            'teste': 'Nenhum - Todos valores NA',
            'p_valor': 1.0,
            'significativa': False
        }
        resultados.append(resultado)
        testes_aplicados['Outros'] += 1
        continue
    
    # Determinar o tipo da feature
    if feature_data.dtype == 'object' or pd.api.types.is_categorical_dtype(feature_data):
        tipo = 'Qualitativa'
    else:
        # Verificar se é numérica discreta ou contínua
        unique_values = feature_data.dropna().unique()
        if len(unique_values) <= 10:
            tipo = 'Qualitativa'  # Tratamos numéricas discretas como qualitativas
        else:
            tipo = 'Quantitativa'
    
    # Aplicar o teste apropriado
    try:
        if tipo == 'Qualitativa':
            # Criar tabela de contingência
            crosstab = pd.crosstab(feature_data, target)
            
            # Se todas as colunas ou linhas são zero, não podemos realizar o teste
            if crosstab.shape[0] <= 1 or crosstab.shape[1] <= 1:
                p_valor = 1.0
                teste = 'Nenhum - Variabilidade insuficiente'
                testes_aplicados['Outros'] += 1
            else:
                # Verificar se devemos usar teste exato de Fisher
                usar_fisher = (crosstab.shape[0] == 2 and crosstab.shape[1] == 2 and 
                               (crosstab < 5).any().any())
                
                if usar_fisher:
                    # Teste exato de Fisher para tabelas 2x2 com valores esperados pequenos
                    if stats is not None:
                        try:
                            _, p_valor = stats.fisher_exact(crosstab)
                            teste = 'Teste Exato de Fisher'
                            testes_aplicados['Teste Exato de Fisher'] += 1
                        except Exception as e:
                            print(f"Erro no teste exato de Fisher para {col}: {str(e)}")
                            p_valor = fisher_exact_simplified(crosstab)
                            teste = 'Teste Exato de Fisher (simplificado)'
                            testes_aplicados['Teste Exato de Fisher'] += 1
                    else:
                        p_valor = fisher_exact_simplified(crosstab)
                        teste = 'Teste Exato de Fisher (simplificado)'
                        testes_aplicados['Teste Exato de Fisher'] += 1
                else:
                    # Teste Chi-quadrado para tabelas maiores
                    if stats is not None:
                        try:
                            chi2, p_valor, _, _ = stats.chi2_contingency(crosstab)
                            teste = 'Chi-quadrado'
                            testes_aplicados['Chi-quadrado'] += 1
                        except Exception as e:
                            print(f"Erro no teste chi-quadrado para {col}: {str(e)}")
                            p_valor = chi2_simplified(crosstab)
                            teste = 'Chi-quadrado (simplificado)'
                            testes_aplicados['Chi-quadrado'] += 1
                    else:
                        p_valor = chi2_simplified(crosstab)
                        teste = 'Chi-quadrado (simplificado)'
                        testes_aplicados['Chi-quadrado'] += 1
        
        else:  # Quantitativa
            # Dividir em grupos pela variável alvo
            grupo1 = feature_data[target == 1].dropna()
            grupo2 = feature_data[target == 2].dropna()
            
            # Verificar se há dados suficientes em ambos os grupos
            if len(grupo1) <= 1 or len(grupo2) <= 1:
                p_valor = 1.0
                teste = 'Nenhum - Dados insuficientes'
                testes_aplicados['Outros'] += 1
            else:
                # Verificar normalidade dos dados
                normal1 = check_normality(grupo1)
                normal2 = check_normality(grupo2)
                
                if normal1 and normal2:
                    # Dados normalmente distribuídos - t-test
                    if stats is not None:
                        try:
                            _, p_valor = stats.ttest_ind(grupo1, grupo2, equal_var=False)
                            teste = 't-test'
                            testes_aplicados['t-test'] += 1
                        except Exception as e:
                            print(f"Erro no t-test para {col}: {str(e)}")
                            p_valor = ttest_simplified(grupo1, grupo2)
                            teste = 't-test (simplificado)'
                            testes_aplicados['t-test'] += 1
                    else:
                        p_valor = ttest_simplified(grupo1, grupo2)
                        teste = 't-test (simplificado)'
                        testes_aplicados['t-test'] += 1
                else:
                    # Dados não normais - teste não paramétrico
                    if stats is not None:
                        try:
                            _, p_valor = stats.mannwhitneyu(grupo1, grupo2)
                            teste = 'Mann-Whitney U'
                            testes_aplicados['Mann-Whitney U'] += 1
                        except Exception as e:
                            print(f"Erro no Mann-Whitney U para {col}: {str(e)}")
                            p_valor = mannwhitneyu_simplified(grupo1, grupo2)
                            teste = 'Mann-Whitney U (simplificado)'
                            testes_aplicados['Mann-Whitney U'] += 1
                    else:
                        p_valor = mannwhitneyu_simplified(grupo1, grupo2)
                        teste = 'Mann-Whitney U (simplificado)'
                        testes_aplicados['Mann-Whitney U'] += 1
    
    except Exception as e:
        p_valor = 1.0
        teste = f'Erro: {str(e)[:50]}...'
        testes_aplicados['Outros'] += 1
    
    # Determinar significância (p < 0.05)
    significativa = p_valor < 0.05
    
    # Armazenar resultado
    resultado = {
        'feature': col,
        'classificacao': tipo,
        'teste': teste,
        'p_valor': p_valor,
        'significativa': significativa
    }
    resultados.append(resultado)
    
    # Se for significativa, adicionar à lista
    if significativa:
        features_significativas.append(col)
    
    # Progresso a cada 10 features
    if len(resultados) % 10 == 0:
        print(f"Processadas {len(resultados)} de {len(features.columns)} features...")

# Converter resultados para dataframe
df_resultados = pd.DataFrame(resultados)

# Ordenar por p-valor
df_resultados = df_resultados.sort_values('p_valor')

# Salvar relatório completo
df_resultados.to_csv('resultados/relatorio_estatistico_completo.csv', index=False)

# Salvar lista de features excluídas
df_excluidas = df_resultados[~df_resultados['significativa']]
df_excluidas.to_csv('resultados/features_excluidas.csv', index=False)

# Criar dataset apenas com features significativas
print(f"Criando dataset com {len(features_significativas)} features estatisticamente significativas (p<0.05)...")
cols_significativas = [target_col] + features_significativas
df_significativas = df[cols_significativas]

# Salvar dataset com features significativas
df_significativas.to_csv('dataset_f_est.csv', index=False)

# Estatísticas dos testes
print("\n=== ESTATÍSTICAS DOS TESTES APLICADOS ===")
for teste, contagem in testes_aplicados.items():
    print(f"{teste}: {contagem}")

# Imprimir resumo
total_features = len(df_resultados)
total_significativas = len(features_significativas)
percentual = (total_significativas / total_features) * 100 if total_features > 0 else 0

print("\n=== RESUMO DA ANÁLISE ESTATÍSTICA ===")
print(f"Total de features analisadas: {total_features}")
print(f"Features estatisticamente significativas (p<0.05): {total_significativas} ({percentual:.1f}%)")
print(f"Features não significativas: {total_features - total_significativas}")
print(f"\nResultados salvos em:")
print(f"- Relatório completo: resultados/relatorio_estatistico_completo.csv")
print(f"- Features excluídas: resultados/features_excluidas.csv")
print(f"- Dataset final com features significativas: dataset_f_est.csv") 