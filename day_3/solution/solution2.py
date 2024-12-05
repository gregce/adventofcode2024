import sys
import re

def process_instruction(instruction, is_mul_enabled, total_sum):
    """Process a single instruction, updating the sum and mul enabled status."""
    if instruction == "do()":
        return is_mul_enabled, total_sum
    elif instruction == "don't()":
        return False, total_sum
    else:  # Process mul(X,Y)
        if is_mul_enabled:
            nums = re.findall(r'\d+', instruction)
            x, y = map(int, nums)
            return is_mul_enabled, total_sum + (x * y)
        else:
            return is_mul_enabled, total_sum

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    try:
        with open(input_file) as f:
            data = f.read().strip()
            instructions = re.findall(r'(mul\(\d+,\d+\)|do\(\)|don\'t\(\))', data)
            is_mul_enabled = True
            total_sum = 0

            for instruction in instructions:
                if instruction == "do()":
                    is_mul_enabled = True
                elif instruction == "don't()":
                    is_mul_enabled = False
                else:  # This is a multiplication instruction
                    is_mul_enabled, total_sum = process_instruction(instruction, is_mul_enabled, total_sum)

            print(total_sum)
    except FileNotFoundError:
        print(f"Error: Could not find input file {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()