import numpy as np
import pandas as pd
import json

filename="customer-data.csv"

def readFile(filename):
    return pd.read_csv(filename)

data = readFile(filename)
data['cust_id']=data['cust_id'].apply(lambda x: str(x))


# http://127.0.0.1:5000/avg/cust_id,cust_segment,market/comp_mscore
# http://127.0.0.1:5000/count/cust_id,cust_segment,market/cust_id
# {"yr": 2001, "mk": "APAC", "id": "0", "sg": "Network", "ms": 100.0, "ic": 100.0, "gd": 100.0, "dt": "2001-4-01"}


tempdf = pd.DataFrame(data)
tempdf['date'] = tempdf[['year', 'month', 'market','cust_id','cust_segment','comp_mscore', 'ic_net_score', 'gdi_net_score', 'cc_count_as_zside', 'cc_count_as_aside', 'net_ibx_presence', 'net_metro_presence']].apply(lambda x : '{}-{}-01'.format(x[0],x[1]), axis=1)
tempdf = tempdf.drop(['month', 'cc_count_as_zside', 'cc_count_as_aside', 'net_ibx_presence', 'net_metro_presence'], axis=1)
tempdf.columns = ['yr', 'mk', 'id', 'sg', 'ms', 'ic', 'gd', 'dt']

def getndx():
    global tempdf
    aggregated_list = pd.DataFrame(tempdf).to_dict(orient='records')
    base_list="["
    for dt in aggregated_list:
        if dt == aggregated_list[-1]:
            base_list+=json.dumps(dt)
        else:
            base_list+=json.dumps(dt)+','
    base_list+="]"
    return base_list


def avgAggregator(groupColumns,targetColumn):
    global data
    aggregated_avg=data.groupby(groupColumns)[targetColumn].agg(['mean', 'count'])
    aggregated_list=pd.DataFrame(aggregated_avg).round(2).reset_index().to_dict(orient='records')
    base_list="["
    for dt in aggregated_list:
        if dt == aggregated_list[-1]:
            base_list+=json.dumps(dt)
        else:
            base_list+=json.dumps(dt)+','
    base_list+="]"
    return base_list

def countAggregator(groupColumns,targetColumn):
    global data
    aggregated_count=data.groupby(groupColumns)[targetColumn].count()
    aggregated_count=pd.DataFrame(aggregated_count)
    aggregated_count.columns=['count']
    aggregated_list=aggregated_count.reset_index().to_dict(orient='records')
    base_list="["
    for dt in aggregated_list:
        if dt == aggregated_list[-1]:
            base_list+=json.dumps(dt)
        else:
            base_list+=json.dumps(dt)+','
    base_list+="]"
    return base_list

def getCustomer(custID):
    global data
    custObjs=pd.DataFrame(data)
    custObjs=custObjs[custObjs.cust_id == custID]
    aggregated_list=custObjs.to_dict(orient='records')
    base_list="["
    for dt in aggregated_list:
        if dt == aggregated_list[-1]:
            base_list+=json.dumps(dt)
        else:
            base_list+=json.dumps(dt)+','
    base_list+="]"
    return base_list



def groupLocSector():
    global data
    summary=data.groupby(['market','year'])['comp_mscore']
    #.agg(['min', 'mean', 'max','std', 'quantile([.25])','quantile([.75])','count'])
    summary=pd.DataFrame(summary)
    #summary.columns=['min', 'mean', 'max','std', 'quantile(.25)','quantile(.75)','count']
    #summary=summary.reset_index()
    print (summary)
    return "hi da"




def getLocSpecificData(loc):
    global data
    aggregated_sum=data.groupby(groupColumns)[groupColumns[0]].count()
    aggregated_sum=pd.DataFrame(aggregated_sum)
    aggregated_sum.columns=['count']
    aggregated_sum=aggregated_sum.reset_index()
    aggregated_dict=aggregated_sum.to_dict(orient='records')
    base_dict="{"
    for dt in aggregated_dict:
        base_dict+=json.dumps(dt)
    base_dict+="}"
    return base_dict
