from c_benchmark import *
import argparse
argParser = argparse.ArgumentParser(description='manual to this script')
argParser.add_argument("-aux", type=str, default="")
# example: /ISPD2002/ibm01/ibm01
args=argParser.parse_args()
path = args.aux 
m = Benchmark(path)
m.generate_benchmark()
m.print_info()
# generate_benchmark function generates all the objects needed to describe a benchmark
# Cells, Nets, Rows, and metrics are all calculated in this method.
# Using a debugger you can see an analytical view of all objects and metrics inside m (Benchmark) instance
