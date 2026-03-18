# 导入 CDS API 客户端
import cdsapi

# 初始化客户端（自动读取 .cdsapirc 配置）
c = cdsapi.Client(
    timeout=4800,  # 
    retry_max=5    # 
)

# 核心：申请 ERA5-Land 月平均数据
print("开始申请江宁区 ERA5-Land 数据...")
c.retrieve(
    # 数据集名称（ERA5-Land 月平均再分析）
    'reanalysis-era5-land-monthly-means',
    # 数据筛选条件
    {
        'product_type': 'monthly_averaged_reanalysis',  # 月平均数据
        # 变量列表：包含你需要的4个核心变量
        'variable': [
            '2m_temperature',                # 2米气温
            'total_precipitation',            # 总降水量
            '10m_u_component_of_wind',       # 10米风u分量（东西向）
            '10m_v_component_of_wind',       # 10米风v分量（南北向）
        ],
        'year': '2023',                       # 年份：2023年
        'month': ['06', '07', '08'],          # 月份：6-8月
        'time': '00:00',                      # 时间戳（月平均固定为00:00）
        # 空间范围：江宁区 [北, 西, 南, 东]
        'area': [32.0, 118.5, 31.8, 118.9],
        'format': 'netcdf',                   # 输出格式：NetCDF（便于后续处理）
    },
    # 本地保存文件名（清晰命名，方便识别）
    'ERA5-Land_江宁区_202306-08_4变量.nc'
)

print("数据下载完成！文件已保存为：ERA5-Land_江宁区_202306-08_4变量.nc")