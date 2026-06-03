import pytesseract
from PIL import Image
import re

# classe pra tirar texto da imagem
class OCRProcessor:
    def __init__(self, tesseract_cmd):
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def process_image(self, image_path):
        print("Processando imagem...")
        texto = pytesseract.image_to_string(Image.open(image_path), lang='por')
        print("Imagem processada!")
        return texto

# configurar path de imagem e do tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\pedro\AppData\Local\Programs\Tesseract-OCR\tesseract.exe" # path do executável do tesseract
ocr_processor = OCRProcessor(pytesseract.pytesseract.tesseract_cmd)
texto = ocr_processor.process_image('image.png') #nome do arquivo da imagem (se estiver em pasta diferete, colocar path completo)

# classe formatar texto da imagem
class editorTexto:

    def limpar_lista_compras(texto):
        linhas_limpas = []
        linhas = texto.strip().split("\n")
        
        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue
                
            # filtra os titulos
            if "LISTA DE COMPRAS" in linha or "DIA A DIA" in linha or "MERCADO" in linha:
                linha = linha.strip()
                #limpeza dos titulos
                continue 

            #limpeza nos itens da lista
            linha_limpa = re.sub(r'^[A-Za-z0-9\|\s\-\d\/ ]+?\s+(?=[A-ZÂÃÉÍÓÚ])', '', linha)
            #tira pontos e traços no final das palavras
            linha_limpa = re.sub(r'[\.\-\s]+$', '', linha_limpa)
            linha_limpa = linha_limpa.upper()
            
            # coloca checkbox nos itens
            linhas_limpas.append(f"[ ] {linha_limpa}")
            
        return linhas_limpas
    
class organizar_lista:
        
    def __init__(self):
        self.items = {}


    def popular_lista(self, lista_items_limpos):
        j = 1
        lista = {}
        for item in lista_items_limpos:
            self.items[j] = item
            j += 1
        return self.items 
        
    def exibir_lista(self):
        """Mostra a lista formatada na tela."""
        print("\n--- LISTA DE COMPRAS ---")
        if not self.items:
            print("A lista está vazia.")
            return
                
        for chave in self.items:
            print(f"{chave} - {self.items[chave]}")


class Produto():
    def __init__(self, nome, tipo, preco):
        self.nome = nome
        self.tipo = tipo
        self.preco = preco
    



# classe para editar os produtos da lista
def editar_produto(choice):

    while True:

        if choice in minha_lista.items:
            print(f"Produto escolhido: {minha_lista.items[choice]}")
            while True:
                print("Você deseja:    Classificar (1)    Excluir (2)   Sair (0)")
                option = int(input("Escolha uma opção: "))
                if option == 1:
                    tipo = input("Digite o tipo do produto (Comida, Bebida, Limpeza, Higiene, Outros): ")
                    # Lógica para classificar o produto (a ser implementado)
                    print(f"Produto classificado como: {tipo}")
                    break
                elif option == 2:
                    minha_lista.items.pop(choice)
                    print("Produto excluído!")
                    break
                elif option == 0:
                    return False
                else:
                    print("Opção inválida!")
        elif choice == 0:
            return False
        elif choice not in minha_lista.items:
            print("Produto não encontrado na lista!")
            choice = int(input("Escolha outro produto: "))
        elif isinstance(choice, int) == False:
            print("Entrada inválida! Digite um número.")
            choice = int(input("Escolha outro produto: "))
        
def escolher_produto():
    while True:
        try:
            choice = int(input("\nEscolha o produto que deseja editar(0 para sair): "))
            return choice
        except ValueError:
            print("Entrada inválida! Digite um número.")




# execução do programa 


# 1 passo - processar a imagem e extrair o texto
items_limpos = editorTexto.limpar_lista_compras(texto) 

# 2 passo - organizar a lista e exibir na tela
minha_lista = organizar_lista()
minha_lista.popular_lista(items_limpos)

# 3 passo - escolher o produto e editar
minha_lista.exibir_lista()
choice = escolher_produto()

# 4 passo - editar o produto escolhido
editar_produto(choice)
