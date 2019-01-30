import os
import io


# filenames
fname = 'infile.txt'
fname2 = 'outfile.txt'

# get the fulll path names
path = os.path.abspath(fname)
path2 = os.path.abspath(fname2)

# print message to user
print('copying ', path, 'to ', path2)

# set the blocksize
blocksize = 16

# set the totalsize counter
totalsize = 0

# create a mutable array to hold the bytes
data = bytearray(blocksize)

# open the files, in buffered binary mode
file = open(fname, 'rb')
file2 = open(fname2, 'wb')

# loop until done
while True:
    # read block from source file
    num = file.readinto(data)

    # adjust totalsize
    totalsize += num
    
    # print data, assuming text data
    print(num, data)
    # use following if raw binary data
    #print(num, data.hex())

    # check if full block read
    if num == blocksize:
        # write full block to destination
        file2.write(data)
    else:
        # extract subarray
        data2 = data[0:num]

        # write subarray to destination and break loop
        file2.write(data2)
        break
    
# close files (note will also flush destination file)
file.close()
file2.close()

# print totalsize
print('read ', totalsize, ' bytes')
