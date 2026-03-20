import rasterio
import os
import numpy as np

# ====================== 核心配置（只改这3行） ======================
INPUT_DIR = r"G:\monthly"          # 存放所有TIFF的文件夹
OUTPUT_CSV = r"G:\jiangning_gpp_all.csv"  # 最终结果保存路径
ERA5_POINTS = [                    # 江宁区ERA5经纬度点
    (118.5, 31.8), (118.6, 31.8), (118.7, 31.8), (118.8, 31.8), (118.9, 31.8),
    (118.5, 31.9), (118.6, 31.9), (118.7, 31.9), (118.8, 31.9), (118.9, 31.9),
    (118.5, 32.0), (118.6, 32.0), (118.7, 32.0), (118.8, 32.0), (118.9, 32.0)
]

# ====================== 初始化变量 ======================
final_result = []  # 存储所有文件的结果
# 获取文件夹里所有TIFF文件（按文件名排序）
tif_files = sorted([f for f in os.listdir(INPUT_DIR) if f.startswith("map_") and f.endswith(".tif")])
total_files = len(tif_files)

print(f"共发现 {total_files} 个TIFF文件，开始批量处理...")
print("="*80)

# ====================== 批量处理每个TIFF ======================
for idx, filename in enumerate(tif_files, 1):
    tif_path = os.path.join(INPUT_DIR, filename)
    print(f"[{idx}/{total_files}] 处理文件：{filename}")
    
    # 1. 从文件名提取年月（map_202101.tif → 2021年1月）
    try:
        ym_str = filename.split("_")[1].replace(".tif", "")
        year = int(ym_str[:4])
        month = int(ym_str[4:])
    except:
        print(f"⚠️ 文件名 {filename} 格式异常，跳过")
        continue
    
    # 2. 打开TIFF并提取+修复数值
    try:
        with rasterio.open(tif_path) as src:
            nodata = src.nodata  # 获取TIFF标注的无效值
            
            for lon, lat in ERA5_POINTS:
                # 初始化默认值
                raw_val = np.nan
                fixed_val = np.nan
                reason = "未知错误"
                
                # 步骤1：校验经纬度是否在TIFF范围内
                if not (src.bounds.left <= lon <= src.bounds.right and src.bounds.bottom <= lat <= src.bounds.top):
                    reason = "经纬度超出TIFF范围"
                else:
                    # 步骤2：经纬度转行列号
                    row, col = src.index(lon, lat)
                    if row < 0 or col < 0 or row >= src.height or col >= src.width:
                        reason = "行列号无效"
                    else:
                        # 步骤3：读取原始值
                        raw_val = src.read(1, window=((row, row+1), (col, col+1)))[0, 0]
                        
                        # 步骤4：修复空值（3x3窗口插值）
                        if np.isnan(raw_val) or raw_val == nodata or raw_val == 0:
                            # 读取周围3x3像元
                            window = ((max(0, row-1), min(src.height, row+2)), 
                                     (max(0, col-1), min(src.width, col+2)))
                            surrounding_vals = src.read(1, window=window)
                            # 过滤无效值
                            valid_vals = surrounding_vals[
                                ~np.isnan(surrounding_vals) & 
                                (surrounding_vals != nodata) & 
                                (surrounding_vals != 0)
                            ]
                            if len(valid_vals) > 0:
                                fixed_val = np.mean(valid_vals)
                                reason = "原始值为空，取3x3均值"
                            else:
                                fixed_val = -1  # 完全无有效值标注
                                reason = "周围无有效值"
                        else:
                            fixed_val = raw_val
                            reason = "原始值有效"
                
                # 步骤5：保存结果
                final_result.append({
                    "longitude": lon,
                    "latitude": lat,
                    "year": year,
                    "month": month,
                    "raw_gpp": raw_val,
                    "fixed_gpp": fixed_val,
                    "reason": reason
                })
        print(f"✅ {filename} 处理完成")
    except Exception as e:
        print(f"❌ 处理 {filename} 出错：{str(e)}，跳过")
    print("-"*60)

# ====================== 保存最终结果到CSV ======================
if final_result:
    with open(OUTPUT_CSV, "w", encoding="utf-8") as f:
        # 写表头
        f.write("longitude,latitude,year,month,raw_gpp,fixed_gpp,reason\n")
        # 写数据
        for item in final_result:
            f.write(
                f"{item['longitude']},{item['latitude']},{item['year']},{item['month']},"
                f"{item['raw_gpp']:.2f},{item['fixed_gpp']:.2f},{item['reason']}\n"
            )
    print("="*80)
    print(f"✅ 所有文件处理完成！结果已保存到：{OUTPUT_CSV}")
    print(f"📊 共提取 {len(final_result)} 条数据，文件大小：{os.path.getsize(OUTPUT_CSV)/1024:.2f} KB")
else:
    print("❌ 未提取到任何数据，请检查文件路径/格式！")