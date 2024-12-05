import sys
import re

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    try:
        with open(input_file) as f:
            data = f.read()
            pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
            matches = re.findall(pattern, data)
            result = sum(int(x) * int(y) for x, y in matches)
            print(result)
    except FileNotFoundError:
        print(f"Error: Could not find input file {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()