from PIL import Image
import numpy as np
from viz.image import from_array,to_array

def split_into_squares(img_arr):
  n = 8
  squares = []
  for row in np.split(img_arr,n,axis=0):
    squares.extend(np.split(row,n,axis=1))
  return np.asarray(squares)

def dimensions(img_arr):
  return (len(img_arr),len(img_arr[0]))

def image_to_grayscale(img_arr):
  (height,width) = dimensions(img_arr)
  gray_img_arr = np.zeros((height,width))
  for i in range(0,height):
    for j in range(0,width):
      gray_img_arr[i,j] = pixel_to_grayscale(img_arr[i,j])
  return gray_img_arr.astype(np.uint8)

def pixel_to_grayscale(pixel):
  return round((int(pixel[0]) + int(pixel[1]) + int(pixel[2])) / 3)

def add_filter(img_arr, color_filter):
  img = from_array(img_arr)
  color_filter = Image.new('RGB',img.size,color_filter)
  mask = Image.new('RGBA',img.size,(0,0,0,123)) # Alpha channel mask
  return to_array(Image.composite(img,color_filter,mask).convert('RGB'))

def normalize_image(img_arr):
  return img_arr / 255.0

def normalize_images(img_arrs):
  return np.asarray([normalize_image(img_arr) for img_arr in img_arrs])
