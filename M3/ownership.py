import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

import constants

if __name__ == "__main__":
    # Read in the data
    data = pd.read_csv(constants.BTS_data_file_path)

