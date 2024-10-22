import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import List


def check_coverage_reports(inp_dir: Path, max_allowed_num_uncovered_lines: int) -> None:
    file_to_line_to_was_hit: Dict[str, Dict[int, bool]] = defaultdict(dict)

    for report_path in inp_dir.rglob('*.json'):
        with report_path.open('r') as inp:
            for file_, data in json.load(inp)['files'].items():
                line_to_was_hit = file_to_line_to_was_hit[file_.replace('\\', '/')]
                for line in data['executed_lines']:
                    line_to_was_hit[line] = True
                for line in data['missing_lines']:
                    line_to_was_hit.setdefault(line, False)
        
    num_uncovered_lines = 0
    for file_, line_to_was_hit in file_to_line_to_was_hit.items():
        for line, was_hit in line_to_was_hit.items():
            if not was_hit:
                sys.stderr.write(f'miss at {file_}:{line}\n')
                num_uncovered_lines += 1

    if num_uncovered_lines > max_allowed_num_uncovered_lines:
        raise ValueError('check failed')


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--inp-dir', required=True, type=Path)
    p.add_argument('--max-allowed-num-uncovered-lines', required=True, type=int)

    return p.parse_args()


def main():
    args = parse_args()

    check_coverage_reports(
        inp_dir=args.inp_dir,
        max_allowed_num_uncovered_lines=args.max_allowed_num_uncovered_lines
    )


if __name__ == '__main__':
    main()

