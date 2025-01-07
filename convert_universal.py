import pandas as pd
import os
import sys
import csv
import re
from datetime import datetime, timedelta

import numpy as np

parent_path = os.path.dirname(os.path.abspath(sys.argv[0]))

hostname = os.uname().machine
# Execute only on mac, not on iPhone
if hostname == 'arm64':
    if os.path.isfile('/Volumes/IPOD/.scrobbler.log'):
        os.system('cp /Volumes/IPOD/.scrobbler.log ./scrobbler.log.backup')
        os.system('cp /Volumes/IPOD/.scrobbler.log ./scrobbler.log')

# if True:
if os.path.isfile(os.path.join(parent_path, '.scrobbler.log')):

    filename = os.path.join(parent_path, '.scrobbler.log')
    filenameUTF = os.path.join(parent_path, '.scrobbler_utf8.log')

    # Try to read every line with UTF-8. Append to new file if successfull. (Gets rid of all lines that mess up reading as an UTF-8 file.)
    with open(filename, 'r', encoding='utf-8', errors='ignore') as infile, open(filenameUTF, 'w', encoding='utf-8') as outfile:
            for line in infile:
                try:
                    # Try encoding the line to UTF-8 to see if it works
                    line.encode('utf-8')
                    # If it works, write the line to the output file
                    outfile.write(line)
                except UnicodeEncodeError:
                    # If there is an encoding error, skip the line
                    print(f"Skipping line due to encoding error: {line}")
                    continue

    #data = pd.read_csv(filename, sep='\t', skiprows=range(3), header=None)
    data = pd.read_csv(filenameUTF, sep='\t', skiprows=range(3), header=None, names = ['Interpret', 'Album', 'Trackname', 'Track Nr', 'Length', 'Listen/Skip', 'Timestamp', '8'], on_bad_lines='warn')
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
    # data['Timestamp'] = data['Timestamp'].apply(lambda x: (datetime.fromtimestamp(x) - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'))
    # Winterzeit
    data['Timestamp'] = data['Timestamp'].apply(lambda x: (datetime.fromtimestamp(x) - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'))
    data = data.astype(str)
    data = data.apply(lambda x: '"'+x+'"')
    filenameCSV = os.path.join(parent_path, 'log.csv')
    data.to_csv(filenameCSV, header=False, quoting=csv.QUOTE_NONE, quotechar="", escapechar="\\", index=False)

    # Replace \, with ,
    with open(filenameCSV, 'r') as file_obj:
        content = file_obj.read()
    content = re.sub(r'\\(.)', r'\1', content)
    with open(filenameCSV, 'w') as file_obj:
        file_obj.write(content)

    # Execute only on mac, not on iPhone
    if hostname == 'arm64':
        print("Execution on Mac, deleting .scrobbler.log on iPod"
        os.system(f'open -a Sublime\ Text log.csv')
        os.system('rm /Volumes/IPOD/.scrobbler.log')
else:
    print('iPod not found')
