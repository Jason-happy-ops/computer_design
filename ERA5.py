
import cdsapi
import os


SAVE_FILE = "ERA5-Land_江宁区.nc"
# 江宁经纬度
JIANGNING_AREA = [32.0, 118.5, 31.8, 118.9]
# 时间范围
YEARS = ["2021", "2022", "2023"]
MONTHS = [f"{m:02d}" for m in range(1, 13)]  # 自动生成01-12月

#初始化客户端
try:
    c = cdsapi.Client(
        timeout=8640,  
        quiet=False    # 显示下载进度
    )
    print("成功运行")
except Exception as e:
    print(f" CDS客户端初始化失败:{e}")
    print(" 请检查 .cdsapirc 配置文件是否正确(包含API密钥)")
    exit(1)


if os.path.exists(SAVE_FILE):
    file_size = os.path.getsize(SAVE_FILE) / 1024 / 1024
    print(f"文件已存在：{SAVE_FILE}（大小：{file_size:.2f} MB)")
else:
    try:
        # 核心下载请求
        c.retrieve(
            'reanalysis-era5-land-monthly-means',
            {
                'product_type': 'monthly_averaged_reanalysis',
                'variable': [
                    '2m_temperature',                # 2米气温
                    'total_precipitation',            # 总降水量
                    '10m_u_component_of_wind',       # 10米风u分量
                    '10m_v_component_of_wind',       # 10米风v分量
                    'surface_pressure',              # 地表气压
                    'leaf_area_index_high_vegetation',# 高植被LAI
                ],
                'year': YEARS,
                'month': MONTHS,
                'time': '00:00',
                'area': JIANGNING_AREA,
                'format': 'netcdf',
            },
            SAVE_FILE
        )

        # 验证下载结果
        if os.path.exists(SAVE_FILE):
            file_size = os.path.getsize(SAVE_FILE) / 1024 / 1024
            print(f"文件路径：{os.path.abspath(SAVE_FILE)}")
            print(f"文件大小：{file_size:.2f} MB（3年6变量正常体积）")
        else:
            print("\n数据下载失败")

    except Exception as e:
        print(f"\n下载报错：{e}")
      