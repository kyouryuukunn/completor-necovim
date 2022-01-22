# -*- coding: utf-8 -*-

import logging
import re
import itertools
from completor import Completor, vim, get_encoding, LIMIT
from completor.compat import to_bytes, to_unicode
from completers.common.utils import test_subseq

_cache = {}

logger = logging.getLogger('completor')


class Necovim(Completor):
    filetype = 'vim'
    sync = True
    trigger = re.compile(r'[a-zA-Z0-9#:_]{2,}$', re.U | re.X)

    def gen_entry(self, base):
        gather_candidates = vim.Function('necovim#gather_candidates')

        binput_data = to_bytes(self.input_data, get_encoding())
        bbase = to_bytes(base, get_encoding())

        candidates = gather_candidates(binput_data, bbase)
        for entry in candidates:
            score = test_subseq(base, to_unicode(entry[b'word'], 'utf-8'))
            if score is None:
                continue
            yield entry, score

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
        if len(kw) < self.get_option('min_chars'):
            return []

        items = list(itertools.islice(
            itertools.chain(self.gen_entry(kw)), LIMIT))
        items.sort(key=lambda x: x[1])

        index = match.start()
        index = len(to_bytes(self.cursor_line[:index], get_encoding()))
        start_column = self.start_column()
        prefix = start_column - index
        if prefix < 0:
            prefix = 0

        ret = []
        for item, _ in items:
            ret.append({
                'word': item[b'word'][prefix:],
                'abbr': item[b'word'],
                'dub': 1,
                'menu': '[vim]'
            })

        return ret
