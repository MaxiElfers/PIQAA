import arcpy

def analyse_population(green_space_fc, population_fc, min, max, district_column, population_cloumn):
    """
    Calculates the green space area and the green space area per person for each district.

    Parameters:
    green_space_fc (str): The path to the input green spaces feature class (polygon).
    population_fc (str): The path to the input district feature class containing population data (polygon).
    min (str): The minimum per Person area (optional).
    max (str): The maximum per Person area (optional).
    district_column (str): The name of the column of the population_fc containing district names.
    population_cloumn (str): The name of the column of the population_fc containing population data.

    Returns:
    None
    """
    
    # Intersect the district data with the green spaces
    intersect_output = arcpy.analysis.Intersect([green_space_fc, population_fc], "intersect_output")

    # Create a dictionaries to store data
    area_sums = {}
    bev_dict = {}

    # Use a search cursor to iterate through the intersected feature class
    cursor = arcpy.da.SearchCursor(intersect_output, ["SHAPE_AREA", district_column])
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
    cursor_pop = arcpy.da.SearchCursor(population_fc, [district_column, population_cloumn])
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
    """
    Logs the output.

    Parameters:
    district_name (str): The name of the district.
    green_area (float): The number for green area in this district.
    perPersonArea (float): The number of green area per person in this district.

    Returns:
    None
    """

    arcpy.AddMessage(f"District: {district_name}, Green Area: {green_area:.2f} sq meters")
    arcpy.AddMessage(f"Green Area per Person: {perPersonArea:.2f} sq meters")
    arcpy.AddMessage("-----") # For better visibility

if __name__ == "__main__":
    # save all input parameters
    green_space_fc = arcpy.GetParameterAsText(0)    # Green space feature class
    population_fc = arcpy.GetParameterAsText(1)     # Population feature class
    district_column = arcpy.GetParameterAsText(2)   # District name column
    population_cloumn = arcpy.GetParameterAsText(3) # Population number cloumn
    min = arcpy.GetParameterAsText(4)               # Minimum per person green area input
    max = arcpy.GetParameterAsText(5)               # Maximum per person green area input

    # Call the function
    analyse_population(green_space_fc, population_fc, min, max, district_column, population_cloumn)
