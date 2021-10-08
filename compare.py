# code adapted from: https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/

# import the necessary packages
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
from os import listdir
from os.path import isfile, join
import sys
import csv


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def compare_images(imageA, imageB):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)
    return m, s


def read_files(path):
    files = [path.removesuffix('/') + "/" + f for f in listdir(path)
             if isfile(join(path, f)) and (join(path, f).endswith(".png")
            or join(path, f).endswith(".jpg") or join(path, f).endswith(".jpeg"))]
    return files


def compute_sim(file1, file2):
    img1 = cv2.imread(file1)
    img2 = cv2.imread(file2)

    # convert the images to grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    mse, ssim = compare_images(img1, img2)
    return mse, ssim


def main():
    if len(sys.argv) <= 1:
        print("python compare.py /Users/chaiyong/Desktop/images/ output.csv")
        exit(0)

    # open the file in the write mode
    f = open(sys.argv[2], 'w')
    f.write("file1,file2,similarity\n")

    print("Start checking image similarity at " + sys.argv[1])
    files = read_files(sys.argv[1])
    for i in range(len(files)):
        for j in range(len(files)):
            if not files[i] == files[j]:
                m, s = compute_sim(files[i], files[j])
                print(files[i] + "," + files[j] + "," + str(s))
                # write a row to the csv file
                f.write(files[i] + "," + files[j] + "," + str(s) + "\n")
    # close the file
    f.close()
    print('Done! Bye')


if __name__ == "__main__":
    main()
