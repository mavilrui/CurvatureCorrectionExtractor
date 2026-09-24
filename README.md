# CurvatureCorrectionExtractor

Python3 script that extracts lines from an image based on the indications of a page file, correcting the curvature of lines by straighting the lines based on the baseline segments.

# Usage

python3 curvatureCorrectionExtractor.py \<page-file\> \<img-file\> \<output-directory\> \<top-perc\> \<bot-perc\> \<top-pix\> \<bot-pix\> \<extension-method\>
  
page-file - page file associated with the image to extract line from

img-file - image file to extract lines from

output-directory - directory where extracted lines are to be saved

top-perc - percentaje of pixels from the line regions of the image to get from over the baseline (Format: float : 0.X)

bot-perc - percentaje of pixels from the line regions of the image to get from under the baseline (Format: float : 0.X)

top-pix - number of pixels to get from over the baseline in case that there is no line region (Format: integer : X)

bot-pix - number of pixels to get from under the baseline in case that there is no line region (Format: integer : X)

extension-method - in case the desired line is bigger on either axis than the image the missing pixels will be filled, if EXTEND is passed the last pixel line will be repeated, if BLANK is passed the line will be filled with blanks. (Format: string : EXTEND/BLANK)

To use this script you need Python3 installed on your machine.
