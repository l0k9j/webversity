import settings
import os
import markdown
import utils
import re

class SiteBuilder:
    def build(self):
        self.base_html = utils.read_file(os.path.join(settings.PATH_TEMPLATES, 'base.html'))

        from pathlib import Path
        for md_path in list(Path(settings.PATH_MD).rglob("*.md")):
            self.convert(md_path)

    def convert(self, md_path):
        filename = os.path.basename(md_path)
        
        relpath = os.path.relpath(md_path, settings.PATH_MD)
        if relpath == 'home.md':
            relpath = '../index.md'
        
        ret = os.path.realpath(os.path.join(settings.PATH_HTML, relpath))
        ret = ret.replace('.md', '.html')

        os.makedirs(os.path.dirname(ret), exist_ok=True)

        main = utils.read_file(md_path)

        # extract context definitions from the source file
        context = {}
        def sub_var(match):
            context[match.group(1)] = match.group(2)
            return ''

        main = re.sub(r'(?m)^(\w+)=(.*)$', sub_var, main)

        # convert to html
        main = markdown.markdown(main)
        
        context['main'] = main
        if 'title' not in context:
            context['title'] = filename.replace('.md', '').title()

        # inject into base template
        def sub_context(match):
            ret = match.group(0)

            ret = context.get(match.group(1), ret)

            return ret

        content = re.sub(r'{{\s*(\w+)\s*}}', sub_context, self.base_html)

        content = self.post_process(content)

        with open(ret, 'wt') as fh_html:
            fh_html.write(content)

        print(ret)

    def post_process(self, content):
        ret = content

        # bulma stuff
        if 0:
            ret = re.sub(r'<h(\d)>', r'<h\1 class="title is-\1">', ret)

        return ret


sb = SiteBuilder()
sb.build()
