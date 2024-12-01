// Prompt -- Take a first pass at decomposing @day_1_problem.txt into a set of requirements to build a program in python that solves the problem. Insert that into @instructions.md 

- Read two lists of integers from the puzzle input: the left list and the right list.
- Sort both lists in ascending order.
- Pair up numbers from both lists:
  - Pair the smallest number in the left list with the smallest in the right list, the next smallest with the next smallest, and so on.
- For each pair, calculate the absolute difference between the two numbers.
- Sum all the absolute differences to get the total distance.
- Output the total distance.
