import argparse
import inspect
import re
import sys
import traceback
from typing import Any, Iterator, Union, Optional, TextIO, List, Callable, Type, Tuple, Dict

from traceback_with_variables.color import ColorScheme, ColorSchemes, supports_ansi
from traceback_with_variables.fast_capped_str_casts import to_capped_str


Patterns = Union[None, str, List[str]]  # file filter

ShouldPrint = Callable[[str, Type, str, bool], bool]  # extended var filter
VarFilterItem = Union[str, Type, ShouldPrint]  # any var filter
VarFilter = Union[VarFilterItem, List[VarFilterItem]]  # full final var filter

Print = Callable[[Any], Optional[str]]  # how to print
VarPrinters = List[Tuple[ShouldPrint, Print]]  # pairs for filters and printers


def skip(obj: Any) -> Optional[str]:  # noqa: U100
    return None


def hide(obj: Any) -> Optional[str]:  # noqa: U100
    return '...hidden...'


# never called, for == only, means apply default print
def show(obj: Any) -> Optional[str]:  # noqa: U100
    raise NotImplementedError()


def get_print(name: str, obj: Any, filename: str, is_global: bool, var_printers: VarPrinters) -> Print:
    type_ = type(obj)
    return next((p for should_p, p in var_printers if should_p(name, type_, filename, is_global)), show)


class Format:  # no dataclass for compatibility
    def __init__(
        self,
        max_value_str_len: int = 1000,
        ellipsis_rel_pos: float = 0.7,
        max_exc_str_len: int = 10000,
        objects_details: int = 1,
        ellipsis_: str = '...',
        before: int = 0,
        after: int = 0,
        color_scheme: Optional[ColorScheme] = None,
        skip_files_except: Patterns = None,
        brief_files_except: Patterns = None,
        custom_var_printers: Optional[VarPrinters] = None,  # address examples
    ):
        self._can_grow = True
        self.max_value_str_len = max_value_str_len
        self.ellipsis_rel_pos = ellipsis_rel_pos
        self.max_exc_str_len = max_exc_str_len
        self.objects_details = objects_details
        self.ellipsis_ = ellipsis_
        self.before = before
        self.after = after
        self.color_scheme = color_scheme
        self.skip_files_except: List['re.Pattern'] = _to_patterns(skip_files_except)
        self.brief_files_except: List['re.Pattern'] = _to_patterns(brief_files_except)
        self.custom_var_printers: VarPrinters = [
            (_var_filter_to_should_print(f), p) for f, p in custom_var_printers or []
        ]
        self._can_grow = False

    def __setattr__(self, name, value):
        if (not getattr(self, '_can_grow', True)) and (name not in dir(self)) or (name in dir(type(self))):
            raise AttributeError(f"'Format' object has no attribute '{name}'")
        super().__setattr__(name, value)

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--max-value-str-len", type=int, default=1000)
        parser.add_argument("--ellipsis-rel-pos", type=float, default=0.7)
        parser.add_argument("--max-exc-str-len", type=int, default=10000)
        parser.add_argument("--objects-details", type=int, default=1)
        parser.add_argument("--ellipsis", default="...")
        parser.add_argument("--before", type=int, default=0)
        parser.add_argument("--after", type=int, default=0)
        parser.add_argument("--color-scheme", default='auto',
                            choices=[a for a in dir(ColorSchemes) if not a.startswith('_')])
        parser.add_argument("--skip-files-except", nargs='*')
        parser.add_argument("--brief-files-except", nargs='*')
        parser.add_argument("--no-globals", action='store_true')

    @classmethod
    def parse(cls, ns: argparse.Namespace) -> 'Format':
        return Format(
            max_value_str_len=ns.max_value_str_len,
            ellipsis_rel_pos=ns.ellipsis_rel_pos,
            max_exc_str_len=ns.max_exc_str_len,
            objects_details=ns.objects_details,
            ellipsis_=ns.ellipsis,
            before=ns.before,
            after=ns.after,
            color_scheme=getattr(ColorSchemes, ns.color_scheme),
            skip_files_except=ns.skip_files_except,
            brief_files_except=ns.brief_files_except,
            custom_var_printers=[((lambda n, t, fn, is_global: is_global), lambda v: None)]  # noqa: U100
            if ns.no_globals else None,
        )

    def replace(self, **kwargs: Dict[str, Any]) -> 'Format':
        result = Format()

        for key, value in self.__dict__.items():
            setattr(result, key, value)
        for key, value in kwargs.items():
            setattr(result, key, value)

        return result


def format_exc(
    e: Optional[Exception] = None,
    num_skipped_frames: int = 0,
    fmt: Optional[Format] = None,
    for_file: Optional[TextIO] = None,
) -> str:
    return '\n'.join(iter_exc_lines(
        e=e,
        num_skipped_frames=num_skipped_frames,
        fmt=fmt,
        for_file=for_file,
    ))


def iter_exc_lines(
    e: Optional[Exception] = None,
    num_skipped_frames: int = 0,
    fmt: Optional[Format] = None,
    for_file: Optional[TextIO] = None,
) -> Iterator[str]:
    e_: Optional[Exception] = e or sys.exc_info()[1] or getattr(sys, 'last_value', None)

    if e_ is None:
        raise ValueError('no exception to handle')

    return _iter_lines(
        e=e_,
        frame_infos=inspect.getinnerframes(
            tb=e_.__traceback__,
            context=(max(fmt.before, fmt.after) if fmt else 0) + 1,
        )[num_skipped_frames:],
        fmt=fmt,
        for_file=for_file,
    )


def format_cur_tb(
    num_skipped_frames: int = 0,
    fmt: Optional[Format] = None,
    for_file: Optional[TextIO] = None,
) -> str:
    return '\n'.join(iter_cur_tb_lines(
        num_skipped_frames=num_skipped_frames + 1,
        fmt=fmt,
        for_file=for_file,
    ))


def iter_cur_tb_lines(
    num_skipped_frames: int = 0,
    fmt: Optional[Format] = None,
    for_file: Optional[TextIO] = None,
) -> Iterator[str]:
    frame1 = sys._getframe(1)  # noqa

    return _iter_lines(
        e=None,
        frame_infos=inspect.getouterframes(
            frame1,
            context=(max(fmt.before, fmt.after) if fmt else 0) + 1,
        )[num_skipped_frames:][::-1],
        fmt=fmt,
        for_file=for_file,
    )


# - privates - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def _iter_lines(
    e: Optional[Exception],
    frame_infos: List[inspect.FrameInfo],
    fmt: Optional[Format] = None,
    for_file: Optional[TextIO] = None,
) -> Iterator[str]:
    fmt_: Format = fmt or default_format
    c: ColorScheme = fmt_.color_scheme or \
        (ColorSchemes.common if (for_file and supports_ansi(for_file)) else ColorSchemes.none)

    yield f'{c.c}Traceback with variables (most recent call last):{c.e}'

    for frame, filename, line_num, func_name, code_lines, before in frame_infos:
        if bool(fmt_.skip_files_except) and all(not p.search(filename) for p in fmt_.skip_files_except):
            continue

        yield f'{c.c}  File "{c.f_}{filename}{c.c_}", line {c.ln_}{line_num}{c.c_}, in {c.fn_}{func_name}{c.e}'

        if code_lines:
            code_lines = code_lines[max(0, before - fmt_.before):before + 1 + fmt_.after]
            code_lines = [line.replace('\t', '    ').rstrip() for line in code_lines]
            min_indent = min(len(line) - len(line.lstrip(' ')) for line in code_lines)

            for i, line in enumerate(code_lines):
                prefix = '  '
                if fmt_.after or fmt_.before:
                    prefix = '> ' if max(0, before - fmt_.before) + i == before else '. '

                yield f'{c.c}  {prefix}{c.fs_}{line[min_indent:]}{c.e}'

        if bool(fmt_.brief_files_except) and all(not p.search(filename) for p in fmt_.brief_files_except):
            continue

        num_skipped: int = 0

        for var_name, var in frame.f_locals.items():
            is_global = (var_name in frame.f_globals) and frame.f_globals[var_name] is var

            var_str = _to_cropped_str(
                obj=var,
                is_global=is_global,
                name=var_name,
                filename=filename,
                custom_var_printers=fmt_.custom_var_printers,
                max_value_str_len=fmt_.max_value_str_len,
                objects_details=fmt_.objects_details,
                ellipsis_rel_pos=fmt_.ellipsis_rel_pos,
                max_exc_str_len=fmt_.max_exc_str_len,
                ellipsis_=fmt_.ellipsis_
            )

            if var_str is None:
                num_skipped += 1
                continue

            var_lines = var_str.split('\n')
            yield f'{c.c}      {c.n_}{var_name}{c.c_} = {c.v_}{var_lines[0] if var_lines else var_str}{c.e}'
            for line in var_lines[1:]:
                yield f'{c.c}      {c.v_}{line}{c.e}'

        if num_skipped > 0:
            yield f'{c.c}      {c.n_}...skipped...{c.c_} {c.v_}{num_skipped}{c.c_} vars{c.e}'

    if e:
        yield f'{c.ec}{e.__class__.__module__}.{e.__class__.__qualname__}:{c.et_} {e}{c.e}'


def _crop(line: str, max_len: int, ellipsis_rel_pos: float, ellipsis_: str) -> str:
    pre_len = int(max_len * min(1.0, max(0.0, ellipsis_rel_pos)))
    suf_len = max_len - pre_len
    if pre_len + len(ellipsis_) + suf_len >= len(line):
        return line

    return line[:pre_len] + ellipsis_ + (line[-suf_len:] if suf_len > 0 else '')


def _to_cropped_str(
    obj: Any,
    is_global: bool,
    name: str,
    filename: str,
    custom_var_printers: VarPrinters,
    objects_details: int,
    max_value_str_len: int,
    ellipsis_rel_pos: float,
    max_exc_str_len: int,
    ellipsis_: str
) -> Optional[str]:
    print_ = get_print(name=name, obj=obj, filename=filename, is_global=is_global, var_printers=custom_var_printers)
    try:
        if print_ == show:
            return to_capped_str(
                obj=obj,
                len_cap=max_value_str_len,
                ellipsis=ellipsis_,
                rel_ellipsis_pos=ellipsis_rel_pos,
                obj_depth=objects_details,
            )
        raw = print_(obj)
        return _crop(raw, max_value_str_len, ellipsis_rel_pos, ellipsis_) if raw is not None else None

    except:  # noqa
        lines = traceback.format_exc(chain=False).split('\n')
        for first_li, line in enumerate(lines):
            if line.startswith('  File "') \
                    and ('fast_capped_str_casts.py' not in line) \
                    and ('in _to_cropped_str' not in line):
                break

        return _crop(
            '<exception while printing> ' + '\n  '.join(
                lines[:1] +
                (['  ...traceback_with_variables internal stacks...'] if first_li > 1 else []) +
                lines[first_li:]
            ),
            max_exc_str_len,
            ellipsis_rel_pos,
            ellipsis_,
        )


def _to_patterns(patterns: Patterns) -> List['re.Pattern']:
    p_strs: List[str] = [patterns] if isinstance(patterns, str) else (patterns or [])

    return [re.compile(p) for p in p_strs]


def _should_print(name: str, type_: Type, file: str, is_global: bool, item: VarFilterItem) -> bool:
    if isinstance(item, str):
        return bool(re.search(item, name))

    elif isinstance(item, type):
        return issubclass(item, type_)

    return item(name, type_, file, is_global)


def _var_filter_to_should_print(filter_: VarFilter) -> ShouldPrint:
    def should_print(name: str, type_: Type, file: str, is_global: bool) -> bool:
        return any(
            _should_print(name, type_, file, is_global, item)
            for item in (filter_ if isinstance(filter_, list) else [filter_])
        )

    return should_print


default_format = Format(custom_var_printers=[
    ('.*(?i:pass|secret|token|key|api_key|cred|pwd).*', hide),
])
