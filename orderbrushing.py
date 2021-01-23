import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

order = pd.read_csv('/kaggle/input/order-brushing-dataset-shopee-code-league-week-1/order_brush_order.csv')
order.event_time = pd.to_datetime(order.event_time, format ='%Y-%m-%d %H:%M:%S')

df = order.set_index("event_time").sort_index()
process = df.groupby(['shopid', 'userid', pd.Grouper(freq='H', label='left')]).count()

listuserid = []
supspec = process[process.orderid>=3]
supspec.reset_index().groupby('shopid')['userid'].aplly(lambda x: listuserid.append(x.values))
def concat_userid(data):
    result = '&'.join(str(x) for x in data)
    return result

bulk_userid = []
for i in listuserid:
    bulk_userid.append(concat_userid(i))

df_brush = pd.DataFrame({"shopid": supspec.reset_index()['shopid'].unique(), "userid": bulk_userid})
df0 = pd.DataFrame({'shopid': df['shopid'].unique(), 'userid': 0})
res_df = pd.concat([df0[~df0.shopid.isin(df_brush.shopid)], df_brush])
res_df.to_csv("submission.csv", index=False)