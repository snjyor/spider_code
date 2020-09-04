import os
import pandas as pd

# dir = os.path.dirname(__file__)
# path_list = []
# for root,dirs,files in os.walk(dir):
#     if files:
#         for f in files:
#             if f.endswith('.csv'):
#                 csv_path = os.path.join(root, f)
#                 path_list.append(csv_path)
path_list = []
for i in range(1,947):
    address = '/Users/apple/code/freecode/scripy/spider/' + str(i) + '.csv'
    path_list.append(address)

full_data = pd.DataFrame()
n = 1
for file in path_list:
    df = pd.read_csv(file)
    # df.drop('Unnamed: 0',axis=1,inplace=True)
    full_data = full_data.append(df,ignore_index=True)
    # print(full_data)
    print('正在合并……{0}'.format(n))
    n += 1

# full_data.drop_duplicates(subset='begin_time',keep='first',inplace=True)

# full_data = full_data[~full_data['vol'].isin([0.0])]   # 通过~取反，选取不包含数字1的行

# full_data.reset_index(drop=True,inplace=True)
# print(full_data)
# full_data.to_csv('binance_BTC_history_data_1_min.csv')
full_data.to_csv('./movie_info.csv')