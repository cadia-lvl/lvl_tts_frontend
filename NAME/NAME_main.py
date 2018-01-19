"""
Example for an entry point for a program using main and argparse
"""

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='description of project/program', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('i', type=argparse.FileType('r'), help='Input data')
    parser.add_argument('o', type=argparse.FileType('w'), help='Output file')
    parser.add_argument('--some_int_arg', default=10)
    parser.add_argument('--some_string_arg', default='ent')

    return parser.parse_args()


def main():

    args = parse_args()


if __name__ == '__main__':
    main()
