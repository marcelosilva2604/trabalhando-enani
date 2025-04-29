import pandas as pd
import numpy as np
import os
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

def encode_categorical_columns(df):
    """Codifica variáveis categóricas usando LabelEncoder"""
    df_encoded = df.copy()
    label_encoders = {}
    
    for column in df.columns:
        if df[column].dtype == 'object':
            label_encoders[column] = LabelEncoder()
            df_encoded[column] = label_encoders[column].fit_transform(df[column].astype(str))
    
    return df_encoded, label_encoders

def handle_missing_values(df):
    """Trata valores faltantes usando SimpleImputer"""
    numeric_imputer = SimpleImputer(strategy='mean')
    categorical_imputer = SimpleImputer(strategy='most_frequent')
    
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_columns = df.select_dtypes(include=['object']).columns
    
    if len(numeric_columns) > 0:
        df[numeric_columns] = numeric_imputer.fit_transform(df[numeric_columns])
    if len(categorical_columns) > 0:
        df[categorical_columns] = categorical_imputer.fit_transform(df[categorical_columns])
    
    return df

def main():
    print("="*80)
    print("GERANDO FEATURE SCORE")
    print("="*80)
    
    # Caminhos dos arquivos
    dataset_path = '/Users/marcelosilva/Desktop/artigo_novo/6 - Avaliação Estatística/dataset_f_est.csv'
    output_dir = '/Users/marcelosilva/Desktop/artigo_novo/9'
    
    # Variável alvo
    TARGET = 'aleitamento_materno_exclusivo'
    
    print(f"\nCarregando dataset: {dataset_path}")
    try:
        # Carregar o dataset
        df = pd.read_csv(dataset_path, low_memory=False)
        print(f"Dataset carregado com sucesso: {df.shape[0]} linhas, {df.shape[1]} colunas")
        
        # Separar features e target
        X = df.drop(columns=[TARGET])
        y = df[TARGET]
        
        # Tratar valores faltantes
        print("\nTratando valores faltantes...")
        X = handle_missing_values(X)
        
        # Codificar variáveis categóricas
        print("\nCodificando variáveis categóricas...")
        X_encoded, label_encoders = encode_categorical_columns(X)
        
        # Calcular importância das features usando f_classif
        print("\nCalculando importância das features...")
        selector = SelectKBest(f_classif, k='all')
        selector.fit(X_encoded, y)
        
        # Criar DataFrame com scores das features
        feature_scores = pd.DataFrame({
            'Feature': X_encoded.columns,
            'Score': selector.scores_,
            'P_Value': selector.pvalues_
        })
        
        # Ordenar por score
        feature_scores = feature_scores.sort_values('Score', ascending=False)
        
        # Salvar resultados
        output_file = os.path.join(output_dir, 'feature_score.csv')
        feature_scores.to_csv(output_file, index=False)
        print(f"\nFeature scores salvos em: {output_file}")
        
        # Exibir top 20 features
        print("\nTop 20 features por importância:")
        print(feature_scores.head(20))
        
    except Exception as e:
        print(f"ERRO ao processar dados: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main() 