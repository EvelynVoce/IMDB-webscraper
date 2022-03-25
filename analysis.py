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


#  RECORDING RESULTS:
times_125 = [0.7312756000028457, 2.234334200009471, 5.2900402000086615, 8.616632000004756, 15.225275400007376,
             22.891969800009974, 37.68510119999701, 74.65351410000585, 175.25230530000408, 377.24697809999634,
             678.2674625000072, 1033.5426410000073, 1309.1564021000086, 1463.7566645000043, 1541.8814608999965,
             1579.0557545000047, 1601.119038200006, 1612.5880004000064, 1616.448023200006]

csv_rows_125 = [1, 8, 30, 51, 80, 127, 235, 509, 1202, 2439, 3848, 4926, 5485, 5769, 5916, 5984, 6025, 6040, 6041]

links_checked_rows_125 = [1, 13, 42, 70, 125, 205, 365, 771, 1875, 4174, 7672, 11795, 14876, 16601, 17467, 17901,
                          18141, 18272, 18310]


times_75 = [0.7529272999963723, 2.833102800010238, 6.749618600006215, 10.099141899991082, 14.840400699991733,
            25.315793499990832, 53.6500459999952, 118.76984600001015, 314.63910100000794, 736.8183178000036,
            1437.8533433999983, 2262.7544543000113, 2941.199482099997, 3342.21304100001, 3561.662223799998,
            3662.5079627000086, 3714.2842642999894, 3739.0363727000076, 3746.882399199996, 3750.0064738999936,
            3751.703008200013]

csv_rows_75 = [1, 9, 30, 51, 77, 132, 246, 571, 1446, 3157, 5330, 7073, 8055, 8545,
               8777, 8897, 8951, 8970, 8974, 8976, 8976]

links_checked_rows_75 = [1, 13, 42, 69, 115, 203, 396, 853, 2218, 5195, 10177, 16105,
                         20978, 23894, 25515, 26291, 26687, 26871, 26932, 26955, 26965]


times_20 = [2.622760099999141, 5.3922136000182945, 8.588826699997298, 11.80653010000242, 16.957833699998446,
            24.926257800019812, 46.41941390000284, 98.89623740001116, 258.2024672999978, 683.7612237000139,
            1567.9847641000233, 2855.3819809000124, 4118.067279600014, 4991.211491399998, 5495.102902400016,
            5766.290317800012, 5906.4606957000215, 5962.792101800005, 5984.969308800006, 5996.46351250002,
            6002.199678900011, 6006.281657700019, 6009.838799500023, 6012.948164900008, 6014.698797200021]

csv_rows_20 = [1, 9, 31, 53, 82, 139, 292, 721, 1998, 5313, 11240, 17556, 21704, 23934, 25016,
               25538, 25739, 25835, 25872, 25892, 25903, 25909, 25910, 25911, 25911]

links_checked_rows_20 = [1, 13, 42, 70, 126, 215, 454, 1053, 2945, 8036, 18433, 33279, 47132, 56757,
                         62164, 64935, 66377, 66994, 67232, 67353, 67406, 67439, 67458, 67459, 67461]


def make_plots():
    plt.title("A graph to show the rate of growth of the films.csv file compared to links_scraped.txt")
    plt.xlabel("Number of items")
    plt.ylabel("Run-time (seconds)")

    plt.plot(csv_rows_20, times_20, color='red', marker='o', label='films.csv (20)')
    plt.plot(csv_rows_75, times_75, color='orange', marker='o', label='films.csv (75)')
    plt.plot(csv_rows_125, times_125, color='green', marker='o', label='films.csv (125)')

    #
    # plt.plot(links_checked_rows_20, times_20, color='red', marker='o', label='links_scraped.txt (20)')
    # plt.plot(links_checked_rows_75, times_75, color='orange', marker='o', label='links_scraped.txt (75)')
    # plt.plot(links_checked_rows_125, times_125, color='green', marker='o', label='links_scraped.txt (125)')

    plt.legend()
    plt.savefig('test2.png', bbox_inches="tight")


if __name__ == "__main__":
    make_plots()
