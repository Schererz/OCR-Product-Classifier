import pytesseract
from PIL import Image
import re

class OCRProcessor: # processa a imagem e extrai o texto usando TESSERACT
    def __init__(self, tesseract_cmd):
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def process_image(self, image_path):
        print("Processando imagem...")
        texto = pytesseract.image_to_string(Image.open(image_path), lang='por')
        print("Imagem processada!")
        return texto


class ValidadorEntrada: # classe para validar as entradas do usuário
    def opcao(pedido, opcoes):
        opcoes_upper = [str(opc).upper() for opc in opcoes]
        while True:
            resposta = input(pedido).strip().upper()
            if resposta in opcoes_upper:
                return resposta
            print(f" Opção inválida! Escolha entre: {' ou '.join(opcoes)}")
    
    def numero(pedido):
        while True:
            try:
                return float(input(pedido).replace(",", "."))
            except ValueError:
                print("Entrada inválida! Digite um número válido.")


class GerenciadorTexto: # classe para organizar o texto extraído da imagem
    def limpar_lista_compras(texto):
        linhas_limpas = []
        linhas = texto.strip().split("\n")
        for linha in linhas:
            linha = linha.strip()
            if not linha or any(t in linha for t in ["LISTA DE COMPRAS", "DIA A DIA", "MERCADO"]):
                continue 
            
            linha_limpa = re.sub(r'^[A-Za-z0-9\|\s\-\d\/ ]+?\s+(?=[A-ZÂÃÉÍÓÚ])', '', linha)
            linha_limpa = re.sub(r'[\.\-\s]+$', '', linha_limpa).upper()
            linhas_limpas.append(linha_limpa)
        return linhas_limpas

class Produto:
    def __init__(self, nome):
        self.nome = nome
        self.preco = 0.0
        self.tipo = "Não classificado"

    def classificar(self):
        """Método que será sobrescrito nas subclasses (Polimorfismo)"""
        self.preco = ValidadorEntrada.numero(f"Digite o preço de '{self.nome}': R$ ")

    def obter_detalhes(self):
        return f"Tipo: {self.tipo} | Preço: R$ {self.preco:.2f}"


class ProdutoComida(Produto): # HERANÇA: herda de Produto
    def __init__(self, nome):
        super().__init__(nome)
        self.tipo = "Comida"
        self.validade = "N/A"

    def classificar(self):
        super().classificar() # pega o preço da classe mãe
        opc = ValidadorEntrada.opcao("Perecível? (S/N): ", ["S", "N"])
        if opc == "S":
            self.tipo = "Comida Perecível"
            self.validade = input("Digite a validade (dd/mm/aaaa): ")
        else:
            self.tipo = "Comida Não Perecível"

    def obter_detalhes(self):
        detalhes = super().get_detalhes() if hasattr(super(), 'get_detalhes') else f"Tipo: {self.tipo} | Preço: R$ {self.preco:.2f}"
        return f"{detalhes} | Validade: {self.validade}"


class ProdutoBebida(Produto):
    def __init__(self, nome):
        super().__init__(nome)
        self.tipo = "Bebida"
        self.temperatura = "N/A"

    def classificar(self):
        super().classificar()
        temp = ValidadorEntrada.opcao("Gelada ou Quente? (G/Q): ", ["G", "Q"])
        self.temperatura = "Gelada" if temp == "G" else "Quente"
        self.tipo = f"Bebida {self.temperatura}"


class ProdutoGeral(Produto): # higiene, limpeza, outros
    def __init__(self, nome, categoria):
        super().__init__(nome)
        self.tipo = categoria.capitalize()

class ListaCompras:        
    def __init__(self):
        self.items = {} # ASSOCIAÇÃO: Guarda instâncias de objetos do tipo Produto

    def popular_lista(self, lista_nomes):
        for i, nome in enumerate(lista_nomes, start=1):
            # produto base
            self.items[i] = Produto(nome)
        
    def exibir_lista(self):
        print("\n--- LISTA DE COMPRAS ---")
        if not self.items:
            print("A lista está vazia.")
            return
        for chave, prod in self.items.items():
            print(f"{chave} - [ ] {prod.nome}")
            if prod.tipo != "Não classificado":
                print(f"    └─ {prod.obter_detalhes()}")

    def editar_produto(self, chave):
        if chave not in self.items:
            print("Produto não encontrado!")
            return

        print(f"\nEditando: {self.items[chave].nome}")
        print("1 - Classificar | 2 - Excluir | 0 - Voltar")
        opcao = ValidadorEntrada.opcao("Escolha: ", ["1", "2", "0"])

        if opcao == "1": # POLIMORFISMO: troca a classificação genérica por uma específica
            print("Categorias: comida | bebida | limpeza | higiene | outros")
            cat = input("Digite a categoria: ").strip().lower()
            
            nome_atual = self.items[chave].nome
            if cat == "comida":
                novo_prod = ProdutoComida(nome_atual)
            elif cat == "bebida":
                novo_prod = ProdutoBebida(nome_atual)
            else:
                novo_prod = ProdutoGeral(nome_atual, cat)
            
            novo_prod.classificar()
            self.items[chave] = novo_prod # atualiza a associação

        elif opcao == "2":
            self.items.pop(chave)
            print("Produto excluído!")
