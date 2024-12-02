import sys

def is_report_safe(report):
    increasing = all(report[i] < report[i+1] for i in range(len(report)-1))
    decreasing = all(report[i] > report[i+1] for i in range(len(report)-1))
    if not increasing and not decreasing:
        return False
    return all(1 <= abs(report[i] - report[i+1]) <= 3 for i in range(len(report)-1))

def check_dampener(report):
    for i in range(len(report)):
        modified_report = report[:i] + report[i+1:]
        if is_report_safe(modified_report):
            return True
    return False

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    safe_reports = 0
    try:
        with open(input_file) as f:
            for line in f:
                report = list(map(int, line.strip().split()))
                if not report or len(report) == 1:  # Empty or single-level reports are safe
                    safe_reports += 1
                    continue
                if is_report_safe(report):
                    safe_reports += 1
                elif check_dampener(report):
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