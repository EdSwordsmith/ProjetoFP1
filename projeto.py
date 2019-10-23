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
