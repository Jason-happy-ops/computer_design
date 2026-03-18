import xarray as xr
import pandas as pd
import os

# 桌面路径
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")


def nc2csv(nc_file_path):
    # 1. 读取NC文件
    ds = xr.open_dataset(nc_file_path)
    # 2. 转为DataFrame
    df = ds.to_dataframe().reset_index()
    # 3. 生成桌面的CSV路径
    nc_filename = os.path.basename(nc_file_path)
    csv_filename = os.path.splitext(nc_filename)[0] + ".csv"
    csv_file_path = os.path.join(DESKTOP_PATH, csv_filename)
    # 4. 保存到桌面
    df.to_csv(csv_file_path, index=False, encoding="utf-8-sig")
    # 5. 释放资源
    ds.close()
   


if __name__ == "__main__":
    
    
    nc_file = r"C:\Users\29418\Desktop\614bdabbd0ea2bd515bcd85cd1e4f01e\data_stream-moda.nc"
    nc2csv(nc_file)