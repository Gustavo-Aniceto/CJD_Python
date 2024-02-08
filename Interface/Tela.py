import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class AgendaApp:
    def __init__(self, master):
        self.master = master
        master.title("Agenda")
        master.geometry("500x400")

        self.frame_input = tk.Frame(master, padx=20, pady=10)
        self.frame_input.pack()

        self.label_nome = tk.Label(self.frame_input, text="Nome:", font=("Arial", 12))
        self.label_nome.grid(row=0, column=0, sticky="e")

        self.label_telefone = tk.Label(self.frame_input, text="Telefone:", font=("Arial", 12))
        self.label_telefone.grid(row=1, column=0, sticky="e")

        self.label_email = tk.Label(self.frame_input, text="Email:", font=("Arial", 12))
        self.label_email.grid(row=2, column=0, sticky="e")

        self.entry_nome = tk.Entry(self.frame_input, font=("Arial", 12))
        self.entry_nome.grid(row=0, column=1, padx=10)

        self.entry_telefone = tk.Entry(self.frame_input, font=("Arial", 12))
        self.entry_telefone.grid(row=1, column=1, padx=10)

        self.entry_email = tk.Entry(self.frame_input, font=("Arial", 12))
        self.entry_email.grid(row=2, column=1, padx=10)

        # Frame para os botões de operações
        self.frame_botoes_operacoes = tk.Frame(master)
        self.frame_botoes_operacoes.pack(pady=10)

        self.button_salvar = tk.Button(self.frame_botoes_operacoes, text="Salvar", font=("Arial", 12), command=self.salvar_contato)
        self.button_salvar.grid(row=0, column=0, padx=5)

        self.button_excluir = tk.Button(self.frame_botoes_operacoes, text="Excluir Selecionado", font=("Arial", 12), command=self.confirmar_excluir_contato)
        self.button_excluir.grid(row=0, column=1, padx=5)

        self.button_atualizar = tk.Button(self.frame_botoes_operacoes, text="Atualizar Selecionado", font=("Arial", 12), command=self.atualizar_contato)
        self.button_atualizar.grid(row=0, column=2, padx=5)

        # Frame para os botões de limpar e listar
        self.frame_botoes_limpar_listar = tk.Frame(master)
        self.frame_botoes_limpar_listar.pack(pady=10)

        self.button_limpar = tk.Button(self.frame_botoes_limpar_listar, text="Limpar Campos", font=("Arial", 12), command=self.limpar_campos)
        self.button_limpar.grid(row=0, column=0, padx=5)

        self.button_listar = tk.Button(self.frame_botoes_limpar_listar, text="Listar Contatos", font=("Arial", 12), command=self.listar_contatos)
        self.button_listar.grid(row=0, column=1, padx=5)

        # Frame para a pesquisa
        self.frame_pesquisa = tk.Frame(master)
        self.frame_pesquisa.pack(pady=10)

        self.entry_pesquisa = tk.Entry(self.frame_pesquisa, font=("Arial", 12))
        self.entry_pesquisa.grid(row=0, column=0, padx=5)

        self.button_pesquisar = tk.Button(self.frame_pesquisa, text="Pesquisar", font=("Arial", 12), command=self.pesquisar_contatos)
        self.button_pesquisar.grid(row=0, column=1, padx=5)

        self.tree = ttk.Treeview(master, columns=("ID", "Nome", "Telefone", "Email"), show="headings")
        self.tree.heading('ID', text='ID', command=lambda: self.ordenar_contatos('N_IDCONTATO'))
        self.tree.heading('Nome', text='Nome', command=lambda: self.ordenar_contatos('T_NOMECONTATO'))
        self.tree.heading('Telefone', text='Telefone', command=lambda: self.ordenar_contatos('T_TELEFONECONTATO'))
        self.tree.heading('Email', text='Email', command=lambda: self.ordenar_contatos('T_EMAILCONTATO'))
        self.tree.pack(pady=10)

        self.tree.bind("<ButtonRelease-1>", self.selecionar_contato)

        self.create_db_connection()
        self.listar_contatos()

    def create_db_connection(self):
        self.conn = sqlite3.connect('agenda.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS Contatos
                         (N_IDCONTATO INTEGER PRIMARY KEY AUTOINCREMENT,
                          T_NOMECONTATO TEXT,
                          T_TELEFONECONTATO TEXT,
                          T_EMAILCONTATO TEXT)''')
        self.conn.commit()

    def salvar_contato(self):
        nome = self.entry_nome.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()

        if not nome.strip() or not telefone.strip() or not email.strip():
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        # Validar formato de telefone e email
        if not self.validar_telefone(telefone):
            messagebox.showwarning("Aviso", "Formato de telefone inválido.")
            return

        if not self.validar_email(email):
            messagebox.showwarning("Aviso", "Formato de email inválido.")
            return

        self.c.execute("INSERT INTO Contatos (T_NOMECONTATO, T_TELEFONECONTATO, T_EMAILCONTATO) VALUES (?, ?, ?)",
                       (nome, telefone, email))
        self.conn.commit()

        self.listar_contatos()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Contato salvo com sucesso!")

    def validar_telefone(self, telefone):
        # Adicione sua lógica de validação de telefone aqui
        # Por exemplo, verificando se contém apenas dígitos e tem o formato desejado
        return True

    def validar_email(self, email):
        # Adicione sua lógica de validação de email aqui
        # Por exemplo, usando expressões regulares ou bibliotecas de validação de email
        return True

    def listar_contatos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.c.execute("SELECT * FROM Contatos")
        for row in self.c.fetchall():
            self.tree.insert('', 'end', values=row)

    def confirmar_excluir_contato(self):
        selected_item = self.tree.selection()
        if selected_item:
            confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir o contato selecionado?")
            if confirmar:
                self.excluir_contato()
        else:
            messagebox.showwarning("Aviso", "Selecione um contato para excluir.")

    def excluir_contato(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_contato = self.tree.item(selected_item, 'values')[0]
            self.c.execute("DELETE FROM Contatos WHERE N_IDCONTATO=?", (id_contato,))
            self.conn.commit()
            self.listar_contatos()
            messagebox.showinfo("Sucesso", "Contato excluído com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Selecione um contato para excluir.")

    def atualizar_contato(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_contato = self.tree.item(selected_item, 'values')[0]
            nome = self.entry_nome.get()
            telefone = self.entry_telefone.get()
            email = self.entry_email.get()

            if not nome.strip() or not telefone.strip() or not email.strip():
                messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
                return

            if not self.validar_telefone(telefone):
                messagebox.showwarning("Aviso", "Formato de telefone inválido.")
                return

            if not self.validar_email(email):
                messagebox.showwarning("Aviso", "Formato de email inválido.")
                return

            self.c.execute("UPDATE Contatos SET T_NOMECONTATO=?, T_TELEFONECONTATO=?, T_EMAILCONTATO=? WHERE N_IDCONTATO=?",
                           (nome, telefone, email, id_contato))
            self.conn.commit()
            self.listar_contatos()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Contato atualizado com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Selecione um contato para atualizar.")

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

    def selecionar_contato(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(tk.END, values[1])
            self.entry_telefone.delete(0, tk.END)
            self.entry_telefone.insert(tk.END, values[2])
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(tk.END, values[3])

    def pesquisar_contatos(self):
        termo_pesquisa = self.entry_pesquisa.get()
        self.c.execute("SELECT * FROM Contatos WHERE T_NOMECONTATO LIKE ?", ('%' + termo_pesquisa + '%',))
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.c.fetchall():
            self.tree.insert('', 'end', values=row)

    def ordenar_contatos(self, coluna):
        # Limpa a árvore para reordenar os itens
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.c.execute("SELECT * FROM Contatos ORDER BY {}".format(coluna))
        for row in self.c.fetchall():
            self.tree.insert('', 'end', values=row)

root = tk.Tk()


app = AgendaApp(root)
root.mainloop()
