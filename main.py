from cod_geral import *

# 1 passo - processar a imagem e extrair o texto
items_limpos = editorTexto.limpar_lista_compras(texto) 

# 2 passo - organizar a lista e exibir na tela
minha_lista = organizar_lista()
minha_lista.popular_lista(items_limpos)

# 3 passo - escolher o produto e editar
choice = None
while choice != 0: #loop externo 
    minha_lista.exibir_lista()
    choice = Produto.escolher_produto()

# 4 passo - editar o produto escolhido
    Produto.editar_produto(choice)
