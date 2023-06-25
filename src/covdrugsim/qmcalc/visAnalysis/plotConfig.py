charge_list = ["Mulliken", "NBO", "MK", "Hirshfeld", "CM5", "QTAIM", "ChelpG", "Omega"]
charge_list_A = ["QTAIM", "Omega"]
charge_list_B = ["Mulliken", "NBO", "MK", "Hirshfeld", "CM5", "ChelpG"]
DI_list = ["Thiolate", "Inhibitor", "Activation", "Interaction"]

benchmarking_data = {"Measure": ["RMSD", "RMSD", "RMSD", "RMSD", "RMSD", "RMSD", "RMSD", "RMSD", "RMSD", "RMSD"],
                     "Method": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                     "Error (kcal/mol)": [0.6, 1.0, 4.5, 2.1, 2.6, 1.8, 3.6, 0.5, 1.5, 0.4]}

barrier_data = {"Mechanism": ["Base-Catalysed Proton Abstraction", "Base-Catalysed Proton Abstraction", "Base-Catalysed Proton Abstraction", "Base-Catalysed Proton Abstraction", "Base-Catalysed Proton Abstraction",
                              "4-Membered Intramolecular Proton Transfer", "4-Membered Intramolecular Proton Transfer", "4-Membered Intramolecular Proton Transfer", "4-Membered Intramolecular Proton Transfer", "4-Membered Intramolecular Proton Transfer",
                              "6-Membered Intramolecular Proton Transfer", "6-Membered Intramolecular Proton Transfer", "6-Membered Intramolecular Proton Transfer", "6-Membered Intramolecular Proton Transfer", "6-Membered Intramolecular Proton Transfer"],
                "Inhibitor": ["1", "3", "47", "5", "9",
                           "1", "3", "47", "5", "9",
                           "1", "3", "47", "5", "9"],
                "Elimination Barrier (kcal/mol)": [11.0-(-5.9), 16.0-(-3.9), 13.9-(-4.0), 20.0-(-10.8), 14.2-(-5.5),
                                                   43.4-(-5.9), 42.7-(-3.9), 45.2-(-4.0), 52.0-(-10.8), 47.3-(-5.5),
                                                   24.9-(-5.9), 26.0-(-3.9), 26.3-(-4.0), 28.1-(-10.8), 30.0-(-5.5)]}

combination_dict = {
    "I": {
        "SC": {
            "M": -15.195,
            "C": 50.709,
            "R2": 0.8754,
            "X-AXIS": 0,
            "Y-AXIS": 0.4,
            "LEG": "upper right",
            "ALIGN": "center",
            "FONTSIZE": "medium",
            "X-NAME": r"TS S-C Distance ($\AA$)"
        },

        "LUMO": {
            "M": 0.6121,
            "C": 22.143,
            "R2": 0.8354,
            "X-AXIS": 0,
            "Y-AXIS": 0.4,
            "LEG": "upper left",
            "ALIGN": "center",
            "FONTSIZE": "medium",
            "X-NAME": "Inhibitor LUMO Energy (kcal/mol)"
        },

        "Charge": {
            "Mulliken": {
                "M": -3.5523,
                "C": 10.639,
                "R2": 0.2152,
                "X-AXIS": -0.03,
                "Y-AXIS": 0,
                "LEG": "upper right",
                "ALIGN": "right",
                "FONTSIZE": "small",
                "X-NAME": "Mulliken Charge (e)"
            },
            "NBO": {
                "M": -24.802,
                "C": 9.7637,
                "R2": 0.7967,
                "X-AXIS": -0.01,
                "Y-AXIS": 0,
                "LEG": "upper right",
                "ALIGN": "right",
                "FONTSIZE": "small",
                "X-NAME": "NBO Charge (e)"
            },
            "MK": {
                "M": -7.1748,
                "C": 11.747,
                "R2": 0.3866,
                "X-AXIS": 0.02,
                "Y-AXIS": 0,
                "LEG": "upper right",
                "ALIGN": "left",
                "FONTSIZE": "small",
                "X-NAME": "Merz-Kollman Charge (e)"
            },
            "Hirshfeld": {
                "M": -89.348,
                "C": 12.659,
                "R2": 0.8491,
                "X-AXIS": 0.005,
                "Y-AXIS": 0,
                "LEG": "upper right",
                "ALIGN": "left",
                "FONTSIZE": "x-small",
                "X-NAME": "Hirshfeld Charge (e)"
            },
            "CM5": {
                "M": -54.454,
                "C": 8.8508,
                "R2": 0.7741,
                "X-AXIS": -0.005,
                "Y-AXIS": 0,
                "LEG": "upper right",
                "ALIGN": "right",
                "FONTSIZE": "small",
                "X-NAME": "CM5 Charge (e)"
            },
            "QTAIM": {
                "M": -92.849,
                "C": 14.411,
                "R2": 0.8573,
                "X-AXIS": -0.003,
                "Y-AXIS": 0,
                "LEG": "upper right",
                "ALIGN": "right",
                "FONTSIZE": "small",
                "X-NAME": "QTAIM Charge (e)"
            },
            "ChelpG": {
                "M": -19.394,
                "C": 9.9205,
                "R2": 0.6864,
                "X-AXIS": -0.004,
                "Y-AXIS": 0.2,
                "LEG": "upper right",
                "ALIGN": "right",
                "FONTSIZE": "small",
                "X-NAME": "ChelpG Charge (e)"
            },
            "Omega": {
                "M": -0.7187,
                "C": 59.268,
                "R2": 0.7297,
                "X-AXIS": -0.4,
                "Y-AXIS": 0,
                "LEG": "upper right",
                "ALIGN": "right",
                "FONTSIZE": "small",
                "X-NAME": "Electrophilicity Index"
            },
        },
        "DI": {
            "Thiolate": {
                "M": 17.241,
                "C": 7.6018,
                "R2": 0.798,
                "X-AXIS": -0.02,
                "Y-AXIS": 0,
                "LEG": "upper left",
                "ALIGN": "right",
                "FONTSIZE": "x-small",
                "X-NAME": "Thiolate Distortion Energy (kcal/mol)"
            },
            "Inhibitor": {
                "M": 0.8082,
                "C": 5.3355,
                "R2": 0.9760,
                "X-AXIS": -0.5,
                "Y-AXIS": 0.3,
                # "X-AXIS": -1.0,
                # "Y-AXIS": 0.7,
                "LEG": "best",
                "ALIGN": "left",
                "FONTSIZE": "medium",
                # "FONTSIZE": "x-small",
                "X-NAME": "Inhibitor Distortion Energy (kcal/mol)"
            },
            "Activation": {
                "M": 0.9013,
                "C": 10.439,
                "R2": 0.8943,
                "X-AXIS": -0.3,
                "Y-AXIS": 0,
                "LEG": "upper left",
                "ALIGN": "right",
                "FONTSIZE": "x-small",
                "X-NAME": "Activation Energy (kcal/mol)"
            },
            "Interaction": {
                "M": -1.6397,
                "C": 0.1818,
                "R2": 0.428,
                "X-AXIS": 0.18,
                "Y-AXIS": 0,
                "LEG": "upper right",
                "ALIGN": "left",
                "FONTSIZE": "x-small",
                "X-NAME": "Interaction Energy (kcal/mol)"
            },
        }
    },
    "G": {
        "LUMO": {
            "M": 0.6341,
            "C": 11.665,
            "R2": 0.8038,
            "X-AXIS": 0,
            "Y-AXIS": 0.4,
            "LEG": "upper left",
            "ALIGN": "center",
            "FONTSIZE": "medium",
            "X-NAME": "Inhibitor LUMO Energy (kcal/mol)"
        },

        "Charge": {
            "Mulliken": {
                "M": -3.8031,
                "C": 13.26,
                "R2": 0.2089,
                "X-AXIS": -0.04,
                "Y-AXIS": 0,
                "LEG": "upper right",
                "ALIGN": "right",
                "FONTSIZE": "x-small",
                "X-NAME": "Mulliken Charge (e)"
            },
            "NBO": {
                "M": -24.677,
                "C": 12.381,
                "R2": 0.678,
                "X-AXIS": -0.01,
                "Y-AXIS": 0,
                "LEG": "upper right",
                "ALIGN": "right",
                "FONTSIZE": "x-small",
                "X-NAME": "NBO Charge (e)"
            },
            "MK": {
                "M": -15.228,
                "C": 12.617,
                "R2": 0.7188,
                "X-AXIS": 0.02,
                "Y-AXIS": 0,
                "LEG": "upper right",
                "ALIGN": "left",
                "FONTSIZE": "x-small",
                "X-NAME": "Merz-Kollman Charge (e)"
            },
            "Hirshfeld": {
                "M": -85.733,
                "C": 15.179,
                "R2": 0.7221,
                "X-AXIS": 0.004,
                "Y-AXIS": 0,
                "LEG": "upper right",
                "ALIGN": "left",
                "FONTSIZE": "x-small",
                "X-NAME": "Hirshfeld Charge (e)"
            },
            "CM5": {
                "M": -52.002,
                "C": 11.53,
                "R2": 0.6279,
                "X-AXIS": -0.005,
                "Y-AXIS": 0,
                "LEG": "upper right",
                "ALIGN": "right",
                "FONTSIZE": "x-small",
                "X-NAME": "CM5 Charge (e)"
            },
            "QTAIM": {
                "M": -95.9,
                "C": 15.637,
                "R2": 0.7617,
                "X-AXIS": -0.004,
                "Y-AXIS": 0,
                "LEG": "upper right",
                "ALIGN": "right",
                "FONTSIZE": "x-small",
                "X-NAME": "QTAIM Charge (e)"
            },
            "ChelpG": {
                "M": -23.509,
                "C": 12.432,
                "R2": 0.8589,
                "X-AXIS": -0.007,
                "Y-AXIS": 0.18,
                "LEG": "upper right",
                "ALIGN": "right",
                "FONTSIZE": "x-small",
                "X-NAME": "ChelpG Charge (e)"
            },
            "Omega": {
                "M": -1.046,
                "C": 68.634,
                "R2": 0.5807,
                "X-AXIS": -0.3,
                "Y-AXIS": 0,
                "LEG": "upper right",
                "ALIGN": "right",
                "FONTSIZE": "x-small",
                "X-NAME": "Electrophilicity Index"
            },
        },
        "DI": {
            "Thiolate": {
                "M": 16.642,
                "C": 10.236,
                "R2": 0.6431,
                "X-AXIS": -0.02,
                "Y-AXIS": 0,
                "LEG": "upper left",
                "ALIGN": "right",
                "FONTSIZE": "x-small",
                "X-NAME": "Thiolate Distortion Energy (kcal/mol)"
            },
            "Inhibitor": {
                "M": 0.9119,
                "C": 6.9095,
                "R2": 0.9469,
                "X-AXIS": -1.4,
                "Y-AXIS": 0.55,
                "LEG": "best",
                "ALIGN": "left",
                "FONTSIZE": "x-small",
                "X-NAME": "Inhibitor Distortion Energy (kcal/mol)"
            },
            "Activation": {
                "M": 0.9652,
                "C": 10.666,
                "R2": 0.9044,
                "X-AXIS": -0.35,
                "Y-AXIS": 0.24,
                "LEG": "upper left",
                "ALIGN": "right",
                "FONTSIZE": "x-small",
                "X-NAME": "Activation Energy (kcal/mol)"
            },
            "Interaction": {
                "M": -2.1245,
                "C": 4.387,
                "R2": 0.2975,
                "X-AXIS": 0.1,
                "Y-AXIS": 0,
                "LEG": "lower left",
                "ALIGN": "left",
                "FONTSIZE": "x-small",
                "X-NAME": "Interaction Energy (kcal/mol)"
            },
        }
    },
}
