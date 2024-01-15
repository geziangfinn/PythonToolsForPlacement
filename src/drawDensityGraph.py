from c_benchmark import *
import argparse
import cv2
import numpy as np
import os
argParser = argparse.ArgumentParser(description='manual to this script')
argParser.add_argument("-aux", type=str, default="")
argParser.add_argument("-plPath", type=str, default="")
argParser.add_argument("-output", type=str, default="")
# example: /ISPD2002/ibm01/ibm01
args=argParser.parse_args()

path = args.aux 
plPath=args.plPath
outputPath=args.output

placement = Benchmark(path)
placement.generate_benchmark()
placement.print_info()
print(".pl file at: ",plPath)
plparser=FParser(plPath)

iterNumberStr=plPath.rsplit('_',1)[1]

iterNumberStr=iterNumberStr.split(".")[0]

iterNumber=int(iterNumberStr)

print("Iteration number: ",iterNumber)

if not os.path.exists(outputPath):
    os.system("mkdir "+outputPath)

resultPath=outputPath+"/"+placement.name
if not os.path.exists(resultPath):
    os.system("mkdir "+resultPath)

inputFeatureOutputPath=resultPath+"/inputnpy"
outputFeatureOutputPath=resultPath+"/outputnpy"

print("Input feature map will be at: ",inputFeatureOutputPath)
print("Output feature map will be at: ",outputFeatureOutputPath)

if not os.path.exists(inputFeatureOutputPath):
    os.system("mkdir "+inputFeatureOutputPath)
if not os.path.exists(outputFeatureOutputPath):
    os.system("mkdir "+outputFeatureOutputPath)
# os.makedirs(inputFeatureOutputPath)
# os.makedirs(outputFeatureOutputPath)

inputFileName=inputFeatureOutputPath+"/"+placement.name+"_input_"+iterNumberStr+".npy"
outputFileName=outputFeatureOutputPath+"/"+placement.name+"_output_"+iterNumberStr+".npy"


cellLocations=plparser.read_pl(plPath)

for cell_name in cellLocations.keys():
    # print(cell_name,cellLocations[cell_name])
    placement.setCellLocation(cell_name,cellLocations[cell_name][0],cellLocations[cell_name][1])
    # print(cellLocations[cell_name])


minImgaeLength = 512
xMargin = 30
yMargin = 30

if placement.width < placement.height:
    imageHeight = 1.0 * placement.height / (placement.width / minImgaeLength)
    imageWidth = minImgaeLength
else:

    imageWidth = 1.0 * placement.width / (placement.height / minImgaeLength)
    imageHeight = minImgaeLength


unitX = imageWidth / placement.width
unitY = imageHeight / placement.height





img = np.zeros((int(imageWidth),int(imageHeight)), np.int32)
img.fill(0)
counter=0
for cell_name in placement.cells.keys():
    counter+=1
    
    scaledLeftX=int((placement.cells[cell_name].left_x-placement.left_x)*unitX)
    scaledRightX=int((placement.cells[cell_name].right_x-placement.left_x)*unitX)
    scaledLowY=int((placement.height-(placement.cells[cell_name].high_y-placement.low_y))*unitY)
    scaledHighY=int((placement.height-(placement.cells[cell_name].low_y-placement.low_y))*unitY)

    if(scaledLeftX==scaledRightX):
        scaledRightX=scaledLeftX+1
    if(scaledLowY==scaledHighY):
        scaledHighY=scaledLowY+1

    ps=(int(scaledLeftX),int(scaledLowY))
    pe=(int(scaledRightX),int(scaledHighY))

    subImg=img[ps[1]:pe[1],ps[0]:pe[0]]
    whiteRect=np.ones(subImg.shape, dtype=np.int32)
 
    # res = np.add(subImg,whiteRect)
    # print("first: ",res)
    res=cv2.add(subImg,whiteRect)
    # print("second: ",res)
    img[ps[1]:pe[1],ps[0]:pe[0]] = res


#cv2.imwrite(inputFileName,img)
np.save(inputFileName,img)

bin_dim_x=256# bin dimension x: how many bins in x direction
bin_dim_y=256# bin dimension y: how many bins in y direction

bin_length_x=placement.width/bin_dim_x
bin_length_y=placement.height/bin_dim_y

bins=np.zeros((bin_dim_x,bin_dim_y), np.int32) # matrix for all bins

# bin index:
# 5
# 4
# 3
# 2
# 1
# 0
#  0 1 2 3 4 5

for cell_name in placement.cells.keys():
    bin_start_x=int(placement.cells[cell_name].left_x/bin_length_x)
    bin_end_x=int(placement.cells[cell_name].right_x/bin_length_x)
    bin_start_y=int(placement.cells[cell_name].low_y/bin_length_y)
    bin_end_y=int(placement.cells[cell_name].high_y/bin_length_y)
    
    if bin_end_y>=bin_dim_y:
        bin_end_y=bin_dim_y-1
    if bin_end_x>=bin_dim_x:
        bin_end_x=bin_dim_x-1

    for i in range(bin_start_x,bin_end_x+1):# ignored macro density scaling here!
        bin_ij_left_x=i*bin_length_x
        bin_ij_right_x=(i+1)*bin_length_x
        share_area_right_x=min(bin_ij_right_x,placement.cells[cell_name].right_x)
        share_area_left_x=max(bin_ij_left_x,placement.cells[cell_name].left_x)
        
        for j in range(bin_start_y,bin_end_y+1):
            bin_ij_low_y=j*bin_length_y
            bin_ij_high_y=(j+1)*bin_length_y
            share_area_high_y=min(bin_ij_high_y,placement.cells[cell_name].high_y)
            share_area_low_y=max(bin_ij_low_y,placement.cells[cell_name].low_y)

            share_area_width=share_area_right_x-share_area_left_x
            share_area_height=share_area_high_y-share_area_low_y

            bins[i][j]=share_area_width*share_area_height

# densityimg = np.zeros((int(bin_dim_x),int(bin_dim_y)), np.float32)
# cv2.imwrite(outputFileName,bins)
np.save(outputFileName,bins)

print(np.__version__)
