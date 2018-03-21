import re
from .base import Base
from deoplete.util import debug


class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'confluencewiki'
        self.mark = '[cwiki]'
        self.filetypes = ['confluencewiki']
        self.min_pattern_length = 2
        self.rank = 200
        self.input_pattern = (r'{|:|=|\|')

    def get_complete_position(self, context):
        m = re.search(r'\w*$', context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        debug(self.vim, context['input'])
        m = re.search(r"{(?P<macro>\w*)(?:[:|](?P<param>\w*)(?:=(?P<value>\w*))?)*$", context['input'])

        if m:
            return self.__get_candidates(m.group('macro'), m.group('param'), m.group('value'), m.lastgroup)
        else:
            return []

    def __get_candidates(self, m_macro, m_param, m_value, lastgroup):
        bool_arr = ['true', 'false']
        info_params = {'title': [], 'icon': bool_arr}
        all_candidates = {
            'anchor': {},
            'attachments': {
                'patterns': [],
                'labels': [],
                'old': bool_arr,
                'sortBy': ['date', 'size', 'name', 'created date'],
                'sortOrder': ['ascending', 'descending'],
                'upload': bool_arr,
                'page': [],
                'preview': bool_arr
            },
            'code': {
                # FIXME
                'language': ['actionscript', 'applescript', 'bash', 'csharp', 'cpp', 'css', 'coldfusion', 'delphi',
                             'diff', 'erlang', 'groovy', 'html', 'java', 'javafx', 'javascript', 'plain', 'powershell',
                             'python', 'ruby', 'sql', 'saas', 'scala', 'visualbasic', 'yaml'],
                'title': [],
                'collapse': bool_arr,
                'linenumbers': bool_arr,
                'firstline': [],
                'theme': ['django', 'emacs', 'fadetogrey', 'midnight', 'rdark', 'eclipse', 'confluence']
            },
            'expand': {},
            'info': info_params,
            'tip': info_params,
            'note': info_params,
            'warning': info_params,
            'noformat': {
                'nopanel': bool_arr
            },
            'toc': {
                'type': ['list', 'flat'],
                'outline': [],
                'style': ['none', 'circle', 'disc', 'square', 'decimal', 'lower-alpha', 'lower-roman', 'upper-roman'],
                'indent': [],
                'separator': ['brackets', 'braces', 'parens', 'pipe'],
                'minLevel': [],
                'maxLevel': [],
                'exclude': [],
                'printable': [],
                'class': [],
                'absoluteURL': [],
            },
            'footnote': {},
            'display-footnotes': {}
        }

        if lastgroup == 'macro':
            return [{'word': macro} for macro in all_candidates.keys() if macro.startswith(m_macro)]

        elif lastgroup == 'param' and m_macro in all_candidates:
            return [{'word': param} for param in all_candidates[m_macro].keys() if param.startswith(m_param)]

        elif lastgroup == 'value' and m_macro in all_candidates and m_param in all_candidates[m_macro]:
            return [{'word': value} for value in all_candidates[m_macro][m_param] if value.startswith(m_value)]

        else:
            return []
