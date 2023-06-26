import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from covdrugsim.mdsim.config import MD_PATH, SINGLE_PLOT_WIDTH, SINGLE_PLOT_HEIGHT, SINGLE_PLOT_LEG_WIDTH, \
    SINGLE_PLOT_LEG_HEIGHT, FOUR_PLOTS_WIDTH, FOUR_PLOTS_HEIGHT, SIX_PLOTS_WIDTH, SIX_PLOTS_HEIGHT

sns.set(context='talk', font_scale=0.8)
CURR_DIR = os.getcwd()


if __name__ == "__main__":

    sort_dict, dist_thresh, inhibitor, system_type, num_subplots = False, 10, 1, "cov", 6

    for i in [1, 2]:

        # Update DATA_PATH and reinitialise residue_dict for every replicate
        DATA_DIR = "{0}/{1}/MD/{2}/Rep{3}/analysis/base".format(MD_PATH, str(inhibitor), system_type, i)
        SYSTEM_DIR = "{0}/{1}/{2}".format(CURR_DIR, str(inhibitor), system_type)
        STORE_DIR = "{0}/within_{1}A".format(SYSTEM_DIR, dist_thresh)

        if sort_dict:
            # Sorting and storing the residue data
            within_dist_dict = {"arg": [], "glu": [], "asp": [], "his": [], "lys": []}
            if not os.path.exists("{0}/residue_dict.txt".format(SYSTEM_DIR)):
                residue_dict = {"arg": [], "glu": [], "asp": [], "his": [], "lys": [], "ligand": []}
            else:
                residue_dict = json.load(open("{0}/residue_dict.txt".format(SYSTEM_DIR)))  # All residues
                # Empty the .dat files
                for j, residue in enumerate(residue_dict.keys()):
                    open("{0}/{1}_list.txt".format(SYSTEM_DIR, residue), "w").close()
            # Sort out all .dat files
            for j, filename in enumerate(os.listdir(DATA_DIR)):
                # Filter out files that are not .dat files
                if ".dat" not in filename: continue
                # assign all .dat files to respective residues dictionary
                for k, residue in enumerate(residue_dict.keys()):
                    if residue in filename:
                        if not os.path.exists("{0}/residue_dict.txt".format(SYSTEM_DIR)):
                            with open("{0}/{1}".format(SYSTEM_DIR, "{0}_list.txt".format(residue)), "a+") as res_list_file:
                                res_list_file.write("{0}\n".format(filename))
                                residue_dict[residue].append(filename)
                        with open("{0}/{1}".format(DATA_DIR, filename), "r") as dist_data:

                            # Create necessary directories and files if they don't exist already
                            if not os.path.exists(STORE_DIR):
                                os.mkdir(STORE_DIR)
                            if not os.path.exists("{0}/close_res_list.txt".format(STORE_DIR)):
                                open("{0}/close_res_list.txt".format(STORE_DIR), "w").close()

                            with open("{0}/{1}".format(STORE_DIR, "close_res_list.txt"), "a") as close_res_file:
                                for l, line_entry in enumerate(dist_data.readlines()):
                                    distance = line_entry.split()[-1]
                                    try:
                                        if float(distance) <= dist_thresh:
                                            within_dist_dict[residue].append(filename)
                                            close_res_file.write("{0}\n".format(filename))
                                            break
                                    except (ValueError, TypeError) as error:  # If distance is NaN or dist_thresh=="All"
                                        continue
                    elif residue == "ligand":
                        continue
                        try:
                            resname = filename.split(".")[0].split("_")[-1].upper()
                            int(resname)
                        except TypeError:
                            continue
                    else:
                        continue
            json.dump(within_dist_dict, open("{0}/within_dist_dict.txt".format(STORE_DIR), "w"), indent=4)
            if not os.path.exists("{0}/residue_dict.txt".format(SYSTEM_DIR)):
                json.dump(residue_dict, open("{0}/residue_dict.txt".format(SYSTEM_DIR), "w"), indent=4)

        # Analyse each residue
        within_dist_dict = json.load(open("{0}/within_dist_dict.txt".format(STORE_DIR)))  # Residues of interest only
        residue_dict = json.load(open("{0}/residue_dict.txt".format(SYSTEM_DIR)))  # All residues

        chosen_dict = within_dist_dict  # Choose the dictionary with right data ***************************************

        # Charged Residues from CaH
        if num_subplots == 4:
            PLOTS_WIDTH, PLOTS_HEIGHT = FOUR_PLOTS_WIDTH, FOUR_PLOTS_HEIGHT
        else:
            PLOTS_WIDTH, PLOTS_HEIGHT = SIX_PLOTS_WIDTH, SIX_PLOTS_HEIGHT
        PLOTS_WIDTH, PLOTS_HEIGHT = SINGLE_PLOT_WIDTH, SINGLE_PLOT_HEIGHT
        target_H = "CYS481" if "non" in system_type else "Ca"
        # num_row, subplot_index = int(num_subplots / 2), 0
        # fig, axes = plt.subplots(nrows=num_row, ncols=2, sharex=True, sharey=True, figsize=(PLOTS_WIDTH, PLOTS_HEIGHT))
        fig = plt.figure()
        # fig.subplots_adjust(top=0.98, bottom=0.12, left=0.09, right=0.97, wspace=0.15, hspace=0.15)
        fig.subplots_adjust(top=0.97, bottom=0.15, left=0.14, right=0.96, wspace=0.15, hspace=0.15)
        # fig.suptitle(r"Distance of Charged Residues of Interest from {0} H".format(target_H), horizontalalignment='center',
        #              fontsize=14, weight='bold')
        # fig.text(0.5, 0.02, "Time (ns)", va='center', ha='center')
        fig.text(0.02, 0.5, r"Distance ($\AA$)", va='center', ha='center', rotation='vertical')
        # for j, residue in enumerate(chosen_dict.keys()):
        for residue in ["arg"]:
            label_list = []
            combined_df = pd.DataFrame(list(np.arange(0.000, 100.000, 0.005)), columns=["Time (ns)"])
            for k, dat_file in enumerate(chosen_dict[residue]):
                resname = dat_file.split(".")[0].split("_")[-1].upper()
                df = pd.read_csv("{0}/{1}".format(DATA_DIR, dat_file), index_col=0, delim_whitespace=True)
                df.columns = [resname]
                combined_df = pd.concat([combined_df, df], axis=1, ignore_index=False)
                label_list.append(resname)
                '''
                combined_df = combined_df.melt("Time (ps)", var_name="Residues", value_name=r"Distance ($\AA$)")
                # combined_df = combined_df.drop([0], axis=0)
                fig, ax = plt.subplots()
                fig.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)
                sns.lineplot(x="Time (ps)", y=r"Distance ($\AA$)", data=combined_df, legend="full")
                sns.despine(ax=ax, left=True)  # Remove "chartjunk"
                leg = ax.legend(ncol=3, loc='best', fontsize='small')
                leg.set_title("Residues")
                label_list = combined_df["Residues"]
                for k, res_label in zip(leg.texts, label_list):
                    k.set_text(res_label)
                '''  # Seaborn plots (unsuccessful)
            if combined_df.shape[1] <= 1:  # Don't plot if only time column exists
                continue
            # subplot_index += 1
            # ax1 = plt.subplot(int("{0}2{1}".format(num_row, subplot_index)))
            # plt.figure(figsize=(SINGLE_PLOT_WIDTH, SINGLE_PLOT_LEG_HEIGHT))
            combined_df.plot(x="Time (ns)", y=label_list, kind="line", ax=plt.gca(), lw=0.3, linestyle=":")
            # ax1.tick_params(top=False, bottom=True, left=True, right=False, labelleft=True, labelbottom=True)
            # ax1.xaxis.label.set_visible(False)
            leg = plt.legend(loc="upper right")
            # leg = plt.legend(loc="upper center", ncol=3, bbox_to_anchor=(0.5, -0.3))
            plt.setp(leg.get_lines(), linewidth=4)
            # plt.ylim(None, None); plt.xlim(None, None)
        # fig.delaxes(axes[-1][-1])
        plt.savefig(r"{0}/Distance of {1} H from Arginine Residues Rep {2} within {3} A".format(STORE_DIR, target_H, i, dist_thresh))
        plt.show()
