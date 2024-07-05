# %%
import pandas as pd
import pulp
import datetime
import os
import sys


year = input("何年のシフトを作成しますか:")
month = input("何月のシフトを作成しますか:")
year = int(year)
month = int(month)

file_path = f"{year}-{month:02d}.csv"

if not os.path.exists(file_path):
    print(f"{file_path}は存在しません")
    sys.exit()
else:
    check = input(f"{year}年{month}月のシフトを作成しますか?（はい/いいえ）:")
    if not check == "はい":
        sys.exit()
# 営業日を取得(年,月)
# biz_day=jpbizday.month_bizdays(year, month)
# print(biz_day[0])

# リストの定義
# 日付リスト
data = pd.read_csv(file_path, index_col="Date", encoding="utf-8")
data = data.fillna("")

# 従業員リスト
staffs = data.columns
dates = data.index

shift_type = ["休み", "朝", "昼", "夜", "フル"]
H_hope_0 = []
H_hope_1 = []
H_hope_2 = []
H_hope_3 = []
H_hope_4 = []
"""
shift=[0,1,2,3,4]
staff=list(range(len(staffs)))
day=list(range(len(dates)))
"""
for date in dates:
    for staff in staffs:
        if pd.notna(data.at[date, staff]):
            if data.at[date, staff] in shift_type:
                shift_check = data.at[date, staff]
                if shift_check == "休み":
                    H_hope_0.append((staff, date))
                elif shift_check == "朝":
                    H_hope_1.append((staff, date))
                elif shift_check == "昼":
                    H_hope_2.append((staff, date))
                elif shift_check == "夜":
                    H_hope_3.append((staff, date))
                elif shift_check == "フル":
                    H_hope_4.append((staff, date))


# 最適化モデルの定義
prob = pulp.LpProblem("Shiftmaking", pulp.LpMinimize)

# 変数を用意
x = pulp.LpVariable.dicts("shift", (staffs, dates, shift_type), 0, 3, pulp.LpInteger)

# 希望休を守る
for e, d in H_hope_0:
    prob += pulp.lpSum(x[e][d][s] for s in shift_type) == 1
    prob += x[e][d]["休み"] == 1

# 希望シフト(1:朝)を守る
for e, d in H_hope_1:
    prob += pulp.lpSum(x[e][d][s] for s in shift_type) == 1
    prob += x[e][d]["朝"] == 1

# 希望シフト(2:昼)を守る
for e, d in H_hope_2:
    prob += pulp.lpSum(x[e][d][s] for s in shift_type) == 1
    prob += x[e][d]["昼"] == 1

# 希望シフト(3:夜)を守る
for e, d in H_hope_3:
    prob += pulp.lpSum(x[e][d][s] for s in shift_type) == 1
    prob += x[e][d]["夜"] == 1

# 希望シフト(4:フル)を守る
for e, d in H_hope_4:
    prob += pulp.lpSum(x[e][d][s] for s in shift_type) == 1
    prob += x[e][d]["フル"] == 1


# 各シフトに5人以上のスタッフが必要
for d in dates:
    for s in shift_type[1:4]:
        prob += pulp.lpSum(x[e][d][s] + x[e][d]["フル"] for e in staffs) >= 2

# 各従業員は1日に1つのシフトのみ
for e in staffs:
    for d in dates:
        prob += pulp.lpSum(x[e][d][s] for s in shift_type) == 1

# フルの人数を減らす
for d in dates:
    prob += pulp.lpSum(x[e][d]["フル"] for e in staffs) <= 1

# 休みが多くなり過ぎないようにする(4連休防止)
for e in staffs:
    for d in dates[:-3]:
        prob += (
            x[e][d]["休み"]
            + x[e][
                (
                    datetime.datetime.strptime(d, "%Y-%m-%d")
                    + datetime.timedelta(days=1)
                ).strftime("%Y-%m-%d")
            ]["休み"]
            + x[e][
                (
                    datetime.datetime.strptime(d, "%Y-%m-%d")
                    + datetime.timedelta(days=2)
                ).strftime("%Y-%m-%d")
            ]["休み"]
            + x[e][
                (
                    datetime.datetime.strptime(d, "%Y-%m-%d")
                    + datetime.timedelta(days=3)
                ).strftime("%Y-%m-%d")
            ]["休み"]
            <= 3
        )

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
        prob += (
            pulp.lpSum(x[e][d][s] for d in dates for s in shift_type)
            - pulp.lpSum(x[t][d][s] for d in dates for s in shift_type)
            <= 10
        )

# ペナルティを追加
penalty_full_shift = pulp.lpSum(x[e][d]["フル"] for e in staffs for d in dates)

# 目的関数 (例: 希望休/希望シフトを優先)
prob += penalty_full_shift  # 必要に応じて目的関数を設定

# 求解
status = prob.solve()
print("Status:", pulp.LpStatus[status])

# 計算結果の表示
df = pd.DataFrame(index=dates, columns=staffs)
for e in staffs:
    for d in dates:
        for s in shift_type:
            if x[e][d][s].value() == 1:
                df.at[d, e] = s
""""
# シフト番号をシフト名に変換
dic = {0: '休み', 1: '朝　', 2: '昼　', 3: '夜　', 4: 'フル'}

# DataFrameの各要素をシフト名に変換
df = df.map(lambda x: dic[x] if pd.notnull(x) else x)
"""
# 日付のラベル設定
df.columns = staffs

# インデックスのラベル設定

df.index = dates
print(df)

path = os.getcwd()
df.to_json("shift.json")

# %%
