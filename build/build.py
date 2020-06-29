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

    def build(self, watch=False):
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
            relpath = '../index.md'
        
        ret = os.path.realpath(os.path.join(settings.PATH_HTML, relpath))
        ret = re.sub(r'\.[^.]+', '.html', ret)

        if if_new and utils.get_file_time(md_path) < utils.get_file_time(ret):
            return ret

        os.makedirs(os.path.dirname(ret), exist_ok=True)

        main = utils.read_file(md_path)

        # extract context definitions from the source file
        main, context = utils.extract_context(main)

        if 'title' not in context:
            context['title'] = re.sub(r'\.[^.]*', '', filename)
            if context['title'] == 'index':
                context['title'] = os.path.basename(os.path.dirname(md_path))
            context['title'] = context['title'].title()
        
        context['nav'] = [
            {
                'path': os.path.relpath(
                    os.path.join(settings.PATH_HTML, item if item != 'home' else '..'),
                    os.path.dirname(ret) 
                ),
                'label': item.title(),
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
watch = 'watch' in sys.argv
sb.build(watch=watch)
