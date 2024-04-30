#Large Scale Data Extraction and Analysis for Bigfoot


#Task 5
##Requirements
Python 3.6 or later
pandas library
requests library
OpenAI API key
Usage
Place your dataset file (merged_bfro.csv) in the same directory as the script.
Install the required Python libraries:


pip install pandas requests
Set your OpenAI API key in the script by replacing "key here" with your actual API key.
Run the script:


python bigfoot_image_generator.py
The script will process each row in the dataset and generate an image based on the Observed column. The images will be saved in the images directory with filenames corresponding to the Id column of the dataset. The updated dataset with the paths to the generated images will be saved as your_updated_dataset.csv. 




# Task 6
## Requirements:
* Python 3.11.5 used for this task
* PyCharm was the IDE used when developing and executing the Python scripts
* I had the following installed while completing Task 6 (installed Docker, Git, Node.js):
   * Docker version 25.0.3, build 4debf41
   * git version 2.44.0.windows.1
   * Node v20.11.1
* External Python libraries installed for this task:
   * requests==2.31.0
   * pandas==2.2.1


## The installation and configuration of Docker was done on Windows:
1. Install Docker Desktop for Windows and follow the instructions on how to install it
2. Download the folder containing the BFRO images and make note of where this folder is located in your directory
3. After installing Docker Desktop, clone and set up the Tika Dockers
4. Clone the Tika Docker repository to your current directory:
   1. git clone https://github.com/USCDataScience/tika-dockers.git
5. Navigate into the tika-dockers directory:
   1. cd tika-dockers
6. Pull Docker images directly using the Docker CLI:
   1. docker pull uscdatascience/inception-rest-tika
7. Build the Docker Images for various models:
   1. For the Inception v4 model for Image Detection:
      1. docker build -f InceptionRestDockerfile -t uscdatascience/inception-rest-tika . 
   2.    For the Show and Tell model for Image Text Captioning:
      1. docker build -f Im2txtRestDockerfile -t uscdatascience/im2txt-rest-tika .
   3.    For Object Identification in Videos:
      1. docker build -f InceptionVideoRestDockerfile -t uscdatascience/inception-video-rest-tika . 
8. Verify the image build by listing Docker images:
   1. docker images
9. Run the Docker Containers for the built images:
   1. docker run -it -p 8764:8764 uscdatascience/inception-rest-tika 
10. Test the connection
   1. enter the following URL into your web browser and you should receive a plain text response saying ‘pong’: http://localhost:8764/inception/v4/ping
11. Serve local images to make them accessible via a URL:
   1. Navigate to the directory containing your images (do this in a second terminal, not the same terminal the Docker container is being run in).
12. Start the server in the directory with your image:
   1. http-server -p 8000
   2. This serves your all images in the file at http://localhost:8000.
13. If you encounter PowerShell execution policy errors, run the following in PowerShell to allow script execution:
   1. Set-ExecutionPolicy RemoteSigned -Scope Process
14. Then, run the http-server command again: http-server -p 8000
15. Run the curl command in a separate third terminal
   1. Example of a curl command to run:
curl “http://localhost:8764/inception/v4/classify/image?url=http://192.168.50.238:8000/25979.jpeg”
   2. Make sure to change the IP address to whatever your own IP address is. To check for your IP address in PowerShell, type “ipconfig” and look to see where the information on your IP address is
16. Do steps 5-15 to set up the second Tika Docker (Show and Tell model), and make sure to modify the commands and URLs to fit with setting up the Show and Tell model instead of the Inception v4 model


## The guidelines above were made public to the class by a classmate, but there may be some issues setting up the Tika Docker container that is not noted in the guidelines above. In subsequent attempts to set up the Docker container for the Inception v4 model, there were issues with establishing a connection. This issue was resolved by following these guidelines (skip the build Docker Images step here, trying to run the docker build command here will result in failing to establish a connection with the Docker container):
1. Navigate into the tika-dockers directory:
   1. cd tika-dockers
2. Pull the Docker image directly using the Docker CLI:
   1. docker pull uscdatascience/inception-rest-tika
3. Run the Docker container for the Inception v4 model:
   1. docker run -it -p 8764:8764 uscdatascience/inception-rest-tika
4. Test the connection by accessing the following URL in your web browser:
   1. http://localhost:8764/inception/v4/ping


## After being able to successfully run the Docker container, run the Python script labeled ‘task6_object_detection.py’. This script will query the Tika Inception service and generate object detections for each of the BFRO images. The folder containing the BFRO images was renamed to ‘bfro_images’, and the folder inside that folder is just called ‘images’. Place this folder inside the same directory as the script, and you should make sure to rename the folders to match the path written in the code, or else the images may not be found when running the script. After all the object detections have been generated, the results are saved to a csv file called ‘object_detection_results.csv’, and this csv file is then merged with the csv file from Task 5, ‘task5_dataset.csv’, and the resulting merged csv file is called ‘merged_dataset.csv’. Before merging the datasets, make sure the resulting csv file from Task 5 is named properly and is in the same directory as the Python script, or errors may occur while executing the script.


## Run the second Python script for Task 6, ‘task6_generate_captions.py’. This script will query the Tika caption generator service and produce image captions for each image. Just like with the ‘task6_object_detection.py’ script, make sure the folder containing the BFRO images is in the same directory as the script and is renamed appropriately. The folder containing the BFRO images should be renamed to ‘bfro_images’, and the folder inside that folder is just called ‘images’. If the folder is not named properly, there may be an error when running the script. After all the image captions have been generated, the results are saved to a csv file called ‘image_captions.csv’, and this csv file is then merged with the final csv file from the previous script, the ‘merged_dataset.csv’ file. The resulting merged csv file is called 'task6_dataset.csv', and this is the final resulting dataset for Task 6.




# Task 7
## Requirements:
1. Use Python 2.7.18 for this task
2. The codes here are for Linux system or virtual machine (Ubuntu)
3. The scripts/commands assume that you downloaded the ‘TEAM_10_DSCI550_HW_EXTRACT’ to your home directory ($HOME), if you choose to download the folder in a different way, you will need to adjust the paths accordingly.


## Things you need:
1. GeoTopicParser (https://cwiki.apache.org/confluence/display/tika/GeoTopicParser)
2. Apache Tika 2.9.1 (https://tika.apache.org/download.html)


Note: The above things you need have already been provided in the folder. If you encounter any problems, refer to the links above, and you may choose to download some of the files again. But make sure you follow the structure in this folder to make sure that the path works. In this folder, the custom-mimetypes.xml is also in the location-ner-model directory. 


## Step 1: Adjust the system environment variables
Open your .rc file, this could be ‘.bashrc’, ‘.zshrc’, or ‘.bash_profile’, depending on the system you are using. You can open the .rc file by running the following on your terminal: 
```nano ~/.zshrc```


Add the following to the end of your .rc file:
```
export PATH="$HOME/TEAM_10_DSCI550_HW_EXTRACT/Source\ Code/src/lucene-geo-gazetteer/src/main/bin:$PATH"


export TIKA_PATH="$HOME/TEAM_10_DSCI550_HW_EXTRACT/Source\ Code/tika/libexec/"
export TIKA_SERVER_JAR="$HOME/TEAM_10_DSCI550_HW_EXTRACT/Source\ Code/tika/libexec/tika-server-standard-2.9.1.jar"
export TIKA_STARTUP_MAX_RETRY=3
export TIKA_JAVA_ARGS=-Xmx4g
export TIKA_SERVER_ENDPOINT="http://localhost:9998"
export TIKA_VERSION=2.9.1
export TIKA_SERVER_CLASSPATH="$HOME/TEAM_10_DSCI550_HW_EXTRACT/Source\ Code/src/location-ner-model:$HOME/TEAM_10_DSCI550_HW_EXTRACT/Source\ Code/tika/libexec/tika-parser-nlp-package-2.9.1.jar"
export TIKA_APP="$HOME/TEAM_10_DSCI550_HW_EXTRACT/Source\ Code/tika/libexec/tika-app-2.9.1.jar"


export CLASSPATH="$HOME/TEAM_10_DSCI550_HW_EXTRACT/Source\ Code/tika/liexec/*:$HOME/TEAM_10_DSCI550_HW_EXTRACT/Source\ Code/src/geotopic-mime:$HOME/TEAM_10_DSCI550_HW_EXTRACT/Source\ Code/src/location-ner-model:$CLASSPATH:."
```
Again, please note that this assumes that you downloaded the TEAM_10_DSCI550_HW_EXTRACT folder to your home directory, if not, you may need to adjust the paths accordingly. 


## Step 2: Run the Tika Server
Run the following command:
1. ```cd $HOME```
2. ```java -Xmx4g -cp $HOME/TEAM_10_DSCI550_HW_EXTRACT/Source\ Code/tika/libexec/tika-server-standard-2.9.1.jar:$HOME/TEAM_10_DSCI550_HW_EXTRACT/Source\ Code/tika/libexec/tika-parser-nlp-package-2.9.1.jar:$HOME/TEAM_10_DSCI550_HW_EXTRACT/Source\ Code/src/location-ner-model org.apache.tika.server.core.TikaServerCli --port 9998 --host localhost```


## Step 3: Start the Lucene Gazetteer
Open another terminal, and run the following command
1. ```lucene-geo-gazetteer -server```


## Step 4: Iterate through all the BFRO sightings and then run Tika GeoTopicParser and extract out Location name, including Lat/Lng
Open Jupyter Notebook and run task7_code.ipynd, make sure you run it following the order, and this will output a csv file called task7_dataset.csv, and that’s the result for task 7.




# Task 8：
## Overview
This Python script analyzes the Bigfoot Sighting Dataset by extracting named entities from textual descriptions using the spaCy library. The extracted entities are then stored along with their probabilities in separate columns for further analysis.


## Requirements
Ensure you have the following dependencies installed:
- pandas==1.3.3
- spacy==3.1.3


## Usage
1. Install the required dependencies listed in requirements.txt using pip:
pip install -r requirements.txt


2. Run the script `task8_code.ipynb` in Source Code file to perform entity extraction and generate an updated dataset:
python task8_code.ipynb


## Files
- `task8_code.ipynb`: Python script for entity extraction and dataset processing.
- `task7_dataset.csv`: Input dataset containing Bigfoot sighting records.
- `task8_dataset.csv`: Updated dataset with extracted entities and their probabilities stored in separate columns.
- `task8_dataset.tsv`: Updated dataset saved as a TSV (Tab-Separated Values) file for easier compatibility with other tools.










#Task details
Task 5 Kayden Lea
Task 6 Katherine Lieu
Task 7 Yifeng Zou, Xinyao Fu
Task 8 Kexuan Zou