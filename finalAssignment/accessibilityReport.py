import arcpy
from arcpy.sa import KernelDensity
import os

def create_heatmap(input_features, population_field, dist_name_field, districts, dist_name, layout_name, green_area, population):
    """
    Creates a heatmap (density map) using the Kernel Density tool and adds it to the active map.

    Parameters:
    input_features (str): The path to the input feature class (point).
    population_field (str): Population_field for the Kernel density function (usually None).
    dist_name_field (str): The column of the district names.
    districts (str): The path to the district feature class (polygon).
    dist_name (str): The name of the district to filter.
    layout_name (str): The name of the layout for the print.
    green_area (float): The number of the amount of green area.
    population (float): The number of the population.

    Returns:
    None
    """

    # Set environment settings
    arcpy.env.workspace = arcpy.env.scratchGDB

    # Get the current project and map
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    active_map = aprx.activeMap
    
    # Check if an active map is found
    if active_map is None:
        arcpy.AddError("No active map found. Please ensure there is an active map in the project.")
        return

    # Add user info
    arcpy.AddMessage(f"Processing district: {dist_name}")
    
    # Create virtual layer that only contains the selected district 
    where_clause = f"\"{dist_name_field}\" = '{dist_name}'"
    arcpy.management.MakeFeatureLayer(districts, "DistrictLayer", where_clause)

    # Perform the selection
    arcpy.management.SelectLayerByLocation(input_features, "WITHIN", "DistrictLayer")

    # Create the kernel density raster
    heatmap = KernelDensity(input_features, population_field, cell_size=0.0001)

    # Save the output raster
    out_path = aprx.defaultGeodatabase + r"\heatmap"
    heatmap.save(out_path)

    # Add the heatmap raster to the active map
    heatmap_layer = active_map.addDataFromPath(out_path)

    # Move heatmap layer above the district layer for the visualisation
    reference_layer = active_map.listLayers(districts)[0]
    active_map.moveLayer(reference_layer, heatmap_layer)
        
    # Export the map layout to a PDF
    pdf_path = arcpy.env.scratchFolder + r"\heatmap_report.pdf"
    export_pdf_layout(aprx, pdf_path, dist_name, layout_name, green_area, population)

def export_pdf_layout(aprx, pdf_path, district_name, layout_name, green_area, population):
    """
    Exports the layout to a PDF with the given district name as part of the report.

    Parameters:
    aprx (arcpy.mp.ArcGISProject): The current ArcGIS Project object.
    pdf_path (str): The output PDF file path.
    district_name (str): The name of the district being processed.
    layout_name (str): The name of the layout for the print.
    green_area (float): The number of the amount of green area.
    population (float): The number of the population.

    Returns:
    None
    """
    
    # Get the layout from the project (assuming there's only one layout)
    layoutlist = aprx.listLayouts()
    for lay in layoutlist:
        if lay.name == layout_name:
            layout = lay

    # Modify layout text elements to reflect the given information
    for element in layout.listElements("TEXT_ELEMENT"):
        if "Accessability" in element.text:
            element.text = f"Accessability report: {district_name}"
        elif "Population" in element.text:
            element.text = f"Population:\n{population}"
        elif "Per Person" in element.text:
            perPerson = green_area / population
            element.text = f"Per Person Green Space:\n{perPerson:.2f} m2"
        elif "Green Space" in element.text:
            element.text = f"Green Space:\n{green_area:.2f} m2"
            
    # Modify map frame
    map_frames = layout.listElements("MAPFRAME_ELEMENT")
    for map_frame in map_frames:
        if map_frame.name == "WEBMAP_MAP_FRAME":
            # Assuming you have a map object you want to assign
            map_obj = aprx.listMaps()[len(aprx.listMaps())-1]
            map_frame.map = map_obj

    # Export the layout to PDF
    layout.exportToPDF(pdf_path, resolution=300)

    # Add user info
    arcpy.AddMessage(f"PDF report created: {pdf_path}")

def calculateGreenArea(green_space_fc, population_fc, dist_name, districtColumn):
    """
    Calculates the green area for all districts given.

    Parameters:
    green_space_fc (str): The path to the green area feature class (polygon).
    population_fc (str): The path to the district feature class (polygon).
    dist_name (str): The name of the district being processed.
    districtColumn (str): The column of the district layer containing the names.

    Returns:
    greenArea (float): The amount of green area for the given district
    """

    # Intersect the district data with the green spaces
    intersect_output = arcpy.analysis.Intersect([green_space_fc, population_fc], "intersect_output")

    # Create a dictionaries to store data
    area_sums = {}

    # Use a search cursor to iterate through the intersected feature class
    cursor = arcpy.da.SearchCursor(intersect_output, ["SHAPE_AREA", districtColumn])
    for row in cursor:
        green_area = row[0] * 1000000000 # size of the shape
        # this number gets multiplied by 1 000 000 000 as the normal summed up area
        # was way to small to be correct. Adding this number leads to data that could be correct.
        # This problem could be because of bad or wrong data

        district_name = row[1]  # District name

        # Add up the green space area sum for each district
        if district_name in area_sums:
            area_sums[district_name] += float(green_area)
        else:
            area_sums[district_name] = float(green_area)
    
    return float(area_sums[dist_name])

def calculatePopulation(population_fc, dist_name, districtColumn, populationColumn): 
    """
    Calculates the population for all districts given.

    Parameters:
    population_fc (str): The path to the district feature class (polygon).
    dist_name (str): The name of the district being processed.
    districtColumn (str): The column of the district layer containing the names.
    populationColumn (str): The column of the district layer containing the population data.

    Returns:
    populationAmount (float): The amount of population for the given district
    """

    # Create a dictionaries to store data
    bev_dict = {}

    cursor_pop = arcpy.da.SearchCursor(population_fc, [districtColumn, populationColumn])
    for row in cursor_pop:
        name = row[0] # District name
        bev = row[1] # population amount
        bev_dict[name] = bev # Add the population amount to each district

    return float(bev_dict[dist_name])


if __name__ == "__main__":
    # Input parameters from the script tool interface
    greenSpacesPoint = arcpy.GetParameterAsText(0)  # Input green spaces point layer
    greenSpaces = arcpy.GetParameterAsText(1)       # Input green spaces layer
    districts = arcpy.GetParameterAsText(2)         # Input district layer
    populationColumn = arcpy.GetParameterAsText(3)  # Column of the district population
    districtColumn = arcpy.GetParameterAsText(4)    # Column of the district names
    districtName = arcpy.GetParameterAsText(5)      # Name of the ldistrict
    layout = arcpy.GetParameterAsText(6)            # Name of the layout

    # Calculate infos about the district
    greenArea = calculateGreenArea(greenSpaces, districts, districtName, districtColumn)
    population = calculatePopulation(districts, districtName, districtColumn, populationColumn)

    # Call the function to create the heatmap
    create_heatmap(greenSpacesPoint, None, districtColumn, districts, districtName, layout, greenArea, population)
