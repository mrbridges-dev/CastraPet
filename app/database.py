import mysql.connector
from datetime import date
import os

# Conecta ao banco de dados
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),    # Substitua pelo seu usuário do MySQL
    password=os.getenv("DB_PASSWORD"),    # Substitua pela sua senha do MySQL
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor(dictionary=True)

# Adiciona um novo animal
def adicionar_animal(nome, especie, idade, status, localizacao, foto=None, latitude=None, longitude=None):
    data_cadastro = date.today()
    query = """
        INSERT INTO animais (nome, especie, idade, status, localizacao, data_cadastro, foto, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nome, especie, idade, status, localizacao, data_cadastro, foto, latitude, longitude))
    conn.commit()

# Obtém todos os animais cadastrados
def obter_animais():
    query = "SELECT * FROM animais ORDER BY data_cadastro DESC"
    cursor.execute(query)
    return cursor.fetchall()

# Obtém um animal específico pelo ID
def obter_animal_por_id(id):
    query = "SELECT * FROM animais WHERE id = %s"
    cursor.execute(query, (id,))
    return cursor.fetchone()

# Atualiza os dados de um animal
def atualizar_animal(id, nome, especie, idade, status, localizacao, foto=None, latitude=None, longitude=None):
    if foto is not None:
        query = """
            UPDATE animais 
            SET nome = %s, especie = %s, idade = %s, status = %s, 
                localizacao = %s, foto = %s, latitude = %s, longitude = %s
            WHERE id = %s
        """
        cursor.execute(query, (nome, especie, idade, status, localizacao, foto, latitude, longitude, id))
    else:
        query = """
            UPDATE animais 
            SET nome = %s, especie = %s, idade = %s, status = %s, 
                localizacao = %s, latitude = %s, longitude = %s
            WHERE id = %s
        """
        cursor.execute(query, (nome, especie, idade, status, localizacao, latitude, longitude, id))
    conn.commit()

# Deleta animal pelo ID
def deletar_animal(id):
    # Primeiro, obtém o caminho da foto
    query = "SELECT foto FROM animais WHERE id = %s"
    cursor.execute(query, (id,))
    resultado = cursor.fetchone()
    caminho_foto = resultado['foto'] if resultado else None
    
    # Depois deleta o registro
    query = "DELETE FROM animais WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    
    return caminho_foto

# Criar a tabela se não existir
def criar_tabela():
    query = """
    CREATE TABLE IF NOT EXISTS animais (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        especie VARCHAR(50) NOT NULL,
        idade INT NOT NULL,
        status VARCHAR(50) NOT NULL,
        localizacao VARCHAR(200),
        data_cadastro DATE NOT NULL,
        foto VARCHAR(255),
        latitude DECIMAL(10,8),
        longitude DECIMAL(11,8)
    )
    """
    cursor.execute(query)
    conn.commit()

# Chamada para criar a tabela ao iniciar
criar_tabela()
