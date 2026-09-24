import sys
from PIL import Image
from matplotlib.image import imread
import numpy as np
import xml.etree.ElementTree as ET

if len(sys.argv) != 9:
    print("Missing arguments: python3 correccion_de_curvatura.py <page-file> <img-file> <output-directory> <top-perc> <bot-perc> <top-pix> <bot-pix> <extension-method>")
    sys.exit()

def get_line(p1, p2):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points

tree = ET.parse(sys.argv[1])
root = tree.getroot()
image = np.array(imread(sys.argv[2]))

true_x_length = len(image[0])
count = 0
for i in image:
    count += 1

true_y_length = count
print(true_x_length, true_y_length)
count = 0

this_region = ""
this_line = ""

for child in root:
    for child1 in child:
        child1_tag = child1.tag.split('}')[-1]    
        if child1_tag == 'TextRegion': 
            last = 'TextRegion'
            this_region = child1.attrib['id']
            print(child1.attrib['id'])
        for child2 in child1:
            child2_tag = child2.tag.split('}')[-1]
            if child2_tag == 'TextLine': 
                last = 'TextLine'
                this_line = child2.attrib['id']
                print(this_region, child2.attrib['id'])
            r1nums = []
            r2nums = []
            for child3 in child2:
                child3_tag = child3.tag.split('}')[-1]
                if child3_tag == 'Coords': 
                    r1nums = []
                    for num in child3.attrib['points'].split():
                        nums = num.split(",")
                        num1, num2 = int(nums[0]), int(nums[1])
                        r1nums.append((num1, num2))
                    print(last, child3_tag, r1nums)
                if child3_tag == 'Baseline': 
                    r2nums = []
                    for num in child3.attrib['points'].split():
                        nums = num.split(",")
                        num1, num2 = int(nums[0]), int(nums[1])
                        r2nums.append((num1, num2))
                    print(last, child3_tag, r2nums)
            if len(r1nums) > 0 and len(r2nums) > 0:
                r1ymax, r1ymin = max(r1nums, key=lambda x:x[1])[1], min(r1nums, key=lambda x:x[1])[1]
                r1yspacing = int((r1ymax - r1ymin))
                if r1yspacing != 0:
                    r1topspacing, r1botspacing = int(r1yspacing * float(sys.argv[4])), int(r1yspacing * float(sys.argv[5]))
                else:
                    r1topspacing, r1botspacing = int(sys.argv[6]), int(sys.argv[7])
                pointline = []
                for point in range(len(r2nums)):
                    if point != len(r2nums) - 1:
                        aux_points = get_line(r2nums[point],r2nums[point + 1])
                        for aux_point in aux_points:
                            pointline.append(aux_point)
                image_as_list = []
                print(r1topspacing)
                print(true_x_length, true_y_length)
                for point in pointline:
                    list_of_points = []
                    for j in range(r1topspacing):
                        #
                        try:
                            p0S, p0s, p1S, p1s = 0, 0, 0, 0
                            if point[0] < true_x_length: p0S = 1
                            if point[0] > -1: p0s = 1
                            if point[1] + r1botspacing - j < true_y_length: p1S = 1
                            if point[1] + r1botspacing - j > -1: p1s = 1
                            if sys.argv[8] == "EXTEND":
                                list_of_points.append(image[(point[1] + r1botspacing - j) * p1S * p1s + (true_y_length - 1) * (1 - p1S)][point[0] * p0S * p0s + (true_x_length - 1) * (1 - p0S)])
                            elif sys.argv[8] == "BLANK":
                                if (p0S + p0s + p1S + p1s) != 4:
                                    list_of_points.append([0, 0, 0])
                                else:
                                    list_of_points.append(image[point[1] + r1botspacing - j][point[0]])
                            else:
                                print("WRONG EXTENSION METHOD SET")
                        except:
                            print("EXCEPT")
                        #
                        list_of_points.append(image[point[1] + r1botspacing - j][true_x_length - 1])
                    image_as_list.append(list_of_points)
                #print(image_as_list)
                image_as_array = np.array(image_as_list, dtype=np.uint8)
                img = Image.fromarray(image_as_array, 'RGB')
                img2 = img
                print(sys.argv[3] + "/" + sys.argv[1].split('/')[-1][:-4] + "." + this_region + "." + this_line + ".png")
                img2.save(sys.argv[3] + "/" + sys.argv[1].split('/')[-1][:-4] + "." + this_region + "." + this_line + ".png")

                pre_rot = Image.open(sys.argv[3] + "/" + sys.argv[1].split('/')[-1][:-4] + "." + this_region + "." + this_line + ".png")
                ooo = np.array(imread(sys.argv[3] + "/" + sys.argv[1].split('/')[-1][:-4] + "." + this_region + "." + this_line + ".png"))
                if ooo.shape[0] > ooo.shape[1]:
                    post_rot = pre_rot.transpose(Image.ROTATE_90)
                    post_rot.save(sys.argv[3] + "/" + sys.argv[1].split('/')[-1][:-4] + "." + this_region + "." + this_line + ".png")
