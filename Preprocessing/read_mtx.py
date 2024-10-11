import os
import struct
import numpy as np

def read_bin_float(path: str):
    with open(path, 'rb') as rfile:
        data = []
        while True:
            bytes_read = rfile.read(4)
            if not bytes_read:
                break
            data.append(struct.unpack('f', bytes_read)[0])
    return np.array(data)

def read_bin_unsigned_int(path: str):
    with open(path, 'rb') as rfile:
        data = []
        while True:
            bytes_read = rfile.read(4)
            if not bytes_read:
                break
            data.append(struct.unpack('I', bytes_read)[0])
    return np.array(data)

def read_bin_complex(path: str):
    with open(path, 'rb') as rfile:
        data = []
        while True:
            bytes_read = rfile.read(8)  # 2 floats (4 bytes each)
            if not bytes_read:
                break
            real_part, imag_part = struct.unpack('ff', bytes_read)
            data.append(complex(real_part, imag_part))
    return np.array(data)

def main():
    bin_path = 'bin'  # Adjust the path if necessary

    for item in os.listdir(bin_path):
        item_path = os.path.join(bin_path, item)
        if os.path.isdir(item_path):
            print(f"Processing {item}:")
            try:
                # Read the values
                val_path = os.path.join(item_path, 'val.BIN')
                cid_path = os.path.join(item_path, 'cid.BIN')
                csr_path = os.path.join(item_path, 'csr.BIN')

                # Check the type of data and read accordingly
                if os.path.exists(val_path):
                    if os.path.getsize(val_path) % 8 == 0:  # Check if complex
                        values = read_bin_complex(val_path)
                    else:
                        values = read_bin_float(val_path)
                    
                    print("Values:", values)
                
                print("Column indices:", read_bin_unsigned_int(cid_path))
                print("Row pointers:", read_bin_unsigned_int(csr_path))
                print("-" * 20)

            except Exception as e:
                print(f"Error processing {item}: {e}")

if __name__ == '__main__':
    main()
