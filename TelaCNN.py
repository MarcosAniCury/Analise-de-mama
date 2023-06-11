from tkinter import *
import os
from tkinter import ttk

class TelaCNN:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Tela CNN")
        self.janela.geometry("600x500")
        self.janela.resizable(False, False)
        self.janela.configure(background="white")

        self.frame_texto = Frame(self.janela, width=500, height=200)
        self.frame_texto.configure(background="white")
        self.frame_texto.grid(row=1, column=0, pady=10)

        self.label_texto = Label(self.frame_texto, text="", font=("Arial", 14))
        self.label_texto.configure(background="white")
        self.label_texto.grid(row=0, column=0, pady=10)

        self.frame_botoes = Frame(self.janela, width=500, height=100)
        self.frame_botoes.configure(background="white")
        self.frame_botoes.grid(row=0, column=0, pady=10)

        self.botao_binario_nao_segmentado = Button(self.frame_botoes, text="Binário Não Segmentado", command=self.mostrar_texto_binario_nao_segmentado)
        self.botao_binario_nao_segmentado.grid(row=0, column=0, padx=5)

        self.botao_binario_segmentado = Button(self.frame_botoes, text="Binário Segmentado", command=self.mostrar_texto_binario_segmentado)
        self.botao_binario_segmentado.grid(row=0, column=1, padx=5)

        self.botao_multiclasse_nao_segmentado = Button(self.frame_botoes, text="Multiclasse Não Segmentado", command=self.mostrar_texto_multiclasse_nao_segmentado)
        self.botao_multiclasse_nao_segmentado.grid(row=0, column=2, padx=5)

        self.botao_multiclasse_segmentado = Button(self.frame_botoes, text="Multiclasse Segmentado", command=self.mostrar_texto_multiclasse_segmentado)
        self.botao_multiclasse_segmentado.grid(row=0, column=3, padx=5)

        self.frame_botoes.grid_rowconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)
        self.frame_botoes.grid_columnconfigure(2, weight=1)
        self.frame_botoes.grid_columnconfigure(3, weight=1)

        self.frame_switch = Frame(self.janela, width=500, height=50)
        self.frame_switch.configure(background="white")
        self.frame_switch.grid(row=2, column=0, pady=10)

        self.label_switch = Label(self.frame_switch, text="Treinar:", font=("Arial", 14))
        self.label_switch.configure(background="white")
        self.label_switch.grid(row=0, column=0, padx=5, sticky="e")

        self.switch_var = StringVar(value="Não")
        self.switch = ttk.Combobox(self.frame_switch, textvariable=self.switch_var, values=["Não", "Sim"], state="readonly")
        self.switch.grid(row=0, column=1, padx=5, sticky="w")


    def mostrar_texto_binario_nao_segmentado(self):
        texto = self.ler_arquivo("resultados/texto.txt")
        self.label_texto.configure(text=texto)

    def mostrar_texto_binario_segmentado(self):
        texto = self.ler_arquivo("resultados/texto.txt")
        self.label_texto.configure(text=texto)

    def mostrar_texto_multiclasse_nao_segmentado(self):
        texto = self.ler_arquivo("resultados/texto.txt")
        self.label_texto.configure(text=texto)

    def mostrar_texto_multiclasse_segmentado(self):
        texto = self.ler_arquivo("resultados/texto.txt")
        self.label_texto.configure(text=texto)

    def ler_arquivo(self, caminho_arquivo):
        if os.path.isfile(caminho_arquivo):
            with open(caminho_arquivo, 'r') as arquivo:
                return arquivo.read()
        else:
            return ""

janela = Tk()
tela_cnn = TelaCNN(janela)
janela.mainloop()


