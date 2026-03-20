import pandas as pd

df = pd.read_csv(r"C:\Users\29418\Desktop\计算机大赛\data_stream-moda.csv")
df.info()

df_negative = df[df['GPP'] < 0]
print(df_negative)