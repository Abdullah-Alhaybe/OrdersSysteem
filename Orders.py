import requests
import pandas as pd
import pyodbc


loginUrl = ("https://order.vangilsautodemontage.nl/login.php")
OrdersUrl = ("https://order.vangilsautodemontage.nl//json/getafgerondeorders.php")
payload = {
    'loginUsername':'sherwin',
    'loginPassword':'sherwin',
    'btnLogin':'Login'
}

with requests.session() as s:
    s.post(loginUrl,data=payload)
    r = s.get(OrdersUrl)
    res=r.json()
    dfItem = pd.DataFrame.from_records(res)
    dfItem["datum"] = pd.to_datetime(dfItem["datum"]).dt.normalize()
    value_to_check = pd.to_datetime("today").strftime("%m/%d/%Y")
    df_filtered = dfItem[dfItem['datum'] == '2022-08-06']
    result = dfItem.dtypes


print("data in dataframe ... connecting to sql..")
server = 'vangilsserver1.database.windows.net'
database = 'vangilsdatabase'
username = 'vangilsserveradmin'
password = 'QBRrJzX3tgD57b'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER=' + driver +
                      ';SERVER=' + server +
                      ';DATABASE=' + database +
                      ';UID=' + username +
                      ';PWD=' + password)

cursor = cnxn.cursor()

for index, row in df_filtered.iterrows():
    cursor.execute("INSERT INTO [dbo].[products] (product_id,product_name,price) values(?,?,?)", row.id, row.verkoper, row.klantId)
cnxn.commit()
cursor.close()
print("data-copied")

