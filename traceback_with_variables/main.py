import argparse
import sys
from distutils.spawn import find_executable
from pathlib import Path
from typing import List, Optional, NoReturn, Tuple

from traceback_with_variables import printing_tb


def run_script(
    path: Path,
    argv: List[str],
    max_value_str_len: int,
    max_exc_str_len: int,
    ellipsis_: str,
    num_context_lines: int,
) -> int:
    sys.path[0] = str(path.parent)
    sys.argv = [str(path)] + argv

    with printing_tb(
        reraise=False,
        skip_cur_frame=True,
        max_value_str_len=max_value_str_len,
        max_exc_str_len=max_exc_str_len,
        ellipsis_=ellipsis_,
        num_context_lines=num_context_lines,
    ):
        exec(
            compile(path.read_text(), str(path), "exec"),
            {"__name__": "__main__"},
            {"__name__": "__main__"},
        )

        return 0

    return 1  # noqa # actually 'this code is unreachable' is wrong


# - parse args - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class ParseError(RuntimeError):
    pass


def raising_error_func(message: str) -> NoReturn:
    raise ParseError(message)


def split_argv_to_own_and_sub(
    raising_noabbrev_parser: argparse.ArgumentParser,  # with raising .error, no abbrev
    argv: Optional[List[str]] = None,
) -> Tuple[List[str], List[str]]:
    _argv = (argv or sys.argv)[1:]

    for num_args in range(1, len(_argv) + 1):
        try:
            raising_noabbrev_parser.parse_args(_argv[:num_args])

        except ParseError as e:
            if e.args[0].startswith("unrecognized arguments"):
                return _argv[: num_args - 1], _argv[num_args - 1:]

    return _argv, []


def parse_args_and_script_cmd(
    raising_nohelp_noabbrev_parser: argparse.ArgumentParser,  # with raising .error, no help, no abbrev
) -> Tuple[argparse.Namespace, Path, List[str]]:
    public_parser = argparse.ArgumentParser(parents=[raising_nohelp_noabbrev_parser])
    public_parser.add_argument("script")
    public_parser.add_argument("script-arg", nargs="*")

    own_argv, sub_argv = split_argv_to_own_and_sub(
        raising_nohelp_noabbrev_parser, sys.argv
    )

    try:
        args = raising_nohelp_noabbrev_parser.parse_args(own_argv)
    except ParseError:
        public_parser.parse_args(own_argv)
        args = argparse.Namespace()  # not gonna happen anyway, public_parser exits

    if not sub_argv:
        public_parser.parse_args(own_argv)

    if sub_argv[0] == "--help":
        public_parser.parse_args(["--help"])

    script_path_str = find_executable(sub_argv[0])

    if not script_path_str:
        module = sys.modules.get(script_path_str)

        if not module:
            raise ValueError(f"No such file or command or module: {sub_argv[0]}")

        script_path_str = module.__file__

    return args, Path(script_path_str), sub_argv[1:]


def parse_args() -> Tuple[argparse.Namespace, Path, List[str]]:
    parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    parser.error = raising_error_func

    parser.add_argument("--max-value-str-len", type=int, default=1000)
    parser.add_argument("--max-exc-str-len", type=int, default=10000)
    parser.add_argument("--ellipsis", default="...")
    parser.add_argument("--num-context-lines", type=int, default=1)

    return parse_args_and_script_cmd(parser)


def main():
    args, script_path, script_argv = parse_args()

    sys.exit(
        run_script(
            path=script_path,
            argv=script_argv,
            max_value_str_len=args.max_value_str_len,
            max_exc_str_len=args.max_exc_str_len,
            ellipsis_=args.ellipsis,
            num_context_lines=args.num_context_lines,
        )
    )


if __name__ == "__main__":
    main()
