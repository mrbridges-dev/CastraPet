import streamlit as st
from database import adicionar_animal, atualizar_animal, obter_animal_por_id
import os
from datetime import datetime
import folium
from streamlit_folium import folium_static, st_folium
from folium.plugins import MousePosition
from PIL import Image  # <-- Adiciona PIL para redimensionamento
import cv2
import numpy as np

@st.dialog("Cadastro de Animal")
def exibir_formulario(animal_id=None):
    # Se for edição, carrega os dados do animal
    animal = None
    if animal_id:
        animal = obter_animal_por_id(animal_id)
        if animal and 'selected_location' not in st.session_state:
            st.session_state.selected_location = [float(animal['latitude']), float(animal['longitude'])]
    
    # Inicializa as coordenadas no session_state se não existirem
    if 'selected_location' not in st.session_state:
        st.session_state.selected_location = [-22.5987, -48.8003]  # Lençóis Paulista
    
    with st.form("form_animal"):
        nome = st.text_input("Nome do animal", value=animal['nome'] if animal else "")
        especie = st.selectbox("Espécie", ["Cachorro", "Gato"], 
                             index=0 if not animal else ["Cachorro", "Gato"].index(animal['especie']))
        idade = st.number_input("Idade", min_value=0, step=1, 
                              value=animal['idade'] if animal else 0)
        status = st.selectbox("Status de castração", ["Castrado", "Não Castrado"],
                            index=0 if not animal else ["Castrado", "Não Castrado"].index(animal['status']))

        st.markdown("### Selecione a localização do animal no mapa")
        st.caption("Clique no mapa ou arraste o marcador para definir a localização")
        
        # Cria o mapa para seleção da localização
        m = folium.Map(
            location=st.session_state.selected_location,
            zoom_start=13
        )

        # Adiciona o plugin de posição do mouse
        formatter = "function(num) {return L.Util.formatNum(num, 6);};"
        MousePosition(
            position='topright',
            separator=' | ',
            prefix="Coordenadas:",
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(m)

        # Adiciona marcador na posição atual
        marker = folium.Marker(
            st.session_state.selected_location,
            popup="Local selecionado",
            draggable=True
        )
        marker.add_to(m)

        # Exibe o mapa e captura eventos
        map_data = st_folium(m, width=450, height=300)
        
        # Atualiza as coordenadas quando o mapa é interagido
        if map_data is not None:
            # Captura clique direto no mapa
            if map_data.get("last_clicked"):
                st.session_state.selected_location = [
                    map_data["last_clicked"]["lat"],
                    map_data["last_clicked"]["lng"]
                ]
            # Captura movimentação do marcador
            elif map_data.get("all_drawings"):
                if map_data["all_drawings"]:
                    coordinates = map_data["all_drawings"][-1]["geometry"]["coordinates"]
                    st.session_state.selected_location = [coordinates[1], coordinates[0]]
            # Captura a última posição conhecida do marcador
            elif map_data.get("bounds") and map_data.get("center"):
                st.session_state.selected_location = [
                    map_data["center"]["lat"],
                    map_data["center"]["lng"]
                ]
        
        # Campo para descrição da localização (agora opcional)
        localizacao = st.text_input("Descrição da localização (referência - opcional)", 
                                  value=animal['localizacao'] if animal else "")
        
        # Campo para upload de foto
        foto_file = st.file_uploader("Foto do animal", type=['png', 'jpg', 'jpeg'])
        
        ## Se for edição, mostra a foto atual
        #if animal and animal['foto']:
        #    st.write("Foto atual:")
        #    caminho_foto_atual = os.path.join('assets', 'img', animal['foto'])
        #    if os.path.exists(caminho_foto_atual):
        #        st.image(caminho_foto_atual, width=200)
        
        # Botão de submit com texto apropriado
        submit_label = "Salvar" if animal_id else "Cadastrar"
        enviado = st.form_submit_button(submit_label, use_container_width=True)

        if enviado:
            if not nome:
                st.error("Por favor, insira o nome do animal")
                return False

            try:
                # Processamento da foto
                caminho_foto = None
                if foto_file is not None:
                    diretorio_uploads = os.path.join('assets', 'img', 'uploads')
                    os.makedirs(diretorio_uploads, exist_ok=True)
                    extensao = os.path.splitext(foto_file.name)[1]
                    novo_nome = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}{extensao}"
                    caminho_foto = os.path.join(diretorio_uploads, novo_nome)

                    # Crop centralizado (quadrado) na imagem
                    img_pil = Image.open(foto_file).convert('RGB')
                    largura, altura = img_pil.size
                    lado = min(largura, altura)
                    left = (largura - lado) // 2
                    top = (altura - lado) // 2
                    right = left + lado
                    bottom = top + lado
                    img_cortada = img_pil.crop((left, top, right, bottom))
                    img_cortada = img_cortada.resize((300, 300), Image.LANCZOS)
                    img_cortada.save(caminho_foto, format='JPEG', quality=90)

                    caminho_foto = os.path.join('uploads', novo_nome)
                # Usa as coordenadas atualizadas do session_state
                latitude, longitude = st.session_state.selected_location
                st.write(f"Debug - Coordenadas: {latitude}, {longitude}")  # Debug temporário
                
                if animal_id:
                    # Atualiza o animal existente
                    atualizar_animal(
                        animal_id, nome, especie, idade, status, localizacao or "",
                        caminho_foto if foto_file else None,
                        latitude, longitude
                    )
                    st.success("Animal atualizado com sucesso!")
                    st.session_state.show_modal = False
                    st.session_state.editing_animal_id = None
                    if 'selected_location' in st.session_state:
                        del st.session_state.selected_location
                    st.rerun()
                else:
                    # Adiciona novo animal
                    adicionar_animal(
                        nome, especie, idade, status, localizacao or "",
                        caminho_foto, latitude, longitude
                    )
                    st.session_state.show_modal = False
                    if 'selected_location' in st.session_state:
                        del st.session_state.selected_location
                    st.success("Animal cadastrado com sucesso!")
                    st.rerun()
                
                return True
                
            except Exception as e:
                st.error(f"Erro ao salvar: {str(e)}")
                return False
            
        return False
