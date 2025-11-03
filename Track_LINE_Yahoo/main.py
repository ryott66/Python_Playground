import sys
from app import run

def main(lines):
    output = run(lines)
    if output:
        print(output, end="")

if __name__ == '__main__':
    lines = [l.rstrip('\r\n') for l in sys.stdin]
    main(lines)
