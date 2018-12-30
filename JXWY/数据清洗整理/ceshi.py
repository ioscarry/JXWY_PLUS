import pandas as pd

df1=pd.DataFrame({'key':['b','b','a','a','b','a','c'],'data1':['A','B','C','D','E','F','G']})

df2=pd.DataFrame({'key':['a','b','d'],'data2':['A','B','C']})

print(pd.merge(df1,df2,on='key',how='outer'))