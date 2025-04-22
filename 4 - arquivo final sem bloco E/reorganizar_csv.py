import csv

# Nomes dos arquivos
arquivo_entrada = 'criancas_menores_6_meses_classificadas_sem_bloco_e.csv'
arquivo_saida = 'criancas_menores_6_meses_reorganizado.csv'

try:
    # Lê o CSV de entrada
    with open(arquivo_entrada, 'r', encoding='utf-8') as arquivo_entrada_csv:
        leitor = csv.reader(arquivo_entrada_csv)
        
        # Lê o cabeçalho
        cabecalho = next(leitor)
        
        # Encontra o índice da coluna 'aleitamento_materno_exclusivo'
        try:
            indice_aleitamento = cabecalho.index('aleitamento_materno_exclusivo')
        except ValueError:
            print("Erro: A coluna 'aleitamento_materno_exclusivo' não foi encontrada no arquivo.")
            exit(1)
        
        # Reorganiza o cabeçalho (move 'aleitamento_materno_exclusivo' para o início)
        novo_cabecalho = [cabecalho[indice_aleitamento]] + [col for i, col in enumerate(cabecalho) if i != indice_aleitamento]
        
        # Prepara para escrever no arquivo de saída
        with open(arquivo_saida, 'w', newline='', encoding='utf-8') as arquivo_saida_csv:
            escritor = csv.writer(arquivo_saida_csv)
            
            # Escreve o novo cabeçalho
            escritor.writerow(novo_cabecalho)
            
            # Processa cada linha e reorganiza os dados
            for linha in leitor:
                # Reorganiza a linha (move o valor de 'aleitamento_materno_exclusivo' para o início)
                nova_linha = [linha[indice_aleitamento]] + [val for i, val in enumerate(linha) if i != indice_aleitamento]
                escritor.writerow(nova_linha)
    
    print(f"Arquivo reorganizado criado com sucesso: {arquivo_saida}")
    print(f"A coluna 'aleitamento_materno_exclusivo' agora está na primeira posição (coluna A).")
    
except Exception as e:
    print(f"Erro ao processar o arquivo: {e}") 