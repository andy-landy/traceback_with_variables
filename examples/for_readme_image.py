from traceback_with_variables import printing_tb, ColorSchemes


def mean(vs):
    return sum(vs) / sum(1 for v in vs)


def get_avg_ratio(size1, size2):
    return mean([get_ratio(h, w) for h, w in [size1, size2]])


def get_ratio(h, w):
    return h / w


def main():
    sizes_str = '300 200 300 0'
    with printing_tb(color_scheme=ColorSchemes.common):
        h1, w1, h2, w2 = map(int, sizes_str.split())

        return get_avg_ratio((h1, w1), (h2, w2))


try:
    main()

except:
    pass



