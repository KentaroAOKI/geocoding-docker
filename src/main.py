from flask import Flask, request, render_template, jsonify, abort
import os
import threading
import random
import socket
import sys
import json
import geopandas as gpd
import shapely
import glob

app = Flask(__name__)

# Load configurations from environment or config file
app.config.from_pyfile('config_file.cfg')
df_shp_estat = None
for file in glob.glob("shapes/*.shp"):
    print('Load {0}.'.format(file))
    if df_shp_estat is None:
        df_shp_estat = gpd.read_file(file,encoding='SHIFT-JIS')
    else:
        df_shp_estat = df_shp_estat.append(gpd.read_file(file,encoding='SHIFT-JIS'))
print('Completed loading {0} shapes.'.format(len(df_shp_estat)))

# for e-stat data
def proc_address(prefecture=None,city=None,street=None):
    result = {}
    if request.method == 'GET' and (prefecture != None or city != None or street != None):
        try:
            df_result = df_shp_estat
            if (prefecture != None):
                df_result = df_result[df_result['PREF_NAME'].str.contains(prefecture)]
            if (city != None):
                df_result = df_result[df_result['CITY_NAME'].str.contains(city)]
            if (street != None):
                df_result = df_result[df_result['S_NAME'].str.contains(street)]
            if not df_result.empty:
                output = "result_{0}_{1}.geojson".format( os.getpid(), threading.get_ident())
                df_result.to_file(output, driver="GeoJSON", encoding='UTF-8')
                with open(output, 'r', encoding='UTF-8') as f:
                    result_string = f.read().replace("\n","")
                os.remove(output)
                result = json.loads(result_string)
        except Exception as e:
            print("Exception {0} {1}".format(type(e), e.args))
            abort(404)
    return jsonify(result)

def proc_geometry(df_func):
    result = {}
    if request.method == 'GET':
        return jsonify(result)
    elif request.method == 'POST':
        try:
            req_json = request.data.decode('utf-8')
            req_geometry = shapely.geometry.shape(json.loads(req_json))
            df_result = df_func(df_shp_estat, req_geometry)
            if not df_result.empty:
                output = "result_{0}_{1}.geojson".format( os.getpid(), threading.get_ident())
                df_result.to_file(output, driver="GeoJSON", encoding='UTF-8')
                with open(output, 'r', encoding='UTF-8') as f:
                    result_string = f.read().replace("\n","")
                os.remove(output)
                result = json.loads(result_string)
        except Exception as e:
            print("Exception {0} {1}".format(type(e), e.args))
            abort(404)
    return jsonify(result)

def df_geom_almost_equals(df_shp, geometry):
    return df_shp[df_shp['geometry'].geom_almost_equals(geometry)]
def df_contains(df_shp, geometry):
    return df_shp[df_shp['geometry'].contains(geometry)]
def df_crosses(df_shp, geometry):
    return df_shp[df_shp['geometry'].crosses(geometry)]
def df_disjoint(df_shp, geometry):
    return df_shp[df_shp['geometry'].disjoint(geometry)]
def df_geom_equals(df_shp, geometry):
    return df_shp[df_shp['geometry'].geom_equals(geometry)]
def df_intersects(df_shp, geometry):
    return df_shp[df_shp['geometry'].intersects(geometry)]
def df_overlaps(df_shp, geometry):
    return df_shp[df_shp['geometry'].overlaps(geometry)]
def df_touches(df_shp, geometry):
    return df_shp[df_shp['geometry'].touches(geometry)]
def df_within(df_shp, geometry):
    return df_shp[df_shp['geometry'].within(geometry)]
def df_covers(df_shp, geometry):
    return df_shp[df_shp['geometry'].covers(geometry)]

@app.route('/', methods=['POST'])
def index():
    return(proc_geometry(df_contains))
@app.route('/geom_almost_equals', methods=['POST'])
def geom_almost_equals():
    return(proc_geometry(df_geom_almost_equals))
@app.route('/contains', methods=['POST'])
def contains():
    return(proc_geometry(df_contains))
@app.route('/crosses', methods=['POST'])
def crosses():
    return(proc_geometry(df_crosses))
@app.route('/disjoint', methods=['POST'])
def disjoint():
    return(proc_geometry(df_disjoint))
@app.route('/geom_equals', methods=['POST'])
def geom_equals():
    return(proc_geometry(df_geom_equals))
@app.route('/intersects', methods=['POST'])
def intersects():
    return(proc_geometry(df_intersects))
@app.route('/overlaps', methods=['POST'])
def overlaps():
    return(proc_geometry(df_overlaps))
@app.route('/touches', methods=['POST'])
def touches():
    return(proc_geometry(df_touches))
@app.route('/within', methods=['POST'])
def within():
    return(proc_geometry(df_within))
@app.route('/covers', methods=['POST'])
def covers():
    return(proc_geometry(df_covers))
@app.route('/address', methods=['GET'])
def address():
    prefecture = request.args.get('prefecture')
    city = request.args.get('city')
    street = request.args.get('street')
    return(proc_address(prefecture = prefecture, city = city, street = street))
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Origin,Accept,X-Requested-With,Content-Type,Access-Control-Request-Method,Access-Control-Request-Headers,Range')
  response.headers.add('Access-Control-Allow-Methods', 'GET,POST,HEAD,OPTIONS')
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

if __name__ == "__main__":
    app.run(host='localhost', port=3000, threaded=True)
