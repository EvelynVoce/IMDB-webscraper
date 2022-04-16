from matplotlib import pyplot as plt
from file_handling import get_number_of_items
from time import perf_counter

times = []
csv_rows = []
links_checked_rows = []


def make_plot():
    plt.title("A graph to show the rate of growth of the films.csv file compared to links_scraped.txt")
    plt.xlabel("Number of items")
    plt.ylabel("Run-time (seconds)")
    plt.plot(csv_rows, times, color='blue', marker='o', label='films.csv')
    plt.plot(links_checked_rows, times, color='red', marker='o', label='links_scraped.txt')
    plt.legend()
    plt.savefig('test.png', bbox_inches="tight")

    print(f"times: {times}\n"
          f"csv_rows: {csv_rows}\n"
          f"links_checked_rows: {links_checked_rows}")


def run_analysis(t1):
    t2 = perf_counter()
    with open("films_completed.txt", 'r') as fp:
        num_scraped = len(fp.readlines())

    num_rows: int = get_number_of_items()
    print(f"Iteration completed in: {t2 - t1} - There are {num_rows} rows in the csv and"
          f" {num_scraped} links checked")

    times.append(t2 - t1)
    csv_rows.append(num_rows)
    links_checked_rows.append(num_scraped)