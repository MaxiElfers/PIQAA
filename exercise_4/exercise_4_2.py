from qgis.core import QgsProject, QgsVectorLayer

# Get the selected feature from the Schools layer
layer = QgsProject.instance().mapLayersByName('Schools')[0]
selected_features = layer.selectedFeatures()

csv_path = '/Users/melfers/Desktop/SchoolReport.csv'
with open(csv_path, 'w') as csv_file:
    csv_file.write("Name;X;Y\n")

    # Iterate over selected features
    for feature in selected_features:
        # Get the name of the school
        name = feature['Name']

        # Get the geometry of the feature
        geometry = feature.geometry()

        # Get the X and Y coordinates
        x_coord = geometry.asPoint().x()
        y_coord = geometry.asPoint().y()

        # Write the feature information to the CSV file
        csv_file.write(f"{name};{x_coord};{y_coord}\n")

print("School information has been written to SchoolReport.csv")