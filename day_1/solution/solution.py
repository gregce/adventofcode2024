import sys

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    try:
        left_list = []
        right_list = []
        with open(input_file) as f:
            for line in f:
                left_id, right_id = map(int, line.strip().split())
                left_list.append(left_id)
                right_list.append(right_id)
        
        left_list.sort()
        right_list.sort()

        total_distance = sum(abs(left - right) for left, right in zip(left_list, right_list))

        print(total_distance)
    except FileNotFoundError:
        print(f"Error: Could not find input file {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()