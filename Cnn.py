import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model


def carregar_imagens():
    # Diretórios de treino e teste
    treino_dir = 'treino_mais'
    teste_dir = 'teste'

    # Criação do gerador de imagens de treino e teste
    datagen_treino = ImageDataGenerator(rescale=1./255)
    datagen_teste = ImageDataGenerator(rescale=1./255)

    # Carregar as imagens de treino
    gerador_treino = datagen_treino.flow_from_directory(
        treino_dir,
        # Tamanho das imagens de entrada esperado pela GoogLeNet
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical')

    # Carregar as imagens de teste
    gerador_teste = datagen_teste.flow_from_directory(
        teste_dir,
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical')

    return gerador_treino, gerador_teste


def print_metricas(model, gerador_teste):
    # Avaliar o modelo no conjunto de teste
    loss, accuracy = model.evaluate(gerador_teste)

    # Exibir as métricas
    print('Loss:', loss)
    print('Accuracy:', accuracy)


def GoogLenNet():
    gerador_treino, gerador_teste = carregar_imagens()

    # Carregar o modelo base GoogLeNet
    base_model = InceptionV3(
        weights='imagenet', include_top=False, input_shape=(224, 224, 3))

    # Adicionar camadas densas para a classificação
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    output = Dense(4, activation='softmax')(x)

    # Criar o modelo final
    model = Model(inputs=base_model.input, outputs=output)

    # Congelar os pesos do modelo base
    for layer in base_model.layers:
        layer.trainable = False

    # Compilar o modelo
    model.compile(optimizer='adam', loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # Treinamento do modelo usando o gerador de imagens
    model.fit(gerador_treino, epochs=10, validation_data=gerador_teste)

    # Salvar o modelo treinado
    model.save('googlenet_model.h5')

    print_metricas(model, gerador_teste)
