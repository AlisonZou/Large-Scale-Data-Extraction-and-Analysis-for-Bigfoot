# Assignment 2, Task 6
# Generate Image Captions

# Import libraries
import requests
import socket
import os
import pandas as pd
import csv


# Retrieve the (non-localhost) IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ipaddr = s.getsockname()[0]
print("IP address:" + ipaddr)

# Path to the directory containing the JPEG images
path = "./bfro_images/images"

# Get the list of all JPEG image files in the directory
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(".jpeg")]

# Print out all the jpeg images in the images folder
print(files)

# Print the number of JPEG files
print("Number of JPEG files:", len(files))

# Initialize lists to store data for CSV file that will be created later
image_filenames = []
generated_image_paths = []
captions_data = []

try:
    # Iterate through each image file
    for file in files:
        # Compose the URL to query the Tika caption generator service
        url = f"http://localhost:8764/inception/v3/caption/image?url=http://{ipaddr}:8000/{file}"
        # print("Processing image:", file)

        # Retrieve the text from the given URL
        response = requests.get(url)

        # Handle HTTP errors
        response.raise_for_status()

        # Retrieve the JSON response
        json_response = response.json()

        # Extract the captions from the JSON response
        captions = [caption['sentence'] for caption in json_response.get('captions', [])]

        # Print the captions for the current image
        print(f"Captions for image {file}: {captions}")

        # Append data to lists
        image_filenames.append(file)
        captions_data.append(captions)
        generated_image_paths.append(os.path.join("images", file))

except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")

# Write data to CSV file
output_file = "image_captions.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(['Image', 'Image Caption(s)', 'Generated_Image_Path'])
    # Write data rows
    for i in range(len(image_filenames)):
        writer.writerow([image_filenames[i], captions_data[i], generated_image_paths[i]])

print("CSV file created successfully.")

# Load the merged_dataset.csv
merged_dataset_df = pd.read_csv('merged_dataset.csv')

# Load the image captions from the CSV file
image_captions_df = pd.read_csv('image_captions.csv')

# Drop the 'Image' column from the image captions dataframe
image_captions_df.drop(columns=['Image'], inplace=True)

# Perform a left merge on 'Generated_Image_Path'
merged_df = pd.merge(merged_dataset_df, image_captions_df, on='Generated_Image_Path', how='left')

# Remove brackets and apostrophes from the 'Image Caption(s)' column
# task6_df['Image Caption(s)'] = task6_df['Image Caption(s)'].str.strip("[]").str.replace("'", "")

# Print the merged DataFrame to verify the merge
print(merged_df)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('task6_dataset.csv', index=False)

print("Left merge completed successfully. Merged dataset saved as task6_dataset.csv.")
