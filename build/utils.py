import os
import re
import pandas
import settings
import datetime


def read_file(path):
    ret = ''

    with open(path, 'rt') as fh:
        ret = fh.read()

    return ret

def extrapolate_md(path):
    '''return the content of the md file
    some variables like =now are extrapolated first
    then saved
    '''

    ret0 = read_file(path)

    now_value = '={}'.format(datetime.datetime.utcnow().isoformat())
    ret = re.sub(r'=now\b', now_value, ret0)

    if ret != ret0:
        with open(path, 'wt') as fh:
            fh.write(ret)

    return ret

def get_file_time(path):
    ret = 0

    if os.path.exists(path):
        ret = os.path.getmtime(path)

    return ret


def extract_context(main):
    context = {}

    def sub_var(match):
        val = match.group(2).strip()
        context[match.group(1)] = val

        return ''

    main = re.sub(r'(?m)^(\w+)=(.*)$', sub_var, main)

    process_context(context)

    return main, context


def process_context(context):
    for k in list(context.keys()):
        if k.startswith('csv_'):
            k2 = k[4:]
            context[k2] = pandas.read_csv(os.path.join(settings.PATH_DATA, context[k]))
        if re.match(r'^\d{4}-\d\d-\d\dT\d\d:.*$', context[k]):
            context[k] = datetime.datetime.fromisoformat(context[k])
