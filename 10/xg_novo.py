import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score, confusion_matrix, roc_curve, auc
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV
import os
import joblib
import warnings
warnings.filterwarnings('ignore')

# Função para pré-processar as features específicas do dataset
def preprocess_features(X):
    """Pré-processamento específico para as features do dataset, considerando o significado de cada variável"""
    X_processed = X.copy()
    
    # Tratar k18_somente (88 = ainda amamentando exclusivamente)
    # Criar indicador binário para este caso especial
    X_processed['ainda_amamentando'] = (X_processed['k18_somente'] == 88.0).astype(int)
    
    # Converter k18_somente para uma escala mais interpretável
    # Valores diferentes de 88 representam duração do aleitamento exclusivo
    # Manter o valor original para outros casos
    
    # Importante: b05a_idade_em_meses é ordinal representando a idade em meses (0-5)
    # Já é numérica, não precisa de tratamento especial
    
    # k25_mamadeira é categórica com 3 valores: 
    # "Sim, ainda usa", "Sim, já usou mas não usa mais", "Não, nunca usou"
    # Será tratada pelo LabelEncoder, mas podemos criar dummies se necessário
    
    return X_processed

# Função para codificar variáveis categóricas
def encode_categorical_columns(df):
    """Codifica variáveis categóricas usando LabelEncoder"""
    df_encoded = df.copy()
    label_encoders = {}
    
    for column in df.columns:
        if df[column].dtype == 'object':
            label_encoders[column] = LabelEncoder()
            df_encoded[column] = label_encoders[column].fit_transform(df[column].astype(str))
    
    return df_encoded, label_encoders

# Função para tratar valores faltantes
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

# Função para plotar curva ROC
def plot_roc_curve(y_true, y_pred_proba, title="ROC Curve", filename="roc_curve.png"):
    # Especificar pos_label=2 para indicar que 2 é a classe positiva
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba, pos_label=2)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.legend(loc="lower right")
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()
    
    return roc_auc

# Função principal para executar o modelo otimizado para AUC
def main():
    print("="*80)
    print("MODELO GRADIENT BOOSTING OTIMIZADO PARA AUC")
    print("="*80)
    
    # Caminhos dos arquivos - ajuste para seu ambiente
    dataset_path = '/Users/marcelosilva/Desktop/artigo_novo/8/dataset.csv'
    global output_dir
    output_dir = 'resultados_boosting_otimizado'
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Variável alvo
    TARGET = 'aleitamento_materno_exclusivo'
    
    print(f"\nCarregando dataset: {dataset_path}")
    try:
        # Carregar o dataset
        df = pd.read_csv(dataset_path, low_memory=False)
        print(f"Dataset carregado com sucesso: {df.shape[0]} linhas, {df.shape[1]} colunas")
        
        # Verificar distribuição da variável alvo
        print("\nDistribuição da variável alvo:")
        target_dist = df[TARGET].value_counts(normalize=True) * 100
        print(target_dist)
        
        # Features selecionadas (conforme identificado anteriormente)
        SELECTED_FEATURES = ['k18_somente', 'k25_mamadeira', 'b05a_idade_em_meses']
        
        print("\nAnálise das features selecionadas:")
        for feature in SELECTED_FEATURES:
            print(f"\nFeature: {feature}")
            print(f"Tipo: {df[feature].dtype}")
            print(f"Valores únicos: {df[feature].nunique()}")
            if df[feature].dtype == 'object':
                print(f"Exemplos de valores: {df[feature].unique()[:5]}")
            else:
                print(f"Min: {df[feature].min()}, Max: {df[feature].max()}")
        
        # Separar features e target
        X = df[SELECTED_FEATURES]
        y = df[TARGET]
        
        # Tratar valores faltantes
        print("\nTratando valores faltantes...")
        X = handle_missing_values(X)
        
        # Pré-processar features específicas
        print("\nPré-processando features...")
        X = preprocess_features(X)
        
        # Codificar variáveis categóricas
        print("\nCodificando variáveis categóricas...")
        X_encoded, label_encoders = encode_categorical_columns(X)
        
        # Mostrar a codificação para k25_mamadeira
        if 'k25_mamadeira' in label_encoders:
            print("\nCodificação para k25_mamadeira:")
            for i, categoria in enumerate(label_encoders['k25_mamadeira'].classes_):
                print(f"  {categoria} -> {i}")
        
        # Dividir em treino e teste (70/30) - mantendo estratificação
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y, test_size=0.3, random_state=42, stratify=y
        )
        print(f"\nDivisão dos dados:")
        print(f"  Treino: {X_train.shape[0]} amostras")
        print(f"  Teste: {X_test.shape[0]} amostras")
        
        # Primeira abordagem: Gradient Boosting básico otimizado para AUC
        print("\n1. Treinando Gradient Boosting básico otimizado para AUC...")
        
        # Configurar modelo inicial
        model = GradientBoostingClassifier(
            n_estimators=300,
            learning_rate=0.03,
            max_depth=4,
            min_samples_split=5,
            min_samples_leaf=5,
            subsample=0.8,
            random_state=42
        )
        
        # Treinar modelo inicial
        model.fit(X_train, y_train)
        
        # Avaliar no conjunto de teste
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]  # Prob. da segunda classe (index 1)
        
        # Calcular métricas ajustadas para pos_label=2
        accuracy = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred_proba)
        f1 = f1_score(y_test, y_pred, pos_label=2)
        
        print("\nMétricas do Gradient Boosting inicial:")
        print(f"  Acurácia: {accuracy:.4f}")
        print(f"  AUC: {auc:.4f}")
        print(f"  F1-Score: {f1:.4f}")
        
        # Plotar curva ROC
        print("\nCurva ROC do modelo inicial:")
        plot_roc_curve(y_test, y_pred_proba, "ROC Curve - Gradient Boosting Inicial", "roc_curve_inicial.png")
        
        # Segunda abordagem: Grid Search para encontrar os melhores parâmetros
        print("\n2. Realizando Grid Search para otimizar AUC...")
        
        # Definir grade de parâmetros para busca - versão simplificada para economizar tempo
        param_grid = {
            'n_estimators': [200, 300],
            'max_depth': [3, 4, 5],
            'min_samples_split': [5, 7],
            'subsample': [0.8, 0.9],
            'learning_rate': [0.01, 0.03, 0.05]
        }
        
        # Configurar cross-validation estratificada
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
        # Configurar Grid Search otimizando para AUC
        grid_search = GridSearchCV(
            estimator=GradientBoostingClassifier(random_state=42),
            param_grid=param_grid,
            scoring='roc_auc',
            cv=cv,
            verbose=1,
            n_jobs=-1
        )
        
        # Executar Grid Search
        grid_search.fit(X_train, y_train)
        
        # Obter melhores parâmetros
        best_params = grid_search.best_params_
        print(f"\nMelhores parâmetros: {best_params}")
        
        # Treinar modelo otimizado com os melhores parâmetros
        print("\n3. Treinando modelo Gradient Boosting com parâmetros otimizados...")
        optimized_model = GradientBoostingClassifier(
            **best_params,
            random_state=42
        )
        optimized_model.fit(X_train, y_train)
        
        # Avaliar no conjunto de teste
        y_pred_opt = optimized_model.predict(X_test)
        y_pred_proba_opt = optimized_model.predict_proba(X_test)[:, 1]
        
        # Calcular métricas ajustadas para pos_label=2
        accuracy_opt = accuracy_score(y_test, y_pred_opt)
        auc_opt = roc_auc_score(y_test, y_pred_proba_opt)
        f1_opt = f1_score(y_test, y_pred_opt, pos_label=2)
        
        print("\nMétricas do Gradient Boosting otimizado:")
        print(f"  Acurácia: {accuracy_opt:.4f}")
        print(f"  AUC: {auc_opt:.4f}")
        print(f"  F1-Score: {f1_opt:.4f}")
        
        # Plotar curva ROC para o modelo otimizado
        print("\nCurva ROC do modelo otimizado:")
        plot_roc_curve(y_test, y_pred_proba_opt, "ROC Curve - Gradient Boosting Otimizado", "roc_curve_otimizado.png")
        
        # Terceira abordagem: Calibração de probabilidades para melhorar AUC
        print("\n4. Aplicando calibração de probabilidades para melhorar AUC...")
        calibrated_model = CalibratedClassifierCV(
            optimized_model, 
            method='isotonic',  # 'isotonic' geralmente é bom para AUC
            cv=5
        )
        calibrated_model.fit(X_train, y_train)
        
        # Avaliar o modelo calibrado
        y_pred_calib = calibrated_model.predict(X_test)
        y_pred_proba_calib = calibrated_model.predict_proba(X_test)[:, 1]
        
        # Calcular métricas ajustadas para pos_label=2
        accuracy_calib = accuracy_score(y_test, y_pred_calib)
        auc_calib = roc_auc_score(y_test, y_pred_proba_calib)
        f1_calib = f1_score(y_test, y_pred_calib, pos_label=2)
        
        print("\nMétricas do Gradient Boosting calibrado:")
        print(f"  Acurácia: {accuracy_calib:.4f}")
        print(f"  AUC: {auc_calib:.4f}")
        print(f"  F1-Score: {f1_calib:.4f}")
        
        # Plotar curva ROC para o modelo calibrado
        print("\nCurva ROC do modelo calibrado:")
        plot_roc_curve(y_test, y_pred_proba_calib, "ROC Curve - Gradient Boosting Calibrado", "roc_curve_calibrado.png")
        
        # Quarta abordagem: Implementar modelo híbrido - Regra + Modelo
        print("\n5. Implementando abordagem híbrida (Regra + Gradient Boosting)...")
        
        # Função para predição híbrida com conhecimento do domínio
        def hybrid_predict(X, model):
            """
            Implementa abordagem híbrida que combina conhecimento do domínio com modelo ML:
            1. Se ainda_amamentando = 1 (k18_somente = 88) → classificar como positivo (2)
            2. Para outros casos, usar o modelo de ML
            """
            predictions = []
            probabilities = []
            
            for i, row in X.iterrows():
                # Se ainda está amamentando exclusivamente (k18_somente = 88)
                if 'ainda_amamentando' in row and row['ainda_amamentando'] == 1:
                    predictions.append(2)  # Classe positiva (está em aleitamento exclusivo)
                    probabilities.append(1.0)  # Probabilidade máxima
                else:
                    # Usar o modelo para os outros casos
                    idx = X.index.get_loc(i)
                    proba = model.predict_proba(X.iloc[[idx]])[0, 1]
                    pred = 2 if proba >= 0.5 else 1  # Ajustar para 1 e 2 em vez de 0 e 1
                    predictions.append(pred)
                    probabilities.append(proba)
            
            return np.array(predictions), np.array(probabilities)
        
        # Aplicar abordagem híbrida com o modelo calibrado
        y_pred_hybrid, y_pred_proba_hybrid = hybrid_predict(X_test, calibrated_model)
        
        # Calcular métricas da abordagem híbrida
        accuracy_hybrid = accuracy_score(y_test, y_pred_hybrid)
        
        # Verificar se há várias classes nas probabilidades
        if len(np.unique(y_pred_proba_hybrid)) > 1:
            auc_hybrid = roc_auc_score(y_test, y_pred_proba_hybrid)
            # Plotar curva ROC para o modelo híbrido
            plot_roc_curve(y_test, y_pred_proba_hybrid, "ROC Curve - Modelo Híbrido", "roc_curve_hibrido.png")
        else:
            auc_hybrid = np.nan
            print("Aviso: Não foi possível calcular AUC para o modelo híbrido pois todas as probabilidades são iguais.")
        
        f1_hybrid = f1_score(y_test, y_pred_hybrid, pos_label=2)
        
        print("\nMétricas da abordagem híbrida (Regra + Gradient Boosting):")
        print(f"  Acurácia: {accuracy_hybrid:.4f}")
        if not np.isnan(auc_hybrid):
            print(f"  AUC: {auc_hybrid:.4f}")
        else:
            print("  AUC: Não disponível (probabilidades constantes)")
        print(f"  F1-Score: {f1_hybrid:.4f}")
        
        # Comparar todos os modelos
        results = pd.DataFrame({
            'Modelo': ['Gradient Boosting Inicial', 'Gradient Boosting Otimizado', 
                      'Gradient Boosting Calibrado', 'Híbrido (Regra + GB)'],
            'Acurácia': [accuracy, accuracy_opt, accuracy_calib, accuracy_hybrid],
            'AUC': [auc, auc_opt, auc_calib, auc_hybrid],
            'F1-Score': [f1, f1_opt, f1_calib, f1_hybrid]
        })
        
        print("\nComparação final de todos os modelos:")
        print(results)
        
        # Plotar importância das features, incluindo a feature derivada
        plt.figure(figsize=(10, 6))
        feature_importance = optimized_model.feature_importances_
        feature_names = X_encoded.columns
        sorted_idx = np.argsort(feature_importance)
        plt.barh(np.array(feature_names)[sorted_idx], feature_importance[sorted_idx])
        plt.xlabel('Importância da Feature (Ganho)')
        plt.title('Importância das Features no Gradient Boosting')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'feature_importance.png'))
        plt.close()
        
        # Plotar comparação dos modelos
        plt.figure(figsize=(12, 6))
        results_plot = results.melt('Modelo', var_name='Métrica', value_name='Valor')
        sns.barplot(x='Modelo', y='Valor', hue='Métrica', data=results_plot)
        plt.title('Comparação de Métricas entre Modelos')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'comparacao_modelos.png'))
        plt.close()
        
        # Salvar o melhor modelo (geralmente o híbrido ou o calibrado)
        if not np.isnan(auc_hybrid) and auc_hybrid > auc_calib:
            print("\nO modelo híbrido apresentou o melhor desempenho!")
            # Salvar o modelo calibrado e a função híbrida
            model_path = os.path.join(output_dir, 'modelo_calibrado.pkl')
            joblib.dump(calibrated_model, model_path)
            print(f"Modelo calibrado salvo em: {model_path}")
            print("Para usar o modelo híbrido, é necessário aplicar a função hybrid_predict com este modelo calibrado.")
        else:
            print("\nO modelo calibrado apresentou o melhor desempenho!")
            best_model = calibrated_model
            model_path = os.path.join(output_dir, 'modelo_gradient_boosting_otimizado.pkl')
            joblib.dump(best_model, model_path)
            print(f"Melhor modelo salvo em: {model_path}")
        
        # Salvar os resultados comparativos
        results.to_csv(os.path.join(output_dir, 'resultados_comparativos_final.csv'), index=False)
        
        # Análise adicional para artigo: Criar uma tabela de contingência para k18_somente vs aleitamento_materno_exclusivo
        print("\nAnálise da relação entre k18_somente e aleitamento_materno_exclusivo:")
        
        # Criar categoria para k18_somente
        df['categoria_k18'] = pd.cut(
            df['k18_somente'], 
            bins=[-1, 0, 4, 6, 87, 88],  # Categorias: 0, 1-4, 5-6, 7-87, 88
            labels=['0', '1-4 meses', '5-6 meses', '7+ meses', 'Ainda amamentando']
        )
        
        # Tabela de contingência
        contingency = pd.crosstab(
            df['categoria_k18'], 
            df[TARGET], 
            normalize='index'
        ) * 100  # Converter para percentagem
        
        print("\nPorcentagem de aleitamento exclusivo por categoria de k18_somente:")
        print(contingency)
        
        # Visualizar a tabela de contingência
        plt.figure(figsize=(10, 6))
        contingency.plot(kind='bar', stacked=True)
        plt.title('Aleitamento Materno Exclusivo por Categoria de k18_somente')
        plt.xlabel('Duração do Aleitamento Exclusivo')
        plt.ylabel('Percentagem (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'contingencia_k18_aleitamento.png'))
        plt.close()
        
        # Análise adicional para a relação k25_mamadeira vs aleitamento_materno_exclusivo
        print("\nAnálise da relação entre k25_mamadeira e aleitamento_materno_exclusivo:")
        mamadeira_contingency = pd.crosstab(
            df['k25_mamadeira'], 
            df[TARGET], 
            normalize='index'
        ) * 100  # Converter para percentagem
        
        print("\nPorcentagem de aleitamento exclusivo por categoria de k25_mamadeira:")
        print(mamadeira_contingency)
        
        # Visualizar a tabela de contingência para k25_mamadeira
        plt.figure(figsize=(10, 6))
        mamadeira_contingency.plot(kind='bar', stacked=True)
        plt.title('Aleitamento Materno Exclusivo por Uso de Mamadeira')
        plt.xlabel('Uso de Mamadeira')
        plt.ylabel('Percentagem (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'contingencia_mamadeira_aleitamento.png'))
        plt.close()
        
        return {
            'initial_model': model,
            'optimized_model': optimized_model,
            'calibrated_model': calibrated_model,
            'results': results,
            'contingency_k18': contingency,
            'contingency_mamadeira': mamadeira_contingency
        }
        
    except Exception as e:
        print(f"ERRO ao processar dados: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()