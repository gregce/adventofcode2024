import sys
from collections import defaultdict

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    try:
        left_list = []
        right_list = []
        with open(input_file) as f:
            for line in f:
                left, right = map(int, line.split())
                left_list.append(left)
                right_list.append(right)
        
        freq_right = defaultdict(int)
        for num in right_list:
            freq_right[num] += 1
        
        similarity_score = 0
        for num in left_list:
            if num in freq_right:
                similarity_score += num * freq_right[num]
        
        print(similarity_score)
    except FileNotFoundError:
        print(f"Error: Could not find input file {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()