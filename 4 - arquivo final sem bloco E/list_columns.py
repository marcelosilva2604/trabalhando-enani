import csv

# Load the CSV file
filename = 'criancas_menores_6_meses_classificadas_sem_bloco_e.csv'
try:
    # Open the CSV file and read the header
    with open(filename, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        # Get the header (first row)
        header = next(csv_reader)
        
        # Print all columns
        print("All columns in the CSV file:")
        for i, col in enumerate(header, 1):
            print(f"{i}. {col}")
        
        # Check if there is any column related to exclusive breastfeeding
        breastfeeding_cols = [col for col in header if 'aleitamento' in col.lower() or 'amamenta' in col.lower() or 'leite materno' in col.lower()]
        
        if breastfeeding_cols:
            print("\nColumns potentially related to breastfeeding:")
            for i, col in enumerate(breastfeeding_cols, 1):
                print(f"{i}. {col}")
        else:
            print("\nNo columns explicitly mentioning 'aleitamento', 'amamenta', or 'leite materno' were found.")
            
except Exception as e:
    print(f"Error: {e}") 