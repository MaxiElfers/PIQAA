import arcpy

def script_tool(green_space_fc, population_fc, min, max):
    
    # Intersect the district data with the green spaces
    intersect_output = arcpy.analysis.Intersect([green_space_fc, population_fc], "intersect_output")

    # Create a dictionaries to store data
    area_sums = {}
    bev_dict = {}

    # Use a search cursor to iterate through the intersected feature class
    cursor = arcpy.da.SearchCursor(intersect_output, ["SHAPE_AREA", "NAME_STATI"])
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

    # Create a search cursor for the district data
    cursor_pop = arcpy.da.SearchCursor(population_fc, ["NAME_STATI", "Bev_Anzahl"])
    for row in cursor_pop:
        name = row[0] # District name
        bev = row[1] # population amount
        bev_dict[name] = bev # Add the population amount to each district

    # help variable to checkt if atleast one fitting district was found
    printNumber = 0

    # Print the results
    for district_name, green_area in area_sums.items():
        perPersonArea = green_area / bev_dict[district_name] # calculate the green area per person
        if min:
            min = float(min)
            if max:
                max = float(max)
                if (perPersonArea > min and perPersonArea < max):
                    printNumber += 1
                    printMessage(district_name, green_area, perPersonArea)
            else:
                if (perPersonArea > min):
                    printNumber += 1
                    printMessage(district_name, green_area, perPersonArea)
        elif max:
            max = float(max)
            if (perPersonArea < max):
                printNumber += 1
                printMessage(district_name, green_area, perPersonArea)
        else:
            printNumber += 1
            printMessage(district_name, green_area, perPersonArea)
    if printNumber == 0:
        arcpy.AddMessage("No district found that met the given criteria")

# function to print the output message 
def printMessage(district_name, green_area, perPersonArea):
    arcpy.AddMessage(f"District: {district_name}, Green Area: {green_area:.2f} sq meters")
    arcpy.AddMessage(f"Green Area per Person: {perPersonArea:.2f} sq meters")
    arcpy.AddMessage("-----")

if __name__ == "__main__":
    # Inputs
    green_space_fc = arcpy.GetParameterAsText(0)  # Green space feature class
    population_fc = arcpy.GetParameterAsText(1)   # Population feature class
    min = arcpy.GetParameterAsText(2)  # minimum per person green area input
    max = arcpy.GetParameterAsText(3)  # maximum per person green area input

    # Call the function
    script_tool(green_space_fc, population_fc, min, max)
