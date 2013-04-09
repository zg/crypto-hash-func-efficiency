#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib, numpy as np, os, time

def hamming_distance(s1, s2):
    assert len(s1) == len(s2)
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1,s2))

indices = 25000
data_length = 4096
random_bytes = dict()
random_byte_hashes = [dict(),dict(),dict(),dict()]
algorithms = ['md5','RIPEMD160','SHA1','whirlpool'] # must be in hashlib.algorithms_available
times = np.arange(indices*4*1.0).reshape(4,indices)

"Generate the bytes"
print ("[rpp] Generating random bytes...")
for i in range(0,indices):
    random_bytes[i] = os.urandom(data_length)

print ("[rpp] Measuring time efficiency of %i indices of %i random bytes..." % (indices,data_length))

algorithm_count = 0
"Measure time efficiency and output time"
for algorithm in algorithms:
    tm = time.time()
    for i in random_bytes:
        h = hashlib.new(algorithm)
        h.update(random_bytes[i])
        h.hexdigest()
        random_byte_hashes[algorithm_count][i] = h.hexdigest()
        times[algorithm_count][i] = time.time() - tm
    print ("[rpp] %f seconds - %s" % (time.time()-tm,algorithm))
    algorithm_count = algorithm_count + 1

averages = np.average(times,axis=1)
variance = np.var(times,axis=1)
stddev = np.std(times,axis=1)

for i in range(0,4):
    print("[rpp] avg time: %f, var: %f, std: %f (seconds) for %s" % (averages[i],variance[i],stddev[i],list(algorithms)[i]))

print("[rpp] Computing lowest distances (this will take a while)...")
# 4*n*(n-1) computations
count = 0
lowest_distances = [1024,1024,1024,1024,1024,1024,1024,1024,1024,1024]
for i in range(0,4):
    for j in range(0,25000):
        for k in range(0,25000):
            if j == k:
                continue
            h_distance = hamming_distance(random_byte_hashes[i][j],random_byte_hashes[i][k])
            if h_distance < lowest_distances[9]:
                lowest_distances[9] = h_distance
            lowest_distances.sort()
            if k % 1000 == 0:
                print(lowest_distances)

print(lowest_distances)
