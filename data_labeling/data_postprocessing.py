import numpy as np
import cv2
from imageio import imread, imwrite
import glob
import os
import argparse
from utils import load_imgs, canny_edge, find_contours

parser = argparse.ArgumentParser()
parser.add_argument("--image_path",     type=str,   help="raw image path", default='./data_labeling/data/img/032155_white_50cm/rgb/')
parser.add_argument("--depth_path",     type=str,   help="raw image path", default='./data_labeling/data/img/032155_white_50cm/depth/')
parser.add_argument("--result_path",     type=str,   help="raw image path", default='./data_labeling/data/img/032155_white_50cm/result/')


args = parser.parse_args()
IMAGE_PATH = args.image_path
OPEN_DEPTH_PATH = args.depth_path
RESULT_PATH = args.result_path
RESOLUTION = (640,480)
RGB_PATH = RESULT_PATH+'rgb/'
MASK_PATH = RESULT_PATH+'mask/'
DEPTH_PATH = RESULT_PATH+'depth/'

os.makedirs(RESULT_PATH, exist_ok=True)
os.makedirs(RGB_PATH, exist_ok=True)
os.makedirs(MASK_PATH, exist_ok=True)
os.makedirs(DEPTH_PATH, exist_ok=True)


img_list = glob.glob(os.path.join(IMAGE_PATH,'*.png'))
img_list.sort()
depth_list = glob.glob(os.path.join(OPEN_DEPTH_PATH,'*.tif'))
depth_list.sort()


if __name__ == '__main__': 
    for idx in range(len(img_list)):
        img = cv2.imread(img_list[idx])
        depth = imread(depth_list[idx])
        depth = cv2.resize(depth, dsize=RESOLUTION, interpolation=cv2.INTER_AREA)
        date_name = img_list[idx].split('/')[4]
        
        img_name = img_list[idx].split('/')[5].split('\\')[1].split('.')[0]
        mask, img = load_imgs(img, resize=RESOLUTION)
        mask = canny_edge(mask)
        draw_mask = find_contours(mask, img)

        if len(draw_mask) != 0:
            print('save_image')
            cv2.imwrite(RGB_PATH+date_name + '_' +img_name+'.png', img)
            cv2.imwrite(MASK_PATH+date_name + '_' +img_name+'_mask.png', draw_mask)
            imwrite(DEPTH_PATH+date_name + '_' +img_name+'_depth.tif', depth)