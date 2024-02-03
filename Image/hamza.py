import numpy as np
import cv2
from Crypto.Cipher import AES
import tkinter as tk
from tkinter import filedialog
import pywt
import math
from skimage.metrics import structural_similarity as ssim


# AES encryption
key = b'Key of length 16'
iv = b'ivb of length 16'


def encrypt_image(image):
    # Create an AES cipher object for encryption
    cfb_cipher = AES.new(key, AES.MODE_CFB, iv)

    # Convert the image to bytes
    image_bytes = image.tobytes()

    # Encrypt the image bytes
    encrypted_bytes = cfb_cipher.encrypt(image_bytes)

    # Convert the encrypted bytes back to an image array
    encrypted_image_array = np.frombuffer(encrypted_bytes, dtype=np.uint8)

    # Reshape the image array to its original dimensions
    encrypted_image = encrypted_image_array.reshape(image.shape)

    return encrypted_image


def decrypt_image(encrypted_image):
    # Create an AES cipher object for decryption
    cfb_cipher = AES.new(key, AES.MODE_CFB, iv)

    # Convert the encrypted image to bytes
    encrypted_image_bytes = encrypted_image.tobytes()

    # Decrypt the image bytes
    decrypted_bytes = cfb_cipher.decrypt(encrypted_image_bytes)

    # Convert the decrypted bytes back to an image array
    decrypted_image_array = np.frombuffer(decrypted_bytes, dtype=np.uint8)

    # Reshape the image array to its original dimensions
    decrypted_image = decrypted_image_array.reshape(encrypted_image.shape)

    return decrypted_image


def compress_image(image):
    # Perform DWT on the image
    coeffs = pywt.dwt2(image, 'haar')

    # Keep only the LL subband coefficients
    LL, (LH, HL, HH) = coeffs
    coeffs = LL, (np.zeros_like(LH), np.zeros_like(HL), np.zeros_like(HH))

    # Reconstruct the compressed image
    compressed_image = pywt.idwt2(coeffs, 'haar')

    # Convert the image to unsigned 8-bit integers
    compressed_image = np.uint8(compressed_image)

    # Resize the compressed image to match the input image dimensions
    compressed_image = cv2.resize(compressed_image, (image.shape[1], image.shape[0]))

    return compressed_image


def decompress_image(compressed_image):
    # Perform IDWT on the compressed image
    coeffs = pywt.dwt2(compressed_image, 'haar')
    reconstructed_image = pywt.idwt2(coeffs, 'haar')

    # Convert the image to unsigned 8-bit integers
    reconstructed_image = np.uint8(reconstructed_image)

    # Resize the reconstructed image to match the input image dimensions
    reconstructed_image = cv2.resize(reconstructed_image, (compressed_image.shape[1], compressed_image.shape[0]))

    return reconstructed_image




def evaluate_compression_quality(original_image, compressed_image):
    # Calculate Mean Squared Error (MSE)
    mse = np.mean((original_image.astype(np.float32) - compressed_image.astype(np.float32)) ** 2)

    # Calculate Peak Signal-to-Noise Ratio (PSNR)
    max_pixel_value = np.max(original_image)
    psnr = 20 * math.log10(max_pixel_value / math.sqrt(mse))

    # Calculate Structural Similarity Index (SSIM)
    ssim_value = ssim(original_image, compressed_image)

    return mse, psnr, ssim_value


def open_image():
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        # Load the grayscale image
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        # Create a window and display the original image
        cv2.imshow("Original Image", image)
        cv2.waitKey(0)

        # Compress the image
        compressed_image = compress_image(image)
        cv2.imshow("Compressed Image", compressed_image)
        cv2.waitKey(0)

        # Decompress the image
        decompressed_image = decompress_image(compressed_image)
        cv2.imshow("Decompressed Image", decompressed_image)
        cv2.waitKey(0)

        # Encrypt the image
        encrypted_image = encrypt_image(decompressed_image)
        cv2.imshow("Encrypted Image", encrypted_image)
        cv2.waitKey(0)

        # Decrypt the image
        decrypted_image = decrypt_image(encrypted_image)
        cv2.imshow("Decrypted Image", decrypted_image)
        cv2.waitKey(0)

        # Calculate compression quality metrics
        mse, psnr, ssim = evaluate_compression_quality(image, compressed_image)
        print("MSE:", mse)
        print("PSNR:", psnr)
        print("SSIM:", ssim)

        # Save the images
        save_directory = filedialog.askdirectory()
        if save_directory:
            cv2.imwrite(f"{save_directory}/compressed_image.png", compressed_image)
            cv2.imwrite(f"{save_directory}/encrypted_image.png", encrypted_image)
            cv2.imwrite(f"{save_directory}/decrypted_image.png", decrypted_image)
            cv2.imwrite(f"{save_directory}/decompressed_image.png", decompressed_image)

        cv2.destroyAllWindows()


def main():
    # Create a Tkinter window
    window = tk.Tk()
    window.title("Image Compression and Encryption")

    # Create an "Open Image" button
    open_button = tk.Button(window, text="Open Image", command=open_image)
    open_button.pack(pady=10)

    # Run the Tkinter event loop
    window.mainloop()


if __name__ == "__main__":
    main()

