import PySimpleGUI as sg
from cod_geral import OCRProcessor, editorTexto, organizar_lista, Produto
import pytesseract

# ── Configurações visuais ─────────────────────────────────────────────────────
TESSERACT_PATH = r"C:\Users\pedro\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

sg.theme("DarkGrey13")
FONTE = ("Segoe UI", 11)
FONTE_TITULO = ("Segoe UI", 13, "bold")
VERDE = "#50D054"
VERMELHO = "#E43E32"
AZUL = "#3396E8"
AMARELO = "#FFC107"


# ── Helpers ───────────────────────────────────────────────────────────────────
def nome_limpo(item_dict):
    return item_dict["nome"].strip("[ ]").strip()


def linhas_tabela(lista_obj):
    """Converte o dicionário da lista para linhas exibíveis na tabela."""
    rows = []
    for chave, prod in lista_obj.items.items():
        preco_fmt = f"R$ {prod['preco']:.2f}" if prod['preco'] > 0 else "—"
        rows.append([
            chave,
            nome_limpo(prod),
            prod["tipo"],
            preco_fmt,
            prod["validade"]
        ])
    return rows


# ── Janela: selecionar imagem e processar OCR ─────────────────────────────────
def janela_carregar_imagem():
    layout = [
        [sg.Text("Lista de Compras — OCR", font=FONTE_TITULO, justification="center", expand_x=True)],
        [sg.HorizontalSeparator()],
        [sg.Text("Selecione a imagem da lista:", font=FONTE)],
        [sg.Input(key="-ARQUIVO-", font=FONTE, expand_x=True),
         sg.FileBrowse("Procurar", file_types=(("Imagens", "*.png *.jpg *.jpeg *.bmp *.tiff"),), font=FONTE)],
        [sg.VPush()],
        [sg.Button("Processar Imagem", button_color=(VERDE), font=FONTE, expand_x=True, size=(0, 2))],
        [sg.Button("Sair", button_color=(VERMELHO), font=FONTE, expand_x=True)],
    ]
    return sg.Window("Carregar Imagem", layout, size=(500, 220), finalize=True, font=FONTE)


# ── Janela: classificar produto ───────────────────────────────────────────────
def janela_classificar(nome_produto):
    tipos = ["Comida Perecível", "Comida Não Perecível", "Bebida Gelada",
             "Bebida Quente", "Limpeza", "Higiene", "Outros"]

    layout = [
        [sg.Text(f"Classificar: {nome_produto}", font=FONTE_TITULO)],
        [sg.HorizontalSeparator()],
        [sg.Text("Tipo:", font=FONTE),
         sg.Combo(tipos, key="-TIPO-", font=FONTE, readonly=True, expand_x=True)],
        [sg.Text("Preço (R$):", font=FONTE),
         sg.Input("0.00", key="-PRECO-", font=FONTE, size=(12, 1))],
        [sg.Text("Validade (dd/mm/aaaa):", font=FONTE),
         sg.Input("N/A", key="-VALIDADE-", font=FONTE, size=(14, 1))],
        [sg.VPush()],
        [sg.Button("Salvar", button_color=VERDE, font=FONTE, expand_x=True),
         sg.Button("Cancelar", button_color=VERMELHO, font=FONTE, expand_x=True)],
    ]
    return sg.Window("Classificar Produto", layout, size=(420, 240), modal=True, finalize=True)


# ── Janela: confirmar exclusão ────────────────────────────────────────────────
def confirmar_exclusao(nome_produto):
    return sg.popup_yes_no(
        f"Tem certeza que deseja excluir:\n\n  {nome_produto}?",
        title="Confirmar Exclusão",
        font=FONTE
    )


# ── Janela principal ──────────────────────────────────────────────────────────
def janela_principal(minha_lista):
    cabecalho = ["#", "Produto", "Tipo", "Preço", "Validade"]
    dados = linhas_tabela(minha_lista)

    layout = [
        [sg.Text("🛒  Lista de Compras", font=("Segoe UI", 15, "bold"))],
        [sg.HorizontalSeparator()],
        [sg.Table(
            values=dados,
            headings=cabecalho,
            key="-TABELA-",
            col_widths=[4, 28, 20, 10, 14],
            auto_size_columns=False,
            justification="left",
            font=FONTE,
            header_font=("Segoe UI", 11, "bold"),
            alternating_row_color="#2b2b2b",
            selected_row_colors=("white", AZUL),
            expand_x=True,
            expand_y=True,
            enable_click_events=True,
            num_rows=15,
        )],
        [sg.HorizontalSeparator()],
        [
            sg.Button("✏  Classificar", key="-CLASSIFICAR-", button_color=AZUL, font=FONTE, size=(18, 1)),
            sg.Button("🗑  Excluir", key="-EXCLUIR-", button_color=VERMELHO, font=FONTE, size=(18, 1)),
            sg.Push(),
            sg.Button("Carregar nova imagem", key="-NOVA-", font=FONTE, size=(20, 1)),
            sg.Button("Sair", button_color=VERMELHO, font=FONTE, size=(10, 1)),
        ],
        [sg.Text("Selecione um produto na tabela para editá-lo.", key="-STATUS-",
                 font=("Segoe UI", 10, "italic"), text_color="#aaaaaa")],
    ]

    return sg.Window(
        "Lista de Compras — Gerenciador",
        layout,
        size=(820, 520),
        resizable=True,
        finalize=True,
        font=FONTE,
    )


# ── Loop principal ────────────────────────────────────────────────────────────
def main():
    minha_lista = None
    linha_selecionada = None

    # ── Tela de carregamento da imagem ────────────────────────────────────────
    win_carga = janela_carregar_imagem()

    while True:
        evento, valores = win_carga.read()

        if evento in (sg.WIN_CLOSED, "Sair"):
            win_carga.close()
            return

        if evento == "Processar Imagem":
            caminho = valores["-ARQUIVO-"]
            if not caminho:
                sg.popup_error("Selecione uma imagem primeiro!", font=FONTE)
                continue

            win_carga.hide()
            sg.popup_quick_message("Processando imagem, aguarde...", background_color="#333", font=FONTE_TITULO)

            try:
                ocr = OCRProcessor(TESSERACT_PATH)
                texto = ocr.process_image(caminho)
                items_limpos = editorTexto.limpar_lista_compras(texto)

                if not items_limpos:
                    sg.popup_error("Nenhum item encontrado na imagem.\nVerifique se a imagem é legível.", font=FONTE)
                    win_carga.un_hide()
                    continue

                minha_lista = organizar_lista()
                minha_lista.popular_lista(items_limpos)
                win_carga.close()
                break

            except Exception as e:
                sg.popup_error(f"Erro ao processar imagem:\n{e}", font=FONTE)
                win_carga.un_hide()

    # ── Janela principal ──────────────────────────────────────────────────────
    while True:
        win_main = janela_principal(minha_lista)

        while True:
            evento, valores = win_main.read()

            if evento in (sg.WIN_CLOSED, "Sair"):
                win_main.close()
                return

            # Clique em linha da tabela
            if isinstance(evento, tuple) and evento[0] == "-TABELA-":
                sel = valores["-TABELA-"]
                if sel:
                    linha_selecionada = sel[0]  # índice 0-based na tabela
                    chave = list(minha_lista.items.keys())[linha_selecionada]
                    nome = nome_limpo(minha_lista.items[chave])
                    win_main["-STATUS-"].update(f"Selecionado: {nome}")

            # Botão classificar
            if evento == "-CLASSIFICAR-":
                sel = valores["-TABELA-"]
                if not sel:
                    sg.popup("Selecione um produto na tabela primeiro.", font=FONTE)
                    continue

                chave = list(minha_lista.items.keys())[sel[0]]
                nome = nome_limpo(minha_lista.items[chave])

                win_class = janela_classificar(nome)
                while True:
                    ev2, val2 = win_class.read()
                    if ev2 in (sg.WIN_CLOSED, "Cancelar"):
                        win_class.close()
                        break
                    if ev2 == "Salvar":
                        tipo = val2["-TIPO-"]
                        if not tipo:
                            sg.popup_error("Selecione o tipo do produto!", font=FONTE)
                            continue
                        try:
                            preco = float(val2["-PRECO-"].replace(",", "."))
                        except ValueError:
                            sg.popup_error("Preço inválido! Use números (ex: 5.99)", font=FONTE)
                            continue
                        validade = val2["-VALIDADE-"].strip() or "N/A"

                        prod = Produto(nome, tipo, preco)
                        prod.aplicar_classificacao(minha_lista, chave, tipo, preco, validade)
                        win_class.close()

                        # Atualiza tabela
                        win_main["-TABELA-"].update(values=linhas_tabela(minha_lista))
                        win_main["-STATUS-"].update(f"✔  {nome} classificado com sucesso.")
                        break

            # Botão excluir
            if evento == "-EXCLUIR-":
                sel = valores["-TABELA-"]
                if not sel:
                    sg.popup("Selecione um produto na tabela primeiro.", font=FONTE)
                    continue

                chave = list(minha_lista.items.keys())[sel[0]]
                nome = nome_limpo(minha_lista.items[chave])

                if confirmar_exclusao(nome) == "Yes":
                    del minha_lista.items[chave]
                    win_main["-TABELA-"].update(values=linhas_tabela(minha_lista))
                    win_main["-STATUS-"].update(f"🗑  {nome} removido da lista.")

            # Carregar nova imagem: reinicia o app
            if evento == "-NOVA-":
                win_main.close()
                main()  # reinicia o fluxo
                return


if __name__ == "__main__":
    main()
