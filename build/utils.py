import os
import re
import pandas
import settings
import datetime


def read_file(path):
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


def get_rel_nav_path(item, relative):
    ret = os.path.relpath(
        os.path.join(
            settings.PATH_HTML, item
        ),
        os.path.dirname(relative)
    ).replace(r'\\', '/')

    disk_path = os.path.join(settings.PATH_MD, item)
    if os.path.exists(disk_path) and os.path.isdir(disk_path):
        ret += '/'

    return ret


def process_context(context):
    for k in list(context.keys()):
        if k.startswith('csv_'):
            k2 = k[4:]
            df = pandas.read_csv(os.path.join(settings.PATH_DATA, context[k]))
            # remove empty rows
            df.dropna(how='all', inplace=True)
            df.fillna('', inplace=True)
            context[k2] = df
        if re.match(r'^\d{4}-\d\d-\d\dT\d\d:.*$', context[k]):
            context[k] = datetime.datetime.fromisoformat(context[k])


def get_title_from_filepath(filepath):
    ret = os.path.basename(filepath)
    if ret.startswith('index.'):
        ret = os.path.basename(os.path.dirname(filepath))
    ret = re.sub(r'\.[^.]*', '', ret)
    ret = re.sub(r'[-_]', ' ', ret)
    ret = ret.title()

    return ret


def are_sources_older_than_target(md_path, target_path):
    md_time = get_file_time(md_path)
    target_time = get_file_time(target_path)

    if md_time > target_time:
        return False

    # now compare dependent resources (e.g. csv)
    content = read_file(md_path)
    for match in re.findall(r'(?m)^(\w+)=(.*)$', content):
        if match[0].startswith('csv_'):
            path = os.path.join(settings.PATH_DATA, match[1].strip())
            if get_file_time(path) > target_time:
                return False

    return True
