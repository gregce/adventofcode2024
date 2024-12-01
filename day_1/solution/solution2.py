#!/usr/bin/env python3

"""
Similarity Score Calculator

Process:
1. Read input file containing two columns of numbers
2. Parse into left and right lists
3. For each number in left list:
   - Count occurrences in right list
   - Multiply number by count
   - Add to running total
4. Display detailed calculation steps
5. Output final similarity score

Performance considerations:
- Use dictionary for O(1) lookups of right list counts
- Process file line by line to minimize memory usage
"""

import os  # Add import for path handling

def read_number_lists(filename: str) -> tuple[list[int], list[int]]:
    """
    Read and parse input file into two lists of numbers.
    
    Args:
        filename: Path to input file
        
    Returns:
        Tuple of (left_list, right_list) containing integers
    """
    left_list = []
    right_list = []
    
    try:
        # Get absolute path to input file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to day_1 folder, then into input folder
        input_file_path = os.path.join(os.path.dirname(script_dir), 'input', filename)
        
        with open(input_file_path, 'r') as f:
            # Process each line of the file
            for line in f:
                line = line.strip()  # Remove leading/trailing whitespace
                if not line:  # Skip empty lines
                    continue
                # Split line on whitespace and convert to integers
                parts = line.split()
                if len(parts) != 2:  # Skip invalid lines
                    continue
                left, right = map(int, parts)
                left_list.append(left)
                right_list.append(right)
    except FileNotFoundError:
        print(f"Error: Could not find file {input_file_path}")
        exit(1)
    except ValueError:
        print("Error: File contains invalid number format")
        exit(1)
        
    return left_list, right_list

def count_right_occurrences(right_list: list[int]) -> dict[int, int]:
    """
    Create frequency map of numbers in right list for O(1) lookups.
    
    Args:
        right_list: List of integers to count
        
    Returns:
        Dictionary mapping numbers to their frequency
    """
    counts = {}
    for num in right_list:
        counts[num] = counts.get(num, 0) + 1
    return counts

def calculate_similarity_score(left_list: list[int], right_counts: dict[int, int]) -> int:
    """
    Calculate total similarity score and display calculation steps.
    
    Args:
        left_list: List of numbers to process
        right_counts: Dictionary of number frequencies from right list
        
    Returns:
        Total similarity score
    """
    total_score = 0
    
    print("\nCalculating similarity score:")
    print("-" * 50)
    
    # Process each number in left list
    for i, num in enumerate(left_list, 1):
        # Get count of occurrences in right list (0 if not present)
        count = right_counts.get(num, 0)
        contribution = num * count
        total_score += contribution
        
        # Display calculation step
        print(f"Step {i:4d}: Number {num:5d} appears {count:3d} times "
              f"→ {num} × {count} = {contribution}")
    
    print("-" * 50)
    return total_score

def main():
    """Main program entry point."""
    input_file = "input_data.txt"
    
    # Add output file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file_path = os.path.join(script_dir, 'output_part2.txt')
    
    # Read and parse input file
    print(f"Reading input from {input_file}...")
    left_list, right_list = read_number_lists(input_file)
    
    right_counts = count_right_occurrences(right_list)
    total_score = calculate_similarity_score(left_list, right_counts)
    
    # Write to output file
    with open(output_file_path, 'w') as f:
        f.write("Calculating similarity score:\n")
        f.write("-" * 50 + "\n")
        for i, num in enumerate(left_list, 1):
            count = right_counts.get(num, 0)
            contribution = num * count
            f.write(f"Step {i:4d}: Number {num:5d} appears {count:3d} times "
                   f"→ {num} × {count} = {contribution}\n")
        f.write("-" * 50 + "\n")
        f.write(f"\nFinal similarity score: {total_score}\n")
    
    # Keep terminal output
    print(f"\nFinal similarity score: {total_score}")
    print(f"Results written to {output_file_path}")

if __name__ == "__main__":
    main() 