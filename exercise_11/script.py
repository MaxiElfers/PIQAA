"""
Script documentation

- Tool parameters are accessed using arcpy.GetParameter() or 
                                     arcpy.GetParameterAsText()
- Update derived parameter values using arcpy.SetParameter() or
                                        arcpy.SetParameterAsText()
"""
import arcpy, sys, time


def findNearestBusstop(in_feat, name_field, name_value, in_layer):

    # Set second time step
    arcpy.SetProgressorLabel("Creating temporary layer")
    arcpy.SetProgressorPosition(1)

    # Build a layer with the name field & field value
    sql = f"{name_field}='{name_value}'"
    arcpy.MakeFeatureLayer_management(in_features=in_layer,out_layer='feats_for_near',where_clause=sql)

    # Timeout for progress bar
    time.sleep(2)

    # Set third time step
    arcpy.SetProgressorLabel("Calculating distance")
    arcpy.SetProgressorPosition(2)

    # Near Analysis
    arcpy.analysis.Near('feats_for_near', in_layer)

    # init search cursors
    cursor_fields = ['Shape@XY','NEAR_FID','NEAR_DIST'] # Set all used fields
    cursor_fields_name = ['Shape@XY','OBJECTID','name'] # Set all used fields
    scur = arcpy.da.SearchCursor(in_table=in_feat,field_names=cursor_fields) # Create search cursor
    scur_name = arcpy.da.SearchCursor(in_table=in_layer,field_names=cursor_fields_name) # Create search cursor

    # Timeoffset for progress bar
    time.sleep(2)

    arcpy.SetProgressorLabel("Loading distance and name")
    arcpy.SetProgressorPosition(3)

    # Timeoffset for progress bar
    time.sleep(2)

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

    # adding the progressor
    arcpy.SetProgressor(type='step',message='Starting script',min_range=0, max_range=4,step_value=1)
    time.sleep(0.5)
    # Set the first time step
    arcpy.SetProgressorLabel("Loading the inputs")
    arcpy.SetProgressorPosition(0)

    # get parameter
    in_feat = arcpy.GetParameterAsText(0)
    in_layer =arcpy.GetParameterAsText(1)
    name_field = arcpy.GetParameterAsText(2)
    name_value = arcpy.GetParameterAsText(3)

    # Timeout for progress bar
    time.sleep(2)

    # call find NearestBusstop
    findNearestBusstop(in_feat, name_field, name_value, in_layer)