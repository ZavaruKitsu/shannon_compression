def get_binary_repr(base):
    res = '0.'
    for _ in range(30):
        base *= 2
        res += str(int(base // 1))
        base %= 1

    return res
