# Aprender mais sobre a fila (Queue)


def gerador_num_binario(n):
    res = [""]
    for _ in range(n):
        x = res.pop()
        res.append(x + "0")
        res.append(x + "1")
    return res
