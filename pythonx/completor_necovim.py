# -*- coding: utf-8 -*-

import logging
from completor import Completor, vim, get_encoding
from completor.compat import to_bytes

_cache = {}

logger = logging.getLogger('completor')

#TODO
# baseの指定(:, _)
# triggerの指定(:, _)
# fuzzymatch
class Necovim(Completor):
    filetype = 'necovim'
    sync = True
    trigger = r"""[a-zA-Z0-9#:_]+$"""
    ident = r"""[a-zA-Z0-9#:_]+$"""

    def parse(self, base):
        print(base)
        if not self.ft or not base:
            return []
        start = self.start_column()
        kw = self.input_data[start:]

        gather_candidates = vim.Function('necovim#gather_candidates')
        binput_data = to_bytes(self.input_data, get_encoding())
        bkw = to_bytes(kw, get_encoding())
        candidates = [{
            'word': item[b'word'],
            'dup': 0,
            'menu': b'[vim]',
            'kind': item.get(b'kind', b'')
        } for item in gather_candidates(binput_data, bkw)[:]
              if item[b'word'].startswith(kw.encode('utf-8'))]

        index = kw.rfind(base)
        if index > 0:
            prefix = len(kw[:index])
            for c in candidates:
                c['abbr'] = c['word']
                c['word'] = c['word'][prefix:]
        print(kw)
        return candidates
