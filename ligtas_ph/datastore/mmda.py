import pandas as pd
import re
import os

dirname = os.path.dirname(__file__)
mmda_data = os.path.join(dirname, 'data_mmda_traffic_spatial.csv')

class MMDA:
    def __init__(self):
        self.data = pd.read_csv(mmda_data)

    # Main Clean Data
    def main(self):
        raw = self.data
        # Data Cleaning
        raw.columns = [x.lower() for x in raw.columns] #renames all headers to lowercase
        raw = raw.loc[raw['high_accuracy'] == 1]
        raw = raw.drop_duplicates(subset=['tweet'],keep='first',ignore_index=True) # remove duplicates
        raw['id'] = raw.reset_index().index + 1 # Add ID, Where ID = Row Number
        raw['incident_type'] = raw['type'] #rename type column to incident_type
        return raw
    
    def incident(self):
        incident = self.main()
        incident = incident[['id','date', 'time', 'city', 'location','latitude','longitude', 'direction', 'incident_type', 'lanes_blocked']]
        return incident

    def vehicle(self):
        '''
        Clean Involved and Extract Data from raw incidents dataframe.
        '''
        incidents = self.main()
        data = {'id':[], 'qty':[], 'vehicle':[], 'incident_id':[]}
        for index, row in incidents.iterrows():
            first_split = re.split(',|AND|ANG',str(row['involved']))
            for item in first_split:
                item = item.strip()
                item = item.split(' ')
                try:
                    if item[0] == '':
                        pass
                    elif item[0].isdigit():
                        data['incident_id'].append(row['id'])
                        data['qty'].append(int(item[0]))
                        data['vehicle'].append(''.join(map(str, item[1:])))
                    elif item[0][0].isdigit():
                        data['incident_id'].append(row['id'])
                        data['qty'].append(int(item[0][0]))
                        data['vehicle'].append(item[0][2:])
                    else:
                        data['incident_id'].append(row['id'])
                        data['qty'].append(1)
                        data['vehicle'].append(''.join(map(str, item)))
                except:
                    data['incident_id'].append(row['id'])
                    data['qty'].append(1)
                    data['vehicle'].append(''.join(map(str, item)))
        for x in range(1,len(data['qty'])+1):
            data['id'].append(x)
        data = pd.DataFrame(data=data,columns = list(data.keys()))
        return data.loc[data['vehicle'] != '']

    def tweet(self):
        raw = self.main()
        incident_tweet = raw[['tweet','source','id']]
        incident_tweet = incident_tweet.copy()
        incident_tweet['incident_id'] = incident_tweet['id']
        incident_tweet['id'] = [x for x in range(1,len(incident_tweet)+1)]
        incident_tweet = incident_tweet[['id','tweet','source','incident_id']]
        return incident_tweet