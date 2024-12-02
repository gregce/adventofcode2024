### Problem Analysis

The goal is to analyze a series of reports (each a line of numbers) to determine how many of them are "safe" based on specific criteria related to the numbers' sequence. A report is considered safe if:
1. The numbers (levels) are either all increasing or all decreasing.
2. The difference between any two adjacent levels is at least one and at most three.

#### Input Data Sample

```
2 5 6 8 6
87 89 90 93 96 99 99
...
26 28 29 31 32 34
```

### Input Processing

1. **Input Format**: The input will be a multiline string where each line represents a report with space-separated integers (levels).
2. **Parsing**: Split the input string by new lines to get individual reports, then further split each report by spaces to get the individual levels as integers.

### Solution Strategy

1. **Initialization**: Start by initializing a counter for safe reports.
2. **Processing Each Report**:
    - For each report, perform the following steps:
        a. Convert the report into a list of integers (levels).
        b. Determine if the sequence is increasing, decreasing, or neither:
            - **Increasing**: If each subsequent level is greater than the previous one within the allowed difference range (1 to 3).
            - **Decreasing**: If each subsequent level is smaller than the previous one within the allowed difference range (1 to 3).
            - If neither condition is met or if the difference is outside the allowed range, mark the report as unsafe.
        c. If the report is found to be either increasing or decreasing throughout, increment the safe report counter.
3. **Result**: After processing all reports, the value of the safe report counter is the result.

### Expected Output

- The solution should return an integer representing the number of safe reports.

### Edge Cases

1. **Single-Level Reports**: Though not explicitly mentioned, reports with a single level could be considered safe by default as they trivially meet the criteria.
2. **Equal Adjacent Levels**: Reports with two adjacent levels being equal are immediately considered unsafe as they do not meet the increasing or decreasing condition.
3. **Difference Greater Than Three**: If any two adjacent levels have a difference greater than three, the report is unsafe.
4. **Empty Input**: If the input is empty (no reports), the output should be `0`.