import difflib
import hashlib
import os
import shutil
import sys
import tempfile
import time

from src import AzarArchive
from src.encoders.shannon import ShannonEncoder, ShannonDecoder

w = shutil.get_terminal_size()


def read_string(name: str):
    with open(name, 'rb') as f:
        return f.read()


if len(sys.argv) != 2:
    print('Specify file from ./tests folder')
    exit(-1)

filename = os.path.abspath(f'./tests/{sys.argv[1]}')
if not os.path.exists(filename):
    print('File don\'t exists')
    exit(-1)

print('''
   _   _                     _____                      
  /_\ | | _____  _____ _   _/ _  / __ ___   ____ _ _ __ 
 //_\\| |/ _ \ \/ / _ \ | | \// / / _` \ \ / / _` | '__|
/  _  \ |  __/>  <  __/ |_| |/ //\ (_| |\ V / (_| | |   
\_/ \_/_|\___/_/\_\___|\__, /____/\__,_| \_/ \__,_|_|   
                       |___/                            
''')

tempname1 = tempfile.mktemp()
tempname2 = tempfile.mktemp()

print(f'Processing {filename}')
print()

print('Encoding...')
start = time.time()
with AzarArchive(filename, tempname1, ShannonEncoder) as enc:
    enc.write()
end = time.time()
print(f'{end - start} seconds elapsed')
print()

print('Decoding...')
start = time.time()
with AzarArchive(tempname1, tempname2, ShannonDecoder) as dec:
    dec.read()
end = time.time()
print(f'{end - start} seconds elapsed')
print()

text1 = read_string(filename)
text2 = read_string(tempname2)

hash1 = hashlib.sha1(text1).hexdigest()
hash2 = hashlib.sha1(text2).hexdigest()

valid = hash1 == hash2

print()
print('-' * w.columns)

if not valid:
    print('Hashes mismatch'.center(w.columns))
    print(f'{hash1} != {hash2}'.center(w.columns))

    data1 = text1.decode('utf-8')
    data2 = text2.decode('utf-8')

    res = [item for item in difflib.ndiff(data1, data2) if item[0] != ' ']

    print()
    print('Differences:'.center(w.columns))
    for item in res:
        print(repr(item).center(w.columns))
else:
    print('Hashes are the same'.center(w.columns))
    print()
    print(f'{hash1}'.center(w.columns))

print('-' * w.columns)
print()

print('Cleaning up...')
print()

try:
    os.unlink(tempname1)
    os.unlink(tempname2)
except Exception as e:
    print('Failed to cleanup:', e)
    print(tempname1, tempname2)
