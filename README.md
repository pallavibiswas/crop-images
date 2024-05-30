# Automating cropping of images

Python code to crop images based on coordinates from data annotations. 
- Can crop multiple images from a folder at once, with corressponding coordinates from a directory containing the txt file of the coordinates
- Can do multiple crops in one image based on number of coordinate sets
- Uses the OS module to handle files and the Pillow library to handle the actual cropping
- Useful for training VLMs, for e.g, when we need only the outline of a specific person as data and not the background
