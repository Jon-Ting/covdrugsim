import os


ligand_dict = {
    '1': '74',
    '2': '43',
    '3': '42',
    '4': '73',
    '5': '41',
    '6': '72',
    '7': '23',
    '8': '25',
    '9': '54',
    '10': '44',
    '11': '75',
    '12': '14',
    '13': '40',
    '14': '21',
    '15': '53',
    '16': '19',
    '17': '52',
    '18': '39',
    '19': '46',
    '20': '77',
    '21': '45',
    '22': '76',
    '23': '38',
    '24': '22',
    '25': '16',
    '26': '28',
    '27': '27',
    '28': '26',
    '29': '13',
    '30': '56',
    '31': '55',
    '32': '10',
    '33': '47',
    '34': '24',
    '35': '78',
    '36': '29',
    '37': '57',
    '38': '37',
    '39': '71',
    '40': '70',
    '41': '36',
    '42': '69',
    '43': '68',
    '44': '35',
    '45': '67',
    '46': '66',
    # '47': '18',
    '48': '30',
    '49': '58',
    '50': '59',
}

covbond_dict = {
    '10': '18',
    '17': '31',
    '18': '11',
    '19': '32',
    '20': '79',
    '21': '17',
    '22': '20',
    '23': '9',
    '24': '48',
    '25': '5',
    '26': '4',
    '27': '7',
    '28': '8',
    '35': '12',
    '36': '15',
    '37': '49',
    '38': '50',
    '39': '51',
    '40': '33',
    '41': '60',
    '42': '61',
    '43': '62',
    '44': '34',
    '45': '63',
    '46': '64',
    '47': '65',
}

SEPARATOR = "    "
ATOM_BLOCK_START, ATOM_BLOCK_END = "# atoms", "# total charge of the molecule:"
BOND_BLOCK_START, BOND_BLOCK_END = "# bonds", "# bond angles"
ANGLE_BLOCK_START, ANGLE_BLOCK_END = "# bond angles", "# improper dihedrals"
IMPROPER_BLOCK_START, IMPROPER_BLOCK_END = "# improper dihedrals", "# Dihedrals"
DIHEDRAL_BLOCK_START, DIHEDRAL_BLOCK_END = "# Dihedrals", "# LJ Exceptions"
index_dict = {
    "atom": {"buffer_lines": 2, "start_key": ATOM_BLOCK_START, "end_key": ATOM_BLOCK_END, "start": None, "end": None, "block": None, "sep_col": 2, "sep_col2": 8},  # sep_col actually 1, modified to avoid indexing [0:0]
    "bond": {"buffer_lines": 5, "start_key": BOND_BLOCK_START, "end_key": BOND_BLOCK_END, "start": None, "end": None, "block": None, "sep_col": 3},
    "angle": {"buffer_lines": 5, "start_key": ANGLE_BLOCK_START, "end_key": ANGLE_BLOCK_END, "start": None, "end": None, "block": None, "sep_col": 4},
    "improper": {"buffer_lines": 4, "start_key": IMPROPER_BLOCK_START, "end_key": IMPROPER_BLOCK_END, "start": None, "end": None, "block": None, "sep_col": 5},
    "dihedral": {"buffer_lines": 5, "start_key": DIHEDRAL_BLOCK_START, "end_key": DIHEDRAL_BLOCK_END, "start": None, "end": None, "block": None, "sep_col": 5}
    }


def find_line_index(file_name, keyword, start_from=0):
    index = None
    with open(file_name, "r") as read_file:
        for i, line in enumerate(read_file):
            if i >= start_from:
                if keyword in line:
                    index = i
                    break
    if not index:
        raise Exception("Keyword not found in file {0}".format(file_name))
    else:
        return index


def map_index(block, sep_num, map_dict, index_dict, dof, reverse=0):
    for j, line in enumerate(block):
        line_elements = line.split()[0:sep_num] if reverse == 0 else line.split()[sep_num:]
        new_element_list = []
        for k, element in enumerate(line_elements):
            if element in map_dict:
                new_element_list.append(map_dict[element])
            else:
                new_element_list.append("NA")
        leftover = SEPARATOR.join(line.split()[sep_num:]) if reverse == 0 else SEPARATOR + SEPARATOR.join(line.split()[0:sep_num]) + SEPARATOR
        index_dict[dof]["block"][j] = SEPARATOR + SEPARATOR.join(new_element_list) + SEPARATOR + leftover if reverse == 0 else leftover + SEPARATOR.join(new_element_list)
    return index_dict


def write_map_file(file_name, index_dict):
    with open(file_name, "w+") as write_file:
        for i, dof in enumerate(index_dict.keys()):
            write_file.write("\nDegree of Freedom: {0}\n".format(dof))
            new_block = index_dict[dof]["block"]
            for j, line in enumerate(new_block):
                write_file.write(line + "\n")


def pop_dict(index_dict, org_mtb_file, map_dict):
    for i, dof in enumerate(index_dict.keys()):
        print("Degree of Freedom:", dof)
        start_index = find_line_index(org_mtb_file, index_dict[dof]["start_key"]) + index_dict[dof]["buffer_lines"]
        end_index = find_line_index(org_mtb_file, index_dict[dof]["end_key"])
        index_dict[dof]["start"], index_dict[dof]["end"] = start_index, end_index
        sep_num = index_dict[dof]["sep_col"] - 1
        with open(org_mtb_file, "r") as read_file:  # Extract out the part to be mapped
            index_dict[dof]["block"] = read_file.readlines()[start_index:end_index]
        index_dict = map_index(index_dict[dof]["block"], sep_num, map_dict, index_dict, dof)  # Mapping the indices
        if "sep_col2" in index_dict[dof]:
            sep_num = index_dict[dof]["sep_col2"] - 1
            index_dict = map_index(index_dict[dof]["block"], sep_num, map_dict, index_dict, dof, reverse=1)
    return index_dict


if __name__ == "__main__":
    # 3MJO correction
    org_mtb_file, map_file, map_dict = "3MJO.mtb", "3MJO_mapping.txt", ligand_dict
    index_dict = pop_dict(index_dict, org_mtb_file, map_dict)
    write_map_file(map_file, index_dict)

    # 4EI1 correction
    org_mtb_file, map_file, map_dict = "4EI1.mtb", "4EI1_mapping.txt", covbond_dict
    index_dict = pop_dict(index_dict, org_mtb_file, map_dict)
    write_map_file(map_file, index_dict)
