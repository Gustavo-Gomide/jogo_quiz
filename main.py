# 1. Desenvolva um programa em Python para criar uma base de dados com o SQLite e uma tabela com uma chave primária, pelo menos duas colunas obrigatória e pelo menos duas colunas opcionais. 


# 2. Implemente um programa em Python para inserir dados na tabela criada. Insira pelo menos quatro registros na tabela


# 3. Faça um programa em Python para consultar todos os registros inseridos na tabela criada. Mostre os registros na horizontal e depois na vertical. E inclua a mensagem de “Tabela vazia.”

from operator import le
import pathlib
import sqlite3
import os
from random import choice
from time import sleep
from tabulate import tabulate
import re
import pygame

try:

    ###################################################################
    #                             LIMPAR                              #                        
    ###################################################################
    
    # limpar terminal, windows ou (linux/mac)
    def limpar_terminal():
        if os.name == 'nt':
            os.system("cls")
        else:
            os.system("clear")

    ###################################################################
    #                             COLORIR                             #                        
    ###################################################################

    # colorir letras
    def colorir(texto, cor: str = 'vermelho'):
        """
        ***CORES***: **vermelho**, **verde**, **amarelo**, **azul**, **rosa**, **ciano**
        """
        if cor == 'vermelho':
            return  f"\033[31;1m{str(texto)}\033[m"
        elif cor == 'verde':
            return  f"\033[32;1m{str(texto)}\033[m"
        elif cor == 'amarelo':
            return  f"\033[33;1m{str(texto)}\033[m"
        elif cor == 'azul':
            return  f"\033[34;1m{str(texto)}\033[m"
        elif cor == 'rosa':
            return  f"\033[35;1m{str(texto)}\033[m"
        elif cor == 'ciano':
            return  f"\033[36;1m{str(texto)}\033[m"

    ###################################################################
    #                            FORMATAR                             #                        
    ###################################################################
    def linha(simbolo: str = '-', tam: int = 30):
            print(simbolo * tam)


    # design cabecalho pros menus
    def cabecalho(texto: str = 'CABEÇALHO', tam: int = 30):
        print("╔" + "═"*tam + "╗")
        print("║" + f" {texto} ".center(tam) + "║")
        print("╚" + "═"*tam + "╝")

    # area de texto personalizada
    def criar_texto_formatado(titulo, estilo="clássico"):
        """
            ***TIPOS***: clássico, jogo, elegante;
        """
        designs = {
            "clássico": ("┏━┓", "┃ ┃", "┗━┛"),
            "jogo": ("╔═☆╗", "║ »║", "╚═☆╝"),
            "elegante": ("╭─⋆╮", "│ ☆│", "╰─⋆╯")
        }
        topo, meio, baixo = designs.get(estilo, designs["clássico"])
        largura = len(titulo) + 8
        
        print(topo[0] + topo[1] * (largura - 2) + topo[2])
        print(meio[0] + titulo.center(largura - 2) + meio[1])
        print(baixo[0] + baixo[1] * (largura - 2) + baixo[2])

    ###################################################################
    #                             ESCOLHA                             #                        
    ###################################################################

    # escolha pro menu
    def escolha_int(retorno: callable, escolha: str, minimal = 0, maximal = 3) -> int:
        if escolha.isnumeric():
            escolha = int(escolha)
            if minimal <= escolha <= maximal:
                return escolha
        print("Opção invalida!") 
        sleep(1)
        retorno()

    ###################################################################
    #                              SAIR                               #                        
    ###################################################################

    def sair():
        raise KeyboardInterrupt
    
    ###################################################################
    #                              MENU                               #                        
    ###################################################################

    #  menu com funções para serem chamadas
    def criar_menu_funcoes(retorno: callable, opcoes: dict[(str, callable)], text: str = "MENU", exit: bool = True):
        """
        FUNÇÃO "SAIR" ADICIONADA AUTOMATICAMENTE NO FINAL SE *exit* = True!
        """
        linhas = []
        if exit:
            opcoes['SAIR'] = sair
        # lista de opções para serem printadas, ja com cor
        for numero, chave in enumerate(opcoes.keys()):
            if chave.lower() != 'sair':
                linhas.append([f"[ {colorir(numero, 'ciano')} ]", f"{colorir(chave, 'ciano')}"])
            else:
                linhas.append([f"[ {colorir(numero)} ]", f"{colorir(chave)}"])

        # criar tabela e cabeçalho e mostrar
        tabela = tabulate(linhas, headers=['Opção', "Função"], tablefmt="rounded_grid")
        largura = len(tabela.split('\n')[0])  # Detecta a largura da tabela
        cabecalho(text, largura)
        print(tabela)
        # escolha pode ser qualquer numero inteiro menor que numero total de opções - 1 (começa em 1 -> começa em 0 (com -1))
        escolha = str(input("Escolha: "))
        escolha = escolha_int(retorno, escolha, maximal=len(opcoes)-1)
        for numero, valor in enumerate(opcoes.values()):
            if escolha == numero:
                valor()
        

    ###################################################################
    #                         BANCO DE DADOS                          #                        
    ###################################################################

    # caminho da pasta pai desse arquivo (ex01)
    CAMINHO = pathlib.Path(__file__).parent
    database = f'{CAMINHO}/jogo_quiz.db'

    connection = sqlite3.connect(database)
    cursor = connection.cursor()


    ###################################################################
    #                             CREATE                              #                        
    ###################################################################
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS quiz 
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        resposta TEXT NOT NULL, 
                        tipo TEXT NOT NULL, 
                        dica1 TEXT, 
                        dica2 TEXT
                    )
                   """)
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS usuario 
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        nome TEXT NOT NULL, 
                        recorde INTEGER NOT NULL 
                    )
                   """)
    
    # salvar
    connection.commit()


    ###################################################################
    #                             INSERT                              #                        
    ###################################################################

    def inserir_quiz(resposta: str, tipo: str, dica1: str, dica2: str):
        cursor.execute(
            """
                INSERT INTO quiz 
                (resposta, tipo, dica1, dica2)
                VALUES(?, ?, ?, ?)
            """,(resposta, tipo, dica1, dica2)
        )
        # salvar
        connection.commit()

    def inserir_usuario(nome: str, recorde: int = 0):
        cursor.execute(
            """
                INSERT INTO usuario 
                (nome, recorde)
                VALUES(?, ?)
            """,(nome, recorde)
        )
        # salvar
        connection.commit()

    ###################################################################
    #                              READ                               #                        
    ###################################################################

    def consultar_quiz():
        cursor.execute("SELECT * FROM quiz")
        return cursor.fetchall()
    

    def consultar_usuario():
        cursor.execute("SELECT * FROM usuario")
        usuarios = cursor.fetchall()
        return [{"id": row[0], "nome": row[1], "recorde": row[2]} for row in usuarios]
        

    def buscar_usuario(id: int):
        cursor.execute("SELECT * FROM usuario WHERE id = ?", (id,))
        return cursor.fetchone()

    ###################################################################
    #                             UPDATE                              #                        
    ###################################################################

    def atualizar_usuario(recorde, id):
        # recorde não pode diminuir 
        recorde_atual = buscar_usuario(id)[2]
        if recorde > recorde_atual:
            cursor.execute(
                """
                    UPDATE usuario
                    SET recorde = ?
                    WHERE id = ?;
                """,(recorde, id)
            )
            # salvar
            connection.commit()
        print(buscar_usuario(id))
    
    ###################################################################
    #                              JOGO                               #                        
    ###################################################################
    
    def listar_users():
        lista = []
        for usuario in consultar_usuario():
            lista.append([usuario['id'], usuario['nome']])
        print(tabulate(lista, headers=['id', 'nome'], tablefmt="rounded_grid"))


    def jogar():
        # construindo jogo
        limpar_terminal()
        # verrificar se tem jogador cadastrado
        if not consultar_usuario():
            criar_texto_formatado("Sem Usuarios Cadastrados", 'jogo')
            criar_texto_formatado("ENTER PARA CONTINUAR", 'elegante')
            input()
            cadastrar()
        listar_users()
        escolha = str(input("Qual jogador [id]? "))
        usuario = escolha_int(jogar, escolha, maximal=len(consultar_usuario()))
        opcoes = consultar_quiz()
        # verrificar se tem pergunta cadastrada
        if not opcoes:
            limpar_terminal()
            criar_texto_formatado("Sem Perguntas Cadastradas", 'jogo')
            criar_texto_formatado("ENTER PARA CONTINUAR", 'elegante')
            input()
            adicionar_quiz()
        vida = 5
        pontuacao = 0
        prox_level = True
        tam = 30
        # iniciando
        while vida and opcoes:
            limpar_terminal()
            if prox_level:
                # proximo nivel ao acertar ou começar um novo
                opcao = choice(opcoes)
                prox_level = False
            palavra_alvo = re.sub(r"[^\s]", "*", opcao[1])
            tela = []
            tela.append(["Tipo", opcao[2]])
            tela.append(["Dica 1:", opcao[3]])
            tela.append(["Dica 2", opcao[4]])
            tela.append(["Palavra", palavra_alvo])
            print(tabulate(tela, headers=[f'jogador(a): {buscar_usuario(usuario)[1]}', ('❤️' * vida + '💔' * (5 - vida))], tablefmt="rounded_grid"))
            palpite = str(input("Palpite: "))

            # loop do quiz atual ate acabar as vidas ou acertar
            if palpite == opcao[1]:
                pontuacao += 1
                prox_level = True
                opcoes.remove(opcao)
                print("Resposta correta!")
                sons["acerto"].play()
                sleep(1)
                if not opcoes:
                    print("VOCÊ RESPONDEU TODOS")
                    print("PARABENS!!!")
                    sons["venceu"].play()
                    sleep(2)
                continue
            
            print("Resposta errada!")
            sons["erro"].play()
            sleep(1)
            vida -= 1
            if not vida:
                limpar_terminal()
                print("VOCÊ PERDEU")
                sons["perdeu"].play()
                sleep(4)
        if vida:
            pontuacao *= vida
        atualizar_usuario(pontuacao, usuario)
        resultado(usuario, vida, pontuacao)


    def resultado(usuario, vida, pontuação):
        limpar_terminal()
        cabecalho("FIM DO JOGO")
        nome = buscar_usuario(usuario)[1]
        criar_texto_formatado(f"JOGADOR(A): {nome} | VIDAS RESTANTES: {vida} | PONTUAÇÃO: {pontuação}", "jogo")
        criar_texto_formatado("Pressione Enter para voltar!","elegante")
        input()
        main()


    def placar():
        limpar_terminal()
        usuarios = consultar_usuario()
        rank = sorted(usuarios, key=lambda usuario: usuario["recorde"], reverse=True)

        dados = []
        # formatando e colorindo tabela de rank
        for posicao, usuario in enumerate(rank):
            if posicao == 0:
                dados.append([colorir(posicao+1, 'verde'), colorir(usuario["nome"], 'verde'), colorir(usuario["recorde"], 'verde')])
            elif posicao < 3:
                dados.append([colorir(posicao+1, 'amarelo'), colorir(usuario["nome"], 'amarelo'), colorir(usuario["recorde"], 'amarelo')])
            else:
                dados.append([colorir(posicao+1, 'vermelho'), colorir(usuario["nome"], 'vermelho'), colorir(usuario["recorde"], 'vermelho')])

        tabela = tabulate(dados, headers=['Posição', "Nome", "Recorde"], tablefmt="rounded_grid")

        # Adicionando título
        largura = len(tabela.split('\n')[0])  # Detecta a largura da tabela
        cabecalho("RANKING DOS JOGADORES", largura)
        print(tabela)
        criar_texto_formatado("Pressione Enter para voltar!","elegante")
        input()
        main()


    def adicionar_quiz():
        limpar_terminal()
        cabecalho("NOVO QUIZ")
        resposta = str(input("Resposta: ")).strip()
        tipo = str(input("Tipo: ")).strip()
        dica1 = str(input("Dica 1 (enter pra pular): ")).strip()
        dica2 = str(input("Dica 2 (enter pra pular): ")).strip()
        inserir_quiz(resposta, tipo, dica1, dica2)
        criar_texto_formatado("Pressione Enter para voltar!","elegante")
        input()
        main()


    def cadastrar():
        limpar_terminal()
        cabecalho("CADASTRO")
        nome = str(input("Nome: "))
        inserir_usuario(nome)
        print(colorir("CADASTRADO!", 'verde'))
        sleep(0.5)
        main()

    # menu inicial   
    def main():
        limpar_terminal()
        musica_ligada = True
        iniciar_musica(f"{CAMINHO}/musicas/fundo/Galactic_Rap.mp3")
        criar_menu_funcoes(main, {"jogar": jogar,
                                   "placar recordes": placar, 
                                   "adicionar quiz": adicionar_quiz, 
                                   "cadastrar": cadastrar, 
                                   })

    ###################################################################
    #                             MÚSICA                              #                        
    ###################################################################
    pygame.mixer.init()
    sons = {
    'acerto': pygame.mixer.Sound(f"{CAMINHO}/musicas/efeitos/correto.wav"),
    'erro': pygame.mixer.Sound(f"{CAMINHO}/musicas/efeitos/incorreto.wav"),
    'venceu': pygame.mixer.Sound(f"{CAMINHO}/musicas/efeitos/venceu.wav"),
    'perdeu': pygame.mixer.Sound(f"{CAMINHO}/musicas/efeitos/perdeu.wav"),
    'sair': pygame.mixer.Sound(F"{CAMINHO}/musicas/efeitos/sair.wav")
    }

    def iniciar_musica(caminho_musica: str = None, volume: float = 0.5):
        """Inicia a música de fundo em loop"""
        if caminho_musica:
            pygame.mixer.music.load(caminho_musica)
        else:
            # Você pode adicionar uma música padrão aqui ou deixar None
            pass
        
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)  # -1 faz loop infinito


    def parar_musica():
        """Para a música de fundo"""
        pygame.mixer.music.stop()

    
    def tocar_efeito_sonoro(caminho_som: str, volume: float = 0.7):
        """Toca um efeito sonoro sem interromper a música de fundo"""
        canal_efeitos = pygame.mixer.Channel(1)  # Canal 1 para efeitos (canal 0 é para música)
        try:
            som = pygame.mixer.Sound(caminho_som)
            som.set_volume(volume)
            canal_efeitos.play(som)
        except:
            print(f"Erro ao carregar efeito sonoro: {caminho_som}")


    # inicio
    if __name__ == "__main__":
        main()

except KeyboardInterrupt:
    limpar_terminal()
    print(colorir("Até a próxima","rosa"))

finally:
    parar_musica()
    sons['sair'].play()
    sleep(1)
    cursor.close()
    connection.close()