def eh_labirinto(maze):
    if not type(maze) is tuple:
        return False

    nx, ny = len(maze), 0

    for i in range(nx):
        if not type(maze) is tuple or (ny != len(maze[i]) and i != 0):
            return False

        for j in range(len(maze[i])):
            if maze[i][j] != 0 and maze[i][j] != 1:
                return False
            elif (i == 0 or i == nx - 1) and maze[i][j] != 1:
                return False
            elif (j == 0 or j == ny) and maze[i][j] != 1:
                return False

        ny = len(maze[i])

    return nx >= 3 and ny >= 3


def eh_posicao(pos):
    return type(pos) is tuple and len(pos) == 2 and pos[0] >= 0 and pos[1] >= 0


def eh_conj_posicoes(conj):
    if not type(conj) is tuple:
        return False

    for el in conj:
        if not eh_posicao(el):
            return False
    return True


def tamanho_labirinto(maze):
    if not eh_labirinto(maze):
        raise ValueError("tamanho_labirinto: argumento invalido")
    return (len(maze), len(maze[0]))


def eh_mapa_valido(maze, posicoes):
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
    if not eh_posicao(pos):
        raise ValueError("posicoes_adjacentes: argumento invalido")
    x, y = pos
    posicoes = ()
    if y != 0:
        posicoes = posicoes + ((x, y - 1),)
    if x != 0:
        posicoes = posicoes + ((x - 1, y),)
    return posicoes + ((x + 1, y), (x, y + 1))


def mapa_str(maze, posicoes):
    if not eh_mapa_valido(maze, posicoes):
        raise ValueError("mapa_str: algum dos argumentos e invalido")
    res = ""
    for x in range(len(maze)):
        for y in range(len(maze[x])):
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

