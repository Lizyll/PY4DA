import json  #since it's a web data, use json to parse the data
from collections import defaultdict
from collections import Counter
from pandas import DataFrame, Series
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def get_count(sequence):
    counts = defaultdict(int)  # value will initialize to 0
    for x in sequence:
        counts[x] += 1
    return counts


def top_counts(count_dict, n=10):
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]

#converting a JSON string into a list of python dictionary object
print('-----------------converting-------------------------')
path = 'example.txt'
records = [json.loads(line) for line in open(path)]
time_zone = [rec['tz'] for rec in records if 'tz' in rec]
print('-----------------timezones counting-------------------------')
#counting timezones
counts = get_count(time_zone)
Atz = counts['America/New_York']
print("Ameirica/New_York TimeZone has ", Atz, " records.")
print("The totle record of timezones are ", len(time_zone))
print('-----------------top timezones showing-------------------------')
#top 10 timezones printout
top = top_counts(counts)
print("The top ten time zones are shown below:\n", top)
#collections.Counter to show top 10
counts = Counter(time_zone)
print(counts.most_common(10))
#Counting Time Zones with Pandas
print('-----------------Pandas showing-------------------------')
frame = DataFrame(records)
print(frame) #output shows us the summary view
print("Time zone records in Pandas structure:")
tz_counts = frame['tz'].value_counts()
print(tz_counts[:10])
#munging to fill in a substitute value for unknown and missing time zone records
clean_tz = frame['tz'].fillna('Missing')  #fillna function replaces missing(NA) values and empty strings
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()
print("Clesed data is shown below:\n", tz_counts[:10])
#make a horizontal bar plot
tz_counts[:10].plot(kind='barh', rot=0)
#plt.show()
#parsing user behavior
#Counting Time Zones with Pandas
print('-----------------User behavior-------------------------')
User_Beh = Series([x.split()[0] for x in frame.a.dropna()])
print(User_Beh.value_counts()[:5])
#decompose the time zones into Windows and non-Windows users
print('-----------------Windows, not Windows-------------------------')
cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')
print(operating_system[:5])
by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)
print(agg_counts[:10])
print('-----------------Select the top overall time zones-------------------------')
#use to sort in ascend order
indexer = agg_counts.sum(1).argsort()
print(indexer[:10])
#use take to select the rows in that order, then slice off the last 10 rows
count_subset = agg_counts.take(indexer)[-10:]
print(count_subset)
print('-----------------Ploting-------------------------')
#Top time zones by Windows and non-Windows users
count_subset.plot(kind='barh', stacked=True)
#percentage Windows and non-Windows users in top-occurring time zones
normed_subset = count_subset.div(count_subset.sum(1), axis=0)
normed_subset.plot(kind='barh', stacked=True)
plt.show()
