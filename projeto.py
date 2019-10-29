# 95568, Eduardo Miguel Caetano Espadeiro


def eh_labirinto(tuplo):
    """
    Devolve True se tuplo for um labirinto.
    Um labirinto e um tuplo que contem nx tuplos, cada um
    contem ny inteiros 0 ou 1.
    """
    if not type(tuplo) is tuple:
        return False

    nx, ny = len(tuplo), 0
    for i in range(nx):
        if not type(tuplo[i]) is tuple or (ny != len(tuplo[i]) and i != 0):
            return False

        for j in range(len(tuplo[i])):
            if type(tuplo[i][j]) is not int \
                    or (tuplo[i][j] != 0 and tuplo[i][j] != 1) \
                    or ((i == 0 or i == nx - 1) and tuplo[i][j] != 1) \
                    or ((j == 0 or j == ny) and tuplo[i][j] != 1):
                return False

        ny = len(tuplo[i])

    return nx >= 3 and ny >= 3


def eh_posicao(tuplo):
    """
    Devolve True se pos for uma posicao.
    Uma posicao e um tuplo que contem 2 inteiros nao negativos
    """
    return \
        type(tuplo) is tuple and len(tuplo) == 2 \
        and tuplo[0] >= 0 and tuplo[1] >= 0 \
        and type(tuplo[0]) is int and type(tuplo[1]) is int


def eh_conj_posicoes(tuplo):
    """
    Devolve True se tuplo for um conjunto de posicoes.
    Um conjunto de posicoes e um tuplo que contem tuplos que verifiquem eh_posicao.
    """
    if not type(tuplo) is tuple:
        return False

    elementos = []
    for el in tuplo:
        if not eh_posicao(el) or el in elementos:
            return False
        elementos.append(el)
    return True


def tamanho_labirinto(labirinto):
    """
    Devolve um tuplo com dois inteiros que correspondem as dimensoes do labirinto
    """
    if not eh_labirinto(labirinto):
        raise ValueError("tamanho_labirinto: argumento invalido")
    return (len(labirinto), len(labirinto[0]))


def eh_mapa_valido(labirinto, unidades):
    """
    Devolve True se labirinto e unidades formam um mapa valido.
    Um mapa e valido se as unidades se encontram dentro do labirinto em
    posicoes que nao estejam ocupadas por paredes.
    """
    if not eh_labirinto(labirinto) or not eh_conj_posicoes(unidades):
        raise ValueError("eh_mapa_valido: algum dos argumentos e invalido")

    nx, ny = tamanho_labirinto(labirinto)
    for pos in unidades:
        if pos[0] >= nx or pos[0] < 0 or pos[1] >= ny \
                or pos[1] < 0 or labirinto[pos[0]][pos[1]] == 1:
            return False
    return True


def eh_posicao_livre(labirinto, unidades, posicao):
    """
    Verifica se a posicao pos nao se encontra ocupada por uma parede ou unidade.
    """
    if not eh_labirinto(labirinto) or not eh_conj_posicoes(unidades) or not eh_posicao(posicao)\
            or not eh_mapa_valido(labirinto, unidades):
        raise ValueError("eh_posicao_livre: algum dos argumentos e invalido")

    nx, ny = tamanho_labirinto(labirinto)
    if posicao[0] >= nx or posicao[0] < 0 or posicao[1] >= ny \
            or posicao[1] < 0 or labirinto[posicao[0]][posicao[1]] == 1:
        return False

    for p in unidades:
        if p[0] == posicao[0] and p[1] == posicao[1]:
            return False
    return True


def posicoes_adjacentes(posicao):
    """
    Devolve um tuplo contendo as posicoes adjancentes a posicao
    """
    if not eh_posicao(posicao):
        raise ValueError("posicoes_adjacentes: argumento invalido")

    posicoes = ()
    if posicao[1] != 0:
        posicoes = posicoes + ((posicao[0], posicao[1] - 1),)
    if posicao[0] != 0:
        posicoes = posicoes + ((posicao[0] - 1, posicao[1]),)
    return posicoes + ((posicao[0] + 1, posicao[1]), (posicao[0], posicao[1] + 1))


def mapa_str(labirinto, unidades):
    """
    Devolve uma cadeia de carateres com o mapa do labirinto
    """
    if not eh_labirinto(labirinto) or not eh_conj_posicoes(unidades) \
            or not eh_mapa_valido(labirinto, unidades):
        raise ValueError("mapa_str: algum dos argumentos e invalido")

    res = ""
    for y in range(len(labirinto[0])):
        for x in range(len(labirinto)):
            if labirinto[x][y] == 1:
                res = res + "#"
            elif not eh_posicao_livre(labirinto, unidades, (x, y)):
                res = res + "O"
            else:
                res = res + "."
        res = res + "\n"
    return res[:-1]


def obter_objetivos(labirinto, unidades, posicao):
    """
    Devolve as posicoes adjancestes as unidades, que sejam
    posicoes livres no labirinto, nao inclui as posicoes adjancentes
    a unidade correspondente a pos.
    """
    if not eh_labirinto(labirinto) or not eh_conj_posicoes(unidades) or not eh_posicao(posicao) \
        or posicao not in unidades or not eh_mapa_valido(labirinto, unidades):
        raise ValueError("obter_objetivos: algum dos argumentos e invalido")
    res = ()
    for unidade in unidades:
        if unidade == posicao:
            continue
        for pos in posicoes_adjacentes(unidade):
            if pos not in res and eh_posicao_livre(labirinto, unidades, pos):
                res = res + (pos,)
    return res


def obter_caminho(labirinto, unidades, posicao):
    """
    Devolve o conjunto de posicoes para resolver o labirinto.
    """
    if not eh_labirinto(labirinto) or not eh_conj_posicoes(unidades) or not eh_posicao(posicao)\
            or posicao not in unidades or not eh_mapa_valido(labirinto, unidades):
        raise ValueError("obter_caminho: algum dos argumentos e invalido")

    fila_exploracao = [(posicao,)]
    visitadas = []
    objetivos = obter_objetivos(labirinto, unidades, posicao)

    while fila_exploracao:
        caminho_atual = fila_exploracao.pop(0)
        posicao_atual = caminho_atual[-1]

        if posicao_atual not in visitadas:
            visitadas.append(posicao_atual)
            if posicao_atual in objetivos:
                return caminho_atual
            for pos in posicoes_adjacentes(posicao_atual):
                if eh_posicao_livre(labirinto, unidades, pos):
                    novo_caminho = caminho_atual + (pos,)
                    fila_exploracao.append(novo_caminho)
    return ()


def mover_unidade(labirinto, unidades, posicao):
    if not eh_labirinto(labirinto) or not eh_conj_posicoes(unidades) or not eh_posicao(posicao) \
            or posicao not in unidades or not eh_mapa_valido(labirinto, unidades):
        raise ValueError("mover_unidade: algum dos argumentos e invalido")

    if len(unidades) > 1:
        caminho = obter_caminho(labirinto, unidades, posicao)
        for i in range(len(unidades)):
            if unidades[i] == posicao:
                return unidades[:i] + (caminho[1],) + unidades[i+1:]

    return unidades
