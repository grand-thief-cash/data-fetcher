
import pandas as pd

def merge_two_csv_by_index(csv1_path, csv2_path, index_col, output_csv):
    # 读取两个 CSV 文件
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)

    # 连表操作
    merged_df = pd.merge(df1, df2, on=index_col)

    # 保存为新的 CSV 文件
    merged_df.to_csv(output_csv, index=False)


def merge_two_csv_by_two_index(csv1_path, csv2_path, index_col1, index_col2, output_csv):
    # 读取两个 CSV 文件
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)

    # 连表操作
    merged_df = df1.merge(df2, left_on=index_col1, right_on=index_col2)

    # 保存为新的 CSV 文件
    merged_df.to_csv(output_csv, index=False)

