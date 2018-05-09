import processing, indexing
import os

def setup():
    modified_ap_path = 'modified-attack-patterns/'
    ap_path = 'attack-patterns/'

    # check to see if attack patterns have already been transformed
    if not os.path.exists(modified_ap_path):
        # check to see original patterns exist
        if os.path.exists(ap_path):
            print("Creating modified attack patterns in " + modified_ap_path)
            processing.transform()
        else:
            print("Could not locate attack-patterns directory...")
    else:
        print('Modified attack patterns located in ' + modified_ap_path)

    #create attack-pattern index and perform bulk indexing on modified patterns
    print("Attempting to create index and perform bulk indexing...")
    indexing.bulk_indexing()

#run setup function
setup()
