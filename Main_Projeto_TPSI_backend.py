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

def adicionar_lista(campos):
    try:
        inicio_d = campos["inicio"].strip()
        if inicio_d:
            data_i = datetime.strptime(inicio_d, "%d/%m/%Y")
        else:
            data_i = "Por ler"

        fim_d = campos["fim"].strip()
        if fim_d:
            data_f = datetime.strptime(fim_d, "%d/%m/%Y")
        elif data_i == "Por ler":
            data_f = "Por ler"
        else:
            data_f = "Em Leitura"

        data_r = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        autor_r = campos["autor"].strip()
        titulo_r = campos["titulo"].strip()
        ano_p_r = datetime.strptime(campos["ano"].strip(), "%Y")
        preco_r = float(campos["preco"].strip())
        edicao_r = int(campos["edicao"].strip())
        paginas_r = int(campos["paginas"].strip())
        tema_r = campos["tema"].strip()
        avaliacao_r = float(campos["avaliacao"].strip())

        if not (0 <= avaliacao_r <= 5):
            messagebox.showerror("Erro", "A avaliação deve estar entre 0 e 5.")
            return False

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
        return True
        
    except ValueError:
        messagebox.showerror("Erro! Formato dos valores errado!")
        return False





