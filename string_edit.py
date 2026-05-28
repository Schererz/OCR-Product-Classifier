import re

padrao = r"([a-zA-Zá-úÁ-Ú\s]+?)\s+(\d+[\.,]\d{2})"

string = ("Arroz 20.00 feijao 45.00 macarrao 10.00")

matches = re.findall(padrao, string)
print(matches)

dicionario_produtos = {nome.strip().lower(): preco for nome, preco in matches}

for i, (produto, preco) in enumerate(dicionario_produtos.items(), start=1):
    # Padroniza o preço para usar vírgula na exibição
    preco_br = preco.replace('.', ',')
    print(f"{i}- {produto}, R$ {preco_br}")

'''lista = {}
def add_item(obj):
    id = max(lista.keys() or [0]) + 1
    lista[id] = obj
    lista[preco] = obj

prod = input("Digite o nome do produto: ")
add_item(prod)

print(lista)

choice = int(input("Selecione o ID do produto: "))

if choice in lista:
    print(f"Produto selecionado: {lista[choice]}")
else:    
    print("ID inválido.")

preco = float(input("Digite o preço do produto: "))

lista[preco] = obj

print(f"O preço do produto '{lista[choice]}' é: R${preco:.2f}")'''
