from arcgis.gis import GIS
from arcgis import features
from arcgis.features import FeatureLayer
from arcgis.features import FeatureLayerCollection
import cred

gis = GIS(cred.AGOL,cred.USER,cred.AGOL_PASS)
csv_path = cred.CSV
titleSearch = 'title:' + cred.FEATURE


search_results = gis.content.search(titleSearch,'Feature Layer')
feature_item = search_results[0]

client_flayer_collection = FeatureLayerCollection.fromitem(feature_item)

client_flayer_collection.manager.overwrite(csv_path)

feature_layers = feature_item.layers
layer = feature_layers[0]
featureNumbRows = layer.query(where='1=1', return_count_only=True)
if featureNumbRows < 1:
    print = "There are no records in the published feature layer.  This needs to be corrected immediately"
else:
    print = "The CSV has successfully published " + str(featureNumbRows) + " records."



