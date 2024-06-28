#%%
import pandas as pd
import pulp
import jpbizday
import calendar
import datetime
from datetime import datetime, timedelta,date
import os
import sys
import numpy
import json

year=input("何年のシフトを作成しますか:")
month=input("何月のシフトを作成しますか:")
year = int(year)
month=int(month)

file_path=f"{year}-{month:02d}.json"

if not os.path.exists(file_path):
    print(f"{file_path}は存在しません")
    sys.exit()
else:
    check=input(f"{year}年{month}月のシフトを作成しますか?（はい/いいえ）:")
    if not check=="はい":
        sys.exit()
# 営業日を取得(年,月)
#biz_day=jpbizday.month_bizdays(year, month)
#print(biz_day[0])

# リストの定義
# 日付リスト
H_hope_0=[]
H_hope_1=[]
H_hope_2=[]
H_hope_3=[]
H_hope_4=[]
staffs=[]
dates = [(date(year, month, 1) + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(calendar.monthrange(year, month)[1])]

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
    
    for person in data["person"]:  
        name = person["name"]
        hope = person["hope"]
        day = person["day"]

        if name not in staffs:
            staffs.append(name)

        if hope == "rest":
            H_hope_0.append((name, day))
        elif hope == "morning":
            H_hope_1.append((name, day))
        elif hope == "noon":
            H_hope_2.append((name, day))
        elif hope == "night":
            H_hope_3.append((name, day))
        elif hope == "full":
            H_hope_4.append((name, day))        


shift_type=['rest','morning','noon','night','full']

"""
shift=[0,1,2,3,4]
staff=list(range(len(staffs)))
day=list(range(len(dates)))
"""


# 最適化モデルの定義
prob = pulp.LpProblem('Shiftmaking', pulp.LpMinimize)

# 変数を用意
x = pulp.LpVariable.dicts("shift", (staffs, dates, shift_type), 0, 3, pulp.LpInteger)

# 希望休を守る
for e, d in H_hope_0:
    prob += pulp.lpSum(x[e][d][s] for s in shift_type) == 1
    prob += x[e][d]["rest"] == 1

# 希望シフト(1:朝)を守る
for e, d in H_hope_1:
    prob += pulp.lpSum(x[e][d][s] for s in shift_type) == 1
    prob += x[e][d]["morning"] == 1

# 希望シフト(2:昼)を守る
for e, d in H_hope_2:
    prob += pulp.lpSum(x[e][d][s] for s in shift_type) == 1
    prob += x[e][d]["noon"] == 1

# 希望シフト(3:夜)を守る
for e, d in H_hope_3:
    prob += pulp.lpSum(x[e][d][s] for s in shift_type) == 1
    prob += x[e][d]["night"] == 1

# 希望シフト(4:フル)を守る
for e, d in H_hope_4:
    prob += pulp.lpSum(x[e][d][s] for s in shift_type) == 1
    prob += x[e][d]["full"] == 1



# 各シフトに5人以上のスタッフが必要
for d in dates:
    for s in shift_type[1:4]:
        prob += pulp.lpSum(x[e][d][s]+x[e][d]["full"] for e in staffs) >= 2
    

# 各従業員は1日に1つのシフトのみ
for e in staffs:
    for d in dates:
        prob += pulp.lpSum(x[e][d][s] for s in shift_type) == 1

#フルの人数を減らす
for d in dates:
    prob += pulp.lpSum(x[e][d]["full"] for e in staffs) <=3

#休みが多くなり過ぎないようにする(4連休防止)
for e in staffs:
    for d in dates[:-3]:
        prob += x[e][d]["rest"]+x[e][(datetime.strptime(d, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")]["rest"]+x[e][(datetime.strptime(d, "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d")]["rest"]+x[e][(datetime.strptime(d, "%Y-%m-%d") + timedelta(days=3)).strftime("%Y-%m-%d")]["rest"] <=3
        
"""""
for e in staffs:
    for d in dates[:-3]:
        prob += pulp.lpSum(x[e][d][s] for s in shift_type[1:]) +pulp.lpSum(x[e][(datetime.datetime.strptime(d, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")][s] for s in shift_type[1:])+pulp.lpSum(x[e][(datetime.datetime.strptime(d, "%Y-%m-%d") + datetime.timedelta(days=2)).strftime("%Y-%m-%d")][s] for s in shift_type[1:])+pulp.lpSum(x[e][(datetime.datetime.strptime(d, "%Y-%m-%d") + datetime.timedelta(days=3)).strftime("%Y-%m-%d")][s] for s in shift_type[1:]) <=3
"""       
"""
for d in dates:
    for s in shift_type[1:]:
        for a in shift_type[1:]:
            # 朝、昼、夜、フルシフトがかぶらないようにする
            prob += x["加藤"][d][s] + x["武藤"][d][a] <= 1
"""

for e in staffs:
    for t in staffs:
        prob += pulp.lpSum(x[e][d][s] for d in dates for s in shift_type) - pulp.lpSum(x[t][d][s] for d in dates for s in shift_type) <= 10

#ペナルティを追加
penalty_full_shift = 3*pulp.lpSum(x[e][d]["full"] for e in staffs for d in dates)+pulp.lpSum(x[e][d]["morning"] for e in staffs for d in dates)+pulp.lpSum(x[e][d]["noon"] for e in staffs for d in dates)+pulp.lpSum(x[e][d]["night"] for e in staffs for d in dates)

# 目的関数 (例: 希望休/希望シフトを優先)
prob += penalty_full_shift  # 必要に応じて目的関数を設定

# 求解
status = prob.solve()
print('Status:', pulp.LpStatus[status])

# 計算結果の表示
df = pd.DataFrame(index=dates, columns=staffs)
for e in staffs:
    for d in dates:
        for s in shift_type:
            if x[e][d][s].value() == 1:
                df.at[d, e] = s
# シフト番号をシフト名に変換
"""
dic = {'休み': 'none',  '朝':'morning', '昼':'noon', '夜':'night', 'フル':'full'}
"""
# DataFrameの各要素をシフト名に変換
#df = df.map(lambda x: dic[x] if pd.notnull(x) else x)

# 日付のラベル設定
df.columns = staffs

# インデックスのラベル設定

df.index = dates
print(df)

path=os.getcwd()
df.to_json(f'shift({year}-{month:02}).json')

# %%
