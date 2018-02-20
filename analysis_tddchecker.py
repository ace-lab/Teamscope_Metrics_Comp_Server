import json

json1_file = open("results/result.json")
json1_str = json1_file.read()
data = json.loads(json1_str)
print(data)

#define analysis functions here