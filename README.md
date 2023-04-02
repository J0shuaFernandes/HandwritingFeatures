# Handwriting Features

Handwritten Style Conversion using Image to Image Translation

## Features

Following are the handwriting features extracted by features.py:

![hw_features](C:\Users\Joshua\OneDrive\Documents\hr-style\hw_features.JPG)

#### Measures of Pen Pressure 

3. Measures of Pen Pressure indicate the darkness of writing as writes who would put more pressure would have darker writing while writers who wouldn’t put pressure would have lighter writing. There are three measures of pen pressure, i.e., gray-level distribution, gray-level threshold value and the number of black pixels.

### Measures of Writing Movements

There are two measures of writing movement, interior and exterior contours. Given an image of handwritten text, the image is binarized and its contours are detected. Contours that are contained within a contour are called interior contours while contours that are not contained within any contour are called exterior contours. Writing that is more cursive would have more interior contours whereas straight 

4. No. of Interior Contours

5. No. of Exterior Contours

### Measures of Stroke Formation

Positive, Negative, Horizontal and Vertical Slope components are four measures of stroke formation. To compute these slopes, the contours of handwritten text are approximated and each slope (line between two points) is classified as either positive or negative and horizontal or vertical. A slope is positive if it rises from left to right while a slope is negative if it moves downwards.

6. Positive Slope Components

7. Negative Slope Components
8. Horizontal Slope Components
9. Vertical Slope Components
