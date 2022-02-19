# Kyle Capelli - 23258325
# CITS1401
# Semester 2 - Project 2

def locationDictionaryCreator(inputFile):
    """
    A function that creates a dictionary of locations:
    LocID : ( Latitude, Longitude, Category )
    It handles any exceptional cases and returns None for each
    If a row is corrupt, that row is not entered into the
    dictionary
    """
    data = []
    location_dictionary = {}

    try:
        with open(inputFile, 'r') as file:
            for line in file:
                data.append(line.rstrip("\n").upper().split(","))
            
            # Checks if there is no data in the file
            if len(data) == 0:
                print("There is no data in this file")
                return None
                    
            loc = 0
            lat = 0
            long = 0
            cat = 0
            
            correct_headings = 0
            
            for col in range(len(data[0])):
                if data[0][col] == 'LOCID':
                    loc = col
                    correct_headings += 1
                elif data[0][col] == 'LATITUDE':
                    lat = col
                    correct_headings += 1
                elif data[0][col] == 'LONGITUDE':
                    long = col
                    correct_headings += 1
                elif data[0][col] == 'CATEGORY':
                    cat = col
                    correct_headings += 1
            
            # Checks if the headings LocID, Latitude, Longitude and Category are in the file
            # if not then it will return none and produce an error message
            if correct_headings != 4:
                print('The column headings need to contain "LocID, Latitude, Longitude and Category". \n' +
                      'Please ensure that these are used for this program to run correctly.')
                return None
            
            data.pop(0)
            
            # Retrieves LocIDs of corrupt data incase there is more than two occurrences of the same ID
            corrupt_locations = []
            
            for row in data:
                if corruptData(row, lat, long, cat, loc, location_dictionary, corrupt_locations):
                    continue
                else:
                    location_dictionary[row[loc]] = (float(row[lat]),
                                                     float(row[long]),
                                                     row[cat])
                                      
            return location_dictionary
            
    except FileNotFoundError:
        print("The file was not found, please enter a valid file name.")
        return None


def corruptData(dataList, latIndex, longIndex, catIndex, locIndex, dictionary, corruptLocations):
    """
    A function that checks if any of the data inside of the row is corrupt
    A row is considered corrupt if there is:
    Duplicate location IDs, empty cells and invalid data types
    """
    
    # Check if the location ID is in the dictionary already - if it is then delete occurance
    # and add LocID to to the corrupt locations to check if it occurs again later in the file
    if dataList[locIndex].strip() in dictionary:
        del dictionary[dataList[locIndex]]
        corruptLocations.append(dataList[locIndex])
        return True
    # Check if location ID has already been used before which will be stored in corrupt_locations
    elif dataList[locIndex].strip() in corruptLocations:
        return True
    # Strips extra whitespace and checks if the value == "" which is deemed as corrupt data
    elif dataList[latIndex].strip() == "" or dataList[longIndex].strip() == "" or \
         dataList[catIndex].strip() == "" or dataList[locIndex].strip() == "":
        return True
    # Checks to see if the value in category and location index column are of non string type
    elif isNumber(dataList[locIndex]) or isNumber(dataList[catIndex]) or not \
         isNumber(dataList[latIndex]) or not isNumber(dataList[longIndex]):
        return True
    # Data is not corrupt
    return False
        
        
def insideBoundary(locLat, locLong, sourceLat, sourceLong, radius):
    """
    A function that checks if a location is within a given region
    """
    
    if (sourceLat - locLat)**2 + (sourceLong - locLong)**2 < radius**2:
        return True;
    
    
def isNumber(num):
    """
    A function that checks if a value is a number (int or float)
    """
    try:
        float(num)
        return True
    except ValueError:
        return False


def locationCategoryFinder(locations, locList, radius):
    """
    A function that takes in a list of location IDs and returns a list
    of dictionaries containing the occurrence of each category in the region
    """
    
    try:
        location_list = []
        
        for locID in locList:
            category_dict = getCategories(locations, numberValue=True)
            latitude = locations[locID][0]
            longitude = locations[locID][1]
            
            for value in locations.values():
                
                if insideBoundary(latitude, longitude, value[0], value[1], radius) :
                    category_dict[value[2]] += 1
            
            location_list.append(category_dict)
    except KeyError:
        print("Location ID(s) provided are not found inside of the data file")
        return None
                
    return location_list


def cosineSimilarity(category_list):
    """
    A function that checks the cosine similarity score between two
    dictionaries.
    """
    
    numerator = 0
    denom_val1 = 0
    denom_val2 = 0
    
    A = category_list[0]
    B = category_list[1]
    
    for keys in A.keys():
        numerator += A.get(keys)* B.get(keys)
        denom_val1 += A.get(keys) ** 2
        denom_val2 += B.get(keys) ** 2
    
    try:
        return round(numerator / ((denom_val1)**(0.5) * (denom_val2)**0.5),4)
    except ZeroDivisionError:
        # Have handled this in the main function but if tested separetly
        # having this exception will be vital.
        print("Cannot Divide by Zero")
        return None
      

def commonLocations(locations, locList, radius):
    """
    A function that returns a dictionary of categories with their value
    being a list of locations that intersect both LocID regions
    """
    
    common_locations = getCategories(locations, listValue=True)
    
    locIDs = []
    
    for locID in locList:
        latitude = locations[locID][0]
        longitude = locations[locID][1]
        
        for key, value in locations.items():
            
            if insideBoundary(latitude, longitude, value[0], value[1], radius):
                locIDs.append(key)
    
    # Finds the locIDs that occur in both regions
    repeated_locIDs = list(set([num for num in locIDs if locIDs.count(num) > 1]))
    
    for locID in repeated_locIDs:
        category = locations.get(locID)[2]
        if category not in common_locations:
            common_locations[category] = [locID]
        else:
            common_locations[category].append(locID)
        
    return common_locations
    

def getCategories(locations, listValue=None, numberValue=None):
    """
    A function that filters through the data and returns a dictionary of categories
    listValue = True makes the value of type list
    numberVale = True makes the value of type int
    """
    
    categories = {}
    
    for value in locations.values():
        if value[2] not in categories:
            
            if listValue:
                categories[value[2]] = []
            elif numberValue:
                categories[value[2]] = 0
            
    return categories


def closestLocation(locations, locList, radius):
    """
    A function that returns a list of dictionaries for each LocID
    where the key is the category and the value is a tuple containing
    the LocID of the respective category that is closest to the input LocID
    and its distance from that input LocID
    """
    
    closest_locations = []
    
    for loc in locList:
        
        long = locations.get(loc)[1]
        lat = locations.get(loc)[0]
        
        common_locations = {}
        
        for key, value in locations.items():
            
            x2 = locations.get(key)[1]
            y2 = locations.get(key)[0]
            
            distance = ((x2 - long) ** 2 + (y2 - lat) ** 2) ** (0.5)
            
            if insideBoundary(lat, long, value[0], value[1], radius) and key != loc:
                
                if value[2] not in common_locations:
                    common_locations[value[2]] = (key, distance)
                elif distance < common_locations.get(value[2])[1]:
                    common_locations[value[2]] = (key, distance)
            
            # Round each value of the location distance to 4 decimal places
            for key, values in common_locations.items():
                common_locations[key] = (values[0], round(values[1],4))
                
        closest_locations.append(common_locations)
            
    return closest_locations
            

def main(inputFile, locIDlist, radius):
    
    if len(locIDlist) > 2:
        print("Please only provide 2 locations for this program to run")
        return None, None, None, None
    else:
        try:
            # Converts locationID list to capital letters
            locIDlist = [x.upper() for x in locIDlist]
        except AttributeError:
            # Throws an exception if an integer value is passed in as a location ID
            print("The values passed in as LocIDs need to be a list containing 2 Strings")
            return None, None, None, None
    
        
    # Creates a dictionary of key = locations and their respective values
    location_dict = locationDictionaryCreator(inputFile)
    
    # location_dict = None if file is not found
    # Returns 4 None values
    if location_dict == None:
        return location_dict, None, None, None
    
    # Returns 4 None values if the radius provided is negative
    elif radius <= 0:
        print("Please provide a positive number for the radius")
        return None, None, None, None
    
    # Finds the category and number of occurences of the category
    # If category_counts = None, then one or more of the locations provided
    # in main function argument [locIDlist] do not appear in the location dictionary
    category_counts = locationCategoryFinder(location_dict, locIDlist, radius)
    
    if category_counts == None:
        return category_counts, None, None, None
    
    # Finds the cosine similarity score of 2 locations
    cosine_sim_score = cosineSimilarity(category_counts)
    
    # Finds the intersect locations ie. locations that occur in both
    # regions C1 and C2.
    intersection_by_category = commonLocations(location_dict, locIDlist, radius)

    # Creates a list of 2 dictionaries containing key = category with the closest
    # location within the region represented as a tuple -> (LocID, Distance)
    # Distance = Euclidean Distance between 2 points
    closest_categories = closestLocation(location_dict, locIDlist, radius)
    
    return category_counts, cosine_sim_score, intersection_by_category, closest_categories

a,b,c,d = main("Locations.csv", ["L26", "L52"], 3.5)