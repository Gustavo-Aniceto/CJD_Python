import sqlite3
import os

# criar conexão
def conexaoBanco():
    caminho = "C:\\Users\\guuha\\PycharmProjects\\CJD_Python\\Banco\\agenda.db"
    con = None
    try:
        con = sqlite3.connect(caminho)
        cursor = con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS tb_contatos (N_IDCONTATO INTEGER PRIMARY KEY AUTOINCREMENT, T_NOMECONTATO TEXT (30), T_TELEFONECONTATO TEXT (14), T_EMAILCONTATO TEXT (30))")
        con.commit()
    except sqlite3.Error as ex:
        print(ex)
    return con

def menuPrincipal():
    os.system("cls")
    print("--------------------------------------------------")
    print("1- Inserir Novo Registro")
    print("2- Deletar Registro")
    print("3- Atualizar Registro")
    print("4- Consultar Registro por ID")
    print("5- Consultar Registro por nome")
    print("6- Listar Todos os Contatos")
    print("7- Sair")

def menuConsultarId():
    con = conexaoBanco()
    cursor = con.cursor()
    try:
        id_contato = int(input("Digite o ID do contato: "))
        cursor.execute(f"SELECT * FROM tb_contatos WHERE N_IDCONTATO={id_contato}")
        registro = cursor.fetchone()
        if registro:
            print("--------------------------------------------------")
            print(registro)
        else:
            print("--------------------------------------------------")
            print("Contato não encontrado.")
    except ValueError:
        print("ID inválido.")
    finally:
        cursor.close()
        con.close()

def menuConsultarNome():
    con = conexaoBanco()
    cursor = con.cursor()
    try:
        nome_contato = input("Digite o nome do contato: ")
        cursor.execute(f"SELECT * FROM tb_contatos WHERE T_NOMECONTATO LIKE '%{nome_contato}%'")
        registros = cursor.fetchall()
        if registros:
            for registro in registros:
                print("--------------------------------------------------")
                print(registro)
        else:
            print("--------------------------------------------------")
            print("Nenhum contato encontrado.")
    finally:
        cursor.close()
        con.close()

def menuListarContatos():
    con = conexaoBanco()
    cursor = con.cursor()
    try:
        cursor.execute("SELECT * FROM tb_contatos")
        registros = cursor.fetchall()
        if registros:
            for registro in registros:
                print("--------------------------------------------------")
                print(registro)
        else:
            print("--------------------------------------------------")
            print("Nenhum contato registrado.")
    finally:
        cursor.close()
        con.close()

def menuAtualizar():
    con = conexaoBanco()
    cursor = con.cursor()
    try:
        id_contato = int(input("Digite o ID do contato a ser atualizado: "))
        novo_nome = input("Digite o novo nome: ")
        novo_telefone = input("Digite o novo telefone: ")
        novo_email = input("Digite o novo email: ")
        cursor.execute(f"UPDATE tb_contatos SET T_NOMECONTATO=?, T_TELEFONECONTATO=?, T_EMAILCONTATO=? WHERE N_IDCONTATO=?", (novo_nome, novo_telefone, novo_email, id_contato))
        con.commit()
        print("Contato atualizado com sucesso.")
        print("--------------------------------------------------")
    except ValueError:
        print("ID inválido.")
        print("--------------------------------------------------")
    finally:
        cursor.close()
        con.close()

def menuInserir():
    con = conexaoBanco()
    cursor = con.cursor()
    try:
        nome = input("Digite o nome do novo contato: ")
        telefone = input("Digite o telefone do novo contato: ")
        email = input("Digite o email do novo contato: ")
        cursor.execute("INSERT INTO tb_contatos (T_NOMECONTATO, T_TELEFONECONTATO, T_EMAILCONTATO) VALUES (?, ?, ?)", (nome, telefone, email))
        con.commit()
        print("Contato inserido com sucesso.")
        print("--------------------------------------------------")

    finally:
        cursor.close()
        con.close()

def menuDeletar():
    con = conexaoBanco()
    cursor = con.cursor()
    try:
        id_contato = int(input("Digite o ID do contato a ser deletado: "))
        cursor.execute(f"DELETE FROM tb_contatos WHERE N_IDCONTATO={id_contato}")
        con.commit()
        print("Contato deletado com sucesso.")
        print("--------------------------------------------------")

    except ValueError:
        print("ID inválido.")
    finally:
        cursor.close()
        con.close()

opc = 0
while opc != 7:
    menuPrincipal()
    opc = int(input("Digite uma opção: "))
    if opc == 1:
        menuInserir()
    elif opc == 2:
        menuDeletar()
    elif opc == 3:
        menuAtualizar()
    elif opc == 4:
        menuConsultarId()
    elif opc == 5:
        menuConsultarNome()
    elif opc == 6:
        menuListarContatos()
    elif opc == 7:
        os.system("cls")
        print("Programa finalizado.")
    else:
        os.system("cls")
        print("Opção inválida.")
        os.system("pause")
