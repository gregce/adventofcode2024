import sys

def is_safe(report):
    increasing = all(report[i] < report[i+1] and 1 <= report[i+1] - report[i] <= 3 for i in range(len(report)-1))
    decreasing = all(report[i] > report[i+1] and 1 <= report[i] - report[i+1] <= 3 for i in range(len(report)-1))
    return increasing or decreasing

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    try:
        with open(input_file) as f:
            reports = f.readlines()
            safe_reports = 0
            for report in reports:
                levels = list(map(int, report.split()))
                if is_safe(levels):
                    safe_reports += 1
            print(safe_reports)
    except FileNotFoundError:
        print(f"Error: Could not find input file {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()