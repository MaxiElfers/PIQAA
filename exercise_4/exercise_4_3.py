# Import modules
from qgis.core import QgsVectorLayer, QgsProject
from qgis.core import *
import os


# Supply path to qgis install location
#QgsApplication.setPrefixPath("/path/to/qgis/installation", True)

# Path to data and QGIS-project
layer_path = r"path\to\layer_folder"
project_path = r"path\to\project\name_of_project"  # add the project name too

files = os.listdir(layer_path)


# Create QGIS instance and "open" the project
project = QgsProject.instance()

for file in files:
    # Check if layer is valid
    if(file.endswith(".shp")):
        file_path = os.path.join(layer_path, file)
        toc_name = os.path.splitext(file)[0]

        # Create layer
        layer = QgsVectorLayer(file_path, toc_name, "ogr")
        if not layer.isValid():
            print("Error loading the layer!")
        else:
            # Add layer to project
            project.addMapLayer(layer)
            print("Layer added to project\nProject saved successfully!")

# Save the project
project.write(project_path)

print("Project created successfully!")