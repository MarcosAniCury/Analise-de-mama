import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

def atualizar_imagem():
    global imagem_atual, imagem_atual_photo

    # Carregar a imagem atual
    imagem_atual = Image.open(imagens[indice_imagem_atual])
    imagem_atual_gray = imagem_atual.convert('L')  # converte para escala de cinza
    imagem_atual_resize = imagem_atual_gray.resize((300, 400), Image.LANCZOS)
    imagem_atual_photo = ImageTk.PhotoImage(imagem_atual_resize)

    # Atualizar o Label com a nova imagem
    label_imagem.configure(image=imagem_atual_photo)
    label_imagem.image = imagem_atual_photo  # Atualiza a referência da imagem no Label]
    
def abrir_explorador():
    # Abrir o explorador de arquivos
    initial_path = "C:\\Users\\letic\\Documents\\GitHub\\Analise-de-mama\\mamografias"
    filename = filedialog.askopenfilename(initialdir=initial_path, title="Selecione uma imagem", filetypes=(("Arquivos de imagem", "*.jpg;*.jpeg;*.png"), ("Todos os arquivos", "*.*")))
    # Carregar a imagem selecionada
    imagem = Image.open(filename)

    if filename:
        # Atualizar a lista de imagens com a nova imagem selecionada
        imagens[indice_imagem_atual] = filename

        # Atualizar a imagem exibida
        atualizar_imagem()


def trocar_imagem():
    global indice_imagem

    # incrementa o índice da imagem
    indice_imagem += 1

    # se o índice da imagem for maior ou igual ao comprimento da lista, volta ao início
    if indice_imagem >= len(imagens):
        indice_imagem = 0

    # atualiza a imagem exibida no Label
    imagem_atual = Image.open("mamografias\DleftCC\\" + imagens[indice_imagem] )
    imagem_atual_gray = imagem_atual.convert('L')  # converte para escala de cinza
    imagem_atual_resize = imagem_atual_gray.resize((300, 400), Image.LANCZOS)
    imagem_atual_photo = ImageTk.PhotoImage(imagem_atual_resize)
    label_imagem.configure(image=imagem_atual_photo)
    label_imagem.image = imagem_atual

def update_image(*args):
    # Obtém os valores da barra deslizante
    min_value = min_slider.get()
    max_value = max_slider.get()

    # Aplica o janelamento
    imagem_ndarray = np.asanyarray(imagem_atual_gray)
    output_img = np.zeros_like(imagem_ndarray)
    output_img = np.where(imagem_ndarray <= min_value, 0, output_img)
    output_img = np.where(imagem_ndarray > max_value, 255, output_img)
    output_img = np.where((imagem_ndarray > min_value) & (imagem_ndarray <= max_value),
                        ((imagem_ndarray - min_value) / (max_value - min_value)) * 255,
                        output_img)


    # Converte a imagem para o formato PIL para mostrar na janela
    output_img_pil = Image.fromarray(output_img).resize((300, 400), Image.LANCZOS)
    output_img_tk = ImageTk.PhotoImage(output_img_pil)

    # Atualiza a imagem na janela
    label_imagem.configure(image=output_img_tk)
    label_imagem.image = output_img_tk


global indice_imagem
indice_imagem = 0

# cria uma janela
janela = Tk()


imagens = []
i = 0

for i in range(1,315):
    imagens.append("d_left_cc (" + str(i) + ").png")

indice_imagem_atual = 0

# carrega a imagem
imagem_atual = Image.open("mamografias\DleftCC\d_left_cc (1).png")
imagem_atual_gray = imagem_atual.convert('L')  # converte para escala de cinza
imagem_atual_resize = imagem_atual_gray.resize((300, 400), Image.LANCZOS)
imagem_atual_photo = ImageTk.PhotoImage(imagem_atual_resize)

# cria um widget Label e exibe a imagem na janela
label_imagem = Label(janela, image=imagem_atual_photo)
label_imagem.pack()

botao = Button(janela, text="Selecionar Imagem", command=abrir_explorador)
botao.pack()

min_slider = Scale(janela, from_=0, to=255, orient='horizontal', label='Valor mínimo', command=update_image)
min_slider.pack()

max_slider = Scale(janela, from_=0, to=255, orient='horizontal', label='Valor máximo', command=update_image)
max_slider.pack()

# inicia o loop principal do Tkinter
janela.mainloop()

