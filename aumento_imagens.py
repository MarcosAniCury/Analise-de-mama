from PIL import Image
import cv2
import numpy as np
import os

# Diretório das imagens de treino
train_dir = "treino"
augmented_dir = "treino_mais"

# Criar o diretório para as imagens aumentadas
os.makedirs(augmented_dir, exist_ok=True)

# Função para realizar o aumento de dados em uma imagem
def augment_image(image_path, save_dir):
    # Carregar a imagem com a biblioteca Pillow
    image_pil = Image.open(image_path)

    # Converter a imagem do formato PIL para o formato OpenCV
    image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    # Verificar se a imagem foi carregada corretamente
    if image is not None:
        # Aplicar espelhamento horizontal
        flipped = cv2.flip(image, 1)

        # Aplicar equalização de histograma
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        equalized = cv2.equalizeHist(gray)

        # Gerar variações: espelhada/não espelhada x equalizada/não equalizada
        variations = [
            (image, "nao_espelhada_nao_equalizada"),
            (flipped, "espelhada_nao_equalizada"),
            (equalized, "nao_espelhada_equalizada"),
            (cv2.flip(equalized, 1), "espelhada_equalizada")
        ]

        # Salvar as imagens aumentadas
        base_filename = os.path.splitext(os.path.basename(image_path))[0]
        for variation in variations:
            augmented_image = variation[0]
            variation_name = variation[1]
            save_path = os.path.join(save_dir, f"{base_filename}_{variation_name}.png")
            cv2.imwrite(save_path, augmented_image)
    else:
        print(f"Erro ao carregar a imagem: {image_path}")

# Percorrer todas as imagens na pasta de treino
for root, dirs, files in os.walk(train_dir):
    for file in files:
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            image_path = os.path.join(root, file)
            augment_image(image_path, augmented_dir)
