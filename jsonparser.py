import json 
import numpy as np

def jsonParse(file_path):

    # Open file and refer to it as f
    with open(file_path, 'r') as f:

        # Read the json file stored in f
        config = json.load(f)

        # Create a list to dump the configuration paramters
        cfgs = []
        
        # Loop through the configuration of both detectors
        for obj in config["detection"]:

            # Create an empty dictionary to store values
            cfg = {}

            # Store id value
            cfg["id"] = int(obj["id"])

            # Create a numpy array with integer HSV values
            cfg["HSVmin"] = np.array([int(i) for i in obj["HSVmin"].split(',')])
            cfg["HSVmax"] = np.array([int(i) for i in obj["HSVmax"].split(',')])

            # Create an empty list for th filter configuration
            filters = []

            # Loop through the different filters
            for o in obj["filters"]:

                # Create empty dictionary to store the filter's parameters
                fd = {}
                
                # Store each parameter inside the dictionary
                fd["name"] = o["name"]
                fd["size"] = int(o["size"])
                fd["iters"] = int(o["iters"])

                # Push the dictionary into the list
                filters.append(fd)
            
            cfg["filters"] = filters
                
            # Insert the cfg dictionary and the filters list
            cfgs.append(cfg)
            cfgs.append(filters)

        # Return the processed configuration parameters
        return cfgs

