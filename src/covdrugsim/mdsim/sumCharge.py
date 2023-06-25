total = 0
with open('charges.txt', 'r') as inp, open('tot_charge.txt', 'w') as outp:
   for line in inp:
       try:
           num = float(line) + 0.002
           total += num
           if num >= 0:
               outp.write(" {:3f}\n".format(num))
           else:
               outp.write("{:3f}\n".format(num))
       except ValueError:
           print('{} is not a number!'.format(line))
print('Total charges: {0}'.format(total))

