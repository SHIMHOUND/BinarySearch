import time
import random
import matplotlib.pyplot as plt
import csv


# --- Part A: Sorting Algorithms ---

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
    return arr


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def time_sorting_algorithms(sizes):
    results = {}
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
    }

    for size in sizes:
        arr = [random.randint(0, size * 10) for _ in range(size)]  # Added larger range to create duplicates
        results[size] = {}
        for name, func in algorithms.items():
            start_time = time.time()
            func(arr.copy())  # Sort a copy of the array
            end_time = time.time()
            results[size][name] = end_time - start_time
    return results


def plot_sorting_results(results, filename="sorting_times.png"):
    sizes = sorted(results.keys())
    algorithms = list(results[sizes[0]].keys())

    plt.figure(figsize=(12, 8))
    for name in algorithms:
        times = [results[size][name] for size in sizes]
        plt.plot(sizes, times, label=name)
    plt.xlabel("Input Size")
    plt.ylabel("Running Time (seconds)")
    plt.title("Comparison of Sorting Algorithm Runtimes")
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)


# --- Part B: Credit Card Matching ---
def generate_credit_card_data(num_records):
    networks = ["Visa", "MasterCard", "American Express", "JCB", "Maestro", "Visa Electron", "Diners Club", "RuPay",
                "Maestro UK"]

    records = []

    for i in range(num_records):
        expiry_year = random.randint(2024, 2030)
        expiry_month = random.randint(1, 12)
        expiry_date = f"{expiry_month:02}/{expiry_year}"

        pin = random.randint(1000, 9999)
        card_number = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        verification_code = random.randint(100, 999)
        issuing_network = random.choice(networks)

        records.append([card_number, expiry_date, verification_code, pin, issuing_network])

    return records


def write_to_csv(data, filename):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Credit Card Number", "Expiry Date", "Verification Code", "PIN", "Issueing Network"])
        writer.writerows(data)


def linear_match(dataset1, dataset2):
    matched = []
    dataset2_dict = {row[0]: row for row in dataset2}
    for row1 in dataset1:
        card_number = row1[0]
        if card_number in dataset2_dict:
            matched.append((row1, dataset2_dict[card_number]))
    return matched


def log_linear_match(dataset1, dataset2):
    dataset2_sorted = sorted(dataset2, key=lambda row: row[0])  # Log-linear sort
    matched = []
    for row1 in dataset1:
        card_number = row1[0]
        low = 0
        high = len(dataset2_sorted) - 1
        while low <= high:
            mid = (low + high) // 2
            if dataset2_sorted[mid][0] == card_number:
                matched.append((row1, dataset2_sorted[mid]))
                break
            elif dataset2_sorted[mid][0] < card_number:
                low = mid + 1
            else:
                high = mid - 1
    return matched


def time_matching_algorithms(sizes):
    results = {}
    algorithms = {
        "Linear Match": linear_match,
        "Log-Linear Match": log_linear_match,
    }

    for size in sizes:
        dataset1 = generate_credit_card_data(size)
        dataset2 = generate_credit_card_data(size)
        random.shuffle(dataset2)
        results[size] = {}
        for name, func in algorithms.items():
            start_time = time.time()
            func(dataset1, dataset2)
            end_time = time.time()
            results[size][name] = end_time - start_time
    return results


def plot_matching_results(results, filename="matching_times.png"):
    sizes = sorted(results.keys())
    algorithms = list(results[sizes[0]].keys())

    plt.figure(figsize=(12, 8))
    for name in algorithms:
        times = [results[size][name] for size in sizes]
        plt.plot(sizes, times, label=name)
    plt.xlabel("Input Size")
    plt.ylabel("Running Time (seconds)")
    plt.title("Comparison of Matching Algorithm Runtimes")
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)


# --- Main execution ---
if __name__ == "__main__":
    # Task A: Sorting
    small_sizes = [5, 10, 20, 30, 40, 50]
    large_sizes = [100, 500, 1000, 5000, 10000]
    sorting_results_small = time_sorting_algorithms(small_sizes)
    sorting_results_large = time_sorting_algorithms(large_sizes)

    plot_sorting_results(sorting_results_small, "sorting_times_small.png")
    plot_sorting_results(sorting_results_large, "sorting_times_large.png")

    # Task B: Matching
    matching_sizes = [100, 500, 1000, 5000, 10000, 20000]
    matching_results = time_matching_algorithms(matching_sizes)

    plot_matching_results(matching_results, "matching_times.png")

    # Generate Credit Card Data
    card_data = generate_credit_card_data(20000)
    write_to_csv(card_data, "carddump1.csv")
    card_data_shuffled = card_data.copy()
    random.shuffle(card_data_shuffled)
    write_to_csv(card_data_shuffled, "carddump2.csv")

    print("Card data files created: carddump1.csv and carddump2.csv.")
    print("Graphs created: sorting_times_small.png, sorting_times_large.png, and matching_times.png")