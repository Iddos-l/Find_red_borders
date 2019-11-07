
# Find_red_borders
`Quality Control script for Resolve users`

This script reads exported files from DaVinci Resolve, searches for frame edges errors.  
Exported files generated with `Blanking_Red.dctl`
@Paul Dore 'baldavenger': https://github.com/baldavenger/DCTLs/tree/master/Utility  
The script will create a png file for every frame with red border and will add record timecode to the file name.
### Requirements
* python3
* OpenCV  
`pip3 install opencv-python`
* DaVinci Resolve
* Blanking_Red.dctl

### Usage
Apply Blanking_Red.dctl to timeline node.  
Export a non frame sequential format.  
Run the script, choose the source file and destination folder.
