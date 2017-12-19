import pandas as pd 

xl = pd.ExcelFile("frmDetails.xlsx")
print(xl.sheet_names)

df = xl.parse("frmDetails")
print(df.head())

