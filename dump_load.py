import json

# data = '{"aa":"北京"}'
# dict_data = json.loads(data)
# print(data,type(data))
# print(dict_data,type(dict_data))
# str_data = json.dumps(dict_data)
# print(str_data,type(str_data)),
#
# with open('temp.json','w') as f:
#     f.write(str_data)

with open('temp.json','r') as f:
    data = json.load(f)
print(data)

with open('temp2.json','w') as g:
    json.dump(data,g)