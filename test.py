import pandas as pd

df = pd.DataFrame([
    ['佐藤', 170, 60],
    ['田中', 160, 50],
    ['鈴木', 165, 58]
])

df.columns = ['name', 'height', 'weight']

print(df['height'])
