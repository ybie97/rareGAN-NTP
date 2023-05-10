import numpy as np
import glob
import pandas as pd
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
import matplotlib.pylab as pl
import seaborn as sns
from itertools import cycle, islice
import matplotlib.pyplot as plt
import argparse 
import os 

parser = argparse.ArgumentParser()#help="--fields_path , --data_folder_name  --proto  ")
parser.add_argument('--bd', type=str, default="all",  help = "budget ")
parser.add_argument('--type', type=str, default="all",  help = "budget ")
parser.add_argument('--out_dir', type=str, default="figs",  help = "budget ")
parser.add_argument('--parsed_data', type=str, default="data_dir",  help = "figs is an example ")
args = parser.parse_args()

ntp_types = {
    0: "PEER", 1: "PEER", 4: "SINFO", 6: "IOSTATS", 7: "MSTATS", 9: "TSTATS",
    11: "UCONFIG", 12: "SETFLAG", 13: "CLRFLAG", 16: "RESTRICT", 22: "REPEER",
    23: "REKEYS", 29: "TRAPS", 31: "CLRTRAP", 34: "GETSTATS", 38: "GETKERNEL",
    41: "SETPREC", 43: "HOSTID"
}

def calc_diversity():
    data_dir = os.path.join(os.getcwd(), args.parsed_data)
    all_folders = [x for x in os.listdir(data_dir)]
    if args.bd == "all":
        all_folders = list(filter(lambda x: x[:5] == "query", all_folders))
    else:
        all_folders = list(filter(lambda x: x[:5] == "query" and x.split("_")[4] == args.bd, all_folders))
    # print("all_folders: ", all_folders)

    df = pd.DataFrame()
    for folder in all_folders:
        all_queries_file = os.path.join(data_dir, folder, "complete_info.csv")
        print("Reading all queries files: ", all_queries_file)
        new_df = pd.read_csv(all_queries_file)
        df = pd.concat([df, new_df], ignore_index=True, sort=False)
        print(df.shape)


    # df = df[df.amp_fac != 1]
    b4 = len(df)
    print(len(df), df.head())
    df = df.drop(columns=["amp_fac"])
    df = df.drop_duplicates()
    a4 = len(df)
    print(len(df), df.head())

    print("diversity: ", a4/b4*100)

def calc_total_risk():
    data_dir = os.path.join(os.getcwd(), args.parsed_data)
    all_folders = [x for x in os.listdir(data_dir)]
    if args.bd == "all":
        all_folders = list(filter(lambda x: x[:5] == "query", all_folders))
    else:
        all_folders = list(filter(lambda x: x[:5] == "query" and x.split("_")[4] == args.bd, all_folders))
    print("all_folders: ", all_folders)

    df = pd.DataFrame()
    for folder in all_folders:
        all_queries_file = os.path.join(data_dir, folder, "complete_info.csv")
        print("Reading all queries files: ", all_queries_file)
        new_df = pd.read_csv(all_queries_file)
        df = pd.concat([df, new_df], ignore_index=True, sort=False)
        print(df.shape)

    code = 1
    df = df[df.request_code == code]
    print(df.head())
    # df = df.drop_duplicates(["request_code"])
    # df = df[df.amp_fac != 1]
    total = df["amp_fac"].sum()
    print(f"total for {args.bd}: {total}, {df.shape}")


# from scipy.stats import wasserstein_distance
# def calc_fidelity():
#     res = wasserstein_distance([1,2,3,4,5], [1,2,3,4,5,6,7,8,9])
#     print(res)

def get_max():
    data_dir = os.path.join(os.getcwd(), args.parsed_data)
    all_folders = [x for x in os.listdir(data_dir)]
    if args.bd == "all":
        all_folders = list(filter(lambda x: x[:5] == "query", all_folders))
    else:
        all_folders = list(filter(lambda x: x[:5] == "query" and x.split("_")[4] == args.bd, all_folders))
    print("all_folders: ", all_folders)

    x_num = []
    y_num = []
    for th in ["5", "10", "15", "20", "30"]:
        th_file = list(filter(lambda x: x.split("_")[3] == th, all_folders))[0]
        all_queries_file = os.path.join(data_dir, th_file, "complete_info.csv")
        print("Reading all queries files: ", all_queries_file)
        new_df = pd.read_csv(all_queries_file)
        y_num += list(new_df["amp_fac"])
        x_num += [th]*len(new_df["amp_fac"])
        print(len(y_num), len(x_num))

    plt.figure(figsize=(10, 7))
    sns.boxplot(x=x_num, y=y_num)

    out_dir = os.path.join(os.getcwd(), args.out_dir, "fig3")
    if not os.path.exists(out_dir):
        print(f"creating: {out_dir}")
        os.makedirs(out_dir)

    # num_list = len(list(ntp_types.keys()))
    # plt.xticks(np.arange(0, num_list), ntp_types.values(), rotation=45)
    # plt.tick_params(axis='x', labelsize=5)
    plt.xlabel("Threshold")
    plt.ylabel("Amplification Factor")
    plt.title(f'AF vs Threshold for Budget Size of {args.bd}')
    # plt.savefig(fname , bbox_inches='tight')
    plt.savefig(os.path.join(out_dir, f"AF_thresh_num_{args.bd}.png"))
    plt.show()


if __name__ == '__main__':
    if args.type == "div":
        calc_diversity()
    # elif args.type == "fid":
    #     calc_fidelity()
    elif args.type == "total":
        calc_total_risk()
    elif args.type == "max":
        get_max()
    elif args.type == "all":
        calc_diversity()
        # calc_fidelity()
        calc_total_risk()
        get_max()
    else:
        print(f"invalid type?: {args.type}")
