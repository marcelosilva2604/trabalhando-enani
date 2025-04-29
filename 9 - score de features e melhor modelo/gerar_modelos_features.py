import pandas as pd
import numpy as np
import os
import warnings
from pycaret.classification import setup, create_model, save_model, predict_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_classif
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

def train_model_with_features(X_train, X_test, y_train, y_test, n_features, output_dir):
    """Treina um modelo com n_features selecionadas"""
    print(f"\n{'='*80}")
    print(f"TREINANDO MODELO COM {n_features} FEATURES")
    print(f"{'='*80}")
    
    try:
        # Criar DataFrames para treino e teste
        train_df = pd.concat([X_train, y_train], axis=1)
        test_df = pd.concat([X_test, y_test], axis=1)
        
        # Configurar PyCaret
        setup_params = {
            'data': train_df,
            'target': 'aleitamento_materno_exclusivo',
            'train_size': 0.7,
            'session_id': 42,
            'normalize': True,
            'feature_selection': False,
            'remove_multicollinearity': False,
            'verbose': False,
            'fold': 5
        }
        
        setup_clf = setup(**setup_params)
        
        # Criar modelo XGBoost
        xgboost = create_model('xgboost')
        
        # Salvar modelo
        model_path = os.path.join(output_dir, f'modelo_{n_features}features.pkl')
        save_model(xgboost, model_path)
        
        # Fazer previsões no conjunto de teste
        predictions = predict_model(xgboost, data=test_df)
        
        # Calcular métricas
        from sklearn.metrics import accuracy_score, roc_auc_score, f1_score
        accuracy = accuracy_score(y_test, predictions['prediction_label'])
        auc = roc_auc_score(y_test, predictions['prediction_score'])
        f1 = f1_score(y_test, predictions['prediction_label'])
        
        print(f"\nMétricas do modelo com {n_features} features:")
        print(f"  Acurácia: {accuracy:.4f}")
        print(f"  AUC: {auc:.4f}")
        print(f"  F1-Score: {f1:.4f}")
        
        return {
            'n_features': n_features,
            'accuracy': accuracy,
            'auc': auc,
            'f1': f1
        }
        
    except Exception as e:
        print(f"ERRO ao treinar modelo: {e}")
        return None

def main():
    print("="*80)
    print("GERANDO MODELOS COM DIFERENTES NÚMEROS DE FEATURES")
    print("="*80)
    
    # Caminhos dos arquivos
    dataset_path = '/Users/marcelosilva/Desktop/artigo_novo/6 - Avaliação Estatística/dataset_f_est.csv'
    output_dir = '/Users/marcelosilva/Desktop/artigo_novo/9/resultado_pycaret'
    os.makedirs(output_dir, exist_ok=True)
    
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
        
        # Dividir em treino e teste (70/30)
        X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.3, random_state=42, stratify=y)
        print(f"\nDivisão dos dados:")
        print(f"  Treino: {X_train.shape[0]} amostras")
        print(f"  Teste: {X_test.shape[0]} amostras")
        
        # Calcular importância das features
        print("\nCalculando importância das features...")
        selector = SelectKBest(f_classif, k='all')
        selector.fit(X_train, y_train)
        
        # Criar DataFrame com scores das features
        feature_scores = pd.DataFrame({
            'Feature': X_train.columns,
            'Score': selector.scores_,
            'P_Value': selector.pvalues_
        })
        feature_scores = feature_scores.sort_values('Score', ascending=False)
        
        # Salvar feature scores
        feature_scores.to_csv(os.path.join(output_dir, 'feature_score.csv'), index=False)
        
        # Números de features para testar
        n_features_list = [3, 5, 10, 20, 50, X_train.shape[1]]
        
        # Lista para armazenar resultados
        results = []
        
        # Treinar modelos com diferentes números de features
        for n_features in n_features_list:
            # Selecionar as n_features mais importantes
            selected_features = feature_scores['Feature'].head(n_features).tolist()
            
            # Criar DataFrames com features selecionadas
            X_train_selected = X_train[selected_features]
            X_test_selected = X_test[selected_features]
            
            # Treinar modelo
            result = train_model_with_features(X_train_selected, X_test_selected, y_train, y_test, n_features, output_dir)
            if result:
                results.append(result)
        
        # Criar DataFrame com resultados
        results_df = pd.DataFrame(results)
        results_file = os.path.join(output_dir, 'resultados_comparativos.csv')
        results_df.to_csv(results_file, index=False)
        print(f"\nResultados comparativos salvos em: {results_file}")
        
        # Plotar resultados
        plt.figure(figsize=(10, 6))
        plt.plot(results_df['n_features'], results_df['accuracy'], 'b-o', label='Acurácia')
        plt.plot(results_df['n_features'], results_df['auc'], 'r-o', label='AUC')
        plt.plot(results_df['n_features'], results_df['f1'], 'g-o', label='F1-Score')
        plt.xlabel('Número de Features')
        plt.ylabel('Score')
        plt.title('Desempenho do Modelo por Número de Features')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, 'desempenho_por_features.png'))
        plt.close()
        
    except Exception as e:
        print(f"ERRO ao processar dados: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main() 