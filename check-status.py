from os import error
import os
import json

for i in range(0, 13):
    for j in range(0, 10):
        try:
            if (os.path.exists(f'log/vn_{j}_{i}.json_0.log')):
                with open(f'log/vn_{j}_{i}.json_0.log', 'r') as f:
                    data = f.read()
                    data = str(data).replace("\'", "\"")
                    json_x = json.loads(data)
                    percent = json_x['percent']
                    print(f'{j}_{i}: {percent}')
                    # print(data)
        except error:
            print(error)
