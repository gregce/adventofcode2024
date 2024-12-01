// Prompt -- Take a first pass at decomposing @day_1_problem_part_2.txt into a set of requirements to build a program in python that solves the problem. Insert that into @instructions2.md 


# Instructions for Calculating Similarity Score

## Objective

Calculate the total similarity score between two lists of integers by determining how often each number from the left list appears in the right list.

## Requirements

### 1. Input

- Two lists of integers:
  - **Left List**: A list containing integers, possibly with duplicates.
  - **Right List**: Another list containing integers, possibly with duplicates.

### 2. Process

- **For each** number in the **Left List**:
  1. **Count** how many times this number appears in the **Right List**.
  2. **Multiply** the number by its count from the **Right List**.
  3. **Add** the result to a running total similarity score.

### 3. Output

- The **total similarity score** calculated by summing the results from the above process.

### 4. Constraints

- Both lists can be of different lengths.
- Numbers may appear multiple times in either list.
- Optimize the solution to handle large lists efficiently.
- Ensure that numbers not present in the **Right List** contribute zero to the similarity score.

### 5. Example

Given the following lists:

**Left List**: `3, 4, 2, 1, 3, 3`

**Right List**: `4, 3, 5, 3, 9, 3`

**Calculation Steps**:

1. **Number 3**:
   - Appears **3 times** in the Right List.
   - Contribution: `3 * 3 = 9`
2. **Number 4**:
   - Appears **1 time** in the Right List.
   - Contribution: `4 * 1 = 4`
3. **Number 2**:
   - Appears **0 times** in the Right List.
   - Contribution: `2 * 0 = 0`
4. **Number 1**:
   - Appears **0 times** in the Right List.
   - Contribution: `1 * 0 = 0`
5. **Number 3** (again):
   - Contribution: `3 * 3 = 9`
6. **Number 3** (again):
   - Contribution: `3 * 3 = 9`

**Total Similarity Score**: `9 + 4 + 0 + 0 + 9 + 9 = 31`

### 6. Assumptions

- Input will consist strictly of integers.
- The environment for reading input and outputting the result remains consistent with previous problems.

### 7. Edge Cases

- If a number in the Left List does not appear in the Right List, its contribution is zero.
- Duplicate numbers in the Left List should be processed individually.

### 8. Performance Considerations

- Implement efficient counting to handle large lists (e.g., use hash maps or dictionaries).

### 9. Testing

- Verify the solution with the provided example.
- Test with additional cases, such as:
  - Left List or Right List being empty.
  - All numbers in the Left List are not present in the Right List.
  - All numbers in the Left List are present multiple times in the Right List.

## Additional Notes

- Reuse code from previous solutions where applicable.
- Write clean, maintainable code with appropriate comments. 