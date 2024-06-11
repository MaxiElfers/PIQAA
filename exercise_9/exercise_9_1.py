import arcpy
import os

# Set Workspace for the file
arcpy.env.workspace = r"C:\Users\maxim\Downloads\data\exercise_arcpy_1.gdb" # Change this path to the correct path on your device

# Load data from the database
fc_list = arcpy.ListFeatureClasses(feature_type='Point')

# Remove the "active_assests" from the list
fc_list.remove("active_assets")

fc_path_insert = os.path.join(arcpy.env.workspace,"active_assets") # path for insert cursor

# Iterate over each item of the list
for feat in fc_list:
    fc_path_search = os.path.join(arcpy.env.workspace,feat) # path for search cursor

    cursor_fields = ['Shape@XY','status','type'] # Set all used fields
    icur = arcpy.da.InsertCursor(in_table=fc_path_insert,field_names=cursor_fields) # Create Insert cursor
    scur = arcpy.da.SearchCursor(in_table=fc_path_search,field_names=cursor_fields) # Create search cursor

    for row in scur:
        if (row[1] == "active"):
            icur.insertRow(row) # Insert the row to "active_assests" if the row is set to active

    del icur # delete insert cursor
