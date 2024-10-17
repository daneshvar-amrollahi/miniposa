
import math

def unsolvability_test(sample_success_rate, sample_size, r_solvable=0.05, alpha=-1.645):
    """
    Test whether the solving rate is less than the solvable rate.

    H0: r >= r_solvable
    HA: r < r_solvable
    """
    if sample_success_rate >= r_solvable:
        return False  # Fail to reject H0 because r >= r_solvable
    
    # Calculate the standard error for proportions
    standard_error = math.sqrt((r_solvable * (1 - r_solvable)) / sample_size)
    
    # Calculate the z-score
    z_score = (sample_success_rate - r_solvable) / standard_error
    
    # print("z_score for solvability test: ", z_score)

    # Return True if H0 is rejected (r < r_solvable), False otherwise
    return z_score < alpha


def instability_test(sample_success_rate, sample_size, r_stable=0.95, alpha=-1.645):
    """
    Test whether the solving rate is less than the stable rate.

    H0: r >= r_stable
    HA: r < r_stable
    """

    if sample_success_rate >= r_stable:
        return False

    # Calculate the standard error for proportions
    standard_error = math.sqrt((r_stable * (1 - r_stable)) / sample_size)
    
    # Calculate the z-score
    z_score = (sample_success_rate - r_stable) / standard_error
    
    # print("z_score for instability test: ", z_score)

    # Return True if H0 is rejected (r < r_stable), False otherwise
    return z_score < alpha


def stability_test(sample_success_rate, sample_size, r_stable=0.95, alpha=-1.645):
    """
    Test whether the solving rate is at least the stable rate.

    H0: r < r_stable
    HA: r >= r_stable
    """
    if sample_success_rate < r_stable:
        return False  # Fail to reject H0 because r < r_stable

    # Calculate the standard error for proportions
    standard_error = math.sqrt((r_stable * (1 - r_stable)) / sample_size)
    
    # Calculate the z-score
    z_score = (sample_success_rate - r_stable) / standard_error
    
    # print("z_score for stability test: ", z_score)

    # Since this is testing for "greater than or equal to," we use the opposite tail
    return z_score > -alpha  # -alpha for the upper tail at 0.05




def solvability_test(sample_success_rate, sample_size, r_solvable=0.05, alpha=-1.645):
    """
    Test whether the solving rate is at least the stable rate.

    H0: r < r_solvable
    HA: r >= r_solvable
    """
    if sample_success_rate < r_solvable:
        return False  # Fail to reject H0 

    # Calculate the standard error for proportions
    standard_error = math.sqrt((r_solvable * (1 - r_solvable)) / sample_size)
    
    # Calculate the z-score
    z_score = (sample_success_rate - r_solvable) / standard_error
    
    # print("z_score for stability test: ", z_score)

    # Since this is testing for "greater than or equal to," we use the opposite tail
    return z_score > -alpha  # -alpha for the upper tail at 0.05











def categorize(sample_success_rate, T_mean, sample_size=60 , T_limit=60, omega=0.8):
    """
    Categorize a benchmark as unsolvable/unstable/stable/inconclusive.

    Parameters:
    - sample_success_rate (float): The observed success rate (r̂) in the sample.
    - sample_size (int): The number of samples (n).
    - T_mean (float): The mean time to solve the benchmark.
    - T_limit (int): The time limit for the benchmark (default is 60 seconds).
    - omega (float): For tolerance testing (default is 0.8).

    Returns:
    - (str): The category of the benchmark (unsolvable/unstable/stable/inconclusive).
    """
    # print()
    # print("sample_success_rate: ", sample_success_rate)

    # Check for solvability
    reject_solvable = unsolvability_test(sample_success_rate, sample_size)
    if reject_solvable:
        # print("unsolvable")
        # print()
        return "unsolvable"
    
    reject_unsolvable = solvability_test(sample_success_rate, sample_size)
    # if not reject_unsolvable:
        # print("inconclusive")
    #     # print()
    #     return "inconclusive"

    # Check for instability
    reject_instable = instability_test(sample_success_rate, sample_size)
    # print("T_mean " , T_mean)
    
    # if reject_instable and T_mean < omega * T_limit:
    if reject_instable and T_mean < omega * T_limit:
        # print("reject_instable is True")
        # print("unstable")
        # print()
        return "unstable"
    
    # Check for stability
    reject_stable = stability_test(sample_success_rate, sample_size)
    if reject_stable:
        # print("stable")
        # print()
        return "stable"

    # print("inconclusive")
    # print()
    return "inconclusive"
