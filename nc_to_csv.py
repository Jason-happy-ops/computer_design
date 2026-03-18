import xarray as xr
import pandas as pd
import os  # 新增：用于处理路径

# ----------------------
# 1. 读取 NetCDF 文件
# ----------------------
nc_file_path = r"C:\Users\29418\Desktop\9ee57604b49bef221035448799e2dceb\data_stream-moda.nc"
ds = xr.open_dataset(nc_file_path)

# ----------------------
# 2. 单位转换
# ----------------------
if "t2m" in ds:
    ds["t2m"] = ds["t2m"] - 273.15
if "tp" in ds:
    ds["tp"] = ds["tp"] * 1000

# 重命名变量
rename_dict = {
    "t2m": "2米气温_℃",
    "tp": "总降水量_mm",
    "u10": "10m风u分量_m/s",
    "v10": "10m风v分量_m/s"
}
ds = ds.rename({k: v for k, v in rename_dict.items() if k in ds})

# ----------------------
# 3. 导出为 DataFrame
# ----------------------
df = ds.to_dataframe().reset_index()
df = df.rename(columns={"latitude": "纬度", "longitude": "经度"})

# ----------------------
# 4. 指定保存到桌面（关键修改）
# ----------------------
csv_file_path = r"C:\Users\29418\Desktop\ERA5-Land_江宁区_202306-08_4变量.csv"
df.to_csv(csv_file_path, index=False, encoding="utf-8-sig")

# ----------------------
# 5. 打印完整路径
# ----------------------
full_csv_path = os.path.abspath(csv_file_path)
print(f"CSV文件已保存到：{full_csv_path}")
print(f"共生成 {len(df)} 行数据")
print("\n数据预览：")
print(df.head())