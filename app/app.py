import streamlit as st
from components.formulario import exibir_formulario
from components.tabela import exibir_tabela_animais
from components.mapa import exibir_mapa_animais

st.set_page_config(
    page_title="CastraPet",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Esconde o botão Deploy e o menu de três pontos do Streamlit
st.markdown("""
    <style>
    [data-testid="stDeployButton"], [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Configuração da navegação
st.sidebar.title("🐾 CastraPet")
st.sidebar.divider()

# Dicionário de páginas
PAGES = {
    "📋 Cadastros": {
        "title": "Cadastro de Animais",
        "icon": "📋",
        "function": lambda: show_cadastros()
    },
    "🗺️ Localização": {
        "title": "Mapa de Animais",
        "icon": "🗺️",
        "function": lambda: show_mapa()
    }
}

# Seleção da página
if "current_page" not in st.session_state:
    st.session_state.current_page = "📋 Cadastros"

selected_page = st.sidebar.radio("", list(PAGES.keys()), index=list(PAGES.keys()).index(st.session_state.current_page))
st.session_state.current_page = selected_page

def show_cadastros():
    
    # Criando colunas para o layout do cabeçalho
    col_titulo, col_botao = st.columns([3, 1], vertical_alignment="center")

    # Título
    with col_titulo:
        st.title("📋 Lista de Animais")

    # Botão de cadastro
    with col_botao:
        if st.button("➕ Cadastrar Novo Animal"):
            st.session_state.show_modal = True
            if 'editing_animal_id' in st.session_state:
                del st.session_state.editing_animal_id

    # Flag para controle do pop-up
    if "show_modal" not in st.session_state:
        st.session_state.show_modal = False

    # Simulando o modal
    if st.session_state.show_modal:
        animal_id = st.session_state.get('editing_animal_id', None)
        if exibir_formulario(animal_id):
            if 'editing_animal_id' in st.session_state:
                del st.session_state.editing_animal_id
            st.rerun()

    st.divider()
    exibir_tabela_animais()

def show_mapa():
    st.title(f"{PAGES['🗺️ Localização']['icon']} {PAGES['🗺️ Localização']['title']}")
    exibir_mapa_animais()

# Exibe a página selecionada
PAGES[selected_page]["function"]()