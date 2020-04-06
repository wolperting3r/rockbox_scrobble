import pandas as pd
import os
import sys
import csv
import re
from datetime import datetime

parent_path = os.path.dirname(os.path.abspath(sys.argv[0]))


filename = os.path.join(parent_path, 'scrobbler.log')
os.system(f'cp /Volumes/IPOD/.scrobbler.log {filename}')
#data = pd.read_csv(filename, sep='\t', skiprows=range(3), header=None)
data = pd.read_csv(filename, sep='\t', skiprows=range(3), header=None, names = ['Interpret', 'Album', 'Trackname', 'Track Nr', 'Length', 'Listen/Skip', 'Timestamp', '8'])
data = data.drop(['Track Nr', 'Listen/Skip', '8'], axis=1)
# "{artist}", "{track}", "{album}", "{timestamp}", "{album artist}", "{duration}"
data['Albumartist'] = data['Interpret']
data = data.reindex(['Interpret', 'Trackname', 'Album', 'Timestamp', 'Albumartist', 'Length'], axis=1)
data['Timestamp'] = data['Timestamp'].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
data = data.astype(str)
data = data.apply(lambda x: '"'+x+'"')
filename = os.path.join(parent_path, 'log.csv')
data.to_csv(filename, header=False, quoting=csv.QUOTE_NONE, quotechar="", escapechar="\\", index=False)

# Replace \, with ,
with open(filename, 'r') as file_obj:
    content = file_obj.read()
content = re.sub(r'\\(.)', r'\1', content)
with open(filename, 'w') as file_obj:
    file_obj.write(content)

os.system(f'open -a Sublime\ Text log.csv')
os.system('rm /Volumes/IPOD/.scrobbler.log')
