
<p align="center">
  <img src="cybersecurity_data_generator2.png" 
       alt="Centered Image" 
       style="width: 600px; height: auto;">
</p>
🔗 Live Dashboard:
<a 
  href="https://colab.research.google.com/github/atsuvovor/Cybersecurity-Data-Generator/blob/main/CyberInsightDataGenerator.ipynb" 
  target="_parent"
>
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>


## Overview

This project provides a Python script designed to generate synthetic cybersecurity issue data. The goal is to create a realistic dataset that simulates both normal and anomalous cybersecurity events, which can be used for various purposes such as:

*   **Training anomaly detection models:** The generated data includes labeled normal and anomalous samples.
*   **Testing security information and event management (SIEM) systems:** The dataset mimics real-world security logs and incidents.
*   **Developing and validating security analytics:** The diverse set of features allows for exploring various security metrics and indicators.
*   **Demonstrating cybersecurity concepts:** The dataset can be used for educational purposes to illustrate different types of attacks and their characteristics.

The script generates data with a variety of attributes, including issue details, user activity, system metrics, and threat indicators. It also incorporates a simple adaptive defense mechanism based on the calculated threat level and severity.

## Script Structure and Functionality

The script is organized into several classes, each responsible for a specific part of the data generation and processing pipeline:

*   **`DataConfig`**: This class holds all the configuration parameters and constants used throughout the script. This includes the number of normal and anomalous issues, user and department counts, date ranges, file paths for saving data to Google Drive, lists of possible categories, severities, statuses, reporters, assignees, users, departments, locations, and column names. It also stores pre-defined DataFrames for Key Threat Indicators (KTIs) and Scenarios with Colors.

*   **`DataGenerator`**: This class is responsible for generating the synthetic data for both normal and anomalous issues.
    *   It includes methods to map issue categories to synthetic normal and anomalous issue names (`generate_normal_issues_name`, `generate_anomalous_issue_name`).
    *   It filters categories into KPIs and KRIs (`filter_kpi_and_kri`).
    *   It generates random dates within a specified range (`random_date`).
    *   A key function is `calculate_threat_level`, which computes a threat score and assigns a threat level based on several input features.
    *   The `adaptive_defense_mechanism` function determines suggested defense actions based on threat level, severity, and activity context.
    *   The core data generation logic resides in `generate_normal_issues_df` and `generate_anomalous_issues_df`, which create pandas DataFrames for each type of issue. These functions include enhanced logic to simulate more realistic data distributions and dependencies between features, as well as temporal patterns and nuanced anomalous behaviors.
    *   The `data_generation_pipeline` orchestrates the generation of both normal and anomalous data and combines them into a single DataFrame, adding an "Is Anomaly" label.

*   **`DataProcessor`**: This class handles data processing tasks.
    *   The `map_threat_severity_to_color` method adds a "Color" column to the DataFrame based on the threat level and severity, providing a visual indicator of the issue's risk.

*   **`DataSaver`**: This class is responsible for saving the generated DataFrames.
    *   The `save_dataframe_to_google_drive` method saves a single DataFrame to a specified path in Google Drive as a CSV file. It also includes error handling to ensure the directory exists.
    *   The `save_the_data_to_CSV_to_google_drive` method calls the single-save method for all the generated DataFrames.

*   **`DataDisplay`**: This class provides functionality to display information about the generated DataFrames.
    *   The `display_the_data_frames` method uses `display()` to show the head, info, and describe outputs for each generated DataFrame, allowing for a quick overview of the data structure and statistics.

## How to Use the Script

1.  **Run the Code Cell:** Execute the Python code cell containing the script.
2.  **Data Generation and Saving:** The script will automatically:
    *   Clone the projet repository from GitHub to Colab environment /content/
    *  Run the exec file cyberdatagen.py
    *   Initialize the configuration.
    *   Generate the normal and anomalous datasets.
    *   Combine the datasets.
    *   Apply the color mapping based on threat level and severity.
    *   Display the head, info, and describe outputs for the generated dataframes in the Colab output.  
    *   Prompt the user to download the generated dataframes (normal, anomalous, combined, KTIs, and scenarios with colors) as CSV files   

3.  **Access the Data:** The generated CSV files will be available locally in the user download folder   

## Customization

We can customize the data generation process by modifying the parameters in the `DataConfig` class. This includes:

*   Changing the number of normal and anomalous issues.
*   Adjusting the number of unique users, reporters, and assignees.
*   Modifying the date ranges for data generation.
*   Updating the lists of categories, severities, statuses, etc.
*   Adjusting the parameters within the `DataGenerator` class methods to fine-tune the distributions and relationships between features for both normal and anomalous data.

## Future Enhancements

Potential future enhancements for this project include:

*   Implementing more sophisticated anomaly generation techniques to simulate a wider variety of attack types and patterns.
*   Adding more complex dependencies and interactions between features to increase the realism of the dataset.
*   Incorporating network traffic data, log file entries, and other types of security-related information.
*   Developing a user interface or command-line tool for easier configuration and execution of the data generator.
*   Exploring different data formats for saving the generated data (e.g., Parquet, JSON).

```python
!git clone https://github.com/atsuvovor/Cybersecurity-Data-Generator.git
%run /content/Cybersecurity-Data-Generator/cyberdatagen.py
```
