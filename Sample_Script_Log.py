from arcgis.gis import GIS
from arcgis import features
import time
import datetime
import smtplib
import _thread
import cred
from arcgis.features import FeatureLayer
gis = GIS(cred.AGOL,cred.USER,cred.AGOL_PASS)
csv_path = cred.CSV
x = datetime.datetime.now()
titleSearch = 'title:' + cred.FEATURE

def log_file(MSG):
    logFileName = "CSV_Upload_Log_" + x.strftime("%d-%b-%y")+ ".txt"
    logFile = open(logFileName,"w")
    logFile.write(MSG)
    logFile.close() 

try:
    search_results = gis.content.search(titleSearch,'Feature Layer')
    feature_item = search_results[0]

    from arcgis.features import FeatureLayerCollection
    client_flayer_collection = FeatureLayerCollection.fromitem(feature_item)

    client_flayer_collection.manager.overwrite(csv_path)

    feature_layers = feature_item.layers
    layer = feature_layers[0]
    featureNumbRows = layer.query(where='1=1', return_count_only=True)
    if featureNumbRows < 1:
        MSG = "There are no records in the published feature layer.  This needs to be corrected immediately"
        log_file(MSG)
    else:
        MSG = "The CSV has successfully published " + str(featureNumbRows) + " records."
        log_file(MSG)
except:
    MSG = "The CSV did not publish"
    log_file(MSG)
