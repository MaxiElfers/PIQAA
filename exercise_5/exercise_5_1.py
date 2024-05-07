from PyQt5.QtWidgets import QMessageBox
from qgis.core import QgsGeometry
from qgis.core import QgsDistanceArea

distance_area = QgsDistanceArea()

layerDistricts = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
layerSchools = QgsProject.instance().mapLayersByName('Schools')[0]

# initiate request for features and ordering
request = QgsFeatureRequest()
nameClause = QgsFeatureRequest.OrderByClause("Name", ascending = True)
orderby = QgsFeatureRequest.OrderBy([nameClause])
request.setOrderBy(orderby)

districts_names = []
for feature in layerDistricts.getFeatures(request):
    name = feature["Name"]
    districts_names.append(name)

parent = iface.mainWindow()
sDistrict, bOk = QInputDialog.getItem(parent, "District Names", "Select District: ", districts_names)

if bOk == False:
    QMessageBox.warning(parent, "Schools", "User cancelled")


# polygon from district
for feature in layerDistricts.getFeatures():
    if feature['Name'] == sDistrict:
        selectedDistrict = feature
        
# remove previous selection
layerSchools.removeSelection()


# intersect with schools
schoolsInDistrict = []
for school in layerSchools.getFeatures():
    schoolGeometry = school.geometry()
    districtGeometry = selectedDistrict.geometry()
    
    # check, if schools are within
    if schoolGeometry.within(districtGeometry):
        layerSchools.select(school.id())
        
        # centroid calculation
        centroid = districtGeometry.centroid()
        centroid_coords = centroid.asPoint()
        
        # distance calculation
        distance = distance_area.measureLine(school.geometry().asPoint(), centroid_coords)
        distance /= 1000
        distance = round(distance, 2)
        
        # adding school and distance to list
        schoolsInDistrict.append([school['NAME'], distance])
        

# sort schools
schoolsInDistrict = sorted(schoolsInDistrict, key=lambda x: x[0])
# zoom to selected schools
iface.mapCanvas().zoomToSelected(layerSchools)


# output schools within the district
print(schoolsInDistrict)
msg_box = QMessageBox()
msg_box.setWindowTitle(f"Schools in {sDistrict}")
msg = ""
# check if schools were selected
if schoolsInDistrict:
    for school in schoolsInDistrict:
        msg +="\n" + f"{school[0]} distance to district centrum {school[1]} km."
else:
    msg += "Es befinden sich keine Schulen in dem ausgewählten District."
    
msg_box.setText(msg)
msg_box.setIcon(QMessageBox.Information)
msg_box.addButton(QMessageBox.Ok)
msg_box.exec_()