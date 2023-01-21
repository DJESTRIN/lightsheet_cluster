import tifffile
from concurrent.futures import ThreadPoolExecutor
import argparse
from skimage.util import view_as_windows
import numpy as np

# Define a function to perform local contrast enhancement on a single image
def enhance_image(image, window_size, stride):
    # Create the view of the image as windows
    windows = view_as_windows(image, window_size, stride)

    # Compute the mean and standard deviation of each window
    means = np.mean(windows, axis=(-3, -2))
    stds = np.std(windows, axis=(-3, -2))

    # Perform local contrast enhancement on each window
    contrast_enhanced = (windows - means[..., np.newaxis, np.newaxis]) / stds[..., np.newaxis, np.newaxis]

    # Reconstruct the image from the contrast-enhanced windows
    reconstructed = np.zeros_like(image)
    count = np.zeros_like(image)
    for i in range(0, image.shape[0] - window_size[0], stride):
        for j in range(0, image.shape[1] - window_size[1], stride):
            reconstructed[i:i + window_size[0], j:j + window_size[1]] += contrast_enhanced[i // stride, j // stride]
            count[i:i + window_size[0], j:j + window_size[1]] += 1
    reconstructed /= count
    return reconstructed

if __name__=='__main__':
  # Use argparse to define command-line arguments
  parser = argparse.ArgumentParser(description="Perform local contrast enhancement on a TIFF stack.")
  parser.add_argument("input_directory", type=str, help="The directory containing the input TIFF stack.")
  parser.add_argument("output_directory", type=str, help="The directory to save the output TIFF stack.")
  parser.add_argument("--window_size", type=int, nargs=2, default=(50,50), help="The size of the window for tiling")
  parser.add_argument("--stride", type=int, default=10, help="The stride for tiling")
  args = parser.parse_args()

  # Read in the TIFF stack
  with tifffile.TiffFile(args.input_directory) as tif:
      stack = tif.asarray()

  window_size = tuple(args.window_size)
  stride = args.stride

  # Use a ThreadPoolExecutor to process the images in parallel
  with ThreadPoolExecutor() as executor:
      # Submit the enhance_image function for each image in the stack to the executor
      futures = [executor.submit(enhance_image, image, window_size, stride) for image in stack]

      # Iterate over the completed futures to get the contrast-enhanced images
      contrast_enhanced_images = [future.result() for future in futures]

   # Convert the list
  tifffile.imsave(args.output_directory, contrast_enhanced_images)
