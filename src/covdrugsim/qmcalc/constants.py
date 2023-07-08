keywordDict = {
    'GOVF': {'grid': ' opt=calcfc int(grid=ultrafine)', 'freq': ' freq', 'mem': int(4000), 'jobfs': int(9000), 'time': '24:00:00'},  # geometry optimization with vibrational frequency calculation
    'TSGOVF': {'grid': ' opt=(ts,calcfc,noeigentest,maxcyc=200) int(grid=ultrafine) scf=tight', 'freq': ' freq=noraman', 'mem': int(4000), 'jobfs': int(4000), 'time': '10:00:00'},  # transition state GOVF

    'SPEXGO': {'grid': '', 'time': '48:00:00', 'vmem': int(10000), 'ncpus': int(16)},  # single-point energy calculation without geometry optimization
    'IRC': {'grid': ' irc=(maxpoints=6,stepsize=10,calcfc,maxcyc=200)', 'time': '10:00:00'},  # intrinsic reaction coordinate calculation
    'SPEiS': {'grid': ' int(grid=ultrafine) scf=tight', 'freq': '', 'time': '07:00:00', 'mem': int(70000), 'jobfs': int(100000)},  # single-point energy calculation in solvent
    'MO': {'grid': ' gfinput iop(6/7=3)', 'time': '10:00:00'},  # print molecular orbitals for Molden display
    'FBRGO': {'grid': ' opt=modredundant int(grid=ultrafine) scf=tight', 'freq': ' freq=noraman', 'edit_charge': int(-1), 'time': '18:00:00', 'mem': int(4000), 'jobfs': int(4000)},  # freeze a bond, optimize the rest
    'SBGO': {'grid': ' opt=(z-matrix)'},  # stretch a bond, optimize for each point
    }

