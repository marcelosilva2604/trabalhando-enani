import re

# Abre o arquivo
with open('features_enani.txt', 'r') as f:
    content = f.read()

# Encontra todas as variáveis
pattern = r'Variável: ([a-zA-Z0-9_]+)'
variables = re.findall(pattern, content)

# Conta variáveis por prefixo de letra
prefixes = {}
for var in variables:
    prefix = var.split('_')[0][0]  # Pega a primeira letra do nome da variável
    if prefix in prefixes:
        prefixes[prefix] += 1
    else:
        prefixes[prefix] = 1

# Imprime o resultado
print('Número de variáveis por letra inicial:')
for prefix in sorted(prefixes.keys()):
    print(f'  {prefix}: {prefixes[prefix]}')

print(f'\nTotal: {len(variables)} variáveis') 