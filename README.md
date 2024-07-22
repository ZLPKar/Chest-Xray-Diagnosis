# Chest-Xray-Diagnosis
Chest X-ray Diagnosis Software is a GUI-based application designed to assist healthcare professionals in diagnosing pneumonia and COVID-19 from chest X-ray images. The software leverages advanced machine learning models to provide a quick analysis of X-ray images, categorizing them into Normal, Bacterial Pneumonia, Viral Pneumonia, or COVID-19 related anomalies.

## Features

- **X-ray Image Upload**: Users can upload chest X-ray images for analysis.
- **Automated Diagnosis**: Utilizes 2 pre-trained deep learning models to diagnose potential medical conditions from X-ray images.
- **Patient Data Management**: Supports entering patient details and viewing diagnostic history with search and filter capabilities.

## Installation

To set up Chest X-ray Diagnosis Software on your local machine, follow these steps:

### Prerequisites

- Python 3.8 or above
- pip3

### Setup

1. **Clone the repository**

   ```bash
   git clone https://campus.cs.le.ac.uk/gitlab/zjp1/final-year-project.git
   cd chest-diagnosis-software

2. **Create and activate a virtual environment (optional but recommended):**
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


3. **Install the required packages:**

pip install -r requirements.txt


## Running the Application
Run the application using the following command:
python main.py

as of 07/05/2024 exe still not working


## Usage
After launching the software, you will be greeted with a login screen. Use the following credentials for initial access:

Username: admin
Password: admin
This will allow you to register new users. Once logged in, you can:

Upload X-ray images for diagnosis.
View and filter diagnosed patient records.



## Contributing
Contributions to Chest X-ray Diagnosis Software are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit (git commit -am 'Add some feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.



### Notes
- **Repository URL**:https://campus.cs.le.ac.uk/gitlab/zjp1/final-year-project.git
- **Contact Information**: zjp1@student.le.ac.uk
- **Detailed Instructions**

This README is structured to provide a clear and professional overview of your software, making it accessible for new users and potential contributors.



## License
This project is licensed under the MIT License - see the LICENSE file for details.
