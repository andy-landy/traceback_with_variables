import inspect
import sys
import traceback
from contextlib import contextmanager


@contextmanager
def rich_traceback(reraise=True, file_=sys.stderr, flush=False, max_locals_str_length=500):
    try:
        yield

    except Exception as e:
        if file_:
            try:
                trace_str = get_trace_str(e, list(inspect.trace())[2:], max_locals_str_length)
                file_.write(trace_str)
            except Exception:  # shit happens)
                file_.write(f'{traceback.format_exc()}\nRichTraceback raised an exception')

            file_.write('\n')
            if flush:
                file_.flush()

        if reraise:
            raise e


def dict_to_str(dict_, max_total_length):
    if not dict_:
        return ''

    # print as is
    tokens = [token for name in sorted(dict_) for token in (name, to_str(dict_[name]))]
    optimistic_str = tokens_to_str(tokens)
    if len(optimistic_str) <= max_total_length or max_total_length < 0:
        return optimistic_str

    # croping needed, here is some info to print
    suffix = f'...({len(optimistic_str)} chars)'
    if len(suffix) >= max_total_length:
        return suffix[:max_total_length]

    # crop the longest, get optimal max_token_length
    misc_length = len(optimistic_str) - sum(map(len, tokens))
    total_token_length_left = max_total_length - misc_length - len(suffix)
    for i, len_ in enumerate(sorted(map(len, tokens))):
        max_token_length = max(1, 1 + total_token_length_left // (len(tokens) - i))
        if len_ >= max_token_length:
            surplus = (len(tokens) - i) * max_token_length - total_token_length_left
            break
        total_token_length_left -= len_

    for i, token in enumerate(tokens):
        if len(token) >= max_token_length:
            tokens[i] = crop(token, max_token_length - (1 if surplus > 0 else 0))
            surplus -= 1

    return tokens_to_str(tokens)[:max_total_length - len(suffix)] + suffix


def crop(line, max_length):
    return line if len(line) <= max(max_length, 2) else (line[:max(max_length - 1, 1)] + '~')


def to_str(obj):
    try:
        return str(obj)
    except:
        traceback.print_exc()
        return '<exception while printing>'


def tokens_to_str(tokens):
    return '\n      '.join(f'{tokens[i]}={tokens[i + 1]}' for i in range(0, len(tokens), 2))


def get_trace_str(e, trace, max_locals_size):
    lines = []

    lines.append('RichTraceback (most recent call last):')
    for frame, filename, linenum, funcname, codelines, funclinenum in trace:
        lines.append(f'  File "{filename}", line {linenum}, in {funcname}')
        if codelines:
            lines.append('    ' + ''.join(codelines).rstrip('\n').lstrip(' '))
        try:
            lines.append('      ' + dict_to_str(frame.f_locals, max_locals_size))
        except:
            traceback.print_exc()
            lines.append('      <exception while printing locals (fix it!)>')  # must be a bug here
    lines.append(f'{e.__class__.__module__}.{e.__class__.__name__}: {e}')

    return '\n'.join(lines)

