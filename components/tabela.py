import streamlit as st
from database import obter_animais, deletar_animal
import os

def exibir_tabela_animais():
    animais = obter_animais()

    if not animais:
        st.info("Nenhum animal cadastrado.")
        return

    # Criando um container para os cards
    col1, col2 = st.columns(2)
    
    # Distribuindo os cards entre as colunas
    for i, animal in enumerate(animais):
        # Alternando entre as colunas
        col = col1 if i % 2 == 0 else col2
        
        # Criando o card
        with col:
            with st.container():
                st.markdown("""
                    <style>
                        .animal-card {
                            background-color: #f0f2f6;
                            border-radius: 10px;
                            padding: 20px;
                            margin-bottom: 20px;
                        }
                    </style>
                """, unsafe_allow_html=True)
                
                with st.container():
                    st.markdown('<div class="animal-card">', unsafe_allow_html=True)
                    
                    # Criando colunas dentro do card
                    img_col, info_col = st.columns([4, 6])
                    
                    # Coluna da imagem
                    with img_col:
                        if animal['foto'] and os.path.exists(os.path.join('assets', 'img', animal['foto'])):
                            st.image(os.path.join('assets', 'img', animal['foto']), 
                                   width=200,
                                   output_format="JPEG",
                                   use_container_width=False)
                        else:
                            st.markdown("📷 Sem foto")
                    
                    # Coluna das informações
                    with info_col:
                        st.markdown(f"### {animal['nome']}")
                        st.markdown(f"**Espécie:** {animal['especie']}")
                        st.markdown(f"**Idade:** {animal['idade']} anos")
                        st.markdown(f"**Status:** {animal['status']}")
                        st.markdown(f"**Localização:** {animal['localizacao']}")
                        
                        # Botões de ação em linha única
                        if st.button("✏️ Editar", key=f"edit_{animal['id']}"):
                            st.session_state.show_modal = True
                            st.session_state.editing_animal_id = animal['id']
                            st.rerun()
                        
                        if st.button("🗑️ Deletar", key=f"del_{animal['id']}"):
                            # Obtém o caminho da foto e deleta o registro
                            caminho_foto = deletar_animal(animal['id'])
                            
                            # Se existe uma foto, deleta o arquivo
                            if caminho_foto:
                                caminho_completo = os.path.join('assets', 'img', caminho_foto)
                                if os.path.exists(caminho_completo):
                                    os.remove(caminho_completo)
                            
                            st.success("Animal deletado com sucesso!")
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
