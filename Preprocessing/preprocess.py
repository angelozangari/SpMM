import os
from scipy.io import mmread
from scipy.sparse import csr_matrix
import copy
import struct
import numpy as np
import config


def write_to_bin_float(path: str, obj: list):
    with open(path, 'wb') as wfile:
        for i in range(len(obj)):
            wfile.write(struct.pack('f', obj[i]))


def write_to_bin_unsigned_int(path: str, obj: list):
    with open(path, 'wb') as wfile:
        for item in obj:
            wfile.write(struct.pack('I', item))


def write_to_bin_complex(path: str, obj: list):
    with open(path, 'wb') as wfile:
        for item in obj:
            real_part = item.real
            imag_part = item.imag
            wfile.write(struct.pack('ff', real_part, imag_part))

def main():
    if not os.path.exists('bin'):
        os.mkdir('bin')

    for item in os.listdir(config.bench_path):
        if os.path.isdir(config.bench_path + '/' + item):
            target_mat_file = config.bench_path + '/' + item + '/' + item + '.mtx'
            origin_matrix_a = mmread(target_mat_file).tocsr()

            print("-"*20)
            print("Processing {}".format(item))
            
            if not os.path.exists('bin/' + item):
                os.mkdir('bin/' + item)
    
            # check if matrix is complex
            if np.iscomplexobj(origin_matrix_a.data):
                write_to_bin_complex('bin/' + item + '/val.BIN', origin_matrix_a.data)
            else:
                write_to_bin_float('bin/' + item + '/val.BIN', origin_matrix_a.data.tolist())
            # write_to_bin_unsigned_int('bin/poisson3Da/rcsr.BIN', rcsr)
            write_to_bin_unsigned_int('bin/' + item + '/cid.BIN', origin_matrix_a.indices.tolist())
            write_to_bin_unsigned_int('bin/' + item + '/csr.BIN', origin_matrix_a.indptr.tolist())
            print(len(origin_matrix_a.indptr.tolist()))
            print(len(origin_matrix_a.indices.tolist()))


if __name__ == '__main__':
    main()
