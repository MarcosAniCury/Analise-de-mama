import os
import cv2
from utils import separacao_imagens
from segmentar_imagens import remove_variacoes_imagem, remove_contornos_menores
from aumento_imagens import augmentacao
from Cnn import GoogLenNet

def tratar_imagens():
    treino_dir = "treino"
    # Percorrer todas as pastas dentro do diretório de treino
    for dirpath, dirnames, filenames in os.walk(treino_dir):
        for dirpath_class, dirnames_class, filenames_class in os.walk(dirpath):
            # Percorre todos os arquivos
            for arquivo in filenames_class:
                # Pega apenas os arquivos de imagem
                if arquivo.endswith(".png") or arquivo.endswith(".jpg") or arquivo.endswith(".jpeg"):
                    path_image = os.path.join(dirpath_class, arquivo)
                    image = cv2.imread(path_image)
                    # Remove variacoes de cores da imagem
                    result_image = remove_variacoes_imagem(image)

                    # Área mínima para considerar um contorno como elemento principal
                    threshold_area = 10000  
                    # Remove objetos menores que o threshold_area
                    result_image = remove_contornos_menores(result_image, threshold_area)
                    # Sobre escreve imagens anteriores pelas pré-processadas
                    cv2.imwrite(path_image, result_image)
                    print(arquivo)

def execucao():
    # separacao_imagens()
    # tratar_imagens()
    # augmentacao()
    GoogLenNet()

execucao()