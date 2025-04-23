import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Configurar estilo de visualização
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("talk")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.family'] = 'sans-serif'

# Criar pasta para salvar gráficos
os.makedirs('./7/graficos', exist_ok=True)

# Carregar os resultados da análise
resultados = pd.read_csv('./7/analise_associacoes.csv')

# Filtrar apenas resultados significativos
resultados_significativos = resultados[resultados['significancia'] == 'Significativa']

# Top variáveis com maior força de associação
top_n = 20
top_variaveis = resultados_significativos.sort_values(by='forca_associacao', ascending=False).head(top_n)

# Gráfico 1: Top 20 variáveis com maior força de associação
plt.figure(figsize=(14, 10))
colors = sns.color_palette('viridis', len(top_variaveis))

# Mapear classificação para cores
classificacao_cores = {
    'Forte': '#1a9641',
    'Relativamente forte': '#a6d96a', 
    'Moderada': '#ffffbf',
    'Fraca': '#fdae61',
    'Negligenciável': '#d7191c'
}

# Criar barras com cores baseadas na classificação
bars = plt.barh(
    top_variaveis['feature'], 
    top_variaveis['forca_associacao'],
    color=[classificacao_cores[c] for c in top_variaveis['classificacao_forca']]
)

# Adicionar valores nas barras
for i, bar in enumerate(bars):
    plt.text(
        bar.get_width() + 0.01, 
        bar.get_y() + bar.get_height()/2, 
        f"{top_variaveis['forca_associacao'].iloc[i]:.3f}", 
        va='center'
    )

plt.xlabel('Força de Associação')
plt.title('Top 20 Variáveis com Maior Força de Associação com Aleitamento Materno Exclusivo')

# Adicionar legenda para classificação
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color=classificacao_cores['Forte'], lw=4, label='Forte'),
    Line2D([0], [0], color=classificacao_cores['Relativamente forte'], lw=4, label='Relativamente forte'),
    Line2D([0], [0], color=classificacao_cores['Moderada'], lw=4, label='Moderada'),
    Line2D([0], [0], color=classificacao_cores['Fraca'], lw=4, label='Fraca'),
    Line2D([0], [0], color=classificacao_cores['Negligenciável'], lw=4, label='Negligenciável')
]
plt.legend(handles=legend_elements, title='Classificação', loc='lower right')

plt.tight_layout()
plt.savefig('./7/graficos/top_variaveis_forca.png', dpi=300, bbox_inches='tight')
plt.close()

# Gráfico 2: Distribuição por tipo de variável
contagem_tipos = resultados['tipo_variavel'].value_counts()
plt.figure(figsize=(12, 6))
ax = sns.barplot(x=contagem_tipos.index, y=contagem_tipos.values, palette='viridis')

# Adicionar rótulos de contagem
for i, v in enumerate(contagem_tipos.values):
    ax.text(i, v + 0.5, str(v), ha='center')

plt.title('Distribuição por Tipo de Variável')
plt.ylabel('Contagem')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('./7/graficos/distribuicao_tipos_variavel.png', dpi=300, bbox_inches='tight')
plt.close()

# Gráfico 3: Distribuição por classificação de força
contagem_classificacao = resultados_significativos['classificacao_forca'].value_counts()
plt.figure(figsize=(12, 6))

# Ordenar as classificações de força por intensidade
ordem_classificacao = ['Negligenciável', 'Fraca', 'Moderada', 'Relativamente forte', 'Forte']
contagem_classificacao = contagem_classificacao.reindex(ordem_classificacao)

# Cores específicas para cada classificação
cores_classificacao = [classificacao_cores[c] for c in contagem_classificacao.index]

ax = sns.barplot(x=contagem_classificacao.index, y=contagem_classificacao.values, palette=cores_classificacao)

# Adicionar rótulos de contagem
for i, v in enumerate(contagem_classificacao.values):
    ax.text(i, v + 0.5, str(v), ha='center')

plt.title('Distribuição por Classificação de Força (Apenas Variáveis Significativas)')
plt.ylabel('Contagem')
plt.tight_layout()
plt.savefig('./7/graficos/distribuicao_classificacao.png', dpi=300, bbox_inches='tight')
plt.close()

# Gráfico 4: Distribuição de p-valores (em escala log)
plt.figure(figsize=(12, 6))
plt.hist(resultados_significativos['valor_p'].dropna(), bins=30, alpha=0.7, log=True)
plt.axvline(0.05, color='red', linestyle='dashed', linewidth=1)
plt.text(0.06, plt.ylim()[1]*0.9, 'p = 0.05', color='red')
plt.xlabel('Valor p')
plt.ylabel('Contagem (escala log)')
plt.title('Distribuição de p-valores para Variáveis Significativas')
plt.tight_layout()
plt.savefig('./7/graficos/distribuicao_p_valores.png', dpi=300, bbox_inches='tight')
plt.close()

# Gráfico 5: Relação entre força e p-valor (escala log)
plt.figure(figsize=(12, 8))
plt.scatter(
    resultados_significativos['valor_p'], 
    resultados_significativos['forca_associacao'],
    alpha=0.6,
    c=[classificacao_cores[c] for c in resultados_significativos['classificacao_forca']]
)

# Adicionar linhas de referência para classificação de força
plt.axhline(y=0.1, color='gray', linestyle='--', alpha=0.3)
plt.axhline(y=0.3, color='gray', linestyle='--', alpha=0.3)
plt.axhline(y=0.5, color='gray', linestyle='--', alpha=0.3)
plt.axhline(y=0.7, color='gray', linestyle='--', alpha=0.3)

# Textos para referência
plt.text(0.049, 0.05, 'Negligenciável', ha='right', va='center', color='gray')
plt.text(0.049, 0.2, 'Fraca', ha='right', va='center', color='gray')
plt.text(0.049, 0.4, 'Moderada', ha='right', va='center', color='gray')
plt.text(0.049, 0.6, 'Relativamente forte', ha='right', va='center', color='gray')
plt.text(0.049, 0.8, 'Forte', ha='right', va='center', color='gray')

# Adicionar nomes das variáveis principais
for i, row in top_variaveis.head(10).iterrows():
    plt.annotate(
        row['feature'], 
        (row['valor_p'], row['forca_associacao']),
        xytext=(5, 0), 
        textcoords='offset points', 
        fontsize=9
    )

plt.xscale('log')
plt.xlim(1e-200, 0.05)  # Limitar ao intervalo de significância
plt.xlabel('Valor p (escala log)')
plt.ylabel('Força de Associação')
plt.title('Relação entre Força de Associação e p-valor')

# Adicionar legenda para classificação
plt.legend(handles=legend_elements, title='Classificação', loc='upper left')

plt.tight_layout()
plt.savefig('./7/graficos/relacao_forca_p_valor.png', dpi=300, bbox_inches='tight')
plt.close()

# Gráfico 6: Força de associação por método utilizado
metodos = resultados_significativos['metodo_utilizado'].value_counts().head(5)
plt.figure(figsize=(12, 6))
ax = sns.barplot(x=metodos.index, y=metodos.values, palette='viridis')

# Adicionar rótulos de contagem
for i, v in enumerate(metodos.values):
    ax.text(i, v + 0.5, str(v), ha='center')

plt.title('Métodos Estatísticos Mais Utilizados')
plt.ylabel('Contagem')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('./7/graficos/metodos_estatisticos.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualizações geradas com sucesso. Os gráficos foram salvos na pasta '/7/graficos/'.") 