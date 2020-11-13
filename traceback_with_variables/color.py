def to_ansi(str_: str) -> str:
    return f'\033[{str_}m' if str_ else ''


class ColorScheme:
    def __init__(
        self,
        common: str,
        file_: str,
        line_num: str,
        func_name: str,
        func_snippet: str,
        name: str,
        value: str,
        exc_class: str,
        exc_text: str,
        end: str,
    ):
        self.c = to_ansi(common)  # used by internals, needs shortest names
        self.f = to_ansi(file_)
        self.ln = to_ansi(line_num)
        self.fn = to_ansi(func_name)
        self.fs = to_ansi(func_snippet)
        self.n = to_ansi(name)
        self.v = to_ansi(value)
        self.ec = to_ansi(exc_class)
        self.et = to_ansi(exc_text)
        self.e = to_ansi(end)

        self.c_ = self.e + self.c
        self.f_ = self.e + self.f
        self.ln_ = self.e + self.ln
        self.fn_ = self.e + self.fn
        self.fs_ = self.e + self.fs
        self.n_ = self.e + self.n
        self.v_ = self.e + self.v
        self.ec_ = self.e + self.ec
        self.et_ = self.e + self.et


class ColorSchemes:
    none = ColorScheme('', '', '', '', '', '', '', '', '', '')
    common = ColorScheme('37', '36;1', '36;1', '36;1', '36', '32;1', '37', '31', '91', '0')
    synthwave = ColorScheme('38;2;255;153;255', '38;2;255;153;0', '38;2;255;153;0', '38;2;255;153;0',
                            '38;2;50;100;255', '38;2;254;0;254', '38;2;153;204;255', '38;2;255;0;53',
                            '38;2;255;0;123', '0')
