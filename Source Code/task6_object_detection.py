# Assignment 2, Task 6
# Object Detection

# Import libraries
import requests
import socket
import os
import csv
import pandas as pd


# Retrieve the (non-localhost) IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ipaddr = s.getsockname()[0]
print("IP address:" + ipaddr)

# Path to the directory containing the JPEG images
path = "./bfro_images/images"

# Get the list of all JPEG image files in the directory
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(".jpeg")]

# Initialize lists to store data for CSV file that will be created later
image_filenames = []
object_detection_results = []
generated_image_paths = []

# Iterate through each image file
for file in files:
    # Compose the URL to query the Tika Inception service
    url = f"http://localhost:8764/inception/v4/classify/image?url=http://{ipaddr}:8000/{file}"
    print("Processing image:", file)
    try:
        # Retrieve the text from the given URL
        response = requests.get(url)
        # Handle HTTP errors
        response.raise_for_status()
        # Retrieve the JSON response
        text = response.json()

        # Append data to lists
        image_filenames.append(file)
        object_detection_results.append(text['classnames'])
        generated_image_paths.append(os.path.join("images", file))

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")

# Write data to CSV file
output_file = "object_detection_results.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(['Image', 'Detected Object(s)', 'Generated_Image_Path'])
    # Write data rows
    for i in range(len(image_filenames)):
        writer.writerow([image_filenames[i], object_detection_results[i], generated_image_paths[i]])

print("CSV file created successfully.")

# Load the task5_dataset.csv
task5_dataset_df = pd.read_csv('task5_dataset.csv')

# Load the object detection results from the CSV file
object_detection_df = pd.read_csv('object_detection_results.csv')

# Drop the 'Image' column from the object detection results
object_detection_df.drop(columns=['Image'], inplace=True)

# Perform a left merge on 'Generated_Image_Path'
merged_df = pd.merge(task5_dataset_df, object_detection_df, on='Generated_Image_Path', how='left')

# Remove brackets and apostrophes from the 'Detected Object(s)' column
# merged_df['Detected Object(s)'] = merged_df['Detected Object(s)'].str.strip("[]").str.replace("'", "")

# Print the merged DataFrame to verify the merge
print(merged_df)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('merged_dataset.csv', index=False)

print("Left merge completed successfully. Merged dataset saved as merged_dataset.csv.")
