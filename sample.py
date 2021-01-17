import requests
import json

def main():
    json_data = '{"type": "Point", "coordinates": [143.0737013,43.0388559]}'
    response = requests.post('http://127.0.0.1:3000/contains',data=json_data)

    # or
    # json_data = json.loads('{"type": "Point", "coordinates": [143.0737013,43.0388559]}')
    # response = requests.post('http://127.0.0.1:3000/',json=json_data)

    if (response.status_code == 200):
        print(response.json())

if __name__=='__main__':
    main()
