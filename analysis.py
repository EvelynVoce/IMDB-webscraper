from matplotlib import pyplot as plt
from file_handling import performance_test
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

    print(f"times: {times}")
    print(f"csv_rows: {csv_rows}")
    print(f"links_checked_rows: {links_checked_rows}")


def run_analysis(t1):
    t2 = perf_counter()
    num_rows = performance_test()
    with open("films_completed.txt", 'r') as fp:
        num_scraped = len(fp.readlines())

    print(f"Iteration completed in: {t2 - t1} - There are {num_rows} rows in the csv and"
          f" {num_scraped} links checked")

    times.append(t2 - t1)
    csv_rows.append(num_rows)
    links_checked_rows.append(num_scraped)


# #  RECORDING RESULTS:
# times_125 = [0.7312756000028457, 2.234334200009471, 5.2900402000086615, 8.616632000004756, 15.225275400007376,
#              22.891969800009974, 37.68510119999701, 74.65351410000585, 175.25230530000408, 377.24697809999634,
#              678.2674625000072, 1033.5426410000073, 1309.1564021000086, 1463.7566645000043, 1541.8814608999965,
#              1579.0557545000047, 1601.119038200006, 1612.5880004000064, 1616.448023200006]
#
# csv_rows_125 = [1, 8, 30, 51, 80, 127, 235, 509, 1202, 2439, 3848, 4926, 5485, 5769, 5916, 5984, 6025, 6040, 6041]
#
# links_checked_rows_125 = [1, 13, 42, 70, 125, 205, 365, 771, 1875, 4174, 7672, 11795, 14876, 16601, 17467, 17901,
#                           18141, 18272, 18310]
#
#
# def make_plots():
#     plt.title("A graph to show the rate of growth of the films.csv file compared to links_scraped.txt")
#     plt.xlabel("Number of items")
#     plt.ylabel("Run-time (seconds)")
#
#     plt.plot(csv_rows_125, times_125, color='blue', marker='o', label='films.csv (125)')
#     plt.plot(links_checked_rows_125, times_125, color='red', marker='o', label='links_scraped.txt (125)')
#
#     plt.legend()
#     plt.savefig('test.png', bbox_inches="tight")
#
#     print(f"times: {times}")
#     print(f"csv_rows: {csv_rows}")
#     print(f"links_checked_rows: {links_checked_rows}")
