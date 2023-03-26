from tkinter import *
from PIL import ImageTk, Image

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
imagem_atual = imagem_atual.resize((300, 400), Image.ANTIALIAS)  # redimensiona a imagem para exibir na janela
imagem_atual = ImageTk.PhotoImage(imagem_atual)

# cria um widget Label e exibe a imagem na janela
label_imagem = Label(janela, image=imagem_atual)
label_imagem.pack()

def trocar_imagem():
    global indice_imagem

    # incrementa o índice da imagem
    indice_imagem += 1

    # se o índice da imagem for maior ou igual ao comprimento da lista, volta ao início
    if indice_imagem >= len(imagens):
        indice_imagem = 0

    # atualiza a imagem exibida no Label
    imagem_atual = Image.open("mamografias\DleftCC\\" + imagens[indice_imagem] )
    imagem_atual = imagem_atual.resize((300, 400), Image.LANCZOS)
    imagem_atual = ImageTk.PhotoImage(imagem_atual)
    label_imagem.configure(image=imagem_atual)
    label_imagem.image = imagem_atual

botao = Button(janela, text="Trocar imagem", command=trocar_imagem)
botao.pack()

# inicia o loop principal do Tkinter
janela.mainloop()

