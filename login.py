import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta

def verificar_login():
    usuario = login_entry.get()
    senha = senha_entry.get()

    try:
        banco = sqlite3.connect('banco_cadastro.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dados WHERE login=? AND senha=?", (usuario, senha))
        resultado = cursor.fetchone()

        if resultado:
            data_registro = datetime.strptime(resultado[5], '%d-%m-%Y %H:%M:%S')
            data_limite = data_registro + timedelta(minutes=1)
            if datetime.now() <= data_limite:
                abrir_pagina_entrou()
            else:
                messagebox.showerror("Erro", "Tempo de acesso expirado")
        else:
            messagebox.showerror("Erro", "Credenciais incorretas")

        banco.close()
    except sqlite3.Error as erro:
        print("Erro ao verificar login: ", erro)

def abrir_pagina_entrou():
    nova_janela = tk.Toplevel(root)
    nova_janela.title("Página Entrou")
    label_entrou = tk.Label(nova_janela, text="Entrou")
    label_entrou.pack()

def abrir_tela_registro():
    tela_registro = tk.Toplevel(root)
    tela_registro.title("Registro")

    # Campos de registro
    nome_label = tk.Label(tela_registro, text="Nome:")
    nome_entry = tk.Entry(tela_registro)
    idade_label = tk.Label(tela_registro, text="Idade:")
    idade_entry = tk.Entry(tela_registro)
    email_label = tk.Label(tela_registro, text="E-mail:")
    email_entry = tk.Entry(tela_registro)
    login_label = tk.Label(tela_registro, text="Login:")
    login_entry = tk.Entry(tela_registro)
    senha_label = tk.Label(tela_registro, text="Senha:")
    senha_entry = tk.Entry(tela_registro, show="*")

    # Botão de registrar
    registrar_button = tk.Button(tela_registro, text="Registrar", command=lambda: registrar(nome_entry.get(), idade_entry.get(), email_entry.get(), login_entry.get(), senha_entry.get()))

    # Posicionamento dos widgets do registro
    nome_label.grid(row=0, column=0, sticky="e")
    nome_entry.grid(row=0, column=1)
    idade_label.grid(row=1, column=0, sticky="e")
    idade_entry.grid(row=1, column=1)
    email_label.grid(row=2, column=0, sticky="e")
    email_entry.grid(row=2, column=1)
    login_label.grid(row=3, column=0, sticky="e")
    login_entry.grid(row=3, column=1)
    senha_label.grid(row=4, column=0, sticky="e")
    senha_entry.grid(row=4, column=1)
    registrar_button.grid(row=5, columnspan=2)

def registrar(nome, idade, email, login, senha):
    try:
        banco = sqlite3.connect('banco_cadastro.db')
        cursor = banco.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS dados (nome text, idade integer, email text, login text, senha text, data_hora_registro text)")
        cursor.execute("INSERT INTO dados VALUES (?, ?, ?, ?, ?, ?)", (nome, idade, email, login, senha, datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
        banco.commit()
        banco.close()
        messagebox.showinfo("Sucesso", "Registro realizado com sucesso!")
    except sqlite3.Error as erro:
        messagebox.showerror("Erro", "Erro ao registrar: " + str(erro))

# Configuração da janela principal
root = tk.Tk()
root.title("Login")

# Campos de entrada do login
login_label = tk.Label(root, text="Login:")
login_entry = tk.Entry(root)
senha_label = tk.Label(root, text="Senha:")
senha_entry = tk.Entry(root, show="*")

# Botões entrar e registrar
entrar_button = tk.Button(root, text="Entrar", command=verificar_login)
registrar_button = tk.Button(root, text="Registrar", command=abrir_tela_registro)

# Posicionamento dos widgets do login
login_label.grid(row=0, column=0, sticky="e")
login_entry.grid(row=0, column=1)
senha_label.grid(row=1, column=0, sticky="e")
senha_entry.grid(row=1, column=1)
entrar_button.grid(row=2, column=0)
registrar_button.grid(row=2, column=1)

root.mainloop()
