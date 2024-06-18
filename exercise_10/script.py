"""
Script documentation

- Tool parameters are accessed using arcpy.GetParameter() or 
                                     arcpy.GetParameterAsText()
- Update derived parameter values using arcpy.SetParameter() or
                                        arcpy.SetParameterAsText()
"""
import arcpy


def findNearestBusstop(param):
    # load data
    near_features = "stops_ms_mitte"
    in_features = param

    # Near Analysis
    arcpy.analysis.Near(in_features, near_features)

    # init search cursors
    cursor_fields = ['Shape@XY','NEAR_FID','NEAR_DIST'] # Set all used fields
    cursor_fields_name = ['Shape@XY','OBJECTID','name'] # Set all used fields
    scur = arcpy.da.SearchCursor(in_table=in_features,field_names=cursor_fields) # Create search cursor
    scur_name = arcpy.da.SearchCursor(in_table=near_features,field_names=cursor_fields_name) # Create search cursor

    # output data
    for row in scur:
        obj_id = row[1]
        if(obj_id == -1):
            # output if no busstop is found
            arcpy.AddMessage("Keine Haltestelle gefunden")
            continue
        dist = row[2]
        # output distance
        arcpy.AddMessage(f"Entfernung: {dist}")
        for row_name in scur_name:
            if(row_name[1] == obj_id):
                name = row_name[2]
                # output name of the stop
                arcpy.AddMessage(f"Name der Haltestelle: {name}")

    return


if __name__ == "__main__":

    # get parameter
    param0 = arcpy.GetParameterAsText(0)
    # call find NearestBusstop
    findNearestBusstop(param0)