import re

from PIL import Image
import os
import img2pdf

import cv2
import os


def convert_to_jpeg2000_opencv(input_dir, output_dir, compression_ratio=100):
    """
    Convert JPEG images to JPEG 2000 with specified compression ratio using OpenCV.

    :param input_dir: Directory containing JPEG images
    :param output_dir: Directory to save converted JPEG 2000 images
    :param compression_ratio: Higher value means lower quality and more compression.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith(".jpeg") or filename.endswith(".JPG"):
            img_path = os.path.join(input_dir, filename)
            img = cv2.imread(img_path)

            # Define the output file name (convert to .jp2)
            output_filename = f"{os.path.splitext(filename)[0]}.jp2"
            output_path = os.path.join(output_dir, output_filename)

            # Use OpenCV's imwrite to save as JPEG 2000 with compression
            # Compression params: [cv2.IMWRITE_JPEG2000_COMPRESSION_X1000, compression_ratio]
            # Compression ratio of 1000 gives the smallest size (max compression)
            cv2.imwrite(output_path, img, [cv2.IMWRITE_JPEG2000_COMPRESSION_X1000, compression_ratio])
            print(f"Converted {filename} to {output_filename} with compression ratio {compression_ratio}")


def natural_sort_key(filename):
    # Extract the numeric part from the filename using a regular expression
    return [int(part) if part.isdigit() else part for part in re.split('(\d+)', filename)]


def compile_images_to_pdf(jp2_dir, output_pdf):
    """
    Compile JPEG 2000 images into a single PDF.

    :param jp2_dir: Directory containing JPEG 2000 images
    :param output_pdf: Path to save the final PDF
    """
    # jp2_files = sorted([os.path.join(jp2_dir, f) for f in os.listdir(jp2_dir) if f.endswith(".jp2")])
    jp2_files = sorted(
        [os.path.join(jp2_dir, f) for f in os.listdir(jp2_dir) if f.endswith(".jp2")],
        key=natural_sort_key
    )

    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(jp2_files))

    print(f"Compiled images into {output_pdf}")


if __name__ == "__main__":
    # Directory containing the original JPEG images (numbered as 1.jpeg, 2.jpeg, etc.)
    input_dir = "imgs/"

    # Directory to save the converted JPEG 2000 images
    output_dir = input_dir + "jp2"

    # Path to save the final PDF
    output_pdf = input_dir + "a2-compression-50.pdf"

    # Step 1: Convert JPEG to JPEG 2000 with low quality
    convert_to_jpeg2000_opencv(input_dir, output_dir, compression_ratio=50)

    # Step 2: Compile JPEG 2000 images into a single PDF
    compile_images_to_pdf(output_dir, output_pdf)
