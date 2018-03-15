import json

fn = './allen_structures_non_nested_rma.json'
jsonData = open(fn).read()
data = json.loads(jsonData)['msg']
id = 560581568
idNums = [d['id'] for d in data]
