import cugraph
import cudf
import argparse


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Collect results for approximate algorithms into a csv")
	parser.add_argument("--input-file", default="/", 
		    help="the input csv of a graph to be analyzed")
    	args = parser.parse_args()

 	input_file = args.input_file;

# read data into a cuDF DataFrame using read_csv
gdf = cudf.read_csv(, names=["src", "dst"], dtype=["int32", "int32"])

# We now have data as edge pairs
# create a Graph using the source (src) and destination (dst) vertex pairs
G = cugraph.Graph()
G.from_cudf_edgelist(gdf, source='src', destination='dst')

# Let's now get the PageRank score of each vertex by calling cugraph.pagerank
df_page = cugraph.pagerank(G)
vertex_bc = cugraph.betweenness_centrality(G)
edge_bc = cugraph.edge_betweenness_centrality(G)

# Let's look at the PageRank Score (only do this on small graphs)
for i in range(5):
	print("vertex " + str(df_page['vertex'].iloc[i]) +
		" PageRank is " + str(df_page['pagerank'].iloc[i]))
