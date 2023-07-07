from os import listdir
from os.path import isdir
import re

import pandas as pd


def sortHuman(alist):
    """Sort a given alist in a more 'human' way"""
    convert = lambda text: float(text) if text.isdigit() else text
    alphanum = lambda key: [convert(c) for c in re.split('([-+]?[0-9]*\.?[0-9]*)', key)]
    alist.sort(key=alphanum)
    return alist


def replaceMultiple(mainStr, toBeReplaced, newStr):
    """Replace multiple strings of mainStr"""
    for elem in toBeReplaced:
        if elem in mainStr:
            mainStr = mainStr.replace(elem, newStr)
    return mainStr


def findVal(lineList, targetStr):
    """Find the values of interest from Gaussian output files"""
    val, isEnergy, isMethod = None, 'Energies' in targetStr[0] or 'Enthalpies' in targetStr[0], '%chk' in targetStr[0]
    for i, string in enumerate(targetStr):
        for j, line in enumerate(lineList):
            if string in line:
                if isMethod:
                    valueInc = lineList[j - 2]
                    val = valueInc.split(' ')[2]; break
                else:
                    valueInc = line.split(string)[-1].strip()
                    if isEnergy:
                        val = float(valueInc.split('=')[-1].strip().replace(' ', '')); break
                    else:
                        if '\\' in valueInc:
                            val = valueInc.split('\\')[0].split('=')[-1]
                        else:
                            val = valueInc + lineList[j - 1].split('\\')[0]
                            val = val.split('=')[-1]
                        try:
                            val = val.replace(' ', '')
                            float(val); break
                        except ValueError:
                            continue
    if val is None:
        raise Exception('Target string {0} not found!'.format(targetStr))
    # print(targetStr, val, lineList[-3])  # For debugging
    return val


def writeToExcel(dir_path):
    """Write a new Excel file tabulating the quantities of interest"""
    methodList, titleList, moleculeList, conformerList, NImagList, ZList, EList, HList, GList, MP2List = [], [], [], [], [], [], [], [], [], []
    varFillList = [methodList, NImagList, ZList, EList, HList, GList]
    keywordList = [['%chk'], ['NI', 'Im'], ['zero-point Energies'], ['HF'], ['thermal Enthalpies'], ['thermal Free Energies']]
    for j, title in enumerate(groups):
        conformerDir = '{0}/{1}'.format(inputDir, title)
        print("Conformer:", title)
        try:
            with open('{0}/{1}.out'.format(conformerDir, title), 'r') as f:
                lineList = f.readlines()
                lineList.reverse()
                for i, varList in enumerate(varFillList):
                    val = findVal(lineList, keywordList[i])
                    varList.append(val)
                titleList.append(title)
                moleculeList.append(replace_multiple(title.split('c')[0].replace('_', ''), ['TR', 'TSS', 'TP'], ''))
                conformerList.append('c' + title.split('c')[-1])
        except FileNotFoundError:
            print("{0}/{1}.out not found!".format(conformerDir, title))
            continue
    data = {'Method': methodList, 'Title': titleList, 'Molecule': moleculeList, 'Conformer': conformerList, 'NImag': NImagList,
           'Z (Hartree)': ZList, 'E (Hartree)': EList, 'H (Hartree)': HList, 'G (Hartree)': GList}
    df = pd.DataFrame(data, columns=['Method', 'Title', 'Molecule', 'Conformer', 'NImag', 'Z (Hartree)', 'E (Hartree)', 'H (Hartree)', 'G (Hartree)'])
    titleList = sortHuman(titleList)
    sortedDF = df.set_index('Title').reindex(titleList).reset_index()
    print("# Sorted data frame:\n", sortedDF)

    print("# Writing to Excel sheet...")
    # sortedDF.to_excel('{0}/Energies.xlsx'.format(inputDir), sheet_name='Sheet1')
    writer = pd.ExcelWriter('{0}/Energies.xlsx'.format(inputDir), engine='xlsxwriter')
    sortedDF.to_excel(writer, startrow=1, sheet_name='Sheet1', index=False)
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    for i, col in enumerate(sortedDF.columns):
        column_len = sortedDF[col].astype(str).str.len().max()
        column_len = max(column_len, len(col)) + 2
        worksheet.set_column(i, i, column_len)
    writer.save()
    return workbook


if __name__ == "__main__":

    # Change this!
    inputDir = "/User/kahochow/Desktop/Li_mechanism/Li_work/Reactant"

    groups = [f for f in listdir(inputDir) if isdir('{0}/{1}'.format(inputDir, f))]
    print("\n# Tabulating values of interest from Gaussian .out files to an Excel sheet...")
    print("\n# Input directory:\n", inputDir, "\n\n# Groups:\n", groups, "\n")
    workbook = writeToExcel(inputDir)

