# Step-by-step guide:
# 1. Initialize two empty lists to hold the left and right numbers.
# 2. Read the file 'day_1/input_data.txt'.
#    - For each line, split it into two numbers and add them to the respective lists.
# 3. Sort both lists in ascending order.
# 4. Initialize a variable to hold the total distance.
# 5. Pair up the numbers from both lists in order.
#    - For each pair, calculate the absolute difference and add it to the total distance.
#    - Also, display the pairings and their distances.
# 6. After processing all pairs, output the total distance.

import os

# Initialize empty lists for the left and right numbers
left_numbers = []  # List to store numbers from the left column
right_numbers = []  # List to store numbers from the right column

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to day_1 folder, then into input folder
input_file_path = os.path.join(os.path.dirname(script_dir), 'input', 'input_data.txt')
output_file_path = os.path.join(script_dir, 'output_part1.txt')

# Open and read the input data file
with open(input_file_path, 'r') as file:  # Open the file for reading
    for line in file:
        line = line.strip()  # Remove leading/trailing whitespace
        if not line:
            continue  # Skip empty lines
        # Split the line into two numbers based on whitespace
        parts = line.split()  # Split line into parts
        if len(parts) != 2:
            continue  # Skip lines that don't have exactly two numbers
        # Convert the split strings to integers
        left_num = int(parts[0])  # First number in the line
        right_num = int(parts[1])  # Second number in the line
        # Add the numbers to the respective lists
        left_numbers.append(left_num)  # Append to left_numbers list
        right_numbers.append(right_num)  # Append to right_numbers list

# Sort both lists in ascending order
left_numbers.sort()  # Sort left_numbers list
right_numbers.sort()  # Sort right_numbers list

# Initialize a variable to hold the total distance
total_distance = 0  # Sum of absolute differences

# Display the pairings and their distances
print("Pairings and their distances:")
for left_num, right_num in zip(left_numbers, right_numbers):
    distance = abs(left_num - right_num)  # Calculate the absolute difference
    total_distance += distance  # Add distance to total_distance
    # Print the pairing and the calculated distance
    print(f"{left_num} paired with {right_num}, distance: {distance}")

# Output the total distance
with open(output_file_path, 'w') as f:
    f.write("Pairings and their distances:\n")
    for left_num, right_num in zip(left_numbers, right_numbers):
        distance = abs(left_num - right_num)
        f.write(f"{left_num} paired with {right_num}, distance: {distance}\n")
    f.write(f"\nTotal distance: {total_distance}\n")
 