from django.http import HttpResponse
from django.template import loader

from .models import Shop
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
import requests
import json
from django.contrib.gis.geos import Point, Polygon
from django.http import JsonResponse
from django.shortcuts import redirect

def index(request):
    template = loader.get_template('polls/indexMobile.html')
    context = {

    }
    return HttpResponse(template.render(context, request))

class MapPage(TemplateView):
    template_name = '../templates/polls/indexMobile.html'


def get_amenities(request):
    """
    make a call to Overpass API and return the results of a search in GeoJSON
    :param request: Incoming request includes a search string and a bbox string
    :return: Results in GeoJSON
    """
    import overpy
    api = overpy.Overpass()
    print(request.body)

    amenity = ""
    requestByteString = request.body
    requestString = str(requestByteString, 'utf-8')
    print(requestString)
    amenity = requestString
    if amenity:
        amenity = amenity.lower()

    print(amenity)

    query = """
    [out:json][timeout:25];
    area[name="Dublin"]->.searchArea;
    (
        node[%s](area.searchArea); 
        way[%s](area.searchArea); 
        rel[%s](area.searchArea); 
    ); 
    out center body qt; 
    """ % ( amenity,amenity,amenity )
    print(query)
    try:
        result = api.query(query)

        result_geojson = {"type": "FeatureCollection", "features": []}

        for node in result.nodes:
            this_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [None, None]
                },
                "properties": {
                }
            }

            this_feature["geometry"]["coordinates"][0] = float(node.lon)
            this_feature["geometry"]["coordinates"][1] = float(node.lat)

            for tag in node.tags:
                this_feature["properties"][tag] = node.tags[tag]

            result_geojson["features"].append(this_feature)

        for way in result.ways:
            this_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [None, None]
                },
                "properties": {
                }
            }

            this_feature["geometry"]["coordinates"][0] = float(way.center_lon)
            this_feature["geometry"]["coordinates"][1] = float(way.center_lat)

            for tag in way.tags:
                this_feature["properties"][tag] = way.tags[tag]

            result_geojson["features"].append(this_feature)

        return JsonResponse(result_geojson, status=200)

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)
