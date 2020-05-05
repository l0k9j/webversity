import settings
import os
import markdown
import utils
import re

class SiteBuilder:
    def build(self):
        self.base_html = utils.read_file(os.path.join(settings.PATH_TEMPLATES, 'base.html'))

        for f in os.listdir(settings.PATH_MD):
            if f.endswith('.md'):
                self.convert(os.path.join(settings.PATH_MD, f))

    def convert(self, md_path):
        ret = os.path.join(settings.PATH_HTML, os.path.basename(md_path))
        ret = ret.replace('.md', '.html')

        main = utils.read_file(md_path)
        main = markdown.markdown(main)
        content = re.sub(r'{{\s*main\s*}}', main, self.base_html)

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
