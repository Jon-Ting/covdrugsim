# TODO: Create and add other functions to this file

def sumCharge(inpFileName, outFileName, verbose=False):
    totalCharge = 0
    with open(inpFileName, 'r') as inpfile, open(outFileName, 'w') as outfile:
        for chargeStr in inpfile:
            try:
                charge = float(chargeStr) + 0.002
                totalCharge += charge
                if charge >= 0:
                    outfile.write(" {:3f}\n".format(charge))
                else:
                    outfile.write("{:3f}\n".format(charge))
            except ValueError:
                print('{} is not a number!'.format(chargeStr))
    if verbose:
        print('Total charges: {0}'.format(totalCharge))


if __name__ == '__main__':
    sumCharge('charges.txt', 'totCharge.txt', True)
