import numpy as np
import sys
import os
from pathlib import Path
cdir = os.getcwd()
rareGan_filepath = Path(cdir).parents[1].resolve()
ampmap_data_dir_filepath = os.path.join(rareGan_filepath.parents[0], "ampmap-main", "postprocess", "data_dir")

if not os.path.exists(ampmap_data_dir_filepath):
    print(f"your ampmap-main > postprocess > data_dir do not exist: {ampmap_data_dir_filepath}")
    exit(666)

sys.path.append(str(rareGan_filepath))

from lib.data.input_definition import InputDefinition
import pprint
import csv

files = {
    "20000": ["bgt-20000,threshold-10.npz", "bgt-20000,threshold-5.npz", "bgt-20000,threshold-15.npz",
              "bgt-20000,threshold-20.npz", "bgt-20000,threshold-30.npz"],
    "200000": ["bgt-200000,threshold-5.npz", "bgt-200000,threshold-20.npz", "bgt-200000,threshold-10.npz",
               "bgt-200000,threshold-15.npz", "bgt-200000,threshold-30.npz"]
         }
thresh = 999
budget = "20000"
if __name__ == '__main__':
    if len(sys.argv) == 3:
        budget = sys.argv[1]
        thresh = sys.argv[2]
        files = list(filter(lambda f: f[4:-4].startswith(budget + ",") and f[4:-4].endswith("-" + thresh), files[budget]))
        print(f"testing ntp_private files with threshold: {thresh} and budget: {budget}", files)
    else:
        print("need to give threshold and budget")
        exit(666)

    if len(files) == 0:
        print(f"no files found with threshold: {thresh} and budget: {budget}")
        exit(666)

    # budget = budget[:-1]
    # thresh
    # print(files)
    # exit(0)

    input_definition = InputDefinition("../../input_definitions/ntp_private_input_definition.json")
    output = []
    for tf in files:
        generated_data = np.load(f"../../generated_data/{tf}")
        generated_data_field_dict = input_definition.numpy_to_field_dict(generated_data['numpy_inputs'])
        generated_data_amp = generated_data['amplifications']


        for gd in range(len(generated_data_field_dict)):
            generated_data_field_dict[gd]["amp_fac"] = generated_data_amp[gd]
            generated_data_field_dict[gd]["server_id"] = "IP_8080"
            generated_data_field_dict[gd]["data"] = "dummy"

        output += generated_data_field_dict

    save_data_dir = os.path.join(ampmap_data_dir_filepath, f"query_searchout_NTPPrivate_{thresh}_{budget}")
    if not os.path.exists(save_data_dir):
        print(f"making a new directory: {save_data_dir}")
        os.makedirs(save_data_dir)

    with open(f"{save_data_dir}/complete_info.csv", "w", newline="") as f:
        title = "amp_fac,server_id,auth,data_item_size,err,implementation,mbz,mode,more,nb_items,request_code,response,seq,version,data".split(",")  # quick hack
        cw = csv.DictWriter(f, title, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        cw.writeheader()
        cw.writerows(output)

    print(f"completed: query_searchout_NTPPrivate_{thresh}_{budget}" )



