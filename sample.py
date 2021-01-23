import requests
import json

def main():
    # json_data = '{"type": "Point", "coordinates": [143.0737013,43.0388559]}'
    # response = requests.post('http://127.0.0.1:3000/contains',data=json_data)
    # if (response.status_code == 200):
    #     print(response.json())

    json_data = json.loads('{"type": "Point", "coordinates": [139.76549104760798,35.680515955032476]}')
    response = requests.post('http://127.0.0.1:3000/',json=json_data)
    if (response.status_code == 200):
        print(response.json())

    # for e-stat data
    response = requests.get('http://127.0.0.1:3000/address?prefecture=千葉&city=浦安',json=json_data)
    if (response.status_code == 200):
        print(response.json())

if __name__=='__main__':
    main()
