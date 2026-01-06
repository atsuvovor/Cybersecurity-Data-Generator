
<p align="center">
  <img src="https://github.com/atsuvovor/Cybersecurity-Data-Generator/blob/main/cybersecurity_data_generator2.png" 
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



**Core Data Schema**:
   Each column will be structured to simulate real-world attributes.  

  
   - `Issue ID`, `Issue Key`: Unique identifiers.
   - `Issue Name`, `Category`, `Severity`: Descriptive issue metadata with categorical values.
   - `Status`, `Reporters`, `Assignees`: Status categories and personnel involved.
   - `Date Reported`, `Date Resolved`: Randomized dates across a timeline.
   - `Impact Score`, `Risk Level`: Randomized scores to reflect varying severity.
   - `Cost`: Randomized to reflect the volatility in month-over-month impact.  

**User Activity Columns**:
   Columns like `user_id`, `timestamp`, `activity_type`, `location`, `session_duration`, and `data_transfer_MB` will be generated to simulate behavioral patterns.

**Monthly Volatility**:  
  - **Impact Score**, **Cost**, and **data_transfer_MB** We use synthetic techniques to create spikes or drops in activity between months, simulating the volatility in issues or user activity.
  - For example, we use random walks to vary values in a non-linear fashion to capture realistic volatility.

**Data Augmentation**:
   - **Scaling Up Data Points**: We will use SMOTE or random sampling for categorical columns to add diversity.
   - **Label Swapping for `Assignees`, `Departments`**: Here, we randomly reassign categories periodically to simulate changing roles.
   - **Time-Series Variability**: We use simulated timestamps within and across sessions to show login attempts, data transfer spikes, and session durations.

**User activity features:**  

  - user_id: Identifier for each user.  
  - timestamp: Time of the activity.  
  - activity_type: Type of activity (e.g., "login," "file_access," "data_modification").  
  - location: User's location (e.g., IP region).  
  - session_duration: Length of session in seconds.  
  - num_files_accessed: Number of files accessed in a session.  
  - ogin_attempts: Number of login attempts in a session.  
  - data_transfer_MB: Amount of data transferred (MB).  

**Anomalies:**  

  - We include some rows with anomalous patterns like high login attempts, unusual session duration and high data transfer volumes from unexpected locations

**Explanation of Key Parts:**
- **Volatile Data Generation**: The `generate_volatile_data` function adds random fluctuations to values, simulating high month-over-month volatility.
- **User Activity Features**: Columns like `activity_type`, `session_duration`, `num_files_accessed`, `login_attempts`, and `data_transfer_MB` are varied to reflect real user behaviors.
- **Random Timestamps**: Activity timestamps are spread across the timeline from `start_date` to `end_date`.

- **Generate normal issues dataset**: First, we a normal issue dataset with almost no data anomaly
- **Generate anomalous issues dataset**: The we introduce anomaly to the detaset
- **Combine normal and anomalous data**: We combine both normal and anomalous datasets  
- **Adressing class imbalance in datasets**:Using SMOTE (Synthetic Minority Over-sampling Technique) we make sure that class imbalance in the dataset is resolved.  
all the data files are saves on google drive  

  
**User Activities Generation Metrics Formula**  

The expression:  base_value + base_value * volatility * (np.random.randn()) * (1.2 if severity in ['High', 'Critical'] else 1)

means that we’re generating a value based on a starting point (base_value) and adjusting it for both randomness and severity level. Here's a breakdown:

- **base_value**: This is the initial value that the output is based on.
- **volatility * (np.random.randn())**: This part adds a random fluctuation around the base_value. `np.random.randn()` generates a value from a standard normal distribution (centered around 0), so it could be positive or negative, creating variation. Multiplying by volatility scales the randomness, making the fluctuation stronger or weaker.
- **(1.2 if severity in ['High', 'Critical'] else 1)**: This adds an additional factor to increase the outcome by 20% if the severity is "High" or "Critical." If severity isn’t in these categories, the factor is simply 1, meaning no extra adjustment.

So, if severity is "High" or "Critical," the result is a base value adjusted for both volatility and severity; otherwise, it’s just the base value with volatility adjustment.  


**Treat level Identification and Adaptive Defense Systems Setting**

We will set up a threat level based our cybersecurity dataset generated. We will create a threat scoring model that combines multiple relevant features.  

**Key Threat Indicators (KTIs) Definition**  

The following columns will be uses as key threat indicators (KTIs):  

   - **Severity**: Indicates the criticality of the issue.
   - **Impact Score**: Represents the potential damage if the threat is realized.
   - **Risk Level**: A general indicator of risk associated with each issue.
   - **Issue Response Time Days**: The longer it takes to respond, the higher the threat level could be.
   - **Category**: Certain categories (e.g., unauthorized access) carry a higher base threat level.
   - **Activity Type**: Suspicious activity types (e.g., high login attempts, data modification) indicate a greater threat.
   - **Login Attempts**: Unusually high login attempts signal a brute force attack.
   - **Num Files Accessed** and **Data Transfer MB**: Large data transfers or access to many files in a session could indicate data exfiltration or suspicious activity.

**KTIs based Scoring**
  
For each KTI we will define the acriteria to be used to assigne a score  

| KTI               | Condition                                      | Score   |
|-------------------|------------------------------------------------|---------|
| Severity          | Critical = 10, High = 8, Medium = 5, Low = 2   | 2 - 10  |
| Impact Score      | 1 to 10 (already a score)                      | 1 - 10  |
| Risk Level        | High = 8, Medium = 5, Low = 2                  | 2 - 8   |
| Response Time     | >7 days = 5, 3-7 days = 3, <3 days = 1         | 1 - 5   |
| Category          | Unauthorized Access = 8, Phishing = 6, etc.    | 1 - 8   |
| Activity Type     | High-risk types (e.g., login, data_transfer)   | 1 - 5   |
| Login Attempts    | >5 = 5, 3-5 = 3, <3 = 1                        | 1 - 5   |
| Num Files Accessed| >10 = 5, 5-10 = 3, <5 = 1                      | 1 - 5   |
| Data Transfer MB  | >100 MB = 5, 50-100 MB = 3, <50 MB = 1         | 1 - 5   |  

  


**Threat Score Calculation**
The threat level is calculated as a weighted sum of these scores. For example:

*Threat Score = 0.3 × Severity + 0.2 × Impact Score + 0.2 × Risk Level + 0.1 × Response Time + 0.1 × Login Attempts + 0.05 × Num Files Accessed + 0.05 × Data Transfer MB*

Note: The weights could be adjusted based on the importance of each factor in your specific cybersecurity context.

**Threat Level Thresholds Definition**  

We use the final threat score to categorize the threat level:
   - **Low Threat**: 0–3
   - **Medium Threat**: 4–6
   - **High Threat**: 7–9
   - **Critical Threat**: 10+

**Real-Time Calculation and Monitoring Implementation**
To implement this dynamically we :
   - Calculate and log the threat score whenever new data is added.
   - Set up alerts for high and critical threat scores.
   - Integrate this scoring model into a real-time dashboard or cybersecurity scorecard.

This method provides a structured and quantifiable approach to assessing the threat level based on multiple relevant indicators from the initial dataset.  

**Rule-based Adaptive Defense Mechanism**  

Here we will add logic that monitors specific threat conditions in real-time and adapt responses based on defined rules. This will include automatic flagging of high-threat issues, increasing logging frequency for suspicious activities, and assigning specific mitigation actions based on the threat level and activity context.

**Rules Definition**  
 We will use the following features to define rules that will be applied to identify potential threats and recommend defensive actions: `Threat Level`, `Severity`, `Impact Score`, `Login Attempts`, `Risk Level`, `Issue Response Time Days`, `Num Files Accessed`,`Data Transfer MB`.   

**Defense Mechanism**: The system will respond adaptively by adding flags and assigning custom actions based on the rule evaluations and scenarios colors

   
 The defense mechanism assigns an adaptive `Defense Action` to each issue based on threat conditions, adding an extra layer of automated response for varying threat levels and behaviors.
 The treat conditions are implemented by Color-coding cybersecurity scenarios, we bealieve, is a helpful way to quickly communicate risk levels and prioritize response actions. Here's a suggested approach to buld the scenarios, where we use **intensity of red, orange, yellow, and green** to represent risk:

**Color Scheme**
- **Critical Threat & Severity**: **Dark Red** – Highest urgency.
- **High Threat or Severity**: **Orange** – Serious, but not the highest urgency.
- **Medium Threat or Severity**: **Yellow** – Moderate concern.
- **Low Threat & Severity**: **Green** – Low concern, monitor as needed.

Here is the table **with colored emoji icons added** beside each color name in **Suggested Color**.
These icons render correctly in GitHub, Markdown, Slack, Teams, Notion, and Streamlit.  






## **Scenarios with Colors**

| **Scenario** | **Threat Level** | **Severity** | **Suggested Color**  | **Rationale**                                                                         |
| ------------ | ---------------- | ------------ | -------------------- | ------------------------------------------------------------------------------------- |
| **1**        | Critical         | Critical     | 🔴 **Dark Red**      | Maximum urgency, both threat and impact are critical. Immediate action required.      |
| **2**        | Critical         | High         | 🟥 **Red**           | Very high risk, threat is critical and impact is significant. Prioritize response.    |
| **3**        | Critical         | Medium       | 🟧 **Orange-Red**    | Significant threat but moderate impact. Act promptly to prevent escalation.           |
| **4**        | Critical         | Low          | 🟧 **Orange**        | High potential risk, current impact is minimal. Monitor closely and mitigate quickly. |
| **5**        | High             | Critical     | 🟥 **Red**           | High threat combined with critical impact. Needs immediate action.                    |
| **6**        | High             | High         | 🟧 **Orange-Red**    | High threat and significant impact. Prioritize response.                              |
| **7**        | High             | Medium       | 🟧 **Orange**        | Elevated threat and moderate impact. Requires attention.                              |
| **8**        | High             | Low          | 🟨 **Yellow-Orange** | High threat with low impact. Proactive monitoring recommended.                        |
| **9**        | Medium           | Critical     | 🟧 **Orange**        | Moderate threat with critical impact. Prioritize addressing the severity.             |
| **10**       | Medium           | High         | 🟨 **Yellow-Orange** | Medium threat with high impact. Needs resolution soon.                                |
| **11**       | Medium           | Medium       | 🟨 **Yellow**        | Medium threat and impact. Plan to address it.                                         |
| **12**       | Medium           | Low          | 🟨 **Light Yellow**  | Moderate threat, minimal impact. Monitor as needed.                                   |
| **13**       | Low              | Critical     | 🟨 **Yellow**        | Low threat but high impact. Address severity first.                                   |
| **14**       | Low              | High         | 🟨 **Light Yellow**  | Low threat with significant impact. Plan mitigation.                                  |
| **15**       | Low              | Medium       | 💛 **Green-Yellow**  | Low threat, moderate impact. Routine monitoring.                                      |
| **16**       | Low              | Low          | 🟩 **Green**         | Minimal risk. No immediate action required.                                           |  





This color based scenarios approach aligns urgency with the dual factors of **threat level** and **severity**, ensuring quick comprehension and appropriate prioritization.  



#### **2. Explanatory Data Analysis(EDA)**

The following steps were implemented in the exploratory data analysis (EDA) pipeline to analyze the dataset's key features and distribution patterns:

**Data Normalization:**
   - Implemented a function to normalize numerical features using Min-Max Scaling for consistent feature scaling.

**Time-Series Visualization:**
   - Plotted daily distribution of numerical features pre- and post-normalization using line plots for visualizing trends over time.

**Statistical Feature Analysis:**
   - Developed histograms and boxplots for all features, including overlays of statistical metrics (mean, standard deviation, skewness, kurtosis) for numerical features.
   - Integrated risk levels with customized color palettes for categorical data.

**Scatter Plot and Correlation Analysis:**
   - Created scatter plots to analyze relationships between key features such as session duration, login attempts, data transfer, and user location.
   - Generated a correlation heatmap to visualize interdependencies among numerical features.

**Distribution Analysis Pipeline:**
   - Built a modular pipeline to evaluate and compare the distribution of activity features across daily and aggregated reporting frequencies (e.g., monthly, quarterly).

**Comprehensive Feature Analysis:**
   - Combined scatter plots, heatmaps, and distribution visualizations into a unified framework for insights into user behavior and feature relationships.

**Dynamic Layouts and Annotations:**
   - Optimized subplot layouts to handle a variable number of features and annotated plots with key statistics for enhanced interpretability.

This pipeline provides a detailed understanding of numerical and categorical feature behaviors while highlighting correlations and potential anomalies in the dataset.

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
    *   Display Plottings  
        1. Descriptive Statistics
           Computes summary statistics (.describe()).
           Detects categorical vs numerical features.
           Highlights distributions, outliers, and correlations.  
        📌 The core of classical EDA, enabling users to spot anomalies and trends.

        2. Visualization
            Plots histograms, correlation heatmaps, and categorical distributions.
            Supports matplotlib and seaborn for visual clarity.  
        📌 Visual EDA complements numerical summaries by revealing hidden structures.
       
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

---

## 🤝 Connect With Me
I am always open to collaboration and discussion about new projects or technical roles.

Atsu Vovor  
Consultant, Data & Analytics    
Ph: 416-795-8246 | ✉️ atsu.vovor@bell.net    
🔗 <a href="https://www.linkedin.com/in/atsu-vovor-mmai-9188326/" target="_blank">LinkedIn</a> | <a href="https://atsuvovor.github.io/projects_portfolio.github.io/" target="_blank">GitHub</a> | <a href="https://public.tableau.com/app/profile/atsu.vovor8645/vizzes" target="_blank">Tableau Portfolio</a>    
📍 Mississauga ON      

### Thank you for visiting!🙏
