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
texto = ocr_processor.process_image('image.png') #nome do arquivo da imagem

# classe para formatar texto da imagem
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
                continue 

            #limpeza nos itens da lista
            linha_limpa = re.sub(r'^[A-Za-z0-9\|\s\-\d\/ ]+?\s+(?=[A-ZÂÃÉÍÓÚ])', '', linha)
            #tira pontos e traços no final das palavras
            linha_limpa = re.sub(r'[\.\-\s]+$', '', linha_limpa)
            linha_limpa = linha_limpa.upper()
            
            # coloca checkbox nos itens
            linhas_limpas.append(f"[ ] {linha_limpa}")
            # saida exemplo [ ] Nome do produto
            
        return linhas_limpas

# organizar a lista e exibir na tela
class organizar_lista:        
    def __init__(self):
        self.items = {}

    # adicionar os itens no dicionário da lista
    def popular_lista(self, lista_items_limpos):
        j = 1
        for item in lista_items_limpos:
            self.items[j] = {
                "nome": item,
                "tipo": "Não classificado",
                "preco": 0.0,
                "validade": "N/A"
            }
            j += 1
        return self.items
        
    def exibir_lista(self):
        """Mostra a lista formatada na tela com seus detalhes."""
        print("\n--- LISTA DE COMPRAS ---")
        if not self.items:
            print("A lista está vazia.")
            return
                
        for chave in self.items:
            prod = self.items[chave]
            print(f"{chave} - {prod['nome']}")
            # exibe os subdados caso o produto já tenha sido classificado
            if prod['tipo'] != "Não classificado":
                print(f"    └─ Tipo: {prod['tipo']} | Preço: R$ {prod['preco']:.2f} | Validade: {prod['validade']}")


# validar as entradas do usuário sem precisar repetir código
class validador_entrada:
    def opcao(pedido, opcoes): # para opçao
        opcoes_upper = [str(opc).upper() for opc in opcoes]
        
        while True:
            resposta = input(pedido).strip().upper()
            if resposta in opcoes_upper:
                return resposta
            print(f" Opção inválida! Escolha entre: {'ou '.join(opcoes)}")
    
    def numero(pedido): # para o preco
        while True:
            try:
                valor = float(input(pedido).replace(",", "."))
                return valor
            except ValueError:
                print("Entrada inválida! Digite um número válido.")

# classe do produto e editar produto
class Produto():
    def __init__(self, nome, tipo, preco):
        self.nome = nome.strip("[ ]").strip()
        self.tipo = tipo
        self.preco = preco
        self.validade = "N/A" # padrão
    
    def classificar_produto(self, objeto_lista, chave_produto):
        # pergunta o preço de forma genérica para qualquer produto
        perg_preco = validador_entrada.numero(f"Digite o preço do produto {self.nome}: R$ ")
        self.preco = perg_preco

        tipo_input = input("Digite o tipo do produto (comida, bebida, limpeza, higiene, outros): ").strip().lower()
        
        # aqui começa os ifs pra classificação 
        if tipo_input == "comida":
            self.tipo = "Comida"
            perg_tipoComida = validador_entrada.opcao(
                "Perecível ou Não Perecível? ",
                opcoes=["Perecível", "perecivel", "Não Perecível", "nao perecivel"]
            )
            self.tipoComida = perg_tipoComida
            if self.tipoComida.lower() in ["perecível", "perecivel"]:
                self.tipo = "Comida Perecível"
                validade = input("Digite a validade do produto (dd/mm/aaaa): ")
                self.validade = validade
                print(f"\nProduto {self.nome} classificado como: {self.tipo} com validade {self.validade}")
            else: 
                self.tipo = "Comida Não Perecível"
                print(f"\nProduto {self.nome} classificado como: {self.tipo}")
            

        if tipo_input == "bebida":
            self.tipo = "Bebida"
            self.tipoBebida = input("Gelada ou quente? ").strip().lower()
            if self.tipoBebida == "gelada":
                self.tipo = "Bebida Gelada"
            elif self.tipoBebida == "quente":
                self.tipo = "Bebida Quente"
            print(f"\nProduto {self.nome} classificado como: {self.tipo}")
        else:
            # escolha limpeza, higiene ou outros
            self.tipo = tipo_input.capitalize()
            print(f"\nProduto {self.nome} classificado como: {self.tipo}")
        
        # adicionar ou atualiza os dados no dicionario da lista
        objeto_lista.items[chave_produto]["tipo"] = self.tipo
        objeto_lista.items[chave_produto]["preco"] = self.preco
        objeto_lista.items[chave_produto]["validade"] = self.validade


    def editar_produto(choice):

        if choice in minha_lista.items: # perguntas pra escolher e editar o produto escolhido
            print(f"Produto escolhido: {minha_lista.items[choice]['nome']}")
            while True:
                print("Você deseja:    Classificar (1)    Excluir (2)   Sair (0)")
                option = int(input("Escolha uma opção: "))
                if option == 1:
                    class_prod = Produto(minha_lista.items[choice]['nome'], "", 0)
                    class_prod.classificar_produto(minha_lista, choice) # chamar a função de classificação
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
        elif isinstance(choice, int) == False:
            print("Entrada inválida! Digite um número.")
            
    def escolher_produto():
        while True:
            try: # loop pra validar a escolha do produto a ser editado
                choice = int(input("\nEscolha o produto que deseja editar(0 para sair): "))
                return choice
            except ValueError:
                print("Entrada inválida! Digite um número.")



# EXECUÇÃO DO PROGRAMA 

# 1 passo - processar a imagem e extrair o texto
items_limpos = editorTexto.limpar_lista_compras(texto) 

# 2 passo - organizar a lista e exibir na tela
minha_lista = organizar_lista()
minha_lista.popular_lista(items_limpos)
'''
# 3 passo - escolher o produto e editar
choice = None
while choice != 0: #loop externo 
    minha_lista.exibir_lista()
    choice = Produto.escolher_produto()

# 4 passo - editar o produto escolhido (dentro do loop)
    Produto.editar_produto(choice)'''
