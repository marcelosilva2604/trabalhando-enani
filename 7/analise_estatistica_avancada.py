import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import chi2_contingency, pearsonr, spearmanr, pointbiserialr, kendalltau
import warnings
warnings.filterwarnings('ignore')

# Função para determinar o tipo de variável
def identificar_tipo_variavel(series):
    """
    Identifica o tipo de variável:
    - Categórica nominal
    - Categórica ordinal
    - Numérica discreta
    - Numérica contínua
    """
    unique_values = series.nunique()
    
    # Verifica se é string
    if series.dtype == 'object':
        # Verificar se pode ser convertida para numérica
        try:
            numeric_series = pd.to_numeric(series)
            if (numeric_series == numeric_series.astype(int)).all():
                # É numérica discreta convertida de string
                return "Numérica discreta"
            else:
                # É numérica contínua convertida de string
                return "Numérica contínua"
        except:
            # É categórica
            if unique_values <= 10:
                # Assumindo como nominal se tiver poucos valores únicos
                return "Categórica nominal"
            else:
                return "Categórica nominal"
    
    # Verifica se é numérica
    elif pd.api.types.is_numeric_dtype(series):
        # Verifica se os valores são inteiros
        if (series.dropna() == series.dropna().astype(int)).all():
            if unique_values <= 10:
                # Valores inteiros com poucos únicos
                return "Categórica ordinal"
            else:
                # Valores inteiros com muitos únicos
                return "Numérica discreta"
        else:
            # Valores com decimais
            return "Numérica contínua"
    
    # Outros tipos de dados
    else:
        return "Desconhecida"

# Função para calcular a força da associação
def calcular_forca_associacao(feature, target, tipo_feature):
    """
    Calcula a força da associação entre uma feature e a variável alvo
    baseada no tipo de variável, retornando também o método utilizado
    """
    method = ""
    strength = np.nan
    
    # Remover valores ausentes
    data = pd.DataFrame({
        'feature': feature,
        'target': target
    }).dropna()
    
    # Se não houver dados suficientes após remoção de NA
    if len(data) < 5:
        return np.nan, "Dados insuficientes"
    
    feature = data['feature']
    target = data['target']
    
    # Variável categórica vs categórica (Chi-quadrado + Cramer's V)
    if tipo_feature in ["Categórica nominal", "Categórica ordinal"]:
        try:
            # Converter para strings para garantir tabela de contingência correta
            contingency_table = pd.crosstab(feature.astype(str), target.astype(str))
            
            # Calcular Cramer's V
            chi2, p, dof, expected = chi2_contingency(contingency_table)
            n = contingency_table.sum().sum()
            phi2 = chi2 / n
            r, k = contingency_table.shape
            phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
            rcorr = r - ((r-1)**2)/(n-1)
            kcorr = k - ((k-1)**2)/(n-1)
            strength = np.sqrt(phi2corr / min((kcorr-1), (rcorr-1)))
            method = "Cramer's V"
        except Exception as e:
            # Erro ao calcular Cramer's V
            try:
                # Tentar correlação de Spearman (para ordinais)
                correlation, p = spearmanr(feature, target)
                strength = abs(correlation)
                method = "Spearman's Rank Correlation"
            except:
                strength = np.nan
                method = f"Erro: {str(e)}"
    
    # Variável numérica vs categórica binária
    elif tipo_feature in ["Numérica discreta", "Numérica contínua"] and target.nunique() <= 2:
        try:
            # Correlação Point-Biserial
            correlation, p = pointbiserialr(target, feature)
            strength = abs(correlation)
            method = "Point-Biserial Correlation"
        except Exception as e:
            strength = np.nan
            method = f"Erro: {str(e)}"
    
    # Variável numérica vs categórica (mais de 2 categorias)
    elif tipo_feature in ["Numérica discreta", "Numérica contínua"]:
        try:
            # ANOVA para categorias
            categories = target.unique()
            samples = [feature[target == cat].dropna() for cat in categories]
            f_stat, p_val = stats.f_oneway(*samples)
            
            # Eta squared como medida de força
            SS_total = sum((feature - feature.mean())**2)
            SS_between = sum(len(sample) * ((sample.mean() - feature.mean())**2) for sample in samples)
            strength = SS_between / SS_total
            method = "Eta-squared (ANOVA)"
        except Exception as e:
            try:
                # Kruskal-Wallis para distribuições não normais
                h_stat, p_val = stats.kruskal(*samples)
                strength = h_stat / (len(feature) - 1)  # Aproximação da força
                method = "Kruskal-Wallis H (normalizado)"
            except:
                strength = np.nan
                method = f"Erro: {str(e)}"
    
    # Se não for possível calcular
    if np.isnan(strength):
        try:
            # Último recurso: Kendall's Tau
            correlation, p = kendalltau(feature, target)
            strength = abs(correlation)
            method = "Kendall's Tau"
        except Exception as e:
            strength = np.nan
            method = f"Sem método apropriado: {str(e)}"
    
    return strength, method

# Função para classificar a força da associação
def classificar_forca(valor, metodo):
    """
    Classifica a força da associação com base no valor e método
    """
    if pd.isna(valor):
        return "Não calculável"
    
    # Classificação específica por método
    if "Cramer's V" in metodo:
        if valor < 0.1:
            return "Negligenciável"
        elif valor < 0.2:
            return "Fraca"
        elif valor < 0.3:
            return "Moderada"
        elif valor < 0.4:
            return "Relativamente forte"
        else:
            return "Forte"
    
    elif "Pearson" in metodo or "Spearman" in metodo or "Point-Biserial" in metodo or "Kendall" in metodo:
        if valor < 0.1:
            return "Negligenciável"
        elif valor < 0.3:
            return "Fraca"
        elif valor < 0.5:
            return "Moderada"
        elif valor < 0.7:
            return "Relativamente forte"
        else:
            return "Forte"
    
    elif "Eta-squared" in metodo or "ANOVA" in metodo:
        if valor < 0.01:
            return "Negligenciável"
        elif valor < 0.06:
            return "Fraca"
        elif valor < 0.14:
            return "Moderada"
        else:
            return "Forte"
    
    # Classificação genérica para outros métodos
    else:
        if valor < 0.2:
            return "Fraca"
        elif valor < 0.4:
            return "Moderada"
        elif valor < 0.6:
            return "Relativamente forte"
        else:
            return "Forte"

# Função para calcular o valor p para a associação
def calcular_valor_p(feature, target, tipo_feature):
    """
    Calcula o valor p para a associação entre uma feature e a variável alvo
    """
    # Remover valores ausentes
    data = pd.DataFrame({
        'feature': feature,
        'target': target
    }).dropna()
    
    # Se não houver dados suficientes após remoção de NA
    if len(data) < 5:
        return np.nan
    
    feature = data['feature']
    target = data['target']
    
    # Variável categórica vs categórica (Chi-quadrado)
    if tipo_feature in ["Categórica nominal", "Categórica ordinal"]:
        try:
            contingency_table = pd.crosstab(feature.astype(str), target.astype(str))
            chi2, p, dof, expected = chi2_contingency(contingency_table)
            return p
        except:
            pass
    
    # Variável numérica vs categórica binária
    elif tipo_feature in ["Numérica discreta", "Numérica contínua"] and target.nunique() <= 2:
        try:
            correlation, p = pointbiserialr(target, feature)
            return p
        except:
            pass
    
    # Variável numérica vs categórica (mais de 2 categorias)
    elif tipo_feature in ["Numérica discreta", "Numérica contínua"]:
        try:
            categories = target.unique()
            samples = [feature[target == cat].dropna() for cat in categories]
            f_stat, p_val = stats.f_oneway(*samples)
            return p_val
        except:
            try:
                h_stat, p_val = stats.kruskal(*samples)
                return p_val
            except:
                pass
    
    # Se nenhum dos métodos acima funcionar, tentar Kendall's Tau
    try:
        correlation, p = kendalltau(feature, target)
        return p
    except:
        return np.nan

# Função principal
def analisar_dataset():
    print("Carregando dataset...")
    df = pd.read_csv('./6 - Avaliação Estatística/dataset_f_est.csv', low_memory=False)
    
    # Variável alvo
    target_col = 'aleitamento_materno_exclusivo'
    target = df[target_col]
    
    print(f"Total de registros no dataset: {len(df)}")
    print(f"Total de variáveis no dataset: {len(df.columns)}")
    
    # Criar dataframe para armazenar resultados
    resultados = []
    
    print("Analisando associações das variáveis com aleitamento materno exclusivo...")
    
    # Analisar cada feature
    for feature_col in df.columns:
        # Pular a própria variável alvo
        if feature_col == target_col:
            continue
        
        feature = df[feature_col]
        
        # Identificar tipo de variável
        tipo_variavel = identificar_tipo_variavel(feature)
        
        # Calcular valor p
        p_valor = calcular_valor_p(feature, target, tipo_variavel)
        
        # Calcular força da associação e método utilizado
        forca, metodo = calcular_forca_associacao(feature, target, tipo_variavel)
        
        # Classificar força da associação
        classificacao = classificar_forca(forca, metodo)
        
        # Verificar significância estatística
        significancia = "Significativa" if p_valor is not None and p_valor < 0.05 else "Não significativa"
        
        # Adicionar resultado
        resultados.append({
            'feature': feature_col,
            'tipo_variavel': tipo_variavel,
            'valor_p': p_valor,
            'significancia': significancia,
            'forca_associacao': forca,
            'classificacao_forca': classificacao,
            'metodo_utilizado': metodo
        })
    
    # Criar DataFrame com resultados
    resultados_df = pd.DataFrame(resultados)
    
    # Ordenar resultados por força de associação (decrescente)
    resultados_df = resultados_df.sort_values(by=['significancia', 'forca_associacao'], 
                                             ascending=[False, False])
    
    # Salvar resultados em arquivo txt formatado
    with open('./7/analise_associacoes.txt', 'w') as f:
        f.write("ANÁLISE DE ASSOCIAÇÃO COM ALEITAMENTO MATERNO EXCLUSIVO\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total de variáveis analisadas: {len(resultados_df)}\n")
        f.write(f"Variáveis significativas (p<0.05): {sum(resultados_df['significancia'] == 'Significativa')}\n\n")
        f.write("="*80 + "\n\n")
        
        f.write("RESULTADOS DETALHADOS (ordenados por significância e força de associação)\n\n")
        
        for _, row in resultados_df.iterrows():
            f.write(f"Variável: {row['feature']}\n")
            f.write(f"Tipo: {row['tipo_variavel']}\n")
            f.write(f"Valor p: {row['valor_p'] if not pd.isna(row['valor_p']) else 'Não calculado'}\n")
            f.write(f"Significância: {row['significancia']}\n")
            f.write(f"Força de associação: {row['forca_associacao'] if not pd.isna(row['forca_associacao']) else 'Não calculada'}\n")
            f.write(f"Classificação da força: {row['classificacao_forca']}\n")
            f.write(f"Método utilizado: {row['metodo_utilizado']}\n")
            f.write("-"*50 + "\n\n")
    
    # Salvar resultados em CSV também para referência
    resultados_df.to_csv('./7/analise_associacoes.csv', index=False)
    
    print(f"Análise concluída! Resultados salvos em './7/analise_associacoes.txt' e './7/analise_associacoes.csv'")
    
    # Retornar a lista de variáveis significativas mais fortes para referência
    significativas = resultados_df[resultados_df['significancia'] == 'Significativa']
    top_10 = significativas.head(10)
    
    print("\nTop 10 variáveis mais fortemente associadas ao aleitamento materno exclusivo:")
    for i, (_, row) in enumerate(top_10.iterrows(), 1):
        print(f"{i}. {row['feature']} - {row['classificacao_forca']} ({row['forca_associacao']:.4f})")

if __name__ == "__main__":
    analisar_dataset() 