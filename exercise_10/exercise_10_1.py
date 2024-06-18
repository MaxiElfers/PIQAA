import arcpy

# load data
arcpy.env.workspace = r"C:\workspace\python_in_qgis_arcgis\PIQAA\exercise_10\Exercise_10.gdb" # Change this path to the correct path on your device
in_features = "dev_input_point"
near_features = "stops_ms_mitte"

# Near Analysis
arcpy.analysis.Near(in_features, near_features)

cursor_fields = ['Shape@XY','NEAR_FID','NEAR_DIST'] # Set all used fields
cursor_fields_name = ['Shape@XY','OBJECTID','name'] # Set all used fields
scur = arcpy.da.SearchCursor(in_table=in_features,field_names=cursor_fields) # Create search cursor
scur_name = arcpy.da.SearchCursor(in_table=near_features,field_names=cursor_fields_name) # Create search cursor

# output data
for row in scur:
    obj_id = row[1]
    dist = row[2]
    arcpy.AddMessage(dist)
    for row_name in scur_name:
        if(row_name[1] == obj_id):
            name = row_name[2]
            arcpy.AddMessage(name)