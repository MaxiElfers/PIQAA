from qgis.core import QgsProject, QgsPointXY, QgsCoordinateReferenceSystem, QgsCoordinateTransform
from PyQt5.QtWidgets import QInputDialog

# Get the district layer
layerDistricts = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]

# Function to check if coordinates fall within any district
def check_district(latitude, longitude):
    # First crs: WGS84
    crsFrom = QgsCoordinateReferenceSystem(4326)
    # Second crs: ETRS89 32N
    crsTo = QgsCoordinateReferenceSystem(25832)
    transformation = QgsCoordinateTransform(crsFrom, crsTo, QgsProject.instance())
    # Create the point from the old coordinates that will be transformed 
    point = QgsPointXY(longitude, latitude)
    # Transform point to new crs 
    transPoint = transformation.transform(point)
    
    # Iterate through district layers
    for feature in layerDistricts.getFeatures():
        # Check if the given coords are within the district
        if feature.geometry().contains(transPoint):
            return True, feature.attributes()[3]
    return False, None
    
parent = iface.mainWindow()
sCoords, bOK = QInputDialog.getText(parent, "Coordinates", "Enter coordinates as latitude, longitude", text = "51.96066,7.62476")

if not bOK:
    print("Input canceled.")
else:
    try: 
        # Create two varibales latitude and longitude from string
        latitude, longitude = map(float, sCoords.split(','))
        # Check if coordinates fall within a district
        in_district, district_name = check_district(latitude, longitude)

        # Output which district was selected or that no district matched the coordinates
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Geoguesser")
        msg = ""
        if in_district:
            msg += f"The coordinates fall within the {district_name} district of Münster."
            msg_box.setIcon(QMessageBox.Information)
        else:
            msg += "The coordinates do not fall within any district of Münster."
            msg_box.setIcon(QMessageBox.Warning)

        msg_box.setText(msg)
        msg_box.addButton(QMessageBox.Ok)
        msg_box.exec_()
    except ValueError:
        print("Invalid input.")
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText('Invalid Values given. Please enter coordinates as "latitude, longitude"')
        msg_box.addButton(QMessageBox.Ok)
        msg_box.exec_()
    