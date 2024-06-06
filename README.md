# Health Study Data Pipeline

## Overview

This project involves building a data pipeline to process questionnaire data from a health study. The pipeline includes steps for data ingestion, cleaning, transformation, and quality reporting.

## Setup

### Local Setup

1. **Open the project in VSCode**:

   - Open Visual Studio Code (VSCode).
   - Use the File menu to open the project directory where your code is located.


### Docker Setup

1. **Ensure Docker is installed**:

   - Download and install Docker from [Docker's official website](https://www.docker.com/get-started).

2. **Verify your project directory contains the following files**:

   ```
   .
   ├── Dockerfile
   ├── README.md
   ├── main.py
   ├── prefect_flow.py
   ├── requirements.txt
   ├── synthetic_questionnaire.json
   └── synthetic_answers.json
   ```

3. **Create the `Dockerfile`**:
   Ensure you have a file named `Dockerfile` in your project directory with the following content:

   ```dockerfile
   # Use the official Python image from the Docker Hub
   FROM python:3.9-slim

   # Set the working directory in the container
   WORKDIR /app

   # Copy the requirements file into the container
   COPY requirements.txt /app/

   # Install the required Python packages
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy the entire project directory into the container
   COPY . /app

   # Command to run the Prefect flow
   CMD ["python", "prefect_flow.py"]
   ```

4. **Create the `requirements.txt` file**:
   Ensure you have a `requirements.txt` file with the following content:

   ```text
   pandas
   prefect
   ```

5. **Open a terminal and navigate to your project directory**:

   ```bash
   cd /path/to/your/project
   ```

   Replace `/path/to/your/project` with the actual path to your project directory.

6. **Build the Docker image**:
   Run the following command to build the Docker image:

   ```bash
   docker build -t health_study_pipeline .
   ```

7. **Run the Docker container**:
   After the image is built, start a container from the image:

   On Windows:

   ```bash
   docker run health_study_pipeline
   ```

8. **Verify the output**:
   After running the Docker container, you should see the log output indicating the flow is running and the data processing is complete. The cleaned data should be saved in the `cleaned_questionnaire_data.csv` file in your project directory.

## Data Files

- `synthetic_questionnaire.json`: Contains the questionnaire structure and questions.
- `synthetic_answers.json`: Contains the answers provided by participants.


## Additional Information

- The pipeline is designed to be easily extendable for future enhancements.
