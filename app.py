import streamlit as st
import os
import zipfile
import requests
from io import BytesIO
import shutil

# Limpeza do diretório temporário antes de extrair o ZIP
shutil.rmtree("temp_extracted", ignore_errors=True)

# Função para extrair arquivos ZIP
def extract_zip(zip_content, temp_dir):
    with zipfile.ZipFile(zip_content, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

# Função para limpar o diretório temporário
def clean_temp_dir(temp_dir):
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.rmdir(dir_path)

# Configuração do Streamlit
st.title("Aplicativo Streamlit para Processar Arquivo .zip")

# Diretório temporário para extração
temp_dir = "temp_extracted"

# Verifica se o diretório temporário existe, senão, cria
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# URL do arquivo ZIP no GitHub
zip_url = "https://github.com/Henitz/challenge2/raw/master/data/app.zip"

# Obtendo o conteúdo do arquivo ZIP
zip_content = requests.get(zip_url).content

# Verificando se o conteúdo do ZIP foi obtido corretamente
if zip_content:
    try:
        # Limpa o diretório temporário antes da extração
        clean_temp_dir(temp_dir)

        # Extrai os arquivos do ZIP para o diretório temporário
        extract_zip(BytesIO(zip_content), temp_dir)

        st.success("Arquivo ZIP extraído com sucesso!")

        # Executando o arquivo projeto.py
        projeto_path = os.path.join(temp_dir, "projeto.py")
        st.write(f"Executando {projeto_path}")
        os.system(f"streamlit run {projeto_path}")

        st.success("Streamlit app executado com sucesso!")

    except Exception as e:
        st.error(f"Erro ao extrair o arquivo ZIP ou executar o Streamlit app: {e}")

    finally:
        # Limpando o diretório temporário após a execução do Streamlit app
        shutil.rmtree(temp_dir, ignore_errors=True)
        st.write(f"Diretório temporário {temp_dir} removido.")

else:
    st.warning("O arquivo ZIP não foi encontrado. Verifique a URL.")

# Agora, você pode prosseguir com o processamento dos arquivos conforme necessário
# ...
