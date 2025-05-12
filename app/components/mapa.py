import streamlit as st
import folium
from streamlit_folium import folium_static
from database import obter_animais
import os

def exibir_mapa_animais():
    # Obtém os animais cadastrados
    animais = obter_animais()
    
    # Cria o mapa centralizado em Lençóis Paulista, SP
    mapa = folium.Map(
        location=[-22.5987, -48.8003],  # Coordenadas de Lençóis Paulista
        zoom_start=13  # Zoom mais aproximado para visualização da cidade
    )
    
    # Adiciona marcadores para cada animal
    for animal in animais:
        if animal['latitude'] and animal['longitude']:
            # Prepara o HTML do popup com as informações do animal
            foto_html = ""
            if animal['foto'] and os.path.exists(os.path.join('assets', 'img', animal['foto'])):
                foto_html = f"""<img src='assets/img/{animal['foto']}' style='width:100px;'><br>"""
            
            popup_html = f"""
            <div style='width:200px;'>
                {foto_html}
                <strong>{animal['nome']}</strong><br>
                Espécie: {animal['especie']}<br>
                Idade: {animal['idade']} anos<br>
                Status: {animal['status']}<br>
                Localização: {animal['localizacao']}
            </div>
            """
            
            # Adiciona o marcador com popup
            folium.Marker(
                location=[float(animal['latitude']), float(animal['longitude'])],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=animal['nome']
            ).add_to(mapa)
    
    # Exibe o mapa
    folium_static(mapa, width=1200, height=600)