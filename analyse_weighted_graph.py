import cugraph
import cudf as cudf
from dask.distributed import Client
import argparse
import numpy as np

schedulerjson = "/home/clusterusers/pasyloslabini/dask-local-directory/dask-scheduler.json"
client = Client(scheduler_file=schedulerjson)


MAX_WEIGHT = 100000.0
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
gdf = cudf.read_csv(input_file, delimiter = " ", names=["src", "dst", "w"], dtype=["int32", "int32", "float32"])

def invert_weight(w):
	if (w < 1.0/MAX_WEIGHT):
		return MAX_WEIGHT;
	else:
		return 1.0/w;
	
gdf['w'].applymap(invert_weight);

print("csv read")

# We now have data as edge pairs
# create a Graph using the source (src) and destination (dst) vertex pairs
print("Making unweighted graph")
G = cugraph.Graph()
if (thres > 0):
	G.from_cudf_edgelist(gdf[gdf['w'] > 1.0/thres], source='src', destination='dst', renumber = False)
else:
	G.from_cudf_edgelist(gdf, source='src', destination='dst', renumber = False)
print("unweighted graph created")

if (G.has_isolated_vertices()):
    print("G has isolated vertices");


def save_df(df, savename):
	df.sort_values(by = 'vertex');
	df.to_csv(output_folder + "/" + name + savename + ".csv", header = False, index = False, columns = [1,0])
	print(savename + " done");

# Centrality scores
print("evaluating centrality scores")
df_page = cugraph.pagerank(G)
save_df(df_page, "pagerank");

vertex_bc = cugraph.betweenness_centrality(G)
save_df(vertex_bc, "betweenness");

#weighted
G = cugraph.Graph()
if(thres > 0):
	G.from_cudf_edgelist(gdf[gdf['w'] > 1.0/thres], source='src', destination='dst', edge_attr='w', renumber = False)
else:
	G.from_cudf_edgelist(gdf, source='src', destination='dst', edge_attr='w', renumber = False)
	
print("evaluating centrality scores")
df_page = cugraph.pagerank(G)
save_df(df_page, "_w_pagerank")

vertex_bc = cugraph.betweenness_centrality(G)
save_df(vertex_bc, "_w_betweenness")

df_louv, mod_louv = cugraph.louvain(G)
save_df(df_louv, "_w_louvain")

df_ecg = cugraph.ecg(G)
save_df(df_ecg, "_w_ecg")

print("sanity check: printing the first 5 pagerank score")
for i in range(5):
	print("vertex " + str(df_page['vertex'].iloc[i]) +
		" PageRank is " + str(df_page['pagerank'].iloc[i]))
