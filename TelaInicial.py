from tkinter import *
import subprocess

def contraste_zoom():
    # Função a ser executada quando o botão "Contraste e Zoom" for clicado
    window.grab_set()  # Desabilitar a interação com a janela principal
    subprocess.Popen(["python", "TelaContrasteZoom.py"])
    window.wait_window()  # Aguardar até que a nova janela seja fechada
    window.grab_release()  # Reativar a interação com a janela principal

def cnn():
    # Função a ser executada quando o botão "Contraste e Zoom" for clicado
    window.grab_set()  # Desabilitar a interação com a janela principal
    subprocess.Popen(["python", "TelaCNN.py"])
    window.wait_window()  # Aguardar até que a nova janela seja fechada
    window.grab_release()  # Reativar a interação com a janela principal

# Criação da janela principal
window = Tk()

# Configuração da janela
window.title("Processamento e Análise de Mama")
window.geometry("500x300")
window.resizable(False, False)
window.configure(background="white")

# Criação do título centralizado
titulo = Label(window, text="Processamento e Análise de Mama", font=("Helvetica", 20, "bold"))
titulo.grid(row=0, column=0, columnspan=3, pady=20)
titulo.configure(background="white")

# Criação dos botões
btn_contraste_zoom = Button(window, text="Contraste e Zoom", command=contraste_zoom, height=2, font=("Helvetica", 14))
btn_contraste_zoom.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")
btn_cnn = Button(window, text="CNN", command=cnn, height=2, font=("Helvetica", 14))
btn_cnn.grid(row=1, column=2, padx=(10, 20), pady=10, sticky="ew")

# Criação do footer
footer = Label(window, text="", font=("Helvetica", 12))
footer.grid(row=2, column=0, columnspan=3, pady=20)

# Configurar o alinhamento dos itens na grade
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

# Iniciar o loop principal da janela
window.mainloop()
