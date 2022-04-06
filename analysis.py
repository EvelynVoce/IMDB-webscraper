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

times_75 = [0.9641334000043571, 3.356653599999845, 6.401704100018833, 9.059829000005266, 12.673498900025152, 20.139055500010727, 35.267940700025065, 73.22282490000362, 177.61070270001073, 408.86400480000884, 817.0614983000269, 1369.0180751000007, 1853.5027336000057, 2175.1782354000024, 2336.2042249000224, 2417.967430400022, 2457.686892800004, 2476.398890900018, 2485.0464459000214, 2488.669798100018, 2490.018602700002]
csv_rows_75 = [1, 8, 28, 45, 71, 120, 226, 520, 1313, 2883, 4965, 6794, 7887, 8463, 8735, 8873, 8938, 8961, 8969, 8971, 8971]
links_checked_rows_75 = [1, 13, 40, 60, 96, 175, 351, 776, 2011, 4688, 9256, 15114, 20215, 23470, 25273, 26262, 26745, 26982, 27063, 27102, 27103]

# times_20 = [2.622760099999141, 5.3922136000182945, 8.588826699997298, 11.80653010000242, 16.957833699998446,
#             24.926257800019812, 46.41941390000284, 98.89623740001116, 258.2024672999978, 683.7612237000139,
#             1567.9847641000233, 2855.3819809000124, 4118.067279600014, 4991.211491399998, 5495.102902400016,
#             5766.290317800012, 5906.4606957000215, 5962.792101800005, 5984.969308800006, 5996.46351250002,
#             6002.199678900011, 6006.281657700019, 6009.838799500023, 6012.948164900008, 6014.698797200021]
#
# csv_rows_20 = [1, 9, 31, 53, 82, 139, 292, 721, 1998, 5313, 11240, 17556, 21704, 23934, 25016,
#                25538, 25739, 25835, 25872, 25892, 25903, 25909, 25910, 25911, 25911]
#
# links_checked_rows_20 = [1, 13, 42, 70, 126, 215, 454, 1053, 2945, 8036, 18433, 33279, 47132, 56757,
#                          62164, 64935, 66377, 66994, 67232, 67353, 67406, 67439, 67458, 67459, 67461]

times_20 = [0.9967311000000336, 3.3277292999991914, 6.82746159999806, 9.56548969999858, 13.582197900002939,
            21.497953099998995, 42.21117899999808, 92.04938080000284, 241.9133587000033, 640.5655151000028,
            1487.7875222000002, 2709.3291599000004, 3956.332953899997, 4820.621469700003, 5328.6442322,
            5583.729206900003, 5706.653194500002, 5758.871721399999, 5782.662615699999, 5796.0733712,
            5802.023144400002, 5806.102208299999, 5809.400160600002, 5811.279347600001]

csv_rows_20 = [1, 9, 29, 47, 73, 132, 273, 672, 1842, 5001, 10861, 17185, 21504, 23850, 24968, 25484, 25693, 25805,
               25851, 25872, 25883, 25890, 25892, 25892]

links_checked_rows_20 = [1, 13, 40, 62, 98, 185, 416, 989, 2735, 7520, 17692, 32318, 46324, 56199, 61866, 64751, 66153,
                         66762, 67050, 67202, 67260, 67295, 67322, 67326]


def make_plots():
    plt.title("A graph to show the rate of growth of the links_scraped.txt file across each implemented requirement")
    plt.xlabel("Number of items")
    plt.ylabel("Run-time (seconds)")

    for x, i in zip(csv_rows_20, times_20):
        print(x, i)

    plt.plot(csv_rows_20, times_20, color='red', marker='o', label='films.csv (20)')
    # plt.plot(csv_rows_75, times_75, color='orange', marker='o', label='films.csv (75)')
    # plt.plot(csv_rows_125, times_125, color='green', marker='o', label='films.csv (125)')

    # plt.plot(links_checked_rows_20, times_20, color='red', marker='o', label='links_scraped.txt (20)')
    # plt.plot(links_checked_rows_75, times_75, color='orange', marker='o', label='links_scraped.txt (75)')
    # plt.plot(links_checked_rows_125, times_125, color='green', marker='o', label='links_scraped.txt (125)')

    plt.legend()
    plt.savefig('test2.png', bbox_inches="tight")


if __name__ == "__main__":
    make_plots()
