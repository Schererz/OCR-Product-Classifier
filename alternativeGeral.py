import pytesseract
from PIL import Image
import re

# ── OCR ──────────────────────────────────────────────────────────────────────
class OCRProcessor:
    def __init__(self, tesseract_cmd):
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def process_image(self, image_path):
        texto = pytesseract.image_to_string(Image.open(image_path), lang='por')
        return texto


# ── Limpeza do texto extraído ─────────────────────────────────────────────────
class editorTexto:
    def limpar_lista_compras(texto):
        linhas_limpas = []
        linhas = texto.strip().split("\n")

        # Palavras que indicam título/rodapé da lista — ignorar essas linhas inteiras
        TITULOS = ["LISTA DE COMPRAS", "DIA A DIA", "MERCADO"]

        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue

            linha_upper = linha.upper()

            # Ignora linhas de título/rodapé
            if any(titulo in linha_upper for titulo in TITULOS):
                continue

            # Remove caracteres que o OCR coloca no início da linha:
            # checkboxes (□ ☐ ■ • ▪), traços, pipes, números isolados (ex: "1 ", "2.")
            linha_limpa = re.sub(r'^[\u25A0\u25A1\u2610\u2611\u2612\u2022\u25AA\|\-\s\d\.]+', '', linha)

            # Remove pontuação e espaços sobrando no final
            linha_limpa = re.sub(r'[\.\-\s]+$', '', linha_limpa)

            linha_limpa = linha_limpa.strip().upper()

            # Descarta linhas que ficaram vazias ou muito curtas após a limpeza
            if len(linha_limpa) < 2:
                continue

            linhas_limpas.append(f"[ ] {linha_limpa}")

        return linhas_limpas


# ── Organização da lista ──────────────────────────────────────────────────────
class organizar_lista:
    def __init__(self):
        self.items = {}

    def popular_lista(self, lista_items_limpos):
        for j, item in enumerate(lista_items_limpos, start=1):
            self.items[j] = {
                "nome": item,
                "tipo": "Não classificado",
                "preco": 0.0,
                "validade": "N/A"
            }
        return self.items


# ── Produto ───────────────────────────────────────────────────────────────────
class Produto:
    def __init__(self, nome, tipo, preco):
        self.nome = nome.strip("[ ]").strip()
        self.tipo = tipo
        self.preco = preco
        self.validade = "N/A"

    def aplicar_classificacao(self, objeto_lista, chave_produto, tipo, preco, validade="N/A"):
        """Salva os dados no dicionário da lista sem usar input()."""
        objeto_lista.items[chave_produto]["tipo"] = tipo
        objeto_lista.items[chave_produto]["preco"] = float(preco)
        objeto_lista.items[chave_produto]["validade"] = validade
