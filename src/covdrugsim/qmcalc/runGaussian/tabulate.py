import os
import pandas as pd
import re
from os.path import isdir
from covdrugsim.qmcalc.runGaussian.settings import DATA_PATH


def sort_human(list):
    """Sort a given list in a more "human" way"""
    convert = lambda text: float(text) if text.isdigit() else text
    alphanum = lambda key: [convert(c) for c in re.split('([-+]?[0-9]*\.?[0-9]*)', key)]
    list.sort(key=alphanum)
    return list


def replaceMultiple(main_str, toBeReplaced, new_str):
    """Replace multiple strings of main_str"""
    for elem in toBeReplaced:
        if elem in main_str:
            main_str = main_str.replace(elem, new_str)
    return main_str


def find_val(line_list, target_str):
    """Find the values of interest from Gaussian output files"""
    val, isEnergy, isMethod = None, 'Energies' in target_str[0] or 'Enthalpies' in target_str[0], '%chk' in target_str[0]
    for i, string in enumerate(target_str):
        for j, line in enumerate(line_list):
            if string in line:
                if isMethod:
                    value_inc = line_list[j - 2]
                    val = value_inc.split(' ')[2]; break
                else:
                    value_inc = line.split(string)[-1].strip()
                    if isEnergy:
                        val = float(value_inc.split('=')[-1].strip().replace(' ', '')); break
                    else:
                        if '\\' in value_inc:
                            val = value_inc.split('\\')[0].split('=')[-1]
                        else:
                            val = value_inc + line_list[j - 1].split('\\')[0]
                            val = val.split('=')[-1]
                        try:
                            val = val.replace(' ', '')
                            float(val); break
                        except ValueError:
                            continue
    if val is None:
        raise Exception('Target string {0} not found!'.format(target_str))
    # print(target_str, val, line_list[-3])  # For debugging
    return val


def write_Excel(dir_path):
    """Write a new Excel file tabulating the quantities of interest"""
    method_list, title_list, molecule_list, conformer_list, NImag_list, Z_list, E_list, H_list, G_list, MP2_list = [], [], [], [], [], [], [], [], [], []
    var_fill_list = [method_list, NImag_list, Z_list, E_list, H_list, G_list]
    keyword_list = [['%chk'], ['NI', 'Im'], ['zero-point Energies'], ['HF'], ['thermal Enthalpies'], ['thermal Free Energies']]
    for j, title in enumerate(groups):
        conformer_dir = '{0}/{1}'.format(input_dir, title)
        print("Conformer:", title)
        try:
            with open('{0}/{1}.out'.format(conformer_dir, title), 'r') as f:
                line_list = f.readlines()
                line_list.reverse()
                for i, var_list in enumerate(var_fill_list):
                    val = find_val(line_list, keyword_list[i])
                    var_list.append(val)
                title_list.append(title)
                molecule_list.append(replace_multiple(title.split('c')[0].replace('_', ''), ['TR', 'TSS', 'TP'], ''))
                conformer_list.append('c' + title.split('c')[-1])
        except FileNotFoundError:
            print("{0}/{1}.out not found!".format(conformer_dir, title))
            continue
    data = {'Method': method_list, 'Title': title_list, 'Molecule': molecule_list, 'Conformer': conformer_list, 'NImag': NImag_list,
           'Z (Hartree)': Z_list, 'E (Hartree)': E_list, 'H (Hartree)': H_list, 'G (Hartree)': G_list}
    df = pd.DataFrame(data, columns=['Method', 'Title', 'Molecule', 'Conformer', 'NImag', 'Z (Hartree)', 'E (Hartree)', 'H (Hartree)', 'G (Hartree)'])
    title_list = sort_human(title_list)
    sorted_df = df.set_index('Title').reindex(title_list).reset_index()
    print("# Sorted data frame:\n", sorted_df)

    print("# Writing to Excel sheet...")
    # sorted_df.to_excel('{0}/Energies.xlsx'.format(input_dir), sheet_name='Sheet1')
    writer = pd.ExcelWriter('{0}/Energies.xlsx'.format(input_dir), engine='xlsxwriter')
    sorted_df.to_excel(writer, startrow=1, sheet_name='Sheet1', index=False)
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    for i, col in enumerate(sorted_df.columns):
        column_len = sorted_df[col].astype(str).str.len().max()
        column_len = max(column_len, len(col)) + 2
        worksheet.set_column(i, i, column_len)
    writer.save()
    return workbook


if __name__ == "__main__":

    # Change this!
    input_dir = "/User/kahochow/Desktop/Li_mechanism/Li_work/Reactant"

    groups = [f for f in os.listdir(input_dir) if isdir('{0}/{1}'.format(input_dir, f))]
    print("\n# Tabulating values of interest from Gaussian .out files to an Excel sheet...")
    print("\n# Input directory:\n", input_dir, "\n\n# Groups:\n", groups, "\n")
    workbook = write_Excel(input_dir)

