import pandas as pd
import os
import sys
import csv
import re
from datetime import datetime, timedelta

import numpy as np

parent_path = os.path.dirname(os.path.abspath(sys.argv[0]))

if os.path.isfile('/Volumes/IPOD/.scrobbler.log'):
# if True:
    os.system('cp /Volumes/IPOD/.scrobbler.log ./scrobbler.log.backup')
    os.system('cp /Volumes/IPOD/.scrobbler.log ./scrobbler.log')
    # os.system('cp /Users/zach/Downloads/scrobbler.log ./scrobbler.log')

    filename = os.path.join(parent_path, 'scrobbler.log')
    #data = pd.read_csv(filename, sep='\t', skiprows=range(3), header=None)
    data = pd.read_csv(filename, sep='\t', skiprows=range(3), header=None, names = ['Interpret', 'Album', 'Trackname', 'Track Nr', 'Length', 'Listen/Skip', 'Timestamp', '8'], on_bad_lines='warn')
    data = data.dropna(subset=['Timestamp', 'Length'])
    data = data.drop(['Track Nr', 'Listen/Skip', '8'], axis=1)
    # "{artist}", "{track}", "{album}", "{timestamp}", "{album artist}", "{duration}"
    data['Albumartist'] = data['Interpret']
    data = data.reindex(['Interpret', 'Trackname', 'Album', 'Timestamp', 'Albumartist', 'Length'], axis=1)

    fix_timestamps = True
    if fix_timestamps:
        # Fix data with date from 2000
        # Timestamp at which data starts
        false_time = data[data['Timestamp'] < 1000000000]['Timestamp'].max()
        # Timestamp at which data should start
        # <<<< Hier die richtige Zeit eintragen (erster Track) >>>>
        original_time = int((datetime.strptime("2023-02-03 08:40:00", "%Y-%m-%d %H:%M:%S")).timestamp())
        data.loc[data['Timestamp'] < 1000000000, 'Timestamp'] = data[data['Timestamp'] < 1000000000]['Timestamp'] - false_time + original_time

    # print(data.loc[data['Timestamp'].isna()].to_string())
    # Sommerzeit
    data['Timestamp'] = data['Timestamp'].apply(lambda x: (datetime.fromtimestamp(x) - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'))
    # Winterzeit
    # data['Timestamp'] = data['Timestamp'].apply(lambda x: (datetime.fromtimestamp(x) - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'))
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
else:
    print('iPod not found')
