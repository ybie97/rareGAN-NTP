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
parser.add_argument('--out_dir', type=str, default="figs",  help = "figs is an example ")
parser.add_argument('--parsed_data', type=str, default="data_dir",  help = "figs is an example ")
args = parser.parse_args()



ntp_types = {
    0: "PEER", 1: "PEER", 4: "SINFO", 6: "IOSTATS", 7: "MSTATS", 9: "TSTATS",
    11: "UCONFIG", 12: "SETFLAG", 13: "CLRFLAG", 16: "RESTRICT", 22: "REPEER",
    23: "REKEYS", 29: "TRAPS", 31: "CLRTRAP", 34: "GETSTATS", 38: "GETKERNEL",
    41: "SETPREC", 43: "HOSTID"
}

data_dir = os.path.join(os.getcwd(), args.parsed_data)
all_folders = [x for x in os.listdir(data_dir)]
all_folders = list(filter(lambda x: x[:5] == "query", all_folders))
# print("all_folders: ", all_folders)

df = pd.DataFrame()
for folder in all_folders:
    all_queries_file = os.path.join(data_dir, folder, "complete_info.csv")
    print("Reading all queries files: ", all_queries_file)
    new_df = pd.read_csv(all_queries_file)
    df = pd.concat([df, new_df], ignore_index=True, sort=False)
    print(df.shape)


df = df[df.amp_fac != 1]
plt.figure(figsize=(10,7))
sns.boxplot(x=df["request_code"], y=df["amp_fac"])

out_dir = os.path.join(os.getcwd(), args.out_dir, "fig2")
if not os.path.exists(out_dir):
    print(f"creating: {out_dir}")
    os.makedirs(out_dir)

num_list = len(list(ntp_types.keys()))
# plt.xticks(np.arange(0, num_list), ntp_types.values(), rotation=45)
# plt.tick_params(axis='x', labelsize=5)
plt.xlabel("Query Pattern(QP)")
plt.ylabel("Amplification Factor")
plt.title('AF vs Query Pattern')
# plt.savefig(fname , bbox_inches='tight')
plt.savefig(os.path.join(out_dir, "AF_qp_num.png"))
plt.show()
