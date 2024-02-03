import cv2
import matplotlib.pyplot as plt

def plot_histogram(image, title):
    # Calculate histogram
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])

    # Plot histogram
    plt.figure()
    plt.title(title)
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.plot(hist)
    plt.xlim([0, 256])
    plt.show()

def display_histograms(original_video_path, compressed_video_path):
    # Open the original video file for reading
    original_cap = cv2.VideoCapture(original_video_path)

    # Open the compressed video file for reading
    compressed_cap = cv2.VideoCapture(compressed_video_path)
    
    # Create a figure with two subplots
    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    # Loop through the frames
    while original_cap.isOpened() and compressed_cap.isOpened():
        # Read the original frame
        ret_original, original_frame = original_cap.read()

        # Read the compressed frame
        ret_compressed, compressed_frame = compressed_cap.read()

        if ret_original and ret_compressed:
            # Convert the frames to grayscale
            original_frame_gray = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
            compressed_frame_gray = cv2.cvtColor(compressed_frame, cv2.COLOR_BGR2GRAY)

            # Calculate histograms
            original_hist = cv2.calcHist([original_frame_gray], [0], None, [256], [0, 256])
            compressed_hist = cv2.calcHist([compressed_frame_gray], [0], None, [256], [0, 256])

            # Plot histograms
            axs[0].cla()
            axs[0].plot(original_hist)
            axs[0].set_title("Original Frame Histogram")
            axs[0].set_xlabel("Pixel Value")
            axs[0].set_ylabel("Frequency")

            axs[1].cla()
            axs[1].plot(compressed_hist)
            axs[1].set_title("Compressed Frame Histogram")
            axs[1].set_xlabel("Pixel Value")
            axs[1].set_ylabel("Frequency")

            # Update the plot
            plt.tight_layout()
            plt.pause(0.01)

        else:
            break

    # Release the video capture objects
    original_cap.release()
    compressed_cap.release()

    # Close the plot window
    plt.close(fig)

original_video_path = "Cryptos.mp4"
compressed_video_path = "encrypted_video.mp4"

display_histograms(original_video_path, compressed_video_path)
