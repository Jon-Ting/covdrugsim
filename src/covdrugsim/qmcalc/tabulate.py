from os import listdir
from os.path import isdir
import re

import pandas as pd


def sortNatural(targetList):
    """Sort a given list in a more natural way."""
    tryConvertNumeric = lambda text: float(text) if text.isdigit() else text
    alphanum = lambda key: [tryConvertNumeric(c) for c in re.split('([-+]?[0-9]*\.?[0-9]*)', key)]
    targetList.sort(key=alphanum)
    return targetList


def replaceMultiple(str1, strsToReplace, str2):
    """Replace multiple strings of str1 by str2."""
    for strToReplace in strsToReplace:
        if strToReplace in str1:
            str1 = str1.replace(strToReplace, str2)
    return str1


def findVal(lineList, targetStr):
    """Find the values of interest from Gaussian output files."""
    val, isEnergy, isMethod = None, 'Energies' in targetStr[0] or 'Enthalpies' in targetStr[0], '%chk' in targetStr[0]
    for string in targetStr:
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


def writeToExcel(inputDirPath, verbose=False):
    """
    Tabulate the quantities of interest to an Excel document.
    """
    groups = [f for f in listdir(inputDirPath) if isdir('{0}/{1}'.format(inputDirPath, f))]

    if verbose:
        print("\n# Tabulating values of interest from Gaussian .out files to an Excel sheet...")
        print("\n# Input directory:\n", inputDirPath, "\n\n# Groups:\n", groups, "\n")

    methodList, nameList, moleculeList, moleculeList, NImagList, ZList, EList, HList, GList, MP2List = [], [], [], [], [], [], [], [], [], []
    varFillList = [methodList, NImagList, ZList, EList, HList, GList]
    keywordList = [['%chk'], ['NI', 'Im'], ['zero-point Energies'], ['HF'], ['thermal Enthalpies'], ['thermal Free Energies']]
    for name in groups:
        moleculeDir = '{0}/{1}'.format(inputDirPath, name)
        print("Molecule:", name)
        try:
            with open('{0}/{1}.out'.format(moleculeDir, name), 'r') as f:
                lineList = f.readlines()
                lineList.reverse()
                for i, varList in enumerate(varFillList):
                    val = findVal(lineList, keywordList[i])
                    varList.append(val)
                nameList.append(name)
                moleculeList.append(replaceMultiple(name.split('c')[0].replace('_', ''), ['TR', 'TSS', 'TP'], ''))
                moleculeList.append('c' + name.split('c')[-1])
        except FileNotFoundError:
            print("{0}/{1}.out not found!".format(moleculeDir, name))
            continue
    data = {'Method': methodList, 'Name': nameList, 'Molecule': moleculeList, 'Molecule': moleculeList, 'NImag': NImagList,
           'Z (Hartree)': ZList, 'E (Hartree)': EList, 'H (Hartree)': HList, 'G (Hartree)': GList}
    df = pd.DataFrame(data, columns=['Method', 'Name', 'Molecule', 'Molecule', 'NImag', 'Z (Hartree)', 'E (Hartree)', 'H (Hartree)', 'G (Hartree)'])
    nameList = sortNatural(nameList)
    sortedDF = df.set_index('Name').reindex(nameList).reset_index()
    print("# Sorted data frame:\n", sortedDF)

    print("# Writing to Excel sheet...")
    # sortedDF.to_excel('{0}/Energies.xlsx'.format(inputDirPath), sheet_name='Sheet1')
    writer = pd.ExcelWriter('{0}/Energies.xlsx'.format(inputDirPath), engine='xlsxwriter')
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
    inputDirPath = '/mnt/c/Users/ASUS/Documents/covdrugsim/src/covdrugsim/data/exampleXYZs'  # To be modified!
    workbook = writeToExcel(inputDirPath, verbose=True)

