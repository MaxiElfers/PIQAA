"""
Script documentation

- Tool parameters are accessed using arcpy.GetParameter() or 
                                     arcpy.GetParameterAsText()
- Update derived parameter values using arcpy.SetParameter() or
                                        arcpy.SetParameterAsText()
"""
import arcpy


def script_tool(param0):
    # load data
    arcpy.env.workspace = r"C:\workspace\python_in_qgis_arcgis\PIQAA\exercise_10\Exercise_10.gdb" # Change this path to the correct path on your device
    near_features = "stops_ms_mitte"

    # Load data from the database
    fc_list = arcpy.ListFeatureClasses(feature_type='Point')

    near_features = fc_list.find("stops_ms_mitte")

    # Near Analysis
    arcpy.analysis.Near(param0, near_features)

    cursor_fields = ['Shape@XY','NEAR_FID','NEAR_DIST'] # Set all used fields
    cursor_fields_name = ['Shape@XY','OBJECTID','name'] # Set all used fields
    scur = arcpy.da.SearchCursor(in_table=param0,field_names=cursor_fields) # Create search cursor
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

    return


if __name__ == "__main__":

    param0 = arcpy.GetParameterAsText(0)

    script_tool(param0)
    arcpy.SetParameterAsText(2, "Result")