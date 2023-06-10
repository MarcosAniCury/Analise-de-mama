import tensorflow as tf
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model, load_model
from sklearn.metrics import classification_report, confusion_matrix


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

    # Gerar as previsões para o conjunto de teste
    y_pred = model.predict(gerador_teste)
    y_pred_classes = y_pred.argmax(axis=1)
    y_true = gerador_teste.classes

    # Calcular a matriz de confusão
    cm = confusion_matrix(y_true, y_pred_classes)

    # Calcular as métricas de classificação (precision, recall, f1-score, support)
    report = classification_report(y_true, y_pred_classes, output_dict=True)

    # Calcular a especificidade para cada classe
    specificity = {}
    # Ignorar as métricas 'micro avg', 'macro avg', 'weighted avg'
    for class_label in range(len(report.keys()) - 3):
        true_negative = sum(cm[i, j] for j in range(len(report.keys(
        )) - 3) if j != class_label for i in range(len(report.keys()) - 3) if i != class_label)
        false_positive = sum(cm[i, class_label] for i in range(
            len(report.keys()) - 3) if i != class_label)
        specificity[class_label] = true_negative / \
            (true_negative + false_positive)

    # Calcular a média das especificidades
    specificity_avg = sum(specificity.values()) / len(specificity)

    metrics = {
        "accuracy": accuracy,
        "precision": report['weighted avg']['precision'],
        "recall": report['weighted avg']['recall'],
        "f1-score": report['weighted avg']['f1-score'],
        "specificity": specificity_avg,
        "matrix": cm
    }

    # Exibir as métricas
    print('Accuracy:', metrics["accuracy"])
    print('Precision:', metrics['precision'])
    print('Sensitivity Recall:', metrics['recall'])
    print('F1-score:', metrics['f1-score'])
    print('Specificity Average:', metrics["specificity"])
    print('Confusion Matrix:')
    print(metrics["matrix"])

    return metrics


def GoogLenNet(arquive_name, already_trained, eBinarioClassificador):
    result_dir = "resultados"
    model = None
    gerador_treino, gerador_teste = carregar_imagens()
    if already_trained:
        model = load_model(os.path.join(result_dir, f"{arquive_name}.h5"))
    else:
        # Carregar o modelo base GoogLeNet
        base_model = InceptionV3(
            weights='imagenet', include_top=False, input_shape=(224, 224, 3))

        # Adicionar camadas densas para a classificação
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(1024, activation='relu')(x)
        output = Dense(4, activation='softmax')(x)
        loss = 'categorical_crossentropy'
        if eBinarioClassificador:
            output = Dense(1, activation='sigmoid')(x)
            loss = 'binary_crossentropy'

        # Criar o modelo final
        model = Model(inputs=base_model.input, outputs=output)

        # Compilar o modelo
        model.compile(optimizer='adam', loss=loss,
                      metrics=['accuracy'])

        # Treinamento do modelo usando o gerador de imagens
        model.fit(gerador_treino, epochs=5, validation_data=gerador_teste)

        # Salvar o modelo treinado
        model.save(os.path.join(result_dir, f"{arquive_name}.h5"))

    return print_metricas(model, gerador_teste)
