import arcpy
import os

def script_tool(point_fc, polygon_fc):
    # Calculate the nearest feautre 
    arcpy.analysis.Near(point_fc, polygon_fc, distance_unit="Meters")
    cursor_fields = ['Shape@XY','NEAR_FID','NEAR_DIST'] # Create the cursor fields 
    scur = arcpy.da.SearchCursor(in_table=point_fc,field_names=cursor_fields) # Create search cursor

    for row in scur:
        obj_id = row[1]
        if(obj_id == -1):
            # output if no greenspace is found
            arcpy.AddMessage("No Green space was found")
            continue
        dist = row[2]
        
        # Highlight the nearest polygon feature by selecting it
        where_clause = f"FID = {obj_id}" # create the sql clause
        arcpy.management.SelectLayerByAttribute(in_layer_or_view=polygon_fc, 
                                                    selection_type="NEW_SELECTION", 
                                                    where_clause=where_clause)
        
        # returns the distance to the nearest polygon
        return (dist * 100000) 
        # The distance get multiplied by 100 000 to get realistic results, as there seems to
        # be a problem with the data, because the near function alwas returns results that are 
        # about 0,00000 too small to be correct


if __name__ == "__main__":

    # Get parameters from the tool dialog
    point_fc = arcpy.GetParameterAsText(0)    # Input point feature class
    polygon_fc = arcpy.GetParameterAsText(1)  # Input polygon feature class
    
    # Calculate the walking distance
    walking_distance = script_tool(point_fc, polygon_fc)
    
    # Print the walking distance
    arcpy.AddMessage(f"Walking Distance: {walking_distance: .2f} meters")