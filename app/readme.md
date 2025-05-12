# CastraPet 🐾

Sistema web para gerenciamento de animais para castração, desenvolvido com Python e Streamlit.

## Funcionalidades

- Cadastro de animais com informações detalhadas
- Upload de fotos dos animais
- Mapeamento da localização dos animais usando coordenadas geográficas
- Visualização em lista com cards informativos
- Visualização em mapa interativo
- Edição e exclusão de registros
- Sistema de status de castração

## Requisitos

- Python 3.12+
- MySQL Server
- Bibliotecas Python listadas em `requirements.txt`

## Configuração

1. Clone o repositório
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Configure o banco de dados MySQL:
   - Crie um banco de dados chamado `castrapet`
   - Ajuste as credenciais de conexão em `database.py`

## Executando o projeto

Para iniciar a aplicação, execute:
```
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`

## Estrutura do Projeto

- `app.py`: Arquivo principal da aplicação
- `database.py`: Configurações e operações do banco de dados
- `components/`: Módulos com componentes da interface
  - `formulario.py`: Formulário de cadastro/edição
  - `mapa.py`: Componente do mapa interativo
  - `tabela.py`: Listagem dos animais em cards
- `assets/img/`: Diretório para armazenamento das imagens