from arcgis.gis import GIS
from arcgis import features
import time
import smtplib
import _thread
import cred
import pandas as pd
from arcgis.features import FeatureLayer
gis = GIS(cred.AGOL,cred.USER,cred.AGOL_PASS)
csv_path = cred.CSV

def send_msg(MSG):
    server = smtplib.SMTP( "smtp-mail.outlook.com", 587 )
    server.starttls()
    server.login( cred.FROM, cred.PASS )
    str_print =''.join([MSG,time.strftime('%I:%M:%S %p')])
    server.sendmail(cred.FROM, cred.TO, str_print)
    server.quit()

search_results = gis.content.search('title: ClientDataTest','Feature Layer')
feature_item = search_results[0]

from arcgis.features import FeatureLayerCollection
client_flayer_collection = FeatureLayerCollection.fromitem(feature_item)

try:
    open_csv = pd.read_csv(csv_path)
    CSVdimensions = open_csv.shape
    numbRows = CSVdimensions[0]
    if numbRows < 1:
        print ("The rows are empty so do not publish")
        MSG  = '\nThere are no records in the CSV to be published.  Publishing will not take place. '
        send_msg(MSG)
    else:
        client_flayer_collection.manager.overwrite(csv_path)
        feature_layers = feature_item.layers
        layer = feature_layers[0]
        featureNumbRows = layer.query(where='1=1', return_count_only=True)
        featureNumbRows
        query_result1 = layer.query(where="SPID IS NULL")
        nullNumb = len(query_result1.features)
    if nullNumb > 0:
        print ("There are null ID values")
        MSG  = '\nThere are null Account Numbers.  Publishing will continue, but these issues need to be corrected. '
        send_msg(MSG)
    else:
        print ("There are no null ID values")
    if featureNumbRows != numbRows:
        print ("The number of records in the published feature service do not match the number of records in the CSV file ")
        MSG = '\nThe number of records in the published feature service do not match the number of records in the CSV file '
        send_msg(MSG)
    else:
        print ("All systems nominal")
except:
    print ("There is no CSV file in the specified path")
    MSG = '\nThere is no CSV file in the spedified path'
    send_msg(MSG)



