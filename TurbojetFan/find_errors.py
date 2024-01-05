import os
import numpy 
import pandas 
DATA_FOLDER = "data"

def find_data_files(data_folder):
    """Return a list of file names in the data folder"""
    file_names = []
    for file_name in os.listdir(data_folder):
        if file_name.endswith(".txt"):
            file_names.append(file_name)
    return file_names



def get_data(data_folder):
    data_files = find_data_files(data_folder)
    # print(data_files)
    #empty DF
    data = []
    for file_name in data_files:
        with open(os.path.join(data_folder, file_name)) as f:
            data.append([[float(a) for a in x.split()] for x in f.readlines()])
    


    # for x in data:
    #     print(x)
    
    


    print("Data files: {}".format(data_files))
    print(len(data))

    # print(data)
    return pandas.DataFrame(data)

    


if __name__ == "__main__":
    data = get_data(DATA_FOLDER)
