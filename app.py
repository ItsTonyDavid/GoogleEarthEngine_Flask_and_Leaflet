from flask import Flask, render_template, request
import ee
from scripts.Sentinel_CO import get_CO

app = Flask(__name__)

def getCenterCoords(long1, long2, lat1, lat2):
    long = (long1 + long2) / 2
    lat = (lat1 + lat2) / 2
    return [long, lat]

@app.route('/hello')
def hello_world():
    la1 = request.args.get('la1', 0.0, type=float)
    lo1 = request.args.get('lo1', 0.0, type=float)
    la2 = request.args.get('la2', 0.0, type=float)
    lo2 = request.args.get('lo2', 0.0, type=float)
    la3 = request.args.get('la3', 0.0, type=float)
    lo3 = request.args.get('lo3', 0.0, type=float)
    la4 = request.args.get('la4', 0.0, type=float)
    lo4 = request.args.get('lo4', 0.0, type=float)
    coordenates = [[lo1,la1],[lo2,la2],[lo3,la3],[lo4,la4]]

    map_coords = getCenterCoords(coordenates[0][1],coordenates[1][1], coordenates[1][0], coordenates[2][0])
    return render_template('gee_map.html', dict=get_CO(coordenates), setCords=map_coords)

@app.route('/')
def index():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080', debug=True)
