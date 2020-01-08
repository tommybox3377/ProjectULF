import struct
import numpy as np

# the locatoin of the file
dat_file = '/Users/../Downloads/010117000000.dat'

# open the file
f = open(dat_file, 'rb')

# niitialize an array to hold the GPS string header in
str_arr = []

# read through the string header while the data type is string
while True:
    str_bytes = f.read(4)

    if not str_bytes:
        break
    try:
        str_val = str_bytes.decode('utf-8')
        str_arr.append(str_val)
    except:
        break

# do the same for the floats (i.e. actual data)
uint_arr = []

while True:
    uint_bytes = f.read(2)

    if not uint_bytes:
        break

    # I need to get the binary number in order to mask from 16 to 12 bit
    # this line gets the binary representation of the number
    uint_val = bin(struct.unpack('>H', uint_bytes)[0])

    # this line drops the least significant bit, effectively masking to 12 bit
    uint_val = int(uint_val[0:-4], 2)

    # this line subtracts the half scale of a 12 bit int in order to sign the
    # integer, then rescales to +/-10
    uint_val = (uint_val - 2048) / 204.8

    # append to our output array
    uint_arr.append(uint_val)

# close file
f.close()

# gets every other data point starting at the first point
x_data = uint_arr[::2]

# same, but starts from the second point
y_data = uint_arr[1::2]

data = np.concatenate((x_data, y_data), axis=0)

np.savetxt('out_file_name', data)