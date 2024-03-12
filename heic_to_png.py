# PREREQ:           pip install -r requirements.txt
# USAGE 1:          python heic_to_png.py input.HEIC
#                       -> converts input.HEIC (which is in cwd) to input.png [will overwrite file if it already exist]
# USAGE 2:          python heic_to_png.py *.HEIC
#                       -> converts all .HEIC images in cwd to <same-name>.png [will overwrite file if it already exist]

from PIL import Image
import sys
import os
import glob
from pillow_heif import read_heif


def heic_to_png(input_path, output_path):
    try:
        # open HEIC image
        heif_file = read_heif(input_path)
        
        # convert to PIL Image
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )

        # save as PNG
        image.save(output_path, format="PNG")
        print(f"Conversion successful: {input_path} -> {output_path}")
    except Exception as e:
        print(f"Error during conversion: {e}")


def main():
    if len(sys.argv) != 2:
        print("Wrong usage!\nCorrect Usage: python heic_to_png.py inputfilenameOrWildcard")
        return
    
    input_pattern = sys.argv[1]
    output_folder = os.getcwd()

    for input_path in glob.glob(input_pattern):
        if not input_path.lower().endswith('.heic'):
            print(f"Skipping non-HEIC file: {input_path}")
            continue

        output_name = os.path.splitext(os.path.basename(input_path))[0] + ".png"
        output_path = os.path.join(os.getcwd(), output_name) # output path is same is input path which is cwd

        heic_to_png(input_path, output_path)


main()
