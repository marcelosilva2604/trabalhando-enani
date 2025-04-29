import pandas as pd
import numpy as np
import os
import warnings
from pycaret.classification import setup, create_model, save_model, load_model, predict_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
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

def train_optimal_model():
    print("="*80)
    print("TREINAMENTO DO MODELO ÓTIMO")
    print("="*80)
    
    # Caminhos dos arquivos
    dataset_path = '/Users/marcelosilva/Desktop/artigo_novo/6 - Avaliação Estatística/dataset_f_est.csv'
    output_dir = '/Users/marcelosilva/Desktop/artigo_novo/9/resultado_pycaret'
    os.makedirs(output_dir, exist_ok=True)
    
    # Variável alvo
    TARGET = 'aleitamento_materno_exclusivo'
    
    # Features selecionadas (nova combinação)
    SELECTED_FEATURES = ['k18_somente', 'k25_mamadeira', 'b05a_idade_em_meses']
    
    print(f"\nCarregando dataset: {dataset_path}")
    try:
        # Carregar o dataset
        df = pd.read_csv(dataset_path, low_memory=False)
        print(f"Dataset carregado com sucesso: {df.shape[0]} linhas, {df.shape[1]} colunas")
        
        # Separar features e target
        X = df.drop(columns=[TARGET])
        y = df[TARGET]
        
        # Selecionar apenas as features específicas
        X = X[SELECTED_FEATURES]
        
        # Tratar valores faltantes
        print("\nTratando valores faltantes...")
        X = handle_missing_values(X)
        
        # Codificar variáveis categóricas
        print("\nCodificando variáveis categóricas...")
        X_encoded, label_encoders = encode_categorical_columns(X)
        
        # Dividir em treino e teste (70/30)
        X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.3, random_state=42, stratify=y)
        print(f"\nDivisão dos dados:")
        print(f"  Treino: {X_train.shape[0]} amostras")
        print(f"  Teste: {X_test.shape[0]} amostras")
        
        # Criar DataFrames para treino e teste
        train_df = pd.concat([X_train, y_train], axis=1)
        test_df = pd.concat([X_test, y_test], axis=1)
        
        # Configurar PyCaret
        print("\nConfigurando ambiente PyCaret...")
        setup_params = {
            'data': train_df,
            'target': TARGET,
            'train_size': 0.7,
            'session_id': 42,
            'normalize': True,
            'feature_selection': False,
            'remove_multicollinearity': False,
            'verbose': False,
            'fold': 5
        }
        
        setup_clf = setup(**setup_params)
        
        # Criar modelo XGBoost (melhor desempenho)
        print("\nTreinando modelo XGBoost...")
        xgboost = create_model('xgboost')
        
        # Salvar modelo
        model_path = os.path.join(output_dir, 'modelo_otimo_xgboost_novo.pkl')
        save_model(xgboost, model_path)
        print(f"\nModelo salvo em: {model_path}")
        
        # Fazer previsões no conjunto de teste
        predictions = predict_model(xgboost, data=test_df)
        
        # Calcular e exibir métricas
        from sklearn.metrics import accuracy_score, roc_auc_score, f1_score
        accuracy = accuracy_score(y_test, predictions['prediction_label'])
        auc = roc_auc_score(y_test, predictions['prediction_score'])
        f1 = f1_score(y_test, predictions['prediction_label'])
        
        print("\nMétricas do modelo:")
        print(f"  Acurácia: {accuracy:.4f}")
        print(f"  AUC: {auc:.4f}")
        print(f"  F1-Score: {f1:.4f}")
        
        # Gerar gráficos
        try:
            from pycaret.classification import plot_model
            plot_model(xgboost, plot='confusion_matrix', save=True)
            plot_model(xgboost, plot='auc', save=True)
            plot_model(xgboost, plot='feature_importance', save=True)
        except Exception as e:
            print(f"Aviso: Não foi possível gerar alguns gráficos: {e}")
        
        return xgboost, accuracy, auc, f1
        
    except Exception as e:
        print(f"ERRO ao processar dados: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None, None

if __name__ == "__main__":
    train_optimal_model() 