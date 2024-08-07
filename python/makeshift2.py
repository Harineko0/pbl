import pandas as pd
import pulp
import calendar
import datetime
from datetime import datetime, timedelta,date
import os
import sys
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





# リストの定義
# 日付リスト
H_hope_0=[]
H_hope_1=[]
H_hope_2=[]
H_hope_3=[]
H_hope_4=[]
staffs=[]
badpeople=[]
dates = [(date(year, month, 1) + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(calendar.monthrange(year, month)[1])]
if month!=1:
    predates = [(date(year, month-1, 1) + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(calendar.monthrange(year, month-1)[1])]
else:
    predates = [(date(year-1, 12, 1) + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(calendar.monthrange(year-1, 12)[1])]

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
    
    for person in data["person"]:  
        name = person["name"]
        hope = person["hope"]
        bad = person["bad"]

        if name not in staffs:
            staffs.append(name)
        for hate in bad:
            badpeople.append((name,hate))
            
        for hopedata in hope:
            hopedata[0]=int(hopedata[0])
            hopedata[0]=date(year,month,hopedata[0]).strftime('%Y-%m-%d')
            if hopedata[1] == "rest":
                H_hope_0.append((name, hopedata[0]))
            elif hopedata[1] == "morning":
                H_hope_1.append((name, hopedata[0]))
            elif hopedata[1] == "noon":
                H_hope_2.append((name, hopedata[0]))
            elif hopedata[1] == "night":
                H_hope_3.append((name, hopedata[0]))
            elif hopedata[1] == "full":
                H_hope_4.append((name, hopedata[0]))        


shift_type=['rest','morning','noon','night','full']
file_path2=f"shift({year}-{month-1:02d}).json"
penaperson=[]

if os.path.exists(file_path2):
    with open(file_path2) as f:
        data2=json.load(f)
        free=[]
        for e in staffs:
            cnt=0
            for d in predates:
                if data2[e][d] !="rest":
                    cnt += 1
            free.append((e,cnt))
        free.sort(key=lambda x:x[1],reverse=True)
        for p in free[:2]:
            penaperson.append(p[0])
    




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
    prob += pulp.lpSum(x[e][d]["full"] for e in staffs) <=2


        
#3日に１回必ず休む
for e in staffs:
    for d in dates[:-3]:
        prob += x[e][d]["rest"]+x[e][(datetime.strptime(d, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")]["rest"]+x[e][(datetime.strptime(d, "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d")]["rest"] >=1

#仲悪い人と同じ日のシフトに入らない
for people in badpeople:
    for d in dates:
        prob += pulp.lpSum(x[e][d][s] for e in people for s in shift_type[1:]) <= 1

#フルが偏らないようにする
for e in staffs:
    for t in staffs:
        prob += pulp.lpSum(x[e][d]["full"] for d in dates) - pulp.lpSum(x[t][d]["full"] for d in dates) <= 3
        
#シフト差をつけない
for e in staffs:
    for t in staffs:
        prob += pulp.lpSum(x[e][d][s] for d in dates for s in shift_type) - pulp.lpSum(x[t][d][s] for d in dates for s in shift_type) <= 5

#ペナルティを追加
if not os.path.exists(file_path2):
    penalty_full_shift = 4*pulp.lpSum(x[e][d]["full"] for e in staffs for d in dates)+pulp.lpSum(x[e][d]["morning"] for e in staffs for d in dates)+pulp.lpSum(x[e][d]["noon"] for e in staffs for d in dates)+pulp.lpSum(x[e][d]["night"] for e in staffs for d in dates)
else:
    penalty_full_shift = 4*pulp.lpSum(x[e][d]["full"] for e in staffs for d in dates)+pulp.lpSum(x[e][d]["morning"] for e in staffs for d in dates)+pulp.lpSum(x[e][d]["noon"] for e in staffs for d in dates)+pulp.lpSum(x[e][d]["night"] for e in staffs for d in dates)+0.2*pulp.lpSum(x[e][d][s] for e in penaperson for d in dates for s in shift_type[1:4])

# 目的関数 (例: 希望休/希望シフトを優先)
prob += penalty_full_shift  # 必要に応じて目的関数を設定

# 求解
status = prob.solve(pulp.PULP_CBC_CMD(msg=1, options=['maxsol 100'], threads=2, timeLimit=15))
print('Status:', pulp.LpStatus[status])

# 計算結果の表示
df = pd.DataFrame(index=dates, columns=staffs)
for e in staffs:
    for d in dates:
        for s in shift_type:
            if x[e][d][s].value() == 1:
                df.at[d, e] = s


# DataFrameの各要素をシフト名に変換
#df = df.map(lambda x: dic[x] if pd.notnull(x) else x)

# 日付のラベル設定
df.columns = staffs

# インデックスのラベル設定

df.index = dates
print(df)
while True:
    listname=input("スタッフを指定して、データを抽出しますか？(しなければ終了と入力):")
    if listname=="終了":
        break
    elif listname in staffs:
        keepdf=df[f'{listname}']
        keepdf.to_json(f'shift({year}-{month:02}-{listname}).json',indent=4)
        print(f"shift({year}-{month:02}-{listname}).jsonを作成しました")
    else:
        print("指定された名前のスタッフのシフトは存在しません")


path=os.getcwd()
df.to_json(f'shift({year}-{month:02}).json',indent=4)
print(f"shift({year}-{month:02}).jsonを作成しました")
