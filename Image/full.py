import cv2
import numpy as np
import matplotlib.pyplot as plt

def display_histograms(original_image, encrypted_image):
    # Calculate the histograms of the original and encrypted images
    original_hist = cv2.calcHist([original_image], [0], None, [256], [0, 256])
    encrypted_hist = cv2.calcHist([encrypted_image], [0], None, [256], [0, 256])

    # Plot the histograms
    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plt.plot(original_hist, color='b')
    plt.title("Original Image Histogram")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")

    plt.subplot(122)
    plt.plot(encrypted_hist, color='r')
    plt.title("Encrypted Image Histogram")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Frequency")

    # Display the histograms
    plt.tight_layout()
    plt.show()

# Load the original and encrypted images
original_image = cv2.imread("Image\cameramann.jpg", cv2.IMREAD_GRAYSCALE)
encrypted_image = cv2.imread("Image\encrypted_image.png", cv2.IMREAD_GRAYSCALE)

# Display the histograms
display_histograms(original_image, encrypted_image)
