import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from covdrugsim.mdsim.config import MD_PATH, SIX_PLOTS_WIDTH, SIX_PLOTS_HEIGHT, inhibitor_list

sns.set(context='paper', font_scale=1.5)
CURR_DIR = os.getcwd()


if __name__ == "__main__":

    num_subplots, fig_type = 6, "Hist"

    PLOTS_WIDTH, PLOTS_HEIGHT = SIX_PLOTS_WIDTH, SIX_PLOTS_HEIGHT
    num_row, subplot_index = int(num_subplots / 2), 0
    fig, axes = plt.subplots(nrows=num_row, ncols=2, sharex=True, sharey=True, figsize=(PLOTS_WIDTH, PLOTS_HEIGHT))
    if fig_type == "Line":
        fig.subplots_adjust(top=0.95, bottom=0.06, left=0.08, right=0.97, wspace=0.15, hspace=0.15)
        fig.text(0.5, 0.02, "Time (ns)", va='center', ha='center')
        fig.text(0.02, 0.5, "Number of H-Bonds", va='center', ha='center', rotation='vertical')
    elif fig_type == "Hist":
        fig.subplots_adjust(top=0.95, bottom=0.07, left=0.09, right=0.97, wspace=0.15, hspace=0.15)
        fig.text(0.5, 0.02, "Number of H-Bonds", va='center', ha='center')
        fig.text(0.02, 0.5, "Population", va='center', ha='center', rotation='vertical')
    fig.suptitle("Number of H-Bonds throughout MD Simulations of Different Inhibitors", horizontalalignment='center', fontsize=14, weight='bold')

    for i, inhibitor in enumerate(inhibitor_list):
        combined_df = pd.DataFrame(list(np.arange(0.005, 100.005, 0.005)), columns=["Time (ns)"])
        col_label = ["Time (ns)"]
        label_list, run_type_list = [], ["eq", "rep1", "rep2"]
        for j, run_type in enumerate(run_type_list):
            DATA_DIR = "{0}/Overall_Analysis/{1}".format(MD_PATH, str(inhibitor))
            for k in ["A", "B"]:
                dat_file = "{0}_{1}_nhbvtime.dat".format(run_type, k)
                dat_name = "{0} {1}{2}".format(run_type.capitalize(), inhibitor, k)
                df = pd.read_csv("{0}/{1}".format(DATA_DIR, dat_file), index_col=0, delim_whitespace=True)
                df.reset_index(drop=True, inplace=True)
                combined_df = pd.concat([combined_df, df], axis=1, ignore_index=True)
                label_list.append(dat_name)
        col_label += label_list
        combined_df.columns = col_label
        subplot_index += 1
        ax1 = plt.subplot(int("{0}2{1}".format(num_row, subplot_index)))
        if fig_type == "Line":
            combined_df.plot(x="Time (ns)", y=label_list, kind="line", ax=plt.gca(), lw=0.1, linestyle=":")
            ax1.xaxis.label.set_visible(False)
        elif fig_type == "Hist":
            combined_df.plot.bar(x="Time (ns)", y=label_list)
            #combined_df.plot.kde(x="Time (ns)", y=label_list, bw_method=0.5, ax=plt.gca())
            ax1.yaxis.label.set_visible(False)
        ax1.tick_params(top=False, bottom=True, left=True, right=False, labelleft=True, labelbottom=True)
        leg = plt.legend(loc="upper right")
        plt.setp(leg.get_lines(), linewidth=4)
        # plt.locator_params(axis='y', nbins=6)
    plt.savefig("{0}/Number of H Bonds {1}".format(CURR_DIR, fig_type))
    plt.show()
