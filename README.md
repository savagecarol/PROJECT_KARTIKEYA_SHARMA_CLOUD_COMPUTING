# Stroke Prediction Project

This project predicts stroke events using 11 clinical features. The dataset is sourced from Kaggle, and the application is deployed using AWS services and Streamlit.

## Steps to Set Up the Project

### 1. Download the Dataset
Download the stroke prediction dataset from Kaggle. The dataset contains 11 clinical features for predicting stroke events. Save the file as `stroke.csv` in the project directory.

### 2. Set Up AWS S3
- Follow the screenshots [1.png](screenshots/1.png) and [2.png](screenshots/2.png) to set up an S3 bucket.
- Upload the `stroke.csv` file to the S3 bucket.

### 3. Set Up AWS Glue Crawler
- Use AWS Glue to create a crawler for the dataset.
- Refer to the screenshots [3.png](screenshots/3.png), [4.png](screenshots/4.png), [5.png](screenshots/5.png), and [6.png](screenshots/6.png) for step-by-step guidance.

### 4. Add Athena to AWS
- Configure AWS Athena to query the data.
- Follow the screenshots [8.png](screenshots/8.png), [9.png](screenshots/9.png), [10.png](screenshots/10.png), [11.png](screenshots/11.png), [12.png](screenshots/12.png), and [13.png](screenshots/13.png) for detailed instructions.

### 5. Create User and Access Policy
- Create an AWS user with the necessary access policies for S3, Glue, and Athena.
- Generate an access key for the user.

### 6. Code Explanation
The project uses Python and Streamlit for building the application. The main code is in `main.py`, which:
- Reads data from AWS Athena.
- Generates dynamic graphs based on user queries.
- Displays the results using Streamlit.

### 7. Streamlit Application
- The Streamlit app provides an interactive interface for querying and visualizing the data.
- Refer to the screenshots [14.png](screenshots/14.png), [15.png](screenshots/15.png), [16.png](screenshots/16.png), and [17.png](screenshots/17.png) to see the app in action.

### 8. Running the Project
- Complete all the setup steps mentioned above.
- Add your AWS credentials to `.streamlit/secrets.toml` as follows:
  ```toml
  [aws]
  aws_access_key_id = "your_access_key_id"
  aws_secret_access_key = "your_secret_access_key"