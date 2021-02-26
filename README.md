# PoseAnnotation

## Set Up and Installing Requirements
git clone this repo to your local machine

```
git clone https://github.com/moonbeam5115/PoseAnnotation.git
```

```
cd PoseAnnotation
```

Set up virtual environment:  
(Conda)  
```
conda create --prefix ./env python=3.7
```

activate conda environment:  
```
conda activate ./env
```

install requirements: 
```
pip3 install -r requirements.txt
```

## Getting Started
Place images you wish to annotate inside the imgs folder

start program:
python3 main.py

Left Click on image to add joint annotation

Press "e" to undo previous joint annotation

Press "enter" to save results and go to next image

Press "escape" to exit program

## Future Functionality

Create functionality to return to previous image
Allow user to skip occluded joints
