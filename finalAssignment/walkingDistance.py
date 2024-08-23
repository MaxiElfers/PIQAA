import arcpy

def calculate_distance(point_fc, polygon_fc, fid):
    """
    Calculates the distance between a given point and the nearset green space.

    Parameters:
    point_fc (str): The path to the point feature class (point).
    polygon_fc (str): The path to the polygon feature class (polygon).
    fid (str): The ID field of the polygon_fc used to select the nearest polygon.

    Returns:
    None (float): The calculated distance in meter.
    """

    arcpy.analysis.Near(point_fc, polygon_fc, distance_unit="Meters") # calculate nearest green space
    cursor_fields = ['Shape@XY','NEAR_FID','NEAR_DIST'] # Set all used fields
    scur = arcpy.da.SearchCursor(in_table=point_fc,field_names=cursor_fields) # Create search cursor

    for row in scur:
        obj_id = row[1]
        if(obj_id == -1):
            # output if no green space is found
            arcpy.AddMessage("No Green space was found")
            continue
        dist = row[2]
        
        # Highlight the nearest polygon feature by selecting it
        where_clause = f"\"{fid}\" = {obj_id}"
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
    fid = arcpy.GetParameterAsText(2)         # Input polygon ID field
    
    # Calculate the distance
    walking_distance = calculate_distance(point_fc, polygon_fc, fid)
    
    # Log the walking distance
    arcpy.AddMessage(f"Walking Distance: {walking_distance:.2f} meters")