def read_file(path):
    ret = ''

    with open(path, 'rt') as fh:
        ret = fh.read()

    return ret

