# 95568, Eduardo Miguel Caetano Espadeiro


def eh_labirinto(tuplo):
    """
    Devolve True se tuplo for um labirinto.
    """
    if not type(tuplo) is tuple:
        return False

    nx, ny = len(tuplo), 0

    for i in range(nx):
        if not type(tuplo[i]) is tuple or (ny != len(tuplo[i]) and i != 0):
            return False

        for j in range(len(tuplo[i])):
            if (tuplo[i][j] != 0 and tuplo[i][j] != 1) \
                        or ((i == 0 or i == nx - 1) and tuplo[i][j] != 1) \
                        or ((j == 0 or j == ny) and tuplo[i][j] != 1):
                return False

        ny = len(tuplo[i])

    return nx >= 3 and ny >= 3


def eh_posicao(pos):
    """
    Devolve True se pos for uma posicao.
    Uma posicao e um tuplo que contem 2 inteiros nao negativos
    """
    return type(pos) is tuple and len(pos) == 2 and pos[0] >= 0 and pos[1] >= 0


def eh_conj_posicoes(conj):
    """Devolve True se conj for um conjunto de posicoes"""
    if not type(conj) is tuple:
        return False

    for el in conj:
        if not eh_posicao(el):
            return False
    return True


def tamanho_labirinto(maze):
    """Devolve um tuplo com as dimensoes do labirinto"""
    if not eh_labirinto(maze):
        raise ValueError("tamanho_labirinto: argumento invalido")
    return (len(maze), len(maze[0]))


def eh_mapa_valido(maze, posicoes):
    """Devolve true se maze e posicoes formarem um mapa valido"""
    if not eh_labirinto(maze) or not eh_conj_posicoes(posicoes):
        raise ValueError("eh_mapa_valido: algum dos argumentos e invalido")

    nx, ny = tamanho_labirinto(maze)
    for pos in posicoes:
        if pos[0] >= nx or pos[0] < 0 or pos[1] >= ny or pos[1] < 0 or maze[pos[0]][pos[1]] == 1:
            return False
    return True


def eh_posicao_livre(maze, posicoes, pos):
    if not eh_mapa_valido(maze, posicoes) or not eh_posicao(pos):
        raise ValueError("eh_posicao_livre: algum dos argumentos e invalido")
    nx, ny = tamanho_labirinto(maze)
    if pos[0] >= nx or pos[0] < 0 or pos[1] >= ny or pos[1] < 0 or maze[pos[0]][pos[1]] == 1:
        return False

    for p in posicoes:
        if p[0] == pos[0] and p[1] == pos[1]:
            return False
    return True


def posicoes_adjacentes(pos):
    """Devolve um tuplo contendo as posicoes adjancentes a pos"""
    if not eh_posicao(pos):
        raise ValueError("posicoes_adjacentes: argumento invalido")

    posicoes = ()
    if pos[1] != 0:
        posicoes = posicoes + ((pos[0], pos[1] - 1),)
    if pos[0] != 0:
        posicoes = posicoes + ((pos[0] - 1, pos[1]),)
    return posicoes + ((pos[0] + 1, pos[1]), (pos[0], pos[1] + 1))


def mapa_str(maze, posicoes):
    """Devolve uma cadeia de carateres com o mapa do labirinto"""
    if not eh_mapa_valido(maze, posicoes):
        raise ValueError("mapa_str: algum dos argumentos e invalido")

    res = ""
    print(maze)
    for y in range(len(maze[0])):
        for x in range(len(maze)):
            if maze[x][y] == 1:
                res = res + "#"
            else:
                unidade = False
                for pos in posicoes:
                    if pos[0] == x and pos[1] == y:
                        res = res + "0"
                        unidade = True
                        break
                if not unidade:
                    res = res + "."
        res = res + "\n"
    return res
