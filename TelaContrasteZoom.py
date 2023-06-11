import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

def get_image_explorer():
    global imagem_original, imagem_original_photo

    # Carregar a imagem atual
    imagem_original = Image.open(imagens[indice_imagem_original])
    imagem_original_gray = imagem_original.convert('L')  # converte para escala de cinza
    imagem_original_resize = imagem_original_gray.resize((300, 400), Image.LANCZOS)
    imagem_original_photo = ImageTk.PhotoImage(imagem_original_resize)

    # Atualizar o Label com a nova imagem
    label_imagem.configure(image=imagem_original_photo)
    label_imagem.image = imagem_original_photo  # Atualiza a referência da imagem no Label]
    
def abrir_explorador():
    # Abrir o explorador de arquivos
    initial_path = "C:\\Users\\letic\\Documents\\GitHub\\Analise-de-mama\\mamografias"
    filename = filedialog.askopenfilename(initialdir=initial_path, title="Selecione uma imagem", filetypes=(("Arquivos de imagem", "*.jpg;*.jpeg;*.png"), ("Todos os arquivos", "*.*")))

    if filename:
        # Atualizar a lista de imagens com a nova imagem selecionada
        imagens[indice_imagem_original] = filename

        # Atualizar a imagem exibida
        get_image_explorer()


def trocar_imagem():
    global indice_imagem

    # incrementa o índice da imagem
    indice_imagem += 1

    # se o índice da imagem for maior ou igual ao comprimento da lista, volta ao início
    if indice_imagem >= len(imagens):
        indice_imagem = 0

    # atualiza a imagem exibida no Label
    imagem_original = Image.open("mamografias\DleftCC\\" + imagens[indice_imagem] )
    imagem_original_gray = imagem_original.convert('L')  # converte para escala de cinza
    imagem_original_resize = imagem_original_gray.resize((300, 400), Image.LANCZOS)
    imagem_original_photo = ImageTk.PhotoImage(imagem_original_resize)
    label_imagem.configure(image=imagem_original_photo)
    label_imagem.image = imagem_original

def update_image_windowing(*args):
    global imagem_atual_resize, imagem_atual_photo, n_zooms

    # Obtém os valores da barra deslizante
    min_value = min_slider.get()
    max_value = max_slider.get()

    # Aplica o janelamento
    imagem_ndarray = np.asanyarray(imagem_original_gray)
    output_img = np.zeros_like(imagem_ndarray)
    output_img = np.where(imagem_ndarray <= min_value, 0, output_img)
    output_img = np.where(imagem_ndarray > max_value, 255, output_img)
    output_img = np.where((imagem_ndarray > min_value) & (imagem_ndarray <= max_value),
                        ((imagem_ndarray - min_value) / (max_value - min_value)) * 255,
                        output_img)


    # Converte a imagem para o formato PIL para mostrar na janela
    imagem_atual_resize = Image.fromarray(output_img).resize((300, 400), Image.LANCZOS)
    imagem_atual_photo = ImageTk.PhotoImage(imagem_atual_resize)

    # Atualiza a imagem na janela
    label_imagem.configure(image=imagem_atual_photo)
    label_imagem.image = imagem_atual_photo

    n_zooms_temp = n_zooms

    if n_zooms > 0:
        type_zoom = zoom_in
    else: 
        type_zoom = zoom_out
    
    n_zooms = 0

    for i in range(abs(n_zooms_temp)):
        type_zoom()

def zoom_in():
    global imagem_atual_resize, imagem_atual_photo, n_zooms

    n_zooms =  n_zooms + 1

    # Obtém as dimensões atuais da imagem redimensionada
    width, height = imagem_atual_resize.size

    # Calcula as novas dimensões para o zoom
    new_width = int(width * 1.1)
    new_height = int(height * 1.1)

    # Redimensiona a imagem atual para o zoom
    imagem_atual_resize = imagem_atual_resize.resize((new_width, new_height), Image.LANCZOS)

    # Atualiza a imagem atual e a imagem exibida
    imagem_atual_photo = ImageTk.PhotoImage(imagem_atual_resize)
    label_imagem.configure(image=imagem_atual_photo)
    label_imagem.image = imagem_atual_photo

def zoom_out():
    global imagem_atual_resize, imagem_atual_photo, n_zooms

    n_zooms = n_zooms - 1

    # Obtém as dimensões atuais da imagem redimensionada
    width, height = imagem_atual_resize.size

    # Calcula as novas dimensões para o zoom
    new_width = int(width / 1.1)
    new_height = int(height / 1.1)

    # Redimensiona a imagem atual para o zoom
    imagem_atual_resize = imagem_atual_resize.resize((new_width, new_height), Image.LANCZOS)

    # Atualiza a imagem atual e a imagem exibida
    imagem_atual_photo = ImageTk.PhotoImage(imagem_atual_resize)
    label_imagem.configure(image=imagem_atual_photo)
    label_imagem.image = imagem_atual_photo


global indice_imagem
indice_imagem = 0

# cria uma janela
janela = Tk()
janela.title("Contraste e Zoom")
janela.geometry("800x700")
janela.resizable(False, False)
janela.configure(background="white")


imagens = []
i = 0

for i in range(1,315):
    imagens.append("d_left_cc (" + str(i) + ").png")

indice_imagem_original = 0

# carrega a imagem
imagem_original = Image.open("mamografias\DleftCC\d_left_cc (1).png")
imagem_original_gray = imagem_original.convert('L')  # converte para escala de cinza
imagem_original_resize = imagem_original_gray.resize((300, 400), Image.LANCZOS)
imagem_original_photo = ImageTk.PhotoImage(imagem_original_resize)

imagem_atual_resize = imagem_original_resize
imagem_atual_photo = imagem_original_photo

n_zooms = 0

# Cria um widget Label e exibe a imagem na janela
label_imagem = Label(janela, width=800, height=600)
label_imagem.configure(background="white")
label_imagem.grid(row=0, column=0, padx=10, pady=10)

# Atualizar o Label com a imagem atual
label_imagem.configure(image=imagem_original_photo)
label_imagem.image = imagem_original_photo  # Atualiza a referência da imagem no Label

# Cria um frame para os botões
frame_controles = Frame(janela)
frame_controles.configure(background="white")
frame_controles.grid(row=1, column=0, padx=10, pady=10)

# Cria os controles
botao_selecionar = Button(frame_controles, text="Trocar Imagem", command=abrir_explorador)
botao_selecionar.grid(row=0, column=0, padx=5)

min_slider = Scale(frame_controles, from_=1, to=255, orient='horizontal', label='Valor mínimo')
min_slider.configure(background="white")
min_slider.grid(row=0, column=1, padx=5)

max_slider = Scale(frame_controles, from_=1, to=255, orient='horizontal', label='Valor máximo')
max_slider.configure(background="white")
max_slider.grid(row=0, column=2, padx=5)

botao_janelamento = Button(frame_controles, text="Janelamento", command=update_image_windowing)
botao_janelamento.grid(row=0, column=3, padx=5)

botao_zoom_in = Button(frame_controles, text="Zoom In", command=zoom_in)
botao_zoom_in.grid(row=0, column=4, padx=5)

botao_zoom_out = Button(frame_controles, text="Zoom Out", command=zoom_out)
botao_zoom_out.grid(row=0, column=5, padx=5)

# Configura a coluna 0 do grid para expandir
janela.grid_columnconfigure(0, weight=1)

# Exibe a janela
janela.mainloop()

