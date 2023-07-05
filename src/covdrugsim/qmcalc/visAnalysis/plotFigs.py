import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from covdrugsim.qmcalc.visAnalysis.plotConfig import combination_dict, charge_list, charge_list_A, charge_list_B, DI_list, \
    benchmarking_data, barrier_data

sns.set(context='talk', font_scale=0.9)
# sns.despine()  # Remove "chartjunk"

SINGLE_PLOT_WIDTH, SINGLE_PLOT_HEIGHT = 6, 4
TWO_PLOT_WIDTH, TWO_PLOT_HEIGHT = 9, 3.5
FOUR_PLOTS_WIDTH, FOUR_PLOTS_HEIGHT = 8, 6
SIX_PLOTS_WIDTH, SIX_PLOTS_HEIGHT = 8, 10
EIGHT_PLOTS_WIDTH, EIGHT_PLOTS_HEIGHT = 10, 14
BAR_PLOTS_WIDTH, BAR_PLOTS_HEIGHT = 8, 5


def lin_reg(m, c, r2, xlimit, leg_loc, font_size="x-small"):
    x = np.linspace(xlimit[0], xlimit[1], 2)
    y = m * x + c
    plt.plot(x, y, '--r', label="$y = {0:.1f}x + {1:.1f}$\n$R^2 = {2:.2f}$".format(m, c, r2))
    plt.legend(loc=leg_loc, fontsize=font_size)
    plt.locator_params(axis='x', nbins=6)


if __name__ == "__main__":
    analysis_type = "Regression"
    DATA_PATH = '.'
    if analysis_type == "Bar":

        # Statistical Measures
        df = pd.DataFrame(benchmarking_data)
        fig = plt.figure(figsize=(BAR_PLOTS_WIDTH, BAR_PLOTS_HEIGHT))
        fig.subplots_adjust(top=0.95, bottom=0.15, left=0.1, right=0.98)
        data = df.groupby("Error (kcal/mol)").size()
        pal = sns.dark_palette("purple", len(data), reverse=True)
        rank = data.argsort().argsort()
        ax = sns.barplot(x="Method", y="Error (kcal/mol)", data=df, palette=np.array(pal[::-1])[rank], alpha=0.95)
        for p in ax.patches:
            ax.annotate(format(p.get_height(), ".1f"), (p.get_x()+p.get_width()/2., p.get_height()), ha="center",
                        va="center", xytext=(0, 8), textcoords="offset pixels", fontsize=16)
        # leg = ax.legend(); leg.set_title("")
        # plt.legend(loc='upper right'); plt.ylim(None, 5.0); plt.xlim(None, None)
        ax.set(ylabel="Root-Mean-Square Error (kcal/mol)")
        plt.ylim(None, 5)
        plt.savefig("Benchmarking Statistical Measures")
        plt.show()

        # Elimination Barriers
        df = pd.DataFrame(barrier_data)
        fig = plt.figure(figsize=(FOUR_PLOTS_WIDTH, FOUR_PLOTS_HEIGHT))
        fig.subplots_adjust(top=0.97, bottom=0.1, left=0.08, right=0.97)
        ax = sns.barplot(x="Inhibitor", y="Elimination Barrier (kcal/mol)", data=df, hue="Mechanism", palette="deep")
        for p in ax.patches:
            ax.annotate(format(p.get_height(), ".1f"), (p.get_x()+p.get_width()/2., p.get_height()), ha="center",
                        va="center", xytext=(0, 10), textcoords="offset pixels", fontsize=12)
        leg = ax.legend(); leg.set_title("")
        plt.legend(loc='upper left'); plt.ylim(None, None); plt.xlim(None, None)
        plt.savefig("Elimination Barrier for Different Mechanisms")
        # plt.show()

    elif analysis_type == "Regression":
        combination = "outputs/CombinationI"
        csv_file = "{0}/QM/Conformational_Analysis/Most_stable_conformers/{1}_Properties_Correlation.csv".format(DATA_PATH, combination)
        df = pd.read_csv(csv_file, index_col=0)
        print(df)
        prop_dict = combination_dict[combination[-1]]

        # Inhibitor Distortion Energy
        chosen_dict = prop_dict["DI"]["Inhibitor"]
        m, c, r2, x_axis, y_axis, leg, fontsize = chosen_dict["M"], chosen_dict["C"], chosen_dict["R2"], chosen_dict[
            "X-AXIS"], chosen_dict["Y-AXIS"], chosen_dict["LEG"], chosen_dict["FONTSIZE"]
        fig = plt.figure(figsize=(SINGLE_PLOT_WIDTH, SINGLE_PLOT_HEIGHT))
        fig.subplots_adjust(top=0.99, bottom=0.05, left=0.02, right=0.99)
        ax = sns.scatterplot(x="Inhibitor Distortion Energy (kcal/mol)", y="Addition Barrier (kcal/mol)", data=df, hue="Inhibitor", legend=False, s=100)
        ax.set(xlabel=r"Inhibitor Distortion Energy (kcal/mol)")
        ax.set(ylabel=u"$\Delta G^\u2021$ (kcal/mol)")
        for line in range(1, df.shape[0] + 1):
            ax.text(df["Inhibitor Distortion Energy (kcal/mol)"][line] + x_axis, df["Addition Barrier (kcal/mol)"][line] + y_axis,
                    df["Inhibitor"][line], horizontalalignment='center', size='small', color='black')
        lin_reg(m, c, r2, plt.xlim(), leg, fontsize)
        plt.ylim(None, None); plt.xlim(None, None)
        plt.tight_layout()
        plt.savefig(r"{0}/Inhibitor Distortion Energy".format(combination))

        # TS S-C Distance
        chosen_dict = prop_dict["SC"]
        m, c, r2, x_axis, y_axis, leg, fontsize = chosen_dict["M"], chosen_dict["C"], chosen_dict["R2"], chosen_dict[
            "X-AXIS"], chosen_dict["Y-AXIS"], chosen_dict["LEG"], chosen_dict["FONTSIZE"]
        fig = plt.figure(figsize=(SINGLE_PLOT_WIDTH, SINGLE_PLOT_HEIGHT))
        fig.subplots_adjust(top=0.99, bottom=0.05, left=0.05, right=0.99)
        ax = sns.scatterplot(x="TS S-C Distance (A)", y="Addition Barrier (kcal/mol)", data=df, hue="Inhibitor", legend=False, s=100)
        ax.set(xlabel=r"Transition State S-C$\beta$ Distance ($\AA$)")
        ax.set(ylabel=u"$\Delta G^\u2021$ (kcal/mol)")
        for line in range(1, df.shape[0] + 1):
            ax.text(df["TS S-C Distance (A)"][line] + x_axis, df["Addition Barrier (kcal/mol)"][line] + y_axis,
                    df["Inhibitor"][line], horizontalalignment='center', size='small', color='black')
        lin_reg(m, c, r2, plt.xlim(), leg, fontsize)
        plt.ylim(None, None); plt.xlim(None, None)
        plt.tight_layout()
        plt.savefig(r"{0}/TS S-C Distance".format(combination))

        # Inhibitor LUMO Energy
        chosen_dict = prop_dict["LUMO"]
        m, c, r2, x_axis, y_axis, leg, fontsize = chosen_dict["M"], chosen_dict["C"], chosen_dict["R2"], chosen_dict[
            "X-AXIS"], chosen_dict["Y-AXIS"], chosen_dict["LEG"], chosen_dict["FONTSIZE"]
        fig = plt.figure(figsize=(SINGLE_PLOT_WIDTH, SINGLE_PLOT_HEIGHT))
        fig.subplots_adjust(top=0.99, bottom=0.05, left=0.05, right=0.99)
        ax = sns.scatterplot(x="Inhibitor LUMO Energy (kcal/mol)", y="Addition Barrier (kcal/mol)", data=df, hue="Inhibitor", legend=False, s=100)
        ax.set(ylabel=u"$\Delta G^\u2021$ (kcal/mol)")
        for line in range(1, df.shape[0] + 1):
            ax.text(df["Inhibitor LUMO Energy (kcal/mol)"][line] + x_axis, df["Addition Barrier (kcal/mol)"][line] + y_axis,
                    df["Inhibitor"][line], horizontalalignment='center', size='small', color='black')
        lin_reg(m, c, r2, plt.xlim(), leg, fontsize)
        plt.ylim(None, None); plt.xlim(None, None)
        plt.tight_layout()
        plt.savefig("{0}/Inhibitor LUMO Energy".format(combination))
        # plt.show()

        raise
        # Beta-Carbon Charges
        fig = plt.figure(figsize=(EIGHT_PLOTS_WIDTH, EIGHT_PLOTS_HEIGHT))
        fig.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.95, wspace=0.3, hspace=0.45)
        fig.suptitle(r"Correlation between $\beta$-Carbon Charge and Addition Barrier",
                     horizontalalignment='center', fontsize=16, weight='bold')
        for i, model in enumerate(charge_list):
            chosen_dict = prop_dict["Charge"][model]
            m, c, r2, x_axis, y_axis, leg, txt_align, fontsize, x_name = chosen_dict["M"], chosen_dict["C"], chosen_dict["R2"], chosen_dict[
                "X-AXIS"], chosen_dict["Y-AXIS"], chosen_dict["LEG"], chosen_dict["ALIGN"], chosen_dict["FONTSIZE"], chosen_dict["X-NAME"]
            ax1 = fig.add_subplot(4, 2, i + 1)
            p1 = sns.scatterplot(x=x_name, y="Addition Barrier (kcal/mol)", data=df,
                                 hue="Inhibitor", legend=False, s=100)
            for line in range(1, df.shape[0] + 1):
                ax1.text(df[x_name][line] + x_axis, df["Addition Barrier (kcal/mol)"][line] + y_axis,
                         df["Inhibitor"][line], horizontalalignment=txt_align, size='small', color='black')
            lin_reg(m, c, r2, plt.xlim(), leg, fontsize)
        plt.savefig("{0}/Beta-Carbon Charges".format(combination))
        # plt.show()

        # Beta-Carbon Charges for Report
        fig = plt.figure(figsize=(TWO_PLOT_WIDTH, TWO_PLOT_HEIGHT))
        fig.subplots_adjust(top=0.96, bottom=0.18, left=0.08, right=0.97, wspace=0.25, hspace=0.45)
        # fig.suptitle(r"Correlation between $\beta$-Carbon Charge and Addition Barrier",
        #              horizontalalignment='center', fontsize=16, weight='bold')
        for i, model in enumerate(charge_list_A):
            chosen_dict = prop_dict["Charge"][model]
            m, c, r2, x_axis, y_axis, leg, txt_align, fontsize, x_name = chosen_dict["M"], chosen_dict["C"], chosen_dict["R2"], chosen_dict[
                "X-AXIS"], chosen_dict["Y-AXIS"], chosen_dict["LEG"], chosen_dict["ALIGN"], chosen_dict["FONTSIZE"], chosen_dict["X-NAME"]
            ax1 = fig.add_subplot(1, 2, i + 1)
            p1 = sns.scatterplot(x=x_name, y="Addition Barrier (kcal/mol)", data=df,
                                 hue="Inhibitor", legend=False, s=100)
            p1.set(ylabel=u"$\Delta G^\u2021$ (kcal/mol)")
            for line in range(1, df.shape[0] + 1):
                ax1.text(df[x_name][line] + x_axis, df["Addition Barrier (kcal/mol)"][line] + y_axis,
                         df["Inhibitor"][line], horizontalalignment=txt_align, size='small', color='black')
            lin_reg(m, c, r2, plt.xlim(), leg, fontsize)
        fig.text(0.005, 0.96, "(a)", va='center', ha='left'); fig.text(0.5, 0.96, "(b)", va='center', ha='left')
        plt.savefig("{0}/Beta-Carbon Charges for Report A".format(combination))

        fig = plt.figure(figsize=(SIX_PLOTS_WIDTH, SIX_PLOTS_HEIGHT))
        fig.subplots_adjust(top=0.98, bottom=0.06, left=0.09, right=0.97, wspace=0.3, hspace=0.35)
        # fig.suptitle(r"Correlation between $\beta$-Carbon Charge and Addition Barrier",
        #              horizontalalignment='center', fontsize=16, weight='bold')
        for i, model in enumerate(charge_list_B):
            chosen_dict = prop_dict["Charge"][model]
            m, c, r2, x_axis, y_axis, leg, txt_align, fontsize, x_name = chosen_dict["M"], chosen_dict["C"], chosen_dict["R2"], chosen_dict[
                "X-AXIS"], chosen_dict["Y-AXIS"], chosen_dict["LEG"], chosen_dict["ALIGN"], chosen_dict["FONTSIZE"], chosen_dict["X-NAME"]
            ax1 = fig.add_subplot(3, 2, i + 1)
            p1 = sns.scatterplot(x=x_name, y="Addition Barrier (kcal/mol)", data=df,
                                 hue="Inhibitor", legend=False, s=100)
            p1.set(ylabel=u"$\Delta G^\u2021$ (kcal/mol)")
            for line in range(1, df.shape[0] + 1):
                ax1.text(df[x_name][line] + x_axis, df["Addition Barrier (kcal/mol)"][line] + y_axis,
                         df["Inhibitor"][line], horizontalalignment=txt_align, size='small', color='black')
            lin_reg(m, c, r2, plt.xlim(), leg, fontsize)
        fig.text(0.007, 0.98, "(a)", va='center', ha='left'); fig.text(0.505, 0.98, "(b)", va='center', ha='left')
        fig.text(0.007, 0.643, "(c)", va='center', ha='left'); fig.text(0.505, 0.643, "(d)", va='center', ha='left')
        fig.text(0.007, 0.31, "(e)", va='center', ha='left'); fig.text(0.505, 0.31, "(f)", va='center', ha='left')
        plt.savefig("{0}/Beta-Carbon Charges for Report B".format(combination))
        # plt.show()

        # Distortion/Interaction Analysis
        fig = plt.figure(figsize=(FOUR_PLOTS_WIDTH, FOUR_PLOTS_HEIGHT))
        fig.subplots_adjust(top=0.98, bottom=0.11, left=0.09, right=0.97, wspace=0.35, hspace=0.4)
        # fig.suptitle("Correlation between Distortion/Interaction Energies and Addition Barrier",
        #             horizontalalignment='center', fontsize=16, weight='bold')
        for i, aspect in enumerate(DI_list):
            chosen_dict = prop_dict["DI"][aspect]
            m, c, r2, x_axis, y_axis, leg, txt_align, fontsize, x_name = chosen_dict["M"], chosen_dict["C"], chosen_dict["R2"], chosen_dict[
                "X-AXIS"], chosen_dict["Y-AXIS"], chosen_dict["LEG"], chosen_dict["ALIGN"], chosen_dict["FONTSIZE"], chosen_dict["X-NAME"]
            ax1 = fig.add_subplot(2, 2, i + 1)
            p1 = sns.scatterplot(x=x_name, y="Addition Barrier (kcal/mol)", data=df,
                                 hue="Inhibitor", legend=False, s=100)
            p1.set(ylabel=u"$\Delta G^\u2021$ (kcal/mol)")
            if aspect == "Thiolate":
                p1.set(xlabel=u"$\Delta E^\u2021_{d\_MeS^-}$ (kcal/mol)")
            elif aspect == "Inhibitor":
                p1.set(xlabel=u"$\Delta E^\u2021_{d\_MA}$ (kcal/mol)")
            elif aspect == "Activation":
                p1.set(xlabel=u"$\Delta E^\u2021$ (kcal/mol)")
            elif aspect == "Interaction":
                p1.set(xlabel=u"$\Delta E^\u2021_{int}$ (kcal/mol)")
            for line in range(1, df.shape[0] + 1):
                ax1.text(df[x_name][line] + x_axis, df["Addition Barrier (kcal/mol)"][line] + y_axis,
                         df["Inhibitor"][line], horizontalalignment=txt_align, size='small', color='black')
            lin_reg(m, c, r2, plt.xlim(), leg, fontsize)
        fig.text(0.005, 0.98, "(a)", va='center', ha='left'); fig.text(0.51, 0.98, "(b)", va='center', ha='left')
        fig.text(0.005, 0.47, "(c)", va='center', ha='left'); fig.text(0.51, 0.47, "(d)", va='center', ha='left')
        plt.ylim(None, None); plt.xlim(None, None)
        plt.savefig("{0}/Distortion-Interaction Analysis".format(combination))
        # plt.show()
    else:
        raise Exception("Analysis type chosen not known!")
