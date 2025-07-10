import pandas as pd
import numpy as np
import re
import ast
import os

# 讀取 CSV 檔案
df_train = pd.read_csv('C:/Users/ASUS/OneDrive/桌面/文駿/比賽/AI CUP 2025春季賽－桌球智慧球拍資料的精準分析競賽/39_Training_Dataset/train_info.csv')

def fix_format(s):
    # 確保數字之間有逗號，然後轉換為列表
    s = re.sub(r'\s+', ',', s.strip())  # 把空格換成逗號
    s = s.replace('[,', '[')  # 修正開頭逗號
    s = s.replace(',]', ']')  # 修正結尾逗號
    return ast.literal_eval(s)

# 處理 cut_point 欄位成 list（不展開為欄位）
df_train['cut_point'] = df_train['cut_point'].apply(fix_format)

# 設定輸出資料夾
output_folder = 'C:/Users/ASUS/OneDrive/桌面/文駿/比賽/AI CUP 2025春季賽－桌球智慧球拍資料的精準分析競賽/39_Training_Dataset/train_csv/'
os.makedirs(output_folder, exist_ok=True)

# 設定 txt 檔案的路徑
txt_folder = 'C:/Users/ASUS/OneDrive/桌面/文駿/比賽/AI CUP 2025春季賽－桌球智慧球拍資料的精準分析競賽/39_Training_Dataset/train_data/'

# 批量處理 txt 檔案
for i in range(1, 1968): # 1, 1968
    txt_path = os.path.join(txt_folder, f'{i}.txt')

    if not os.path.exists(txt_path):
        print(f"檔案 {i}.txt 不存在，跳過...")
        continue

    # 讀取 txt 檔案
    df_train_txt = pd.read_csv(txt_path, sep='\t', header=None)
    df_train_txt = df_train_txt[0].str.split(expand=True)
    df_train_txt.columns = ['Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz']
    df_train_txt = df_train_txt.astype(int)

    # 取得對應 unique_id 的 row
    df_train_filtered = df_train[df_train['unique_id'] == i].copy()

    if df_train_filtered.empty:
        print(f"找不到 unique_id = {i} 的資料，跳過...")
        continue

    cp_list = df_train_filtered['cut_point'].iloc[0]
    for idx in range(1, 28):  # 1 到 27
        col_name = f'cut_point_{idx}'
        value = cp_list[idx] if len(cp_list) > idx else np.nan
        df_train_filtered[col_name] = value

    # 合併資料
    df_merged = pd.concat([df_train_filtered.reset_index(drop=True), df_train_txt], axis=1)
    df_merged = df_merged.fillna(method='ffill')

    # 儲存結果
    output_path = os.path.join(output_folder, f"unique_id_{i}.csv")
    df_merged.to_csv(output_path, index=False)
    print(f"已儲存 {output_path}")

print('hello world')
