# Efficient Batching
This solution efficiently splits large CSV or TSV files containing millions of rows and over 100 columns into smaller, manageable files. The approach ensures that data distribution adheres to key constraints while maintaining flexibility in configuration.\
The solution processes input files with a header row, ensuring structured output.
It is designed to handle realistic large-scale data efficiently.\
Users can configure and execute the process on a standard Linux system.


## Key Features
- Balanced Splitting: The input file is divided into multiple smaller files of approximately equal size. However, the size balancing is secondary to preserving the integrity of grouped data. \
- Grouping: All rows corresponding to a specific group (identified by the first column) are kept together in the same output file, even if it means slight variations in file sizes.\
- Handling Non-Contiguous Data: While most group-related rows appear sequentially, the solution accounts for instances where rows for the same group appear later in the file.\
- Configurable Split Thresholds: Users can define a threshold (T) for splitting based on either row count or disk size (e.g., ensuring output files stay below 10MB).\
- Preserving Data Structure: The column format and all row data remain unchanged across output files.
- Optional Header Inclusion: The solution provides an option to include or exclude the header row in each split file.\

## Requirments
It sould be CSV/TSV and have unique identifier group by the first column.
Python3

## Run instruction:
1. Make sure you have `python3` installed
2. Navigate to the directory or where you held the python file
```sh
cd ./your/path/to/EfficientBatching.py
```
3. Choose your agruments for the run:

```
usage: solution.py [-h] [--include-header] [--threshold THRESHOLD] [--max_size MAX_SIZE] file_path output_path

Split the input file into smaller files of roughly equal size.

positional arguments:
  file_path             path to the file to split
  output_path           output directory to write new files.

options:
  -h, --help            show this help message and exit
  --include-header      to add header in the output files. Not including headers by default
  --threshold THRESHOLD
                        maximum number of rows per new file. Default 50000
  --max_size MAX_SIZE   maximum file size in MB. Default 10 MB
```
4. Run solution.py with your preferred settings
Example of run for the sample data:

```sh
./EfficientBatching.py shared/sample-data/sample.tsv shared/sample-output
```
## Script run steps:
 - Getting the main information from the input file
 - Read the input file and create 2 dictionaries:
     1. How many rows are in each unique group in the file
     2. All text for each group
 - Creating a dictionary that tells which group goes to each output file
 - Writing output files to the chosen directory

