def eh_labirinto(maze):
    if not type(maze) is tuple:
        return False

    nx, ny = len(maze), 0

    for i in range(nx):
        if not type(maze) is tuple or (ny != len(maze[i]) and i != 0):
            return False
        elif i == 0 or i == nx - 1:
            for el in maze[i]:
                if el != 1:
                    return False
        elif maze[i][0] != 1 or maze[i][-1] != 1:
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
