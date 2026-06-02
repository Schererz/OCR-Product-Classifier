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
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\pedro\AppData\Local\Programs\Tesseract-OCR\tesseract.exe" # tesseract
ocr_processor = OCRProcessor(pytesseract.pytesseract.tesseract_cmd)
texto = ocr_processor.process_image('image.png') #imagem

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
    
#lista formatada em forma de string
texto_limpo = editorTexto.limpar_lista_compras(texto) 
# print(texto_limpo)

# classes dos produtos -----------------------------------------------
class Produto():
    def __init__(self, nome, tipo, preco):
        self.nome = nome
        self.tipo = tipo
        self.preco = preco

class Comida(Produto):
    def __init__(self, nome, tipo, preco, tipoComida):
        super().__init__(nome, tipo, preco)
        self.tipoComida = tipoComida

class perecivel(Comida):
    def __init__(self, nome, tipo, preco, tipoComida, dataValidade):
        super().__init__(nome, tipo, preco, tipoComida)
        self.dataValidade = dataValidade

class Bebida(Produto):
    def __init__(self, nome, tipo, preco, tipoBebida):
        super().__init__(nome, tipo, preco)
        self.tipoBebida = tipoBebida

class Limpeza(Produto):
    def __init__(self, nome, tipo, preco, tipoLimpeza):
        super().__init__(nome, tipo, preco)
        self.tipoLimpeza = tipoLimpeza

class Higiene(Produto):
    def __init__(self, nome, tipo, preco, tipoHigiene):
        super().__init__(nome, tipo, preco)
        self.tipoHigiene = tipoHigiene

class Outros(Produto):
    def __init__(self, nome, tipo, preco, tipoOutros):
        super().__init__(nome, tipo, preco)
        self.tipoOutros = tipoOutros

# organizar com numeração e dicionário
j = 1
lista = {}
for item in texto_limpo:
    lista[j] = item
    j += 1
print("\nLista de compras:")
for item in lista:
    print (f"{item} - {lista[item]}")

# classe para editar os produtos da lista
def editar_produto(choice):
    while True:
        if choice in lista:
            print(f"Produto escolhido: {lista[choice]}")
            while True:
                print("Você deseja:    Classificar (1)    Excluir (2)   Sair (0)")
                option = int(input("Escolha uma opção: "))
                if option == 1:
                    tipo = input("Digite o tipo do produto (Comida, Bebida, Limpeza, Higiene, Outros): ")
                    # Lógica para classificar o produto de acordo com o tipo escolhido
                    pass
                elif option == 2:
                    lista.pop(choice)
                    print("Produto excluído!")
                    pass
                elif option == 0:
                    break
                else:
                    print("Opção inválida!")
        else:
            print("Produto não encontrado na lista!")

choice = int(input("\nEscolha o produto que deseja editar: "))
editar_produto(choice)



