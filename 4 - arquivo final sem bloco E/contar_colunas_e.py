import csv
import re

# Função para verificar se uma coluna pertence ao bloco E
def eh_coluna_bloco_e(nome_coluna):
    return bool(re.match(r'^e\d+', nome_coluna))

# Abre o arquivo CSV
with open('criancas_menores_6_meses_classificadas_sem_bloco_e.csv', 'r', encoding='utf-8') as arquivo:
    # Lê a primeira linha para obter os nomes das colunas
    leitor = csv.reader(arquivo)
    cabecalho = next(leitor)
    
    # Conta quantas colunas começam com 'e' seguido de um número
    colunas_bloco_e = [col for col in cabecalho if eh_coluna_bloco_e(col)]
    
    # Imprime os resultados
    print(f"Total de colunas no arquivo: {len(cabecalho)}")
    print(f"Total de colunas do bloco E encontradas: {len(colunas_bloco_e)}")
    
    if colunas_bloco_e:
        print(f"Algumas colunas do bloco E ainda presentes: {colunas_bloco_e[:5]}...")
    else:
        print("Nenhuma coluna do bloco E encontrada no arquivo.")
        
    # Verificar se existe a coluna de aleitamento materno exclusivo
    if 'aleitamento_materno_exclusivo' in cabecalho:
        print("A coluna 'aleitamento_materno_exclusivo' está presente no arquivo.")
    else:
        print("A coluna 'aleitamento_materno_exclusivo' NÃO está presente no arquivo.") 