import os
import random
from colorama import Fore

def inicializarJogo():
    global jogadas, quemJoga, vit, maxJogadas, velha
    jogadas = 0
    quemJoga = 2
    maxJogadas = 9
    vit = "n"
    velha = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]

def tela():
    global velha, jogadas
    os.system("cls" if os.name == "nt" else "clear")
    print("   0   1   2")
    print("0:  " + velha[0][0] + " | " + velha[0][1] + " | " + velha[0][2])
    print("   -----------")
    print("1:  " + velha[1][0] + " | " + velha[1][1] + " | " + velha[1][2])
    print("   -----------")
    print("2:  " + velha[2][0] + " | " + velha[2][1] + " | " + velha[2][2])
    print("Jogadas: " + Fore.GREEN + str(jogadas) + Fore.RESET)

def jogadorJoga():
    global jogadas, quemJoga
    try:
        if quemJoga == 1 and jogadas < maxJogadas:
            l = int(input("Linha: "))
            c = int(input("Coluna: "))
            while velha[l][c] != " ":
                l = int(input("Linha: "))
                c = int(input("Coluna: "))
            velha[l][c] = "X"
            quemJoga = 2
            jogadas += 1
    except (ValueError, IndexError):
        print('Linha e/ou coluna inválida')

def cpuJoga():
    global jogadas, quemJoga
    if quemJoga == 2 and jogadas < maxJogadas:
        l = random.randrange(0, 3)
        c = random.randrange(0, 3)
        while velha[l][c] != " ":
            l = random.randrange(0, 3)
            c = random.randrange(0, 3)
        velha[l][c] = "O"
        jogadas += 1
        quemJoga = 1

def verificarVitoria():
    global velha, vit
    simbolos = ["X", "O"]
    for s in simbolos:
        # Verificação de linhas e colunas
        for i in range(3):
            if (velha[i][0] == velha[i][1] == velha[i][2] == s) or (velha[0][i] == velha[1][i] == velha[2][i] == s):
                vit = s
                return
        # Verificação de diagonais
        if (velha[0][0] == velha[1][1] == velha[2][2] == s) or (velha[0][2] == velha[1][1] == velha[2][0] == s):
            vit = s
            return

def verificarEmpate():
    global jogadas, maxJogadas, vit
    if jogadas == maxJogadas and vit == "n":
        vit = "E"

def jogarNovamente():
    global jogarNovamente
    jogarNovamente = input("Deseja jogar novamente? (s/n): ").lower()

while True:
    inicializarJogo()
    while True:
        tela()
        jogadorJoga()
        verificarVitoria()
        verificarEmpate()
        if vit != "n":
            break
        cpuJoga()
        verificarVitoria()
        verificarEmpate()
        if vit != "n":
            break

    tela()
    if vit == "E":
        print("Empate!")
    else:
        print("Vitória do jogador:", vit)

    jogarNovamente()
    if jogarNovamente != "s":
        break
