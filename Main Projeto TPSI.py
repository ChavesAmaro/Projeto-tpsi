import tkinter as tk
from datetime import datetime
from tkinter import messagebox


data_inicio = []
data_final = []
data_registo = []
autor = []
titulo = []
ano_publicacao = []
edicao = []
paginas = []
preco = []
tema_principal = []
avaliacao = []

def adicionar_lista():
    try:
        inicio_d = entry_inicio.get().strip()
        if inicio_d:
            data_i = datetime.strptime(inicio_d, "%d/%m/%Y")
        else:
            data_i = "Por ler"

        fim_d = entry_fim.get().strip()
        if fim_d:
            data_f = datetime.strptime(fim_d, "%d/%m/%Y")
        elif data_i == "Por ler":
            data_f = "Por ler"
        else:
            data_f = "Em Leitura"

        data_r = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        autor_r = entry_autor.get().strip()
        titulo_r = entry_titulo.get().strip()
        ano_p_r = datetime.strptime(entry_ano.get().strip(), "%Y")
        preco_r = float(entry_preco.get().strip())
        edicao_r = int(entry_edicao.get().strip())
        paginas_r = int(entry_paginas.get().strip())
        tema_r = entry_tema.get().strip()
        avaliacao_r = float(entry_avaliacao.get().strip())

        if not (0 <= avaliacao_r <= 5):
            messagebox.showerror("Erro", "A avaliação deve estar entre 0 e 5.")
            return

        data_inicio.append(data_i)
        data_final.append(data_f)
        data_registo.append(data_r)
        autor.append(autor_r)
        titulo.append(titulo_r)
        ano_publicacao.append(ano_p_r)
        preco.append(preco_r)
        edicao.append(edicao_r)
        paginas.append(paginas_r)
        tema_principal.append(tema_r)
        avaliacao.append(avaliacao_r)
        
        
        messagebox.showinfo("Livro registado com sucesso!")
        
        for entry in entries:
            entry.delete(0, tk.END)
        
    except ValueError:
        messagebox.showerror("Erro! Formato dos valores errado!")
    
root = tk.Tk()
root.title("Registo de Livros")


labels_text = [
    "Data início (DD/MM/YYYY):",
    "Data fim (DD/MM/YYYY):",
    "Autor:",
    "Título:",
    "Ano de publicação (YYYY):",
    "Preço:",
    "Edição:",
    "Nº de páginas:",
    "Tema principal:",
    "Avaliação (0-5):"
]

entries = []

for i, text in enumerate(labels_text):
    tk.Label(root, text=text).grid(row=i, column=0, sticky="w", padx=5, pady=2)
    entry = tk.Entry(root)
    entry.grid(row=i, column=1, padx=5, pady=2)
    entries.append(entry)

(entry_inicio, entry_fim, entry_autor, entry_titulo,
entry_ano, entry_preco, entry_edicao, entry_paginas,
entry_tema, entry_avaliacao) = entries


tk.Button(root, text="Registar Livro", command=adicionar_lista).grid(row=len(labels_text), columnspan=2, pady=10)

root.mainloop()



