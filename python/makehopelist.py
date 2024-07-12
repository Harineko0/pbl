import csv
from datetime import datetime, timedelta, date
import os
import sys
import calendar
import pandas as pd


# 名前の確認と追加
def check_name(data):
    while True:
        name = input(
            "シフト希望を編集する人の名前を入力してください（例:山田太郎）（終了する場合は終了と入力）: "
        )
        check = input(
            f"希望シフトを編集するのは{name}さんでよろしいですか?(はい/いいえ):"
        )
        if check == "はい":
            if name not in data.columns:
                check = input(
                    f"{name}さんのデータが存在しません。{name}さんを従業員リストに追加しますか?(はい/いいえ):"
                )
                if check == "はい":
                    data[name] = ""
                    print(f"{name}さんを従業員リストに追加しました")
                    return name
            else:
                return name
        elif check == "終了":
            sys.exit()


# CSVファイルの作成、初期設定
def initialize_csv(file_path, date_str):
    year, month = date_str.split("-")[:2]
    year = int(year)
    month = int(month)
    dates = [
        (date(year, month, 1) + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(calendar.monthrange(year, month)[1])
    ]

    data = pd.DataFrame({"Date": dates})
    data.to_csv(file_path, index=False, encoding="utf-8")
    print(f"{file_path} を作成しました。")
    return data


# シフト情報の追加
def add_shift(file_path, name, shift_date_str, shift_type, type_list, data):
    if shift_date_str in data["Date"].values:
        row_index = data[data["Date"] == shift_date_str].index[0]
        current_shift = (
            data.at[row_index, name]
            if name in data.columns and pd.notna(data.at[row_index, name])
            else ""
        )

        if current_shift in type_list:
            check = input(
                f"既にシフト希望が入っています({current_shift})、上書きしますか？（はい/いいえ）:"
            )
            if check == "はい":
                data.at[row_index, name] = shift_type
            else:
                return
        else:
            data.at[row_index, name] = shift_type
    else:
        print(f"日付 {shift_date_str} が存在しません。")

    data.to_csv(file_path, index=False)
    print(f"{name}の{shift_date_str} のシフトを更新しました。")


# ユーザーからの入力を受け取り、CSVファイルを更新する関数
def main():
    while True:
        try:
            year = input("何年のシフト希望を管理しますか？（例:2024）:")
            year = int(year)
            month = input("何月のシフト希望を管理しますか？（例:10）:")
            month = int(month)
            shift_date_str = f"{year}-{month:02d}-01"
            break
        except ValueError:
            print("適切な年・月を入力してください")
            continue

    file_path = f"{year}-{month:02d}.csv"

    if not os.path.exists(file_path):
        check = input(
            f"{file_path} が存在しないため、新しく作成します。よろしいですか?（はい/いいえ）:"
        )
        if check == "はい":
            data = initialize_csv(file_path, shift_date_str)
        else:
            sys.exit()
    else:
        data = pd.read_csv(file_path, encoding="utf-8")

    name = check_name(data)

    while True:
        day = input("日付を入力してください（例:20）（終了する場合は0と入力）: ")
        if day == "0":
            data.to_csv(file_path, index=False)
            sys.exit()
        try:
            day = int(day)
        except ValueError as error:
            print("整数を入力してください")
            continue
        if 1 <= day <= calendar.monthrange(year, month)[1]:
            break
        else:
            print("適切な日を入力してください")

    shift_date_str = f"{year}-{month:02d}-{day:02d}"
    print(shift_date_str)

    while True:
        shift_type = input("シフトの種類を入力してください（休み、朝、昼、夜、フル）: ")
        type_list = ["休み", "朝", "昼", "夜", "フル"]
        if shift_type in type_list:
            break
        else:
            print("適切なシフトを選択してください")
            continue

    add_shift(file_path, name, shift_date_str, shift_type, type_list, data)
    check = input("入力を終わりますか?（終わる場合は終了と入力）:")
    if not check == "終了":
        main


if __name__ == "__main__":
    main()
