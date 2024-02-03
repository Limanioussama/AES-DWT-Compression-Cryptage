import cv2
from skimage.metrics import mean_squared_error, peak_signal_noise_ratio, structural_similarity


def calculate_mse(original_frame, decompressed_frame):
    return mean_squared_error(original_frame, decompressed_frame)

def calculate_psnr(original_frame, decompressed_frame):
    return peak_signal_noise_ratio(original_frame, decompressed_frame)

def calculate_ssim(original_frame, decompressed_frame):
    return structural_similarity(original_frame, decompressed_frame)

def evaluate_compression_quality(original_video_path, compressed_video_path):
    # Open the original video file for reading
    original_cap = cv2.VideoCapture(original_video_path)

    # Open the compressed video file for reading
    compressed_cap = cv2.VideoCapture(compressed_video_path)

    # Variables for tracking metrics
    total_mse = 0.0
    total_psnr = 0.0
    total_ssim = 0.0
    num_frames = 0

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

            # Calculate metrics
            mse = calculate_mse(original_frame_gray, compressed_frame_gray)
            psnr = calculate_psnr(original_frame_gray, compressed_frame_gray)
            ssim = calculate_ssim(original_frame_gray, compressed_frame_gray)

            # Accumulate metrics
            total_mse += mse
            total_psnr += psnr
            total_ssim += ssim
            num_frames += 1

        else:
            break

    # Calculate average metrics
    avg_mse = total_mse / num_frames
    avg_psnr = total_psnr / num_frames
    avg_ssim = total_ssim / num_frames

    # Print the average metrics
    print("Average MSE:", avg_mse)
    print("Average PSNR:", avg_psnr)
    print("Average SSIM:", avg_ssim)
#Result
    #Average MSE: 21.399107471275908
    #Average PSNR: 34.878487242951365
    #Average SSIM: 0.9785335924972558


original_video_path = "Cryptos.mp4"
compressed_video_path = "com_crypto.mp4"

evaluate_compression_quality(original_video_path, compressed_video_path)
