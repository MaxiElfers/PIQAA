import processing
schools = QgsProject.instance().mapLayersByName('Schools')[0]
city_districts = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
result = processing.run("qgis:countpointsinpolygon",
{'POINTS': schools,
'POLYGONS': city_districts,
'WEIGHT': None,
'OUTPUT': 'memory:'})

output_layer = result['OUTPUT']
features = output_layer.getFeatures()

# Iterate through the features
for feature in features:
    print(feature['Name'], ":", feature[7])
