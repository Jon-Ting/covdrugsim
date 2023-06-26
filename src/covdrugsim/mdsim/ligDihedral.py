import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from covdrugsim.mdsim.config import MD_PATH, SIX_PLOTS_WIDTH, SIX_PLOTS_HEIGHT, SIX_PLOTS_HORIZONTAL_WIDTH, SIX_PLOTS_HORIZONTAL_HEIGHT, inhibitor_list

sns.set(context='paper', font_scale=1.5)
CURR_DIR = os.getcwd()


if __name__ == "__main__":

    system_type, num_subplots, fig_type = "noncov", 6, "Hist"

    # PLOTS_WIDTH, PLOTS_HEIGHT = SIX_PLOTS_WIDTH, SIX_PLOTS_HEIGHT
    PLOTS_WIDTH, PLOTS_HEIGHT = SIX_PLOTS_HORIZONTAL_WIDTH, SIX_PLOTS_HORIZONTAL_HEIGHT
    num_row, subplot_index = int(num_subplots / 3), 0
    fig, axes = plt.subplots(nrows=num_row, ncols=3, sharex=True, sharey=True, figsize=(PLOTS_WIDTH, PLOTS_HEIGHT))
    if fig_type == "Line":
        fig.subplots_adjust(top=0.95, bottom=0.06, left=0.10, right=0.97, wspace=0.25, hspace=0.15)
        fig.text(0.5, 0.02, "Time (ns)", va='center', ha='center')
        fig.text(0.02, 0.5, u"Angle (\N{DEGREE SIGN})", va='center', ha='center', rotation='vertical')
    elif fig_type == "Hist":
        #fig.subplots_adjust(top=0.95, bottom=0.06, left=0.10, right=0.97, wspace=0.25, hspace=0.15)
        fig.subplots_adjust(top=0.98, bottom=0.08, left=0.09, right=0.98, wspace=0.25, hspace=0.15)
        fig.text(0.5, 0.02, u"Angle (\N{DEGREE SIGN})", va='center', ha='center')
        fig.text(0.02, 0.5, "Population", va='center', ha='center', rotation='vertical')
    # fig.suptitle("Dihedral of C=C-C=O For All Inhibitors", horizontalalignment='center', fontsize=14, weight='bold')

    for i, inhibitor in enumerate(inhibitor_list):
        combined_df = pd.DataFrame(list(np.arange(0.005, 100.005, 0.005)), columns=["Time (ns)"])
        col_label = ["Time (ns)"]
        label_list = []
        for j in [1, 2]:
            DATA_DIR = "{0}/{1}/MD/{2}/Rep{3}/analysis/dih".format(MD_PATH, str(inhibitor), system_type, j)
            for k in ["A", "B"]:
                dat_file = "{0}_dih{1}.dat".format(inhibitor, k)
                dat_name = "Rep{0} {1}{2}".format(j, inhibitor, k)
                df = pd.read_csv("{0}/{1}".format(DATA_DIR, dat_file), index_col=0, delim_whitespace=True)
                df.reset_index(drop=True, inplace=True)
                combined_df = pd.concat([combined_df, df], axis=1, ignore_index=True)
                label_list.append(dat_name)
        col_label += label_list
        combined_df.columns = col_label
        subplot_index += 1
        ax1 = plt.subplot(int("{0}3{1}".format(num_row, subplot_index)))
        if fig_type == "Line":
            combined_df.plot(x="Time (ns)", y=label_list, kind="line", ax=plt.gca(), lw=0.3, linestyle=":")
            ax1.xaxis.label.set_visible(False)
        elif fig_type == "Hist":
            combined_df.plot.kde(x="Time (ns)", y=label_list, bw_method=0.5, ax=plt.gca())
            ax1.yaxis.label.set_visible(False)
        ax1.tick_params(top=False, bottom=True, left=True, right=False, labelleft=True, labelbottom=True)
        leg = plt.legend(loc="upper right")
        plt.setp(leg.get_lines(), linewidth=4)
        # plt.locator_params(axis='y', nbins=6)
    # fig.text(0.1, 0.941, "(a)", va='center', ha='left'); fig.text(0.583, 0.941, "(b)", va='center', ha='left')
    # fig.text(0.1, 0.6315, "(c)", va='center', ha='left'); fig.text(0.583, 0.6315, "(d)", va='center', ha='left')
    # fig.text(0.1, 0.32, "(e)", va='center', ha='left'); fig.text(0.583, 0.32, "(f)", va='center', ha='left')
    fig.text(0.089, 0.965, "(a)", va='center', ha='left'); fig.text(0.407, 0.965, "(b)", va='center', ha='left'), fig.text(0.725, 0.965, "(c)", va='center', ha='left')
    fig.text(0.089, 0.483, "(d)", va='center', ha='left'); fig.text(0.407, 0.483, "(e)", va='center', ha='left'); fig.text(0.725, 0.483, "(f)", va='center', ha='left')
    plt.savefig("{0}/Dihedral of C=C-C=O For All Inhibitors {1} Test".format(CURR_DIR, fig_type))
    plt.show()
