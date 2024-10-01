# process_benchmarks.py

import pandas as pd
import os
import argparse
from benchmark_categorization import categorize  # Import functions from the other file

def load_csv_files(csv_directory):
    """
    Load all CSV files from a given directory into a list of pandas DataFrames.
    
    Parameters:
    - csv_directory (str): The path to the directory containing the CSV files.

    Returns:
    - dataframes (list): A list of pandas DataFrames, one for each CSV file.
    """
    # Use a list comprehension to get all CSV file paths in the directory
    csv_files = [os.path.join(csv_directory, file) for file in os.listdir(csv_directory) if file.endswith('.csv')]
    
    # Sort files to maintain order (if necessary)
    csv_files.sort()

    # Read all CSV files into a list of DataFrames
    dataframes = [pd.read_csv(file) for file in csv_files]
    
    return dataframes

def calculate_sample_success_rate(dataframes, index):
    """
    Calculate the sample success rate for a single benchmark across all CSV files.

    Parameters:
    - dataframes (list): A list of pandas DataFrames, each representing a mutant sample.
    - index (int): The row index corresponding to the benchmark.

    Returns:
    - sample_success_rate (float): The success rate (number of 'unsat' results) for the benchmark.
    """
    # Count the number of 'unsat' results for the given benchmark (index) across all DataFrames
    unsat_count = sum(1 for df in dataframes if df.iloc[index]['result'] == 'unsat')
    
    # Calculate the sample success rate as the number of 'unsat' results over the total number of CSV files
    sample_success_rate = unsat_count / len(dataframes)
    
    return sample_success_rate

def process_benchmarks(dataframes):
    """
    Process each benchmark across all CSV files and categorize them.

    Parameters:
    - dataframes (list): A list of pandas DataFrames, each representing a mutant sample.

    Returns:
    - results (dict): A dictionary with counts for each category (stable, unstable, unsolvable, inconclusive).
    """
    # Initialize counts for each category
    categories_count = {"stable": 0, "unstable": 0, "unsolvable": 0, "inconclusive": 0}
    
    # Get the number of benchmarks (assumes all CSVs have the same number of benchmarks)
    num_benchmarks = len(dataframes[0])

    # Process each benchmark (by row index)
    for i in range(num_benchmarks):
        # Calculate sample success rate for the current benchmark
        sample_success_rate = calculate_sample_success_rate(dataframes, i)
        
        # Example: Extract mean time (T_mean) for the benchmark
        # Here we take the average CPU time (time_cpu) across all CSV files for the same benchmark
        T_mean = sum(df.iloc[i]['time_cpu'] for df in dataframes) / len(dataframes)

        # Categorize the benchmark
        category = categorize(sample_success_rate, T_mean)

        # Update the count for the determined category
        categories_count[category] += 1

    return categories_count

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process CSV files for SMT solver categorization.')
    parser.add_argument('csv_directory', type=str, help='Directory containing CSV files')

    # Parse arguments
    args = parser.parse_args()

    # Load CSV files from the provided directory
    dataframes = load_csv_files(args.csv_directory)

    # Process benchmarks and categorize
    results = process_benchmarks(dataframes)

    # Print the results
    print("Categorization Results:")
    print(results)  # Output the count of each category

if __name__ == "__main__":
    main()

# Example of how to run the code from the command line:
# python process_benchmarks.py data/
# Replace 'data/' with the actual path to your directory containing the CSV files.
