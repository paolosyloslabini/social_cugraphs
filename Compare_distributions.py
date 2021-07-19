import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Makes images of the distributions")
        parser.add_argument("--input-folder", default="/", help="the input csvs to be analyzed")
        parser.add_argument("--output-folder", default="/", help="where to save images")
        parser.add_argument("--name", default="distribution_image", help="name of the graph")
        args = parser.parse_args()
        input_folder = args.input_folder
        output_folder = args.output_folder
        name = args.name

        
for file in glob.glob(input_folder + "*.csv"):
        
        prop_name = name + "_" + file.split('.')[0]
        
        try:
                df = pd.read_csv(file, header = 0, names = ["index","value", "node"]) 
        except:
                df = pd.read_csv(file, sep = " ", header = 0, names = ["node", "value"])
                
        sorted_data = np.sort(df["value"].tolist())
        
        # Cumulative counts:
        plt.step(sorted_data, np.arange(sorted_data.size))  # From 0 to the number of data points-1

        #plt.legend(bbox_to_anchor=(0.5, 1.00), shadow=True, ncol=4, fontsize=15)
        plt.title(prop_name);   
        plt.savefig(prop_name + ".jpg", format = 'jpg', dpi=300, bbox_inches = "tight")

