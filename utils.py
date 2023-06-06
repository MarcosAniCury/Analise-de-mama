import os
import shutil

# Função para copiar uma imagem para o diretório de destino
def copiar_imagem(origem, destino):
        os.makedirs(destino, exist_ok=True)
        shutil.copy2(origem, destino)

# Separa as imagens de treino e de teste
def separacao_imagens():
    # Caminhos dos diretórios para as imagens de treino e teste
    train_dir = "treino"
    test_dir = "teste"
    
    # Diretório principal onde estão localizadas as imagens de mamografias
    mamografias_dir = "mamografias"

    # Percorrer todas as pastas dentro do diretório de mamografias
    for dirpath, dirnames, filenames in os.walk(mamografias_dir):
        for arquivo in filenames:
            if arquivo.endswith(".png") or arquivo.endswith(".jpg") or arquivo.endswith(".jpeg"):
                nome_arquivo, extensao = os.path.splitext(arquivo)
                numero = nome_arquivo.split("(")[-1].split(")")[0]  # Extrair o número entre parênteses
                if numero.isdigit():
                    numero = int(numero)
                    imagem_origem = os.path.join(dirpath, arquivo)
                    if numero % 4 == 0:
                        copiar_imagem(imagem_origem, test_dir)
                    else:
                        copiar_imagem(imagem_origem, train_dir)
