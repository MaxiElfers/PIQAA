poolLayer = QgsProject.instance().mapLayersByName('public_swimming_pools')[0]

# Getting all fields of the layer
fields = poolLayer.fields()
provider = poolLayer.dataProvider()
capabilities = provider.capabilitiesString()

# Set Type from "H" and "F" to "Hallenbad" and "Freibad"
# Checking if the capabilty is part of the layer
if "Change Attribute Values" in capabilities:
    print("Features of this layer can be modified...")
    
    # If modifying is possible, get all features of the layer 
    # and loop through them.
    for pool in poolLayer.getFeatures():
        
        if pool["Type"] == "H":
            attributes = {poolLayer.fields().indexOf("Type"):"Hallenbad"}
            poolLayer.dataProvider().changeAttributeValues({pool.id():attributes})
            
        if pool["Type"] == "F":
            attributes = {poolLayer.fields().indexOf("Type"):"Freibad"}
            poolLayer.dataProvider().changeAttributeValues({pool.id():attributes})
            
# adding new field district with the city district
district = QgsField('district', QVariant.String, len = 50)
provider.addAttributes([district])
poolLayer.updateFields()

# intersect with schools
districtLayer = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
for pool in poolLayer.getFeatures():
    
    # check, if schools are within
    for district in districtLayer.getFeatures():
        if pool.geometry().within(district.geometry()):
            attributes = {poolLayer.fields().indexOf('district'):district['Name']}
            poolLayer.dataProvider().changeAttributeValues({pool.id():attributes})
            break