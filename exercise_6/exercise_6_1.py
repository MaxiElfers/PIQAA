from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry

# Create layer with uir string
uri = "polygon?crs=EPSG:4326&field=standard_land_value:float&field=type:string&field=district:string&index=yes" 
layer = QgsVectorLayer(uri, "temp_standard_land_value_muenster", "memory")

# Start editing the layer
layer.startEditing()

csv = open('/Users/melfers/Documents/Uni/Master 2.Semester/PythonGIS/Data for Session 6/standard_land_value_muenster.csv', 'r')
lines = csv.readlines()

# Iterate through the file and create features
for line in lines[1:]:
    # split line into parts
    parts = line.strip().split(';')
    # store the single parts in variables
    standard_land_value = parts[0]
    land_type = parts[1]
    district = parts[2]
    wkt = parts[3].replace('\n', '')
        
    geom = QgsGeometry.fromWkt(wkt)
    # Check if the geometry is a polygon
    if geom.type() == 2:
        polygon_geom = QgsGeometry.fromWkt(wkt)

        if polygon_geom.isGeosValid():
            # Add all the fields to the feature
            feat = QgsFeature(layer.fields())
            feat.setAttribute('standard_land_value', standard_land_value)
            feat.setAttribute('type', land_type)
            feat.setAttribute('district', district)
            feat.setGeometry(polygon_geom)
            features.append(feat)
        else:
            print("Invalid geometry found for district:", district)
    else: 
        print("Wrong geometry type for:", district)

# Add features to the layer
layer.addFeatures(features)

# Commit changes
layer.commitChanges()

# Add the layer to the map
QgsProject.instance().addMapLayer(layer)