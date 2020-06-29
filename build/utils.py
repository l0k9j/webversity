import os
import re
import pandas
import settings


def read_file(path):
    ret = ''

    with open(path, 'rt') as fh:
        ret = fh.read()

    return ret


def get_file_time(path):
    ret = 0

    if os.path.exists(path):
        ret = os.path.getmtime(path)

    return ret


def extract_context(main):
    context = {}

    def sub_var(match):
        context[match.group(1)] = match.group(2)
        return ''

    main = re.sub(r'(?m)^(\w+)=(.*)$', sub_var, main)

    process_context(context)

    return main, context


def process_context(context):
    for k in list(context.keys()):
        if k.startswith('csv_'):
            k2 = k[4:]
            context[k2] = pandas.read_csv(os.path.join(settings.PATH_DATA, context[k]))
