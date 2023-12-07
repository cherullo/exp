import os.path
import sys
import subprocess
import io

reqs = subprocess.check_output([sys.executable, '-m', 'pip',
'freeze', '--local'])

print (reqs.decode())

filepath = os.path.dirname(__file__)
filename = os.path.join(filepath, '..//requirements.txt')

with open(filename, 'wb') as f:
    f.write(reqs)



