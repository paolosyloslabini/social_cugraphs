import csv
import argparse


def relabel_graph(infilename, outfilename, mapfilename):
  idx_map = {};
  idx = 0;
  with open(infilename, 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
      if (row[0] not in idx_map):
        idx_map[row[0]] = idx;
        idx += 1;
      if (row[1] not in idx_map):
        idx_map[row[1]] = idx;
        idx += 1;
  with open(infilename, 'r') as csv_file:
    with open(outfilename, 'w') as out_csv_file:
      writer = csv.writer(out_csv_file)
      reader = csv.reader(csv_file)
      writer.writerow(["src","dst"]);
      for row in reader:
        writer.writerow([ idx_map[row[0]], idx_map[row[1]] ])
  with open(mapfilename, 'w') as map_csv_file:
    writer = csv.writer(map_csv_file)
    writer.writerow(["nodename","idx"]);
    for key in idx_map:
      writer.writerow([key, idx_map[key]]);


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Collect results for approximate algorithms into a csv")
    
    parser.add_argument("--input-file", default="/",
        help="the input csv of a graph to be relabeled")
    parser.add_argument("--output-file", default="/",
        help="the output csv containing the relabeled graph")
    parser.add_argument("--output-map", default="RRR",
        help="the output csv containing the mapping between the original nodes and the new indices")

    args = parser.parse_args()

    input_file = args.input_file;
    output_file = args.output_file;
    output_map = args.output_map;   
    
    relabel_graph(input_file, output_file, output_map)
    
