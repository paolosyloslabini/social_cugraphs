import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Makes images of the distributions")
        parser.add_argument("--input-file", default="/", help="the input csv of a graph property to be analyzed")
        parser.add_argument("--output-folder", default="/", help="where to save images")
        parser.add_argument("--name", default="distribution_image", help="name of the graph")
        args = parser.parse_args()
        input_file = args.input_file
        output_folder = args.output_folder
        name = args.name

df = pd.read_csv(input_file, sep = " ", header = None, names = ["node","value"])
          
  
values, base = np.histogram(df["values"], bins=40)
cumulative = np.cumsum(values)
plt.plot(base[:-1], cumulative, c='blue')
#plt.legend(bbox_to_anchor=(0.5, 1.00), shadow=True, ncol=4, fontsize=15)
plt.title(name);   
plt.savefig(output_folder + name + ".jpg", format = 'jpg', dpi=300, bbox_inches = "tight")

