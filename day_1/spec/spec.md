### Problem Analysis

The goal is to compare two lists of historically significant location IDs found in the Chief's office. The challenge lies in reconciling the two lists by calculating the total distance between corresponding elements when the lists are sorted in ascending order.

#### Key Points:
- Each location ID in the lists is represented by a unique number.
- The lists are compared by sorting them in ascending order and then pairing each element from the left list with the corresponding element in the right list based on their positions.
- The "distance" between each pair is the absolute difference between their values.
- The final output is the sum of all distances calculated for each pair.

### Input Processing

1. **Parse the Input**: The input consists of pairs of numbers, each representing a location ID from the left and right lists, respectively. These pairs are separated by spaces and each pair is on a new line.
   
   - Split the input by new lines to separate each pair.
   - For each line, split by space to separate the left list ID from the right list ID.
   - Convert each ID into an integer to facilitate sorting and arithmetic operations.

2. **Store the IDs**: Create two separate arrays or lists, one for each set of IDs (left and right). Populate these arrays with the parsed integers.

3. **Sort the Lists**: Sort both arrays in ascending order to align them for pairwise comparison.

### Solution Strategy

1. **Initialize a Total Distance Variable**: Start with a variable to accumulate the total distance, initialized to 0.

2. **Iterate and Compare**: Loop through the sorted lists simultaneously, since they are now aligned by their sorted order.
   
   - For each pair (i.e., the ith element of the left list paired with the ith element of the right list), calculate the distance: `abs(left[i] - right[i])`.
   - Add this distance to the total distance accumulator.

3. **Handle Unequal Lists**: If the lists have unequal lengths, decide on a policy for handling unmatched elements. Given the problem description, it appears all elements should have a match, but it's good practice to account for potential discrepancies.
   
   - If the left list is longer, you might consider the unmatched elements as having a distance equal to their value (or some other policy).
   - Similarly, handle any extra elements in the right list based on the chosen policy.

4. **Return the Total Distance**: After iterating through both lists and summing up all distances, return the total distance as the final output.

### Expected Output

The solution should output a single integer representing the total distance between the two reconciled lists of location IDs.

### Edge Cases

1. **Empty Lists**: If one or both input lists are empty, the total distance should be calculated accordingly, likely resulting in a total distance of 0 or the sum of all elements in the non-empty list, depending on the handling policy.
   
2. **Unequal Lengths**: As mentioned, a policy should be in place for handling lists of unequal lengths, even if it's expected that all provided inputs will have matched pairs.

3. **Duplicate IDs**: If there are duplicate IDs within a list, the sorting step will naturally group them together. Ensure the pairwise comparison still aligns correctly with these duplicates.

4. **Large Numbers**: Ensure the solution can handle large integers that might exceed typical integer bounds in certain programming languages.

By following this detailed specification, the problem of reconciling the two lists of location IDs can be systematically approached and solved.