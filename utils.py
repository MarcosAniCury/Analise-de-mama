import os
import shutil

# Função para copiar uma imagem para o diretório de destino


def copiar_imagem(origem, destino):
    os.makedirs(destino, exist_ok=True)
    shutil.copy2(origem, destino)

# Retorna um index que indentifica para qual pasta a imagem será salva


def seleciona_classe_imagem(caracter):
    if caracter == 'd':
        return 0
    elif caracter == 'e':
        return 1
    elif caracter == 'f':
        return 2
    elif caracter == 'g':
        return 3

# Separa as imagens de treino e de teste


def separacao_imagens():
    # Caminhos dos diretórios para as imagens de treino e teste
    train_dir = "treino"
    test_dir = "teste"

    class_dir = ["BIRADS_1", "BIRADS_2", "BIRADS_3", "BIRADS_4"]

    # Diretório principal onde estão localizadas as imagens de mamografias
    mamografias_dir = "mamografias"

    # Percorrer todas as pastas dentro do diretório de mamografias
    for dirpath, dirnames, filenames in os.walk(mamografias_dir):
        for arquivo in filenames:
            if arquivo.endswith(".png") or arquivo.endswith(".jpg") or arquivo.endswith(".jpeg"):
                nome_arquivo, extensao = os.path.splitext(arquivo)
                # Extrair o número entre parênteses
                numero = nome_arquivo.split("(")[-1].split(")")[0]
                caracter = nome_arquivo[0]
                index_pasta_classe = seleciona_classe_imagem(caracter)
                if numero.isdigit():
                    numero = int(numero)
                    imagem_origem = os.path.join(dirpath, arquivo)
                    if numero % 4 == 0:
                        copiar_imagem(imagem_origem, os.path.join(
                            test_dir, class_dir[index_pasta_classe]))
                    else:
                        copiar_imagem(imagem_origem, os.path.join(
                            train_dir, class_dir[index_pasta_classe]))
