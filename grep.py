import argparse
import sys
import re


def output(line):
    print(line)

def search_pattern(pattern, line, invert, ignore):
    flag_ignore = re.IGNORECASE if ignore else invert
    search = re.search(pattern, line, flag_ignore)
    if invert:
        search = not search
    return search

def count_src_pattern(pattern, lines, invert, ignore):
    count = 0
    for line in lines:
        line = line.rstrip()
        if search_pattern(pattern, line, invert, ignore):
            count += 1
    return count



def grep(lines, params):
    params.pattern = params.pattern.replace('?', '.').replace('*','.*?')

    if params.count:
        output(str(count_src_pattern(params.pattern, lines, params.invert, params.ignore_case)))

    else:
        count_aft = 0

        before_pattern = max(params.context, params.before_context)
        after_pattern = max(params.context, params.after_context)

        buffer = [None] * before_pattern

        for idx, line in enumerate(lines):
            line = line.rstrip()

            if search_pattern(params.pattern, line, params.invert, params.ignore_case):
                for idx_buf, elem_buf in enumerate(buffer):
                    if elem_buf:
                        if params.line_number:
                            elem_buf = '{}-{}'.format(idx - before_pattern + idx_buf + 1, elem_buf)
                        output(elem_buf)
                buffer = [None] * before_pattern


                count_aft = after_pattern

                if params.line_number:
                    line = '{}:{}'.format(idx + 1, line)
                output(line)

            elif count_aft:
                count_aft -= 1
                if params.line_number:
                    line = '{}-{}'.format(idx + 1, line)
                output(line)
            else:
                buffer.append(line)
                if len(line) > before_pattern:
                    buffer.pop(0)


def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()
