import os
import sys
from core import half_edge_funcoes

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pasta_objetos = 'arquivos_objetos'

caminho = os.path.join(os.path.abspath("."), pasta_objetos)

def obter_nomes_objetos():
    if not os.path.exists(caminho):
        os.makedirs(caminho)
        return []

    arquivos_obj = [f for f in os.listdir(caminho) if f.endswith('.obj')]

    return sorted(arquivos_obj)

def ler_arquivo(nome_arquivo):
    caminho_arquivo = caminho + "/" + nome_arquivo
    arquivoFinal = ''

    try:
        with open(caminho_arquivo, 'r') as arquivo:
            arquivoFinal = arquivo.readlines()
            return half_edge_funcoes.criar_estrutura_half_edge(arquivoFinal)
        
    except Exception as e:
        print(e)