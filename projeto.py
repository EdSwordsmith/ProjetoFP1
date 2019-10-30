# 95568, Eduardo Miguel Caetano Espadeiro


def eh_labirinto(tuplo):
    """
    Devolve True se tuplo for um labirinto.
    Um labirinto e um tuplo que contem nx tuplos,
    cada um contem ny inteiros 1 ou 0.
    """
    if not type(tuplo) is tuple or len(tuplo) < 3 or len(tuplo[0]) < 3:
        return False

    nx, ny = len(tuplo), len(tuplo[0])
    for i in range(nx):
        if type(tuplo[i]) is not tuple or len(tuplo[i]) != ny:
            return False

        for j in range(len(tuplo[i])):
            if type(tuplo[i][j]) is not int \
                    or (tuplo[i][j] != 0 and tuplo[i][j] != 1) \
                    or ((i == 0 or i == nx - 1) and tuplo[i][j] != 1) \
                    or ((j == 0 or j == ny) and tuplo[i][j] != 1):
                return False
    return True


def eh_posicao(tuplo):
    """
    Devolve True se tuplo for uma posicao.
    Uma posicao e um tuplo que contem 2 inteiros nao negativos.
    """
    return type(tuplo) is tuple and len(tuplo) == 2 \
        and type(tuplo[0]) is int and type(tuplo[1]) is int \
        and tuplo[0] >= 0 and tuplo[1] >= 0


def eh_conj_posicoes(tuplo):
    """
    Devolve True se tuplo for um conjunto de posicoes.
    Um conjunto de posicoes e um tuplo que contem tuplos que verifiquem eh_posicao.
    """
    if type(tuplo) is not tuple:
        return False

    elementos = ()
    for el in tuplo:
        if not eh_posicao(el) or el in elementos:
            return False
        elementos = elementos + (el,)
    return True


def tamanho_labirinto(labirinto):
    """
    Devolve um tuplo com dois inteiros que correspondem as dimensoes do labirinto
    """
    if not eh_labirinto(labirinto):
        raise ValueError("tamanho_labirinto: argumento invalido")
    return (len(labirinto), len(labirinto[0]))


def eh_posicao_valida(labirinto, posicao):
    """
    Devolve True se posicao se encontrar dentro do labirinto
    e nao existir paredes nessa posicao.
    """
    nx, ny = tamanho_labirinto(labirinto)
    x, y = posicao
    return 0 <= x < nx and 0 <= y <= ny and labirinto[x][y] == 0


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
        if not eh_posicao_valida(labirinto, pos):
            return False
    return True


def eh_posicao_livre(labirinto, unidades, posicao):
    """
    Verifica se a posicao pos nao se encontra ocupada por uma parede ou unidade.
    """
    if not eh_labirinto(labirinto) or not eh_conj_posicoes(unidades) or not eh_posicao(posicao)\
            or not eh_mapa_valido(labirinto, unidades):
        raise ValueError("eh_posicao_livre: algum dos argumentos e invalido")

    if not eh_posicao_valida(labirinto, posicao):
        return False

    return posicao not in unidades


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
            elif (x, y) in unidades:
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

    # Verificar se a posicao inicial se encontra numa posicao adjacente a alguma unidade
    for unidade in unidades:
        if posicao in posicoes_adjacentes(unidade):
            return (posicao,)

    # Algoritmo BFS
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
    """
    Devolve um conjunto de posicoes correspondente as unidades depois de
    realizado um movimento sobre uma das unidades.
    """
    if not eh_labirinto(labirinto) or not eh_conj_posicoes(unidades) or not eh_posicao(posicao) \
            or posicao not in unidades or not eh_mapa_valido(labirinto, unidades):
        raise ValueError("mover_unidade: algum dos argumentos e invalido")

    caminho = obter_caminho(labirinto, unidades, posicao)

    if len(caminho) > 1:
        for i in range(len(unidades)):
            if unidades[i] == posicao:
                return unidades[:i] + (caminho[1],) + unidades[i+1:]

    return unidades
