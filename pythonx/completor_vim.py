# -*- coding: utf-8 -*-

import logging, re
from completor import Completor, vim, get_encoding
from completor.compat import to_bytes

_cache = {}

logger = logging.getLogger('completor')

class Necovim(Completor):
    filetype = 'vim'
    sync = True
    trigger = re.compile(r'[a-zA-Z0-9#:_]{2,}$', re.U | re.X)

    def parse(self, base):
        if not self.ft or not base:
            return []

        logger.info('start necovim parse: %s', base)

        try:
            match = self.trigger.search(base)
        except TypeError as e:
            logger.exception(e)
            match = None

        if not match:
            logger.info('no matches')
            return []

        kw = match.group()
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

        index = base.rfind(kw)
        start_column = self.start_column()
        prefix = start_column - index
        if prefix > 0:
            for c in candidates:
                c['abbr'] = c['word']
                c['word'] = c['word'][prefix:]
        return candidates
