import csv
import re
import os

# Função para verificar se uma coluna pertence ao bloco E
def eh_coluna_bloco_e(nome_coluna):
    return bool(re.match(r'^e\d+', nome_coluna))

# Caminho para o arquivo original
arquivo_original = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                          '3 - definição desmame/criancas_menores_6_meses_classificadas.csv')

try:
    # Abre o arquivo CSV original
    with open(arquivo_original, 'r', encoding='utf-8') as arquivo:
        # Lê a primeira linha para obter os nomes das colunas
        leitor = csv.reader(arquivo)
        cabecalho_original = next(leitor)
        
        # Conta quantas colunas começam com 'e' seguido de um número
        colunas_bloco_e = [col for col in cabecalho_original if eh_coluna_bloco_e(col)]
        
        # Imprime os resultados
        print(f"Total de colunas no arquivo original: {len(cabecalho_original)}")
        print(f"Total de colunas do bloco E identificadas: {len(colunas_bloco_e)}")
        
        if colunas_bloco_e:
            print(f"Algumas colunas do bloco E: {colunas_bloco_e[:5]}...")
            
    # Comparação com o arquivo atual
    with open('criancas_menores_6_meses_classificadas_sem_bloco_e.csv', 'r', encoding='utf-8') as arquivo_atual:
        leitor_atual = csv.reader(arquivo_atual)
        cabecalho_atual = next(leitor_atual)
        
        print(f"\nTotal de colunas no arquivo atual: {len(cabecalho_atual)}")
        print(f"Diferença (colunas removidas): {len(cabecalho_original) - len(cabecalho_atual)}")
        
        # Verifica se todas as colunas do bloco E foram removidas
        if all(col not in cabecalho_atual for col in colunas_bloco_e):
            print("Todas as colunas do bloco E foram removidas com sucesso!")
        else:
            colunas_restantes = [col for col in colunas_bloco_e if col in cabecalho_atual]
            print(f"Ainda existem {len(colunas_restantes)} colunas do bloco E no arquivo atual.")
            
except FileNotFoundError:
    print(f"Arquivo original não encontrado: {arquivo_original}")
except Exception as e:
    print(f"Erro ao processar os arquivos: {e}") 