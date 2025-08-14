import tkinter as tk
from Main_Projeto_TPSI_backend import adicionar_lista

def abrir_registo():
    def guardar():
        campos = {
            "inicio": entry_inicio.get(),
            "fim": entry_fim.get(),
            "autor": entry_autor.get(),
            "titulo": entry_titulo.get(),
            "ano": entry_ano.get(),
            "preco": entry_preco.get(),
            "edicao": entry_edicao.get(),
            "paginas": entry_paginas.get(),
            "tema": entry_tema.get(),
            "avaliacao": entry_avaliacao.get()
        }
        if adicionar_lista(campos):
            for entry in entries:
                entry.delete(0, tk.END)

    janela_registo = tk.Toplevel(root)
    janela_registo.title("Registo de Livros")

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

    global entry_inicio, entry_fim, entry_autor, entry_titulo
    global entry_ano, entry_preco, entry_edicao, entry_paginas
    global entry_tema, entry_avaliacao, entries

    entries = []
    for i, text in enumerate(labels_text):
        tk.Label(janela_registo, text=text).grid(row=i, column=0, sticky="w", padx=5, pady=2)
        entry = tk.Entry(janela_registo)
        entry.grid(row=i, column=1, padx=5, pady=2)
        entries.append(entry)

    (entry_inicio, entry_fim, entry_autor, entry_titulo,
     entry_ano, entry_preco, entry_edicao, entry_paginas,
     entry_tema, entry_avaliacao) = entries

    tk.Button(janela_registo, text="Registar Livro", command=guardar).grid(row=len(labels_text), columnspan=2, pady=10)


root = tk.Tk()
root.geometry("300x200")
root.title("Menu Principal")


tk.Label(root, text="Bem Vindo", font=("Arial", 12)).pack(pady=10)
tk.Button(root, text="Registar Livros", width=20, command=abrir_registo).pack(pady=5)
tk.Button(root, text="Sair", width=20, command=root.quit).pack(pady=5)

root.mainloop()