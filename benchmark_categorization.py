# benchmark_categorization.py

import math

def solvability_test(sample_success_rate, sample_size, r_solvable=0.05, alpha=-1.645):
    """
    Test whether the solving rate is less than the solvable rate.

    H0: r >= r_solvable
    HA: r < r_solvable

    Parameters:
    - sample_success_rate (float): The observed success rate (r̂) in the sample.
    - sample_size (int): The number of samples (n).
    - r_solvable (float): The threshold solvable rate (default is 5%).
    - alpha (float): Critical value for a one-tailed test at alpha=0.05 (default is -1.645).

    Returns:
    - (bool): True if H0 is rejected (r < r_solvable), False otherwise.
    """
    # Calculate the standard error for proportions
    standard_error = math.sqrt((r_solvable * (1 - r_solvable)) / sample_size)
    
    # Calculate the z-score
    z_score = (sample_success_rate - r_solvable) / standard_error
    
    # Return True if H0 is rejected, False otherwise
    return z_score < alpha


def instability_test(sample_success_rate, sample_size, r_stable=0.95, alpha=-1.645):
    """
    Test whether the solving rate is less than the stable rate.

    H0: r >= r_stable
    HA: r < r_stable

    Parameters:
    - sample_success_rate (float): The observed success rate (r̂) in the sample.
    - sample_size (int): The number of samples (n).
    - r_stable (float): The threshold stable rate (default is 95%).
    - alpha (float): Critical value for a one-tailed test at alpha=0.05 (default is -1.645).

    Returns:
    - (bool): True if H0 is rejected (r < r_stable), False otherwise.
    """
    # Calculate the standard error for proportions
    standard_error = math.sqrt((r_stable * (1 - r_stable)) / sample_size)
    
    # Calculate the z-score
    z_score = (sample_success_rate - r_stable) / standard_error
    
    # Return True if H0 is rejected, False otherwise
    return z_score < alpha


def stability_test(sample_success_rate, sample_size, r_stable=0.95, alpha=-1.645):
    """
    Test whether the solving rate is at least the stable rate.

    H0: r < r_stable
    HA: r >= r_stable

    Parameters:
    - sample_success_rate (float): The observed success rate (r̂) in the sample.
    - sample_size (int): The number of samples (n).
    - r_stable (float): The threshold stable rate (default is 95%).
    - alpha (float): Critical value for a one-tailed test at alpha=0.05 (default is -1.645).

    Returns:
    - (bool): True if H0 is rejected (r >= r_stable), False otherwise.
    """
    # Calculate the standard error for proportions
    standard_error = math.sqrt((r_stable * (1 - r_stable)) / sample_size)
    
    # Calculate the z-score
    z_score = (sample_success_rate - r_stable) / standard_error
    
    # Since this is testing for "greater than or equal to," we use the opposite tail
    return z_score > -alpha  # -alpha for the upper tail at 0.05


def categorize(sample_success_rate, T_mean, T_limit=60, omega=0.8):
    """
    Categorize a benchmark as unsolvable/unstable/stable/inconclusive.

    Parameters:
    - sample_success_rate (float): The observed success rate (r̂) in the sample.
    - T_mean (float): The mean time to solve the benchmark.
    - T_limit (int): The time limit for the benchmark (default is 60 seconds).
    - omega (float): For tolerance testing (default is 0.8).

    Returns:
    - (str): The category of the benchmark (unsolvable/unstable/stable/inconclusive).
    """
    
    reject_solvable = solvability_test(sample_success_rate, 60)
    if reject_solvable:
        return "unsolvable"
    
    reject_instable = instability_test(sample_success_rate, 60)
    if reject_instable:
        if not (T_mean >= omega * T_limit):
            return "unstable"
    
    reject_stable = stability_test(sample_success_rate, 60)
    if reject_stable:
        return "stable"

    return "inconclusive"
