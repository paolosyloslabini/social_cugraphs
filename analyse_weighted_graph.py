import cugraph
import cudf as cudf
from dask.distributed import Client
import argparse
import numpy as np

schedulerjson = "/home/clusterusers/pasyloslabini/dask-local-directory/dask-scheduler.json"
client = Client(scheduler_file=schedulerjson)


MAX_INT = 1000000
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Collect results for approximate algorithms into a csv")
	parser.add_argument("--input-file", default="/", help="the input csv of a graph to be analyzed")
	parser.add_argument("--output-folder", default="/", help="where to save results")
	parser.add_argument("--name", default="g_", help="name of the graph")
	parser.add_argument("--threshold", default=-1, help="threshold for weights")
	args = parser.parse_args()
	input_file = args.input_file
	output_folder = args.output_folder
	name = args.name
	thres = int(args.threshold)

# read data into a cuDF DataFrame using read_csv
print("reading csv")
gdf = cudf.read_csv(input_file, names=["src", "dst", "w"], dtype=["int32", "int32", "float32"])

def remove_greater(w_in, w_dist, t = MAX_INT):
	for i, w in enumerate(w_in):
		if (w >= t):
			w_dist[i] = MAX_INT;
		else:
			w_dist[i] = w;
	
gdf.apply_rows(remove_greater, incols = {"w":"w_in"}, outcols = {'w_dist': np.float32 }, kwargs={"t":thres});

def invert_weight(w_in, w_inverted):
	for i, w in enumerate(w_in):
		if (w == 0):
			w_inverted[i] = MAX_INT;
		else:
			w_inverted[i] = 1/w;
	
gdf.apply_rows(invert_weight, incols = {"w_dist":"w_in"}, outcols = {'w_inverted': np.float32 }, kwargs={});
print("csv read")

# We now have data as edge pairs
# create a Graph using the source (src) and destination (dst) vertex pairs
print("Making unweighted graph")
G = cugraph.Graph()
G.from_cudf_edgelist(gdf, source='src', destination='dst')
print("unweighted graph created")

# Centrality scores
print("evaluating centrality scores")
df_page = cugraph.pagerank(G)
df_page.to_csv(output_folder + "/" + name + "pagerank.csv")
print("pagerank done")

vertex_bc = cugraph.betweenness_centrality(G)
vertex_bc.to_csv(output_folder + "/" + name + "vertex_bc.csv")
print("BC done")

#weighted
G = cugraph.Graph()
G.from_cudf_edgelist(gdf, source='src', destination='dst', edge_attr='w_inverted')

print("evaluating centrality scores")
df_page = cugraph.pagerank(G)
df_page.to_csv(output_folder + "/" + name + "_w_pagerank.csv")
print("pagerank done")

vertex_bc = cugraph.betweenness_centrality(G)
vertex_bc.to_csv(output_folder + "/" + name + "_w_vertex_bc.csv")
print("BC done")


df_louv, mod_louv = cugraph.louvain(G)
df_louv.to_csv(output_folder + "/" + name + "_w_df_louv.csv")
print("Louvain done")

df_ecg = cugraph.ecg(G)
df_ecg.to_csv(output_folder + "/" + name + "_w_df_ecg.csv")
print("ECG done");

print("sanity check: printing the first 5 pagerank score")
for i in range(5):
	print("vertex " + str(df_page['vertex'].iloc[i]) +
		" PageRank is " + str(df_page['pagerank'].iloc[i]))
