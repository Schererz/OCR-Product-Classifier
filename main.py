from cod_geral import *

# (Configuração do OCR mantida igual ao seu original...)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\pedro\AppData\Local\Programs\Tesseract-OCR\tesseract.exe" # path do executável do tesseract
ocr_processor = OCRProcessor(pytesseract.pytesseract.tesseract_cmd)
texto_extraido = ocr_processor.process_image('image.png') #nome do arquivo da imagem

items_limpos = GerenciadorTexto.limpar_lista_compras(texto_extraido) 

minha_lista = ListaCompras()
minha_lista.popular_lista(items_limpos)

while True:
    minha_lista.exibir_lista()
    try:
        choice = int(input("\nEscolha o número do produto para editar (0 para sair): "))
        if choice == 0:
            break
        minha_lista.editar_produto(choice)
    except ValueError:
        print("Digite um número válido!")
