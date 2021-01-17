## Geocoding Server

The Dockerfile that builds an Geocoding server.

## Build
```
git clone https://github.com/KentaroAOKI/geocoding-docker.git
cd geocoding-docker
docker build -t geocoding .
```

## Usage
Specify the port to bind to. Also specify the directory of shape files to mount.
```
docker run -d -p 3000:3000 -v /home/user/shapes:/shapes geocoding
```
You can access the following URL with a geojson.
```
http://xxx/contains
```

## Where should I get the shapefile?
Please refer to the following for Japanese Shape files.
https://qiita.com/kekekekenta/items/9b955b3075fa660e37e2

## How to use an python code.
POST geojson to the URL to get the address.

```python
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
```