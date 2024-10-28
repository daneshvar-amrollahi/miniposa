import pandas as pd
import os
import argparse
from benchmark_categorization import categorize  # Import functions from the other file
import numpy as np  # Import numpy for variance calculation
import matplotlib.pyplot as plt  # For plotting

def load_csv_files(csv_directory):
    """
    Load all CSV files from a given directory into a list of pandas DataFrames.
    
    Parameters:
    - csv_directory (str): The path to the directory containing the CSV files.

    Returns:
    - dataframes (list): A list of pandas DataFrames, one for each CSV file.
    """
    csv_files = [os.path.join(csv_directory, file) for file in os.listdir(csv_directory) if file.endswith('.csv')]
    csv_files.sort()
    dataframes = [pd.read_csv(file) for file in csv_files]
    return dataframes

def calculate_sample_success_rate(dataframes, index):
    """
    Calculate the sample success rate for a single benchmark across all CSV files.

    Parameters:
    - dataframes (list): A list of pandas DataFrames, each representing a mutant sample.
    - index (int): The row index corresponding to the benchmark.

    Returns:
    - sample_success_rate (float): The success rate (number of 'ok' results) for the benchmark.
    """
    ok_count = sum(1 for df in dataframes if df.iloc[index]['status'] == 'ok')
    sample_success_rate = ok_count / len(dataframes)
    return sample_success_rate

def process_benchmarks(dataframes):
    """
    Process each benchmark across all CSV files and categorize them.
    
    Returns:
    - results (dict): A dictionary with counts for each category.
    - sample_success_rates (list): A list of sample success rates for each benchmark.
    """
    categories_count = {"stable": 0, "unstable": 0, "unsolvable": 0, "inconclusive": 0}
    unstable_benchmarks = []
    num_benchmarks = len(dataframes[0])
    sample_success_rates = []  # List to store the success rates of each benchmark

    for i in range(num_benchmarks):
        sample_success_rate = calculate_sample_success_rate(dataframes, i)
        sample_success_rates.append(sample_success_rate)  # Collect sample success rate
        
        # Extract total times
        total_times = []
        for df in dataframes:
            if pd.notna(df.iloc[i]['total_time']) and isinstance(df.iloc[i]['total_time'], (int, float)):
                if df.iloc[i]['status'] == 'ok':
                    total_times.append(df.iloc[i]['total_time'])

        if len(total_times) == 0: # This benchmark is unsolvable
            categories_count["unsolvable"] += 1
            continue


        T_mean = np.mean(total_times)
        
        # Categorize benchmark
        category = categorize(sample_success_rate, T_mean)
        categories_count[category] += 1

        if category == "unstable":
            benchmark_name = dataframes[0].iloc[i]['benchmark']
            unstable_benchmarks.append(benchmark_name)
            # print(f"Unstable benchmark: {benchmark_name}")
            # print("Sample success rate:", sample_success_rate)
            # print()

    return categories_count, unstable_benchmarks


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process CSV files for SMT solver categorization.')
    parser.add_argument('csv_directory', type=str, help='Directory containing CSV files')
    args = parser.parse_args()

    # Load CSV files from the provided directory
    dataframes = load_csv_files(args.csv_directory)

    # Process benchmarks and categorize
    results, unstable_benchmarks = process_benchmarks(dataframes)

    # Print the results
    print("Categorization Results:")
    print(results)


if __name__ == "__main__":
    main()
