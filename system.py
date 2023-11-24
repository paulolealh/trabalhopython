import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def adicionar():
    valor_input = valor.get()
    is_negative = False

    if str(valor_input).__contains__("-"):
        is_negative = True
        valor_input = str(valor_input).replace("-", "")
    
    try:
        valor_input = float(valor_input)
    except:
        messagebox.showerror("Erro", "Insira um número válido para o valor.")
        return

    if is_negative:
        valor_input = "-" + str(valor_input)

    conn = sqlite3.connect('orcamento.db')
    c = conn.cursor()
    c.execute('INSERT INTO Despesas (categoria, descricao, valor, data) VALUES (?, ?, ?, ?)',
              (categoria.get(), descricao.get(), valor_input, data.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Despesa adicionada com sucesso!")
    listar()
    atualizar_saldo()


def abrir_janela_edicao(id_despesa, categoria_val, descricao_val, valor_val, data_val):
    janela_edicao = tk.Toplevel(root)
    janela_edicao.title("Editar Despesa")

    labels = ['Categoria', 'Descrição', 'Valor', 'Data']
    campos = {}
    for i, label in enumerate(labels):
        tk.Label(janela_edicao, text=label).grid(row=i, column=0)
        campo = tk.Entry(janela_edicao)
        campo.grid(row=i, column=1)
        campos[label] = campo

    campos['Categoria'].insert(0, categoria_val)
    campos['Descrição'].insert(0, descricao_val)
    campos['Valor'].insert(0, valor_val)
    campos['Data'].insert(0, data_val)

    def confirmar_edicao():
        atualizar(id_despesa, campos['Categoria'].get(), campos['Descrição'].get(), 
                  campos['Valor'].get(), campos['Data'].get())
        janela_edicao.destroy()

    btn_confirmar = tk.Button(janela_edicao, text="Confirmar Edição", command=confirmar_edicao)
    btn_confirmar.grid(row=5, column=0, columnspan=2)

def atualizar(id_despesa, cat, desc, val, dat):
    conn = sqlite3.connect('orcamento.db')
    c = conn.cursor()
    c.execute('''UPDATE Despesas SET categoria=?, descricao=?, valor=?, data=? 
                 WHERE id=?''', (cat, desc, val, dat, id_despesa))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Despesa atualizada com sucesso!")
    listar()
    atualizar_saldo()


def solicitar_atualizacao():
    selected_item = tabela.focus()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione uma despesa para atualizar.")
        return
    despesa = tabela.item(selected_item, 'values')
    abrir_janela_edicao(*despesa)

def deletar():
    selected_item = tabela.focus()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione uma despesa para deletar.")
        return
    despesa = tabela.item(selected_item, 'values')
    id_despesa = despesa[0]

    conn = sqlite3.connect('orcamento.db')
    c = conn.cursor()
    c.execute('DELETE FROM Despesas WHERE id=?', (id_despesa,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Despesa deletada com sucesso!")
    listar()
    atualizar_saldo()

def listar():
    for i in tabela.get_children():
        tabela.delete(i)
    conn = sqlite3.connect('orcamento.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Despesas')
    rows = c.fetchall()
    for row in rows:
        color = 'positive' if float(row[3]) >= 0 else 'negative'
        tabela.insert('', 'end', values=row, tags=(color,))
    conn.close()

    tabela.tag_configure('positive', foreground='green')
    tabela.tag_configure('negative', foreground='red')
    atualizar_saldo()

def calcular_saldo():
    conn = sqlite3.connect('orcamento.db')
    c = conn.cursor()
    c.execute('SELECT SUM(valor) FROM Despesas')
    saldo = c.fetchone()[0]
    conn.close()
    return saldo if saldo is not None else 0.0

def atualizar_saldo():
    saldo = calcular_saldo()
    label_saldo.config(text=f'Saldo Total: R$ {saldo:.2f}')

root = tk.Tk()
root.title("Controle de Orçamento Pessoal")
root.geometry("1050x500")
root.resizable(False, False)

estilo = ttk.Style()
estilo.configure("TButton", font=('Sans', '10', 'bold'))
estilo.configure("TLabel", font=('Sans', '10'))
estilo.configure("TEntry", font=('Sans', '10'))

frame_entradas = tk.Frame(root)
frame_botoes = tk.Frame(root)
frame_tabela = tk.Frame(root)

frame_entradas.grid(row=0, column=0, padx=10, pady=10)
frame_botoes.grid(row=1, column=0, padx=10, pady=10)
frame_tabela.grid(row=2, column=0, padx=10, pady=10)

labels = ['Categoria', 'Descrição', 'Valor', 'Data']


categoria = tk.Entry(frame_entradas)
descricao = tk.Entry(frame_entradas)
valor = tk.Entry(frame_entradas)
data = tk.Entry(frame_entradas)
entradas = [categoria, descricao, valor, data]
for i, label in enumerate(labels):
    tk.Label(frame_entradas, text=label).grid(row=i, column=0)
    entradas[i].grid(row=i, column=1)

btn_adicionar = ttk.Button(frame_botoes, text="Adicionar", command=lambda: adicionar())
btn_atualizar = ttk.Button(frame_botoes, text="Editar", command=lambda: solicitar_atualizacao())
btn_deletar = ttk.Button(frame_botoes, text="Deletar", command=lambda: deletar())
btn_listar = ttk.Button(frame_botoes, text="Recarregar", command=lambda: listar())
btns = [btn_adicionar, btn_atualizar, btn_deletar, btn_listar]
for i, btn in enumerate(btns):
    btn.grid(row=0, column=i, padx=5)

tabela = ttk.Treeview(frame_tabela, columns=(1, 2, 3, 4, 5), show="headings", height="5")
tabela.grid(row=0, column=0, columnspan=2)
colunas = ['ID', 'Categoria', 'Descrição', 'Valor', 'Data']
for i, col in enumerate(colunas):
    tabela.heading(i+1, text=col)
    tabela.column(i+1, anchor='center') 

for i, label in enumerate(labels):
    tk.Label(frame_entradas, text=label).grid(row=i, column=0, pady=5, padx=5)
    entradas[i].grid(row=i, column=1, pady=5, padx=5)

for i, btn in enumerate(btns):
    btn.grid(row=0, column=i, padx=5, pady=5)

label_saldo = tk.Label(frame_botoes, text='Saldo Total: R$ 0.00', font=('Sans', '10', 'bold'))
label_saldo.grid(row=1, column=0, columnspan=len(btns), pady=10)
    
listar()
root.mainloop()