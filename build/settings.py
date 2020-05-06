import os
PATH_SETTINGS = os.path.dirname(__file__)

def resolve_path(path, make=False):
    global PATH_SETTINGS
    ret = path
    if not os.path.isabs(path):
        ret = os.path.join(PATH_SETTINGS, path)
    ret = os.path.realpath(ret)

    if make:
        os.makedirs(ret, exist_ok=True)

    return ret

PATH_MD = '../content/p/'
PATH_MD = resolve_path(PATH_MD)
PATH_HTML = '../p/'
PATH_HTML = resolve_path(PATH_HTML, True)
PATH_TEMPLATES = '../content/templates/'
PATH_TEMPLATES = resolve_path(PATH_TEMPLATES)

NAVIGATION = [
    'home', 'issues', 'framework', 'actions', 'network', 'about', 
]
