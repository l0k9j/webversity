import settings
import os
import markdown
import utils
import re
import sys
from jinja2 import Template


class SiteBuilder:

    def __init__(self):
        self.finc = 0

    def process(self, action=None):
        show_help = True

        if action:
            method = getattr(self, 'action_'+action, None)
            if method:
                show_help = False
                method()
                print('done')

        if show_help:
            for m in dir(self):
                if m.startswith('action_'):
                    name = m.replace('action_', '')
                    doc = getattr(self, m).__doc__
                    print(name)
                    print('  '+doc)

    def action_serve(self):
        '''Serve your website on your computer for testing purpose'''
        import http.server
        import socketserver

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=settings.PATH_HTML, **kwargs)

            def translate_path(self, path):
                ret = super().translate_path(path)
                if not ret.endswith('/') and '.' not in ret:
                    ret += '.html'
                return ret

        class Server(socketserver.TCPServer):
            allow_reuse_address = True

        with Server(('', settings.TEST_PORT), Handler) as httpd:
            print('localhost:{} [CTRL+C to quit]'.format(settings.TEST_PORT))
            httpd.serve_forever()

    def action_watch(self):
        '''Rebuild the site automatically each time a file has changed'''
        print('waiting for changes... [CTRL+C to quit]')
        self.action_build(watch=True)

    def action_build(self, watch=False):
        '''Build all the html pages from the markdown sources'''
        self.base_html = utils.read_file(os.path.join(settings.PATH_TEMPLATES, 'base.html'))

        from pathlib import Path
        import time
        while 1:
            for md_path in list(Path(settings.PATH_MD).rglob("*.md*")):
                self.convert(md_path, if_new=watch)
            if watch:
                time.sleep(1)
            else:
                break

    def convert(self, md_path, if_new=False):
        filename = os.path.basename(md_path)
        
        relpath = os.path.relpath(md_path, settings.PATH_MD)
        if relpath == 'home.md':
            relpath = 'index.md'
        
        ret = os.path.realpath(os.path.join(settings.PATH_HTML, relpath))
        ret = re.sub(r'\.[^.]+', settings.HTML_EXTENSION, ret)

        if if_new and utils.are_sources_older_than_target(md_path, ret):
            return ret

        os.makedirs(os.path.dirname(ret), exist_ok=True)

        main = utils.extrapolate_md(md_path)

        # extract context definitions from the source file
        main, context = utils.extract_context(main)

        if 'title' not in context:
            context['title'] = utils.get_title_from_filepath(md_path)

        context['nav'] = [
            {
                'path': utils.get_rel_nav_path(item, ret),
                'label': item.title(),
                'is_selected': item in relpath.split('/')[0],
            }
            for item in settings.NAVIGATION
        ]

        main = Template(main).render(**context)
        # convert to html
        context['main'] = markdown.markdown(main)

        # inject context into base template
        template = Template(self.base_html)
        content = template.render(**context)

        content = self.post_process(content)

        with open(ret, 'wt') as fh_html:
            fh_html.write(content)

        self.finc += 1

        print(self.finc, ret)


    def post_process(self, content):
        ret = content

        # bulma stuff
        if 1:
            ret = re.sub(r'<h(\d)>', r'<h\1 class="title is-\1">', ret)

        return ret


sb = SiteBuilder()
action = ''
if len(sys.argv) > 1:
    action = sys.argv[1]
sb.process(action=action)
