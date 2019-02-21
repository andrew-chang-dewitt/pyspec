import sys
from cli import run_tests

def main():
    print('in entry.main()')
    args = sys.argv[1:]
    for arg in args:
        print(f'passed arg: {arg}')

    run_tests.all_tests(args[0])

if __name__ == '__main__':
    main()
