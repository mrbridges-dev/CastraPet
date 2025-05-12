import streamlit as st
from database import obter_animais, deletar_animal
import os

def exibir_tabela_animais():
    animais = obter_animais()

    if not animais:
        st.info("Nenhum animal cadastrado.")
        return

    # Criando um container para os cards
    col1, col2, col3 = st.columns(3, gap="small")
    
    # Distribuindo os cards entre as colunas
    for i, animal in enumerate(animais):
        # Alternando entre as colunas
        if i % 3 == 0:
            col = col1
        elif i % 3 == 1:
            col = col2
        else:
            col = col3
        
        # Criando o card
        with col:
                with st.container(height=200, border=True):
                    
                    # Criando colunas dentro do card
                    img_col, info_col, button_col = st.columns(3)
                    
                    # Coluna da imagem
                    with img_col:
                        if animal['foto'] and os.path.exists(os.path.join('assets', 'img', animal['foto'])):
                            st.image(os.path.join('assets', 'img', animal['foto']), 
                                   width=300,
                                   output_format="JPEG",
                                   use_container_width=False)
                        else:
                            st.markdown("📷 Sem foto")
                    
                    # Coluna das informações
                with info_col:
                    st.markdown(
                        f"""
                        <div style="font-size:16px; line-height:1.5; margin-bottom:10px;">
                            <strong>{animal['nome']}</strong><br>
                            Espécie: {animal['especie']}<br>
                            Idade: {animal['idade']} anos<br>
                            Status: {animal['status']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                    with button_col:    # Botões de ação em linha única
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
