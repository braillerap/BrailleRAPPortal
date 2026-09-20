import json
from osm import OSMprocess
from osm import OSMprocessStreet
from osm import OSMutils

class OSMBridge:
    def __init__(self):
        self.osmt = OSMprocess.Osmprocess()
        self.osms = OSMprocessStreet.OSMprocessStreet()
        self._window = None

    def GetISO639_country_code (self):
        list = OSMutils.omsutils_get_iso639_code ()
        
        return list

    def ReadTransportData (self, city, transport_type, iso639_city_code, place_id):
        ret = self.osmt.ReadTransportData (city, transport_type, iso639_city_code, place_id)
        print ("ReadTransportData", ret)
        if ret == 0:
            ret = self.osmt.ReadTransportData (city, transport_type, iso639_city_code, place_id, direct=True)
        
        js = json.dumps (ret)
        return js


    def GetTransportLines (self):
        #ret = self.osmt.GetTransportLineList ()
        ret = self.osmt.GetTransportDataLineList ()
        print ("ret", ret, type(ret))
        resstr = json.dumps (ret,  ensure_ascii=False)
        print ("GetTransportLineList", resstr)
        return resstr

    def GetTransportDataSvg (self, linelist, drawstation, linestrategy, polygon):
        print ("GetTransportSVG", linelist, drawstation, int(linestrategy), type(linestrategy))

        svg = self.osmt.GetTransportDataSvg (linelist, drawstation, int(linestrategy), polygon)
        print ("GetTransportSVG svg size", len(svg))
        return svg

    def GetTransportData (self, linelist, drawstation, linestrategy, polygon):
        linearray = json.loads (linelist)
        #print ("json decoded", linearray )
        svg = self.GetTransportDataSvg (linearray, drawstation, linestrategy, polygon)
        liststation = self.osmt.GetTransportDataStations (linearray)

        str = json.dumps({"svg": svg, "stations": liststation}, ensure_ascii=False)
        return str

    def GetTransportSVGbase64 (self):
        svg = self.osmt.get_svg ()
        return svg



    def ReadStreetMapData (self, latitude, longitude, radius, building, footpath, polygon, includeWater, cliping):
        street_data = self.osms.ReadStreetMapData (latitude, longitude, radius)
        print ("building", building, "footpath", footpath, "polygon", polygon)
        svg = self.osms.GetStreetMapSVG (street_data, latitude, longitude, building, footpath, polygon,includeWater, cliping)
        
        return svg