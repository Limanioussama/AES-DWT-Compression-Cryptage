import cv2
import numpy as np
from scipy.stats import entropy, pearsonr

def calculate_entropy(image):
    # Flatten the image
    flattened_image = image.flatten()

    # Calculate the probability distribution of pixel values
    pixel_probabilities = np.histogram(flattened_image, bins=256, range=[0, 256], density=True)[0]

    # Calculate the entropy
    image_entropy = entropy(pixel_probabilities, base=2)

    return image_entropy

def calculate_correlation(image1, image2):
    # Flatten the images
    flattened_image1 = image1.flatten()
    flattened_image2 = image2.flatten()

    # Calculate the correlation coefficient
    correlation_coefficient, _ = pearsonr(flattened_image1, flattened_image2)

    return correlation_coefficient

def evaluate_encryption_quality(original_video_path, encrypted_video_path):
    # Open the original video file for reading
    original_cap = cv2.VideoCapture(original_video_path)

    # Open the encrypted video file for reading
    encrypted_cap = cv2.VideoCapture(encrypted_video_path)

    entropy_values = []
    correlation_coefficients = []

    # Loop through the frames
    while original_cap.isOpened() and encrypted_cap.isOpened():
        # Read the original frame
        ret_original, original_frame = original_cap.read()

        # Read the encrypted frame
        ret_encrypted, encrypted_frame = encrypted_cap.read()

        if ret_original and ret_encrypted:
            # Convert the frames to grayscale
            original_frame_gray = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
            encrypted_frame_gray = cv2.cvtColor(encrypted_frame, cv2.COLOR_BGR2GRAY)

            # Calculate entropy of the original frame
            original_entropy = calculate_entropy(original_frame_gray)
            entropy_values.append(original_entropy)

            # Calculate correlation coefficient between the original and encrypted frames
            correlation_coefficient = calculate_correlation(original_frame_gray, encrypted_frame_gray)
            correlation_coefficients.append(correlation_coefficient)

        else:
            break

    # Release the video capture objects
    original_cap.release()
    encrypted_cap.release()

    # Calculate average entropy and correlation coefficient
    avg_entropy = np.mean(entropy_values)
    avg_correlation = np.mean(correlation_coefficients)

    return avg_entropy, avg_correlation

original_video_path = "Cryptos.mp4"
encrypted_video_path = "encrypted_video.mp4"

avg_entropy, avg_correlation = evaluate_encryption_quality(original_video_path, encrypted_video_path)

print("Average Entropy:", avg_entropy)
print("Average Correlation Coefficient:", avg_correlation)

#Result :
#Average Entropy: 2.6359930917993566
#Average Correlation Coefficient: 0.0001336001647048418
