# Sistema Inteligente de Classificação de Produtos (OCR + POO)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Tesseract](https://img.shields.io/badge/Tesseract--OCR-black?style=for-the-badge&logo=google&logoColor=white)
![PIL](https://img.shields.io/badge/Pillow-blue?style=for-the-badge)

Este projeto automatiza o pipeline de leitura, extração, higienização e modelagem de listas de compras obtidas por meio de imagens (scans ou fotos de notas/papéis). Ele combina o poder do **Reconhecimento Ótico de Caracteres (OCR)** e **Expressões Regulares (Regex)** com uma arquitetura robusta baseada em **Programação Orientada a Objetos (POO)**.

O software foi desenvolvido sob rígidos padrões acadêmicos, aplicando conceitos avançados de engenharia de software para eliminar condicionais complexas (`if/else`) através de herança e polimorfismo.

---

## Arquitetura e Conceitos de POO Aplicados

O sistema foi estruturado em **6 classes principais**, garantindo a separação de responsabilidades (SOLID) e alta coesão:

### 1. Herança e Polimorfismo (Core do Domínio)
* **`Produto` (Classe Base):** Modela os atributos comuns a qualquer mercadoria (`nome`, `preco`, `tipo`). Define a assinatura abstrata do método `classificar()` e `obter_detalhes()`.
* **`ProdutoComida` (Subclasse):** Estende a classe base injetando propriedades exclusivas do setor alimentício, como controle de perecibilidade e inserção de data de validade. Sobrescreve dinamicamente o comportamento de classificação.
* **`ProdutoBebida` (Subclasse):** Especializa o produto para armazenar propriedades térmicas de consumo (se deve ser mantido quente ou gelado).
* **`ProdutoGeral` (Subclasse):** Abstração genérica reutilizada para classificar seções secundárias como Higiene Pessoal, Limpeza e Utensílios.

### 2. Associação e Encapsulamento
* **`ListaCompras`:** Funciona como a classe controladora do inventário. Ela encapsula um dicionário de dados (`self.items`) que mantém uma relação de **Associação** direta com as instâncias de `Produto`.

### 3. Infraestrutura e Utilitários (Camada de Suporte)
* **`OCRProcessor`:** Encapsula a biblioteca PyTesseract, isolando a lógica de baixo nível do processamento de imagem da regra de negócios.
* **`GerenciadorTexto`:** Concentra o motor de **Regex (`re`)** responsável por limpar ruídos de caracteres, strings vazias e cabeçalhos textuais gerados no escaneamento.
* **`ValidadorEntrada`:** Centraliza métodos que protegem a aplicação contra quebras de execução causadas por inputs incorretos do usuário (Tratamento de Exceções).

---

## Como Executar o Projeto

### 1. Instalar a Engine do OCR
O projeto depende do motor Tesseract instalado no sistema operacional:
* **Windows:** Baixe o instalador compilado por terceiros (ex: UB-Mannheim) e marque a opção para instalar o pacote de dados em **Português (`por`)**.
* Adicione o caminho do executável `tesseract.exe` na variável correspondente dentro do arquivo `main.py`.
* Adicionar path da imagem a ser escaneada no aqurivo `main.py`.

### 2. Clonar o Repositório e Instalar Dependências
Saída de código
README_GitHub.md gerado!

```bash
# Clonar o repositório
git clone [https://github.com/seu-usuario/nome-do-repositorio.git](https://github.com/seu-usuario/nome-do-repositorio.git)

# Aceder à pasta do projeto
cd nome-do-repositorio

# Instalar bibliotecas necessárias
pip install pytesseract pillow
