import arcpy

# Set Workspace for the file
arcpy.env.workspace = r"C:\Users\maxim\Downloads\data\exercise_arcpy_1.gdb" # Change this path to the correct path on your device

# Load data from the database
active_assets = "active_assets"

# Function to check which buffer need to be added to which field
def get_buffer_dist(asset_type):
    if asset_type == "mast":
        return 300
    elif asset_type == "mobile_antenna":
        return 50
    elif asset_type == "building_antenna":
        return 100
    else:
        return 0

# Define the expression to call the function
expression = "get_buffer_dist(!type!)"

# Add the field 
arcpy.management.AddField(in_table=active_assets, field_name="buffer_dist", field_type="SHORT")
# Calculate the field
arcpy.management.CalculateField(in_table=active_assets, field="buffer_dist", expression=expression)

# Crete buffered feature class
arcpy.analysis.Buffer(active_assets, "coverage", "buffer_dist")
