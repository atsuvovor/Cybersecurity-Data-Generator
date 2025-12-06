# -*- coding: utf-8 -*-
"""
CyberDataGen
Anomalous Behavior Detection in Cybersecurity Analytics using Generative AI
-------------------------------------------------------------------------------
Portable version:
- Works in Colab, JupyterLab, or local Python
- Saves to CyberThreat_Insight/cybersecurity_data/
- Displays datasets (optional)
- Saves 5 CSVs + prints summary
- Prompts user for optional local ZIP download
Author: Atsu Vovor
"""

import os
import shutil
import zipfile
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from IPython.display import display
import argparse
import random
import warnings
warnings.filterwarnings("ignore")
# Try to import Colab-specific files.download (ignored if not available)
try:
    from google.colab import files
    COLAB = True
except ImportError:
    COLAB = False


# =====================================================================
# Configuration
# =====================================================================
class DataConfig:
    def __init__(self):
        # ------------------ Parameters ------------------
        self.num_normal_issues = 800
        self.num_anomalous_issues = 200
        self.total_issues = self.num_normal_issues + self.num_anomalous_issues
        self.num_users = 100
        self.num_reporters = 10
        self.num_assignees = 20
        self.num_departments = 5
        self.current_date = datetime.now()
        self.start_date = datetime(2023, 1, 1)
        self.end_date = datetime(self.current_date.year, self.current_date.month, self.current_date.day)

        # ------------------ Paths ------------------
        self.github_repo_folder = "/content/CyberThreat_Insight/cybersecurity_data"
        os.makedirs(self.github_repo_folder, exist_ok=True)

        self.normal_data_file = os.path.join(self.github_repo_folder, "cybersecurity_dataset_normal.csv")
        self.anomalous_data_file = os.path.join(self.github_repo_folder, "cybersecurity_dataset_anomalous.csv")
        self.combined_data_file = os.path.join(self.github_repo_folder, "cybersecurity_dataset_combined.csv")
        self.key_threat_indicators_file = os.path.join(self.github_repo_folder, "key_threat_indicators.csv")
        self.scenarios_with_colors_file = os.path.join(self.github_repo_folder, "scenarios_with_colors.csv")
        self.zip_file = os.path.join(self.github_repo_folder, "cybersecurity_data.zip")

        # ------------------ Metadata ------------------
        self.issue_ids = [f"ISSUE-{i:04d}" for i in range(1, self.num_normal_issues + 1)]
        self.issue_keys = [f"KEY-{i:04d}" for i in range(1, self.num_normal_issues + 1)]

        self.KPI_list = [
            "Network Security","Access Control","System Vulnerability",
            "Penetration Testing Effectiveness","Management Oversight",
            "Procurement Security", "Control Effectiveness",
            "Asset Inventory Accuracy", "Vulnerability Remediation",
            "Risk Management Maturity", "Risk Assessment Coverage"
        ]
        self.KRI_list = [
            "Data Breach", "Phishing Attack","Malware","Data Leak",
            "Legal Compliance","Risk Exposure", "Cloud Security Posture",
            "Unauthorized Access", "DDOS"
        ]
        self.categories = self.KPI_list + self.KRI_list
        self.severities = ["Low", "Medium", "High", "Critical"]
        self.statuses = ["Open", "In Progress", "Resolved","Closed"]
        self.reporters = [f"Reporter {i}" for i in range(1, self.num_reporters + 1)]
        self.assignees = [f"Assignee {i}" for i in range(1, self.num_assignees + 1)]
        self.users = [f"User_{i}" for i in range(1, self.num_users + 1)]
        self.departments = ["IT", "Finance", "Operations", "HR", "Legal",
                            "Sales", "C-Suite Executives", "External Contractors"]
        self.locations = ["CANADA", "USA", "Unknown", "EU", "DE", "FR", "JP", "CN", "AU", "IN", "UK"]

        self.columns = [
            "Issue ID", "Issue Key", "Issue Name", "Issue Volume", "Category",
            "Severity", "Status", "Reporters", "Assignees", "Date Reported",
            "Date Resolved", "Issue Response Time Days", "Impact Score", "Risk Level",
            "Department Affected", "Remediation Steps", "Cost", "KPI/KRI", "User ID",
            "Timestamps", "Activity Type","User Location", "IP Location",
            "Session Duration in Second", "Num Files Accessed", "Login Attempts",
            "Data Transfer MB", "CPU Usage %", "Memory Usage MB", "Threat Score",
            "Threat Level", "Defense Action"
        ]

        # ------------------ Extra DataFrames ------------------
        self.ktis_data = {
            "KIT": [
                "Severity", "Impact Score", "Risk Level", "Response Time", "Category",
                "Activity Type", "Login Attempts", "Num Files Accessed", "Data Transfer MB",
                "CPU Usage %", "Memory Usage MB"
            ],
            "Condition": [
                "Critical = 10, High = 8, Medium = 5, Low = 2",
                "1 to 10 (already a score)",
                "High = 8, Medium = 5, Low = 2",
                ">7 days = 5, 3-7 days = 3, <3 days = 1",
                "Unauthorized Access = 8, Phishing = 6, etc.",
                "High-risk types (e.g., login, data_transfer)",
                ">5 = 5, 3-5 = 3, <3 = 1",
                ">10 = 5, 5-10 = 3, <5 = 1",
                ">100 MB = 5, 50-100 MB = 3, <50 MB = 1",
                ">80% = 5, 60-80% = 3, <60% = 1",
                ">8000 MB = 5, 4000-8000 MB = 3, <4000 MB = 1"
            ],
            "Score": [
                "2 - 10", "1 - 10", "2 - 8", "1 - 5", "1 - 8", "1 - 5", "1 - 5", "1 - 5", "1 - 5", "1 - 5", "1 - 5"
            ]
        }
        self.ktis_key_threat_indicators_df = pd.DataFrame(self.ktis_data)

        self.scenario_data = {
            "Scenario": list(range(1, 17)),
            "Threat Level": [
                "Critical", "Critical", "Critical", "Critical",
                "High", "High", "High", "High",
                "Medium", "Medium", "Medium", "Medium",
                "Low", "Low", "Low", "Low"
            ],
            "Severity": [
                "Critical", "High", "Medium", "Low",
                "Critical", "High", "Medium", "Low",
                "Critical", "High", "Medium", "Low",
                "Critical", "High", "Medium", "Low"
            ],
            "Suggested Color": [
                "Dark Red", "Red", "Orange-Red", "Orange",
                "Red", "Orange-Red", "Orange", "Yellow-Orange",
                "Orange", "Yellow-Orange", "Yellow", "Light Yellow",
                "Yellow", "Light Yellow", "Green-Yellow", "Green"
            ]
        }
        self.scenarios_with_colors_df = pd.DataFrame(self.scenario_data)

        #---------------------------------------------Define columns---------------------------------------------------
        self.numerical_columns = [
            "Timestamps", "Issue Response Time Days", "Impact Score", "Cost",
            "Session Duration in Second", "Num Files Accessed", "Login Attempts",
            "Data Transfer MB", "CPU Usage %", "Memory Usage MB", "Threat Score"
            ]


        self.explanatory_data_analysis_columns = [
            "Date Reported", "Issue Response Time Days", "Impact Score", "Cost",
            "Session Duration in Second", "Num Files Accessed", "Login Attempts",
            "Data Transfer MB", "CPU Usage %", "Memory Usage MB", "Threat Score"
            ]

        self.user_activity_features = [
            "Risk Level", "Issue Response Time Days", "Impact Score", "Cost",
            "Session Duration in Second", "Num Files Accessed", "Login Attempts",
            "Data Transfer MB", "CPU Usage %", "Memory Usage MB", "Threat Score"
            ]


        self.initial_dates_columns = ["Date Reported", "Date Resolved", "Timestamps"]

        self.categorical_columns = ["Issue ID", "Issue Key", "Issue Name", "Category", "Severity", "Status", "Reporters",
                               "Assignees", "Risk Level", "Department Affected", "Remediation Steps", "KPI/KRI",
                               "User ID", "Activity Type", "User Location", "IP Location", "Threat Level",      "Defense Action", "Color"
                               ]
        self.features_engineering_columns = [
            "Issue Response Time Days", "Impact Score", "Cost",
            "Session Duration in Second", "Num Files Accessed", "Login Attempts",
            "Data Transfer MB", "CPU Usage %", "Memory Usage MB", "Threat Score", "Threat Level"
            ]
        self.numerical_behavioral_features = [
            "Login Attempts", "Data Transfer MB", "CPU Usage %", "Memory Usage MB",
            "Session Duration in Second", "Num Files Accessed", "Threat Score"
            ]

        #IP addresses, port numbers, packet sizes, and time intervals
        # ---------------------Generate user activity metadata------------------------
        self.activity_types = ["login", "file_access", "data_modification"]

    def get_column_dic(self):
        """
        Returns a dictionary containing lists of column names categorized by type.
        """
        columns_dic = {
            "numerical_columns": self.numerical_columns,
            "explanatory_data_analysis_columns": self.explanatory_data_analysis_columns,
            "user_activity_features": self.user_activity_features,
            "initial_dates_columns": self.initial_dates_columns,
            "categorical_columns": self.categorical_columns,
            "features_engineering_columns": self.features_engineering_columns
        }
        return columns_dic

# =====================================================================
# Data Generator (keep your original generation logic here)
# =====================================================================
class DataGenerator:
    def __init__(self, config):
        self.config = config
        self.user_profiles = {user: {'baseline_activity': random.uniform(0.5, 1.5),
                                     'risk_tolerance': random.uniform(0.8, 1.2)} for user in self.config.users}
        self.department_profiles = {dept: {'baseline_risk': random.uniform(0.5, 1.5),
                                         'activity_multiplier': random.uniform(0.8, 1.2)} for dept in self.config.departments}
        self.anomalous_issue_ids = [f"ISSUE-{i:04d}" for i in range(self.config.num_normal_issues +1, self.config.total_issues + 1)]
        self.anomalous_issue_keys = [f"KEY-{i:04d}" for i in range(self.config.num_normal_issues +1, self.config.total_issues + 1)]
    

    #                   -----------------------------------------------------------------------
    #                      Generate normal issue names for each KPI and KRI by Mapping
    #                      normal issue name to issue category using a dictionary
    #                   ---------------------------------------------------------------------
    def generate_normal_issues_name(self, category):# Mapping issue name to issue category using a dictionary
        """
        Maps a category to a synthetic normal issue name.

        Args:
            category (str): The category of the issue.

        Returns:
            str: The corresponding normal issue name, or "Unknown Issue" if not found.
        """
        issue_mapping = {
            "Network Security": "Inadequate Firewall Configurations",
            "Access Control": "Weak Authentication Protocols",
            "System Vulnerability": "Outdated Operating System Components",
            "Penetration Testing Effectiveness": "Unresolved Vulnerabilities from Latest Penetration Test",
            "Management Oversight": "Inconsistent Review of Security Policies",
            "Procurement Security": "Supplier Security Compliance Gaps",
            "Control Effectiveness": "Insufficient Access Control Measures",
            "Asset Inventory Accuracy": "Missing or Inaccurate Asset Records",
            "Vulnerability Remediation": "Delayed Patching of Known Vulnerabilities",
            "Risk Management Maturity": "Incomplete Risk Management Framework",
            "Risk Assessment Coverage": "Insufficient Coverage in Annual Risk Assessment",
            "Data Breach": "Unauthorized Access Leading to Data Exposure",
            "Phishing Attack": "Successful Phishing Attempt Targeting Executives",
            "Malware": "Detected Malware Infiltration in Internal Systems",
            "Data Leak": "Sensitive Data Leak via Misconfigured Cloud Storage",
            "Legal Compliance": "Non-Compliance with Data Protection Regulations",
            "Risk Exposure": "Increased Exposure due to Insufficient Data Encryption",
            "Cloud Security Posture": "Weak Cloud Storage Access Controls",
            "Unauthorized Access": "Access by Unauthorized Personnel Detected",
            "DDOS": "High-Volume Distributed Denial-of-Service Attack"
        }

        return issue_mapping.get(category, "Unknown Issue")


    #                                 -------------------------------------------------------------------
    #                                   Generate anomalous issue names for each KPI and KRI by Mapping
    #                                   anomalous issue name to issue category using a dictionary
    #                                  ------------------------------------------------------------------
    def generate_anomalous_issue_name(self, category):
        """
        Maps a category to a synthetic anomalous issue name.

        Args:
            category (str): The category of the issue.

        Returns:
            str: The corresponding anomalous issue name, or "Unknown Issue" if not found.
        """

        anomalous_issue_mapping = {
            "Network Security": "Sudden Increase in Unfiltered Traffic",
            "Access Control": "Multiple Unauthorized Access Attempts Detected",
            "System Vulnerability": "Newly Discovered Vulnerabilities in Core Systems",
            "Penetration Testing Effectiveness": "Critical Issues Not Detected in Last Penetration Test",
            "Management Oversight": "High Frequency of Policy Violations",
            "Procurement Security": "Supplier Network Breach Exposure",
            "Control Effectiveness": "Ineffective Access Controls in High-Sensitivity Areas",
            "Asset Inventory Accuracy": "Significant Number of Untracked Devices",
            "Vulnerability Remediation": "Delayed Patching of Critical Vulnerabilities",
            "Risk Management Maturity": "Lack of Updated Risk Management Procedures",
            "Risk Assessment Coverage": "Unassessed High-Risk Areas",
            "Data Breach": "Unusual Data Transfer Volumes Detected",
            "Phishing Attack": "Targeted Phishing Campaign Against Executives",
            "Malware": "Malware Detected in Core System Components",
            "Data Leak": "Unusual Data Access from External Locations",
            "Legal Compliance": "Potential Non-Compliance Detected in Sensitive Data Handling",
            "Risk Exposure": "Unanticipated Increase in Risk Exposure",
            "Cloud Security Posture": "Weak Access Controls on Critical Cloud Resources",
            "Unauthorized Access": "Spike in Unauthorized Access Attempts",
            "DDOS": "High-Volume Distributed Denial-of-Service Attack from Multiple Sources"
        }

        return anomalous_issue_mapping.get(category, "Unknown Issue")


    #-------------------------Implementation-----------------------------------
    # filter KPI Vs KRI
    def filter_kpi_and_kri(self, category):
        """
        Categorizes an issue as either a Key Performance Indicator (KPI) or a Key Risk Indicator (KRI).

        Args:
            category (str): The category of the issue.

        Returns:
            str: 'KPI' if the category is in the KPI list, otherwise 'KRI'.
        """
        if category in self.config.KPI_list:
            return 'KPI'
        else:
            return 'KRI'
#
    # Function to generate a random start date within a specific date range--
    def random_date(self, start, end):
        """
        Generates a random datetime object within a specified date range.

        Args:
            start (datetime): The start date of the range.
            end (datetime): The end date of the range.

        Returns:
            datetime: A random datetime object within the specified range.
        """
        # Calculate the difference in days and add a random number of days to the start date
        return start + timedelta(days=np.random.randint(0, (end - start).days))

    # ----------------------------------Define threat level calculation-----------------------------------------------------
    def calculate_threat_level(self, severity, impact_score, risk_level, response_time_days,
                               login_attempts, num_files_accessed, data_transfer_MB,
                               cpu_usage_percent, memory_usage_MB):
        """
        Calculates a threat score and assigns a threat level based on various issue attributes.

        Args:
            severity (str): The severity of the issue ('Low', 'Medium', 'High', 'Critical').
            impact_score (int or float): The impact score of the issue (1-10).
            risk_level (str): The risk level of the issue ('Low', 'Medium', 'High', 'Critical').
            response_time_days (int): The response time in days for the issue.
            login_attempts (int): The number of login attempts.
            num_files_accessed (int): The number of files accessed.
            data_transfer_MB (int or float): The amount of data transferred in MB.
            cpu_usage_percent (int or float): The CPU usage percentage.
            memory_usage_MB (int or float): The memory usage in MB.

        Returns:
            tuple: A tuple containing the calculated threat level (str) and threat score (float).
        """
        # Define scores based on input criteria
        severity_score = {"Critical": 10, "High": 8, "Medium": 5, "Low": 2}.get(severity, 1)
        risk_score = {"Critical": 10, "High": 8, "Medium": 5, "Low": 2}.get(risk_level, 1)

        response_time_score = 5 if response_time_days > 7 else 3 if response_time_days > 3 else 1
        login_attempts_score = 5 if login_attempts > 5 else 3 if login_attempts > 3 else 1
        files_accessed_score = 5 if num_files_accessed > 10 else 3 if num_files_accessed > 5 else 1
        data_transfer_score = 5 if data_transfer_MB > 100 else 3 if data_transfer_MB > 50 else 1

        # New metrics: CPU usage and memory usage
        cpu_usage_score = 5 if cpu_usage_percent > 85 else 3 if cpu_usage_percent > 60 else 1
        memory_usage_score = 5 if memory_usage_MB > 10000 else 3 if memory_usage_MB > 6000 else 1

        # Aggregate the scores
        threat_score = (
            0.25 * severity_score +
            0.2 * impact_score +
            0.15 * risk_score +
            0.1 * response_time_score +
            0.05 * login_attempts_score +
            0.05 * files_accessed_score +
            0.05 * data_transfer_score +
            0.075 * cpu_usage_score +
            0.075 * memory_usage_score
        )

        # Determine threat level based on the calculated score
        if threat_score >= 9:
            return "Critical", threat_score
        elif threat_score >= 7:
            return "High", threat_score
        elif threat_score >= 4:
            return "Medium", threat_score
        else:
            return "Low", threat_score
    
        #--------------------- Adaptive defense mechanism based on threat level and conditions----------------------------------

    def adaptive_defense_mechanism(self, row):
        """
        Determines the adaptive response based on threat level, severity, and activity context.

        Args:
            row (pd.Series): A row from the DataFrame representing a single issue.

        Returns:
            str: The suggested defense action(s).
        """
        action = "Monitor"

        # Map the threat level and severity to actions based on scenarios
        threat_severity_actions = {
            ("Critical", "Critical"): "Immediate System-wide Shutdown & Investigation",
            ("Critical", "High"): "Escalate to Security Operations Center (SOC) & Block User",
            ("Critical", "Medium"): "Isolate Affected System & Restrict User Access",
            ("Critical", "Low"): "Increase Monitoring & Schedule Review",
            ("High", "Critical"): "Escalate to SOC & Restrict Critical System Access",
            ("High", "High"): "Restrict User Activity & Monitor Logs",
            ("High", "Medium"): "Alert Security Team & Review Logs",
            ("High", "Low"): "Flag for Review",
            ("Medium", "Critical"): "Increase Monitoring & Investigate",
            ("Medium", "High"): "Schedule Investigation",
            ("Medium", "Medium"): "Routine Monitoring",
            ("Medium", "Low"): "Log Activity for Reference",
            ("Low", "Critical"): "Log and Notify",
            ("Low", "High"): "Routine Monitoring",
            ("Low", "Medium"): "Log for Reference",
            ("Low", "Low"): "No Action Needed"
        }

        # Assign action based on scenario
        action = threat_severity_actions.get((row["Threat Level"], row["Severity"]), action)

        # Additional responses based on user behavior and thresholds
        if row["Threat Level"] in ["Critical", "High"] and row["Login Attempts"] > 5:
            action += " | Lock Account & Alert"
        if row["Activity Type"] == "File Access" and row["Num Files Accessed"] > 15:
            action += " | Restrict File Access"
        if row["Activity Type"] == "Login" and row["Login Attempts"] > 10:
            action += " | Require Multi-Factor Authentication (MFA)"
        if row["Data Transfer MB"] > 100:
            action += " | Limit Data Transfer"

        return action


    def generate_normal_issues_df(self, p_issue_ids, p_issue_keys):
        """Generates a DataFrame of synthetic normal cybersecurity issue data with enhanced logic."""
        normal_issues_data = []
        time_difference_days = (self.config.end_date - self.config.start_date).days
        # Handle the case where the time difference is zero or negative
        days_increment = max(1, time_difference_days)

        # Ensure the divisor for date calculation is at least 1
        date_divisor = max(1, self.config.num_normal_issues // days_increment)


        for i, (issue_id, issue_key) in enumerate(zip(p_issue_ids, p_issue_keys)):
            issue_volume = 1
            category = random.choice(self.config.categories)
            issue_name = self.generate_normal_issues_name(category)
            severity = random.choice(self.config.severities)
            status = random.choice(self.config.statuses)
            reporter = random.choice(self.config.reporters)
            assignee = random.choice(self.config.assignees)

            # Temporal Pattern: Daily/Weekly spikes and overall trend
            # Adjusted calculation to avoid division by zero
            date_reported = self.config.start_date + timedelta(days=i // date_divisor,
                                                   hours=random.randint(0, 23), minutes=random.randint(0, 59))
            # Add weekly peak
            if date_reported.weekday() in [4, 5]: # Friday, Saturday
                 date_reported += timedelta(hours=random.randint(2, 6))
            # Add daily peak (e.g., morning)
            if date_reported.hour in [9, 10, 11]:
                 date_reported += timedelta(minutes=random.randint(15, 45))


            # Remediation Effectiveness: Depends on severity, status, and a simulated assignee workload
            assignee_workload = random.uniform(0.5, 1.5) # Simulate workload
            severity_factor = {"Low": 0.8, "Medium": 1.0, "High": 1.5, "Critical": 2.0}.get(severity, 1.0)
            status_factor = 1.0 if status in ["Resolved", "Closed"] else 2.0 # Open/In Progress might take longer
            avg_resolution_days = 7 * severity_factor * assignee_workload * status_factor # Base resolution time
            issue_response_time_days = max(1, int(np.random.normal(loc=avg_resolution_days, scale=avg_resolution_days/3)))
            date_resolved = date_reported + timedelta(days=issue_response_time_days) if status in ["Resolved", "Closed"] else self.config.current_date + timedelta(days=random.randint(30,180)) # Simulate future resolution for open issues

            # Feature Dependencies and Realistic Distributions
            user_id = random.choice(self.config.users)
            department_affected = random.choice(self.config.departments)
            user_profile = self.user_profiles[user_id]
            department_profile = self.department_profiles[department_affected]

            timestamp = date_reported + timedelta(hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60))

            activity_type = random.choice(self.config.activity_types)
            user_location = random.choice(self.config.locations) # User location should be generated per issue
            ip_location = user_location if np.random.rand() > 0.8 else random.choice([loc for loc in self.config.locations if loc != user_location])

            # Session Duration: Exponential distribution, adjusted by activity type and profiles
            base_session_duration = 600 # seconds
            activity_multiplier = {"login": 0.5, "file_access": 1.5, "data_modification": 2.0}.get(activity_type, 1.0)
            session_duration = max(10, int(np.random.exponential(scale=base_session_duration * activity_multiplier * user_profile['baseline_activity'])))

            # Num Files Accessed: Poisson or Negative Binomial, adjusted by activity type and profiles
            base_files_accessed = 5
            activity_multiplier_files = {"login": 0.1, "file_access": 2.0, "data_modification": 1.5}.get(activity_type, 1.0)
            num_files_accessed = int(max(1, np.random.poisson(lam=base_files_accessed * activity_multiplier_files * user_profile['baseline_activity'] * department_profile['activity_multiplier'])))


            # Login Attempts: Negative Binomial (for bursty attempts), adjusted by profiles
            base_login_attempts = 3
            login_attempts = max(1, np.random.negative_binomial(n=3, p=0.5) + base_login_attempts * user_profile['baseline_activity'] * department_profile['baseline_risk'])


            # Data Transfer MB: Pareto distribution (few large, many small), adjusted by activity type and profiles
            base_data_transfer = 10 # MB
            activity_multiplier_transfer = {"login": 0.1, "file_access": 1.5, "data_modification": 2.5}.get(activity_type, 1.0)
            data_transfer_MB = max(0.1, np.random.pareto(a=2.0) * base_data_transfer * activity_multiplier_transfer * user_profile['baseline_activity'] * department_profile['activity_multiplier'])

            # CPU/Memory Usage: Dependent on activity type and session duration
            base_cpu = 30
            base_mem = 4000
            cpu_usage_percent = max(1, min(100, np.random.normal(loc=base_cpu + session_duration/300, scale=10)))
            memory_usage_MB = max(512, np.random.normal(loc=base_mem + session_duration*5, scale=1000))


            # Impact Score and Cost: Dependent on Severity and Category
            base_impact = 5
            base_cost = 5000
            severity_impact_multiplier = {"Low": 1.0, "Medium": 1.5, "High": 2.5, "Critical": 4.0}.get(severity, 1.0)
            category_impact_multiplier = {"Data Breach": 3.0, "Malware": 2.0, "Unauthorized Access": 2.5}.get(category, 1.0) # Example category impact
            impact_score = max(1, min(10, int(np.random.normal(loc=base_impact * severity_impact_multiplier * category_impact_multiplier * user_profile['risk_tolerance'], scale=3))))
            cost = max(100, np.random.normal(loc=base_cost * severity_impact_multiplier * category_impact_multiplier * department_profile['baseline_risk'], scale=2000))

            # Risk Level Calculation (was missing)
            risk_level = 'Critical' if impact_score > 8 else 'High' if impact_score > 5 else 'Medium' if impact_score > 3 else 'Low'

            # KPI/KRI Calculation (was missing)
            kpi_kri = self.filter_kpi_and_kri(category)

            remediation_steps = f"Steps to resolve {issue_name}" # Remediation Steps (was missing)


            threat_level, threat_score = self.calculate_threat_level(
                severity, impact_score, risk_level, issue_response_time_days,
                login_attempts, num_files_accessed, data_transfer_MB,
                cpu_usage_percent, memory_usage_MB
            )

            row_data = {
                "Severity": severity, "Impact Score": impact_score, "Risk Level": risk_level,
                "Issue Response Time Days": issue_response_time_days, "Login Attempts": login_attempts,
                "Num Files Accessed": num_files_accessed, "Data Transfer MB": data_transfer_MB,
                "CPU Usage %": cpu_usage_percent, "Memory Usage MB": memory_usage_MB,
                "Threat Level": threat_level, "Activity Type": activity_type
            }
            defense_action = self.adaptive_defense_mechanism(row_data)


            normal_issues_data.append([
                issue_id, issue_key, issue_name, issue_volume, category, severity, status, reporter, assignee,
                date_reported, date_resolved, issue_response_time_days, impact_score, risk_level, department_affected,
                remediation_steps, cost, kpi_kri, user_id, timestamp, activity_type, user_location, ip_location,
                session_duration, num_files_accessed, login_attempts, data_transfer_MB,
                cpu_usage_percent, memory_usage_MB, threat_score, threat_level, defense_action
            ])

        df = pd.DataFrame(normal_issues_data, columns=self.config.columns)
        return df


    def generate_anomalous_issues_df(self, p_anomalous_issue_ids, p_anomalous_issue_keys):
        """Generates a DataFrame of synthetic anomalous cybersecurity issue data with enhanced logic."""
        anomalous_issues_data = []

        for i, (issue_id, issue_key) in enumerate(zip(p_anomalous_issue_ids, p_anomalous_issue_keys)):
            issue_volume = 1
            category = random.choice(self.config.categories)
            issue_name = self.generate_anomalous_issue_name(category)
            severity = np.random.choice(self.config.severities, p=[0.05, 0.15, 0.4, 0.4]) # Higher probability for High/Critical
            status = random.choice(self.config.statuses)
            reporter = random.choice(self.config.reporters)
            assignee = random.choice(self.config.assignees)

            # Temporal Pattern: Deviations from normal patterns
            date_reported = self.random_date(self.config.start_date, self.config.end_date) + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
            # Introduce activity outside typical hours for some anomalies
            if np.random.rand() < 0.4: # 40% chance of off-hours activity
                 date_reported = date_reported.replace(hour=random.choice([0, 1, 2, 3, 4, 5, 6, 22, 23]))

            # Remediation Effectiveness: Can be slower for anomalies
            assignee_workload = random.uniform(1.0, 2.0) # Simulate higher workload for anomalies
            severity_factor = {"Low": 1.5, "Medium": 2.0, "High": 3.0, "Critical": 4.0}.get(severity, 2.0)
            status_factor = 1.5 if status in ["Resolved", "Closed"] else 2.5 # Can take even longer
            avg_resolution_days = 14 * severity_factor * assignee_workload * status_factor # Higher base
            issue_response_time_days = max(1, int(np.random.normal(loc=avg_resolution_days, scale=avg_resolution_days/2)))
            date_resolved = date_reported + timedelta(days=issue_response_time_days) if status in ["Resolved", "Closed"] else self.config.current_date + timedelta(days=random.randint(60,240))


            # Feature Dependencies and Realistic Distributions (shifted for anomalies)
            user_id = random.choice(self.config.users)
            department_affected = random.choice(self.config.departments)
            user_profile = self.user_profiles[user_id]
            department_profile = self.department_profiles[department_affected]


            timestamp = date_reported + timedelta(hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60))

            activity_type = np.random.choice(self.config.activity_types, p=[0.2, 0.4, 0.4]) # Higher chance of file_access, data_modification
            user_location = random.choice(self.config.locations) # User location should be generated per issue
            ip_location = random.choice([loc for loc in self.config.locations if loc != user_location]) # More likely to be from unusual location


            # Session Duration: Exponential distribution, adjusted and potentially shorter/longer for anomalies
            base_session_duration = 900 # seconds
            activity_multiplier = {"login": 0.8, "file_access": 2.0, "data_modification": 3.0}.get(activity_type, 1.5)
            session_duration = max(5, int(np.random.exponential(scale=base_session_duration * activity_multiplier * user_profile['baseline_activity'] * 1.5))) # Higher scale for anomalies

            # Num Files Accessed: Negative Binomial, adjusted and higher for anomalies
            base_files_accessed = 20
            activity_multiplier_files = {"login": 0.5, "file_access": 3.0, "data_modification": 2.5}.get(activity_type, 2.0)
            num_files_accessed = int(max(5, np.random.negative_binomial(n=5, p=0.3) + base_files_accessed * activity_multiplier_files * user_profile['baseline_activity'] * department_profile['activity_multiplier'] * 2.0)) # Higher mean/variance


            # Login Attempts: Negative Binomial (for bursty attempts), adjusted and much higher for anomalies
            base_login_attempts = 10
            login_attempts = max(5, np.random.negative_binomial(n=10, p=0.3) + base_login_attempts * user_profile['baseline_activity'] * department_profile['baseline_risk'] * 3.0) # Much higher mean/variance


            # Data Transfer MB: Pareto distribution, adjusted and much higher for anomalies
            base_data_transfer = 100 # MB
            activity_multiplier_transfer = {"login": 0.5, "file_access": 2.0, "data_modification": 4.0}.get(activity_type, 2.5)
            data_transfer_MB = max(1, np.random.pareto(a=1.5) * base_data_transfer * activity_multiplier_transfer * user_profile['baseline_activity'] * department_profile['activity_multiplier'] * 3.0) # Higher scale, lower 'a' for heavier tail


            # CPU/Memory Usage: Dependent on activity type and session duration, often higher for anomalies
            base_cpu = 60
            base_mem = 8000
            cpu_usage_percent = max(1, min(100, np.random.normal(loc=base_cpu + session_duration/200, scale=15)))
            memory_usage_MB = max(1000, np.random.normal(loc=base_mem + session_duration*10, scale=2000))


            # Nuanced Anomalous Patterns: Unusual combinations
            # Example: High data transfer with very low session duration, or file access from unusual location
            if np.random.rand() < 0.3: # 30% chance of injecting this pattern
                 if data_transfer_MB > 1000 and session_duration < 300:
                      session_duration = max(10, int(session_duration * np.random.uniform(0.2, 0.5))) # Make session duration even shorter
                 if activity_type == 'file_access' and ip_location == user_location and np.random.rand() < 0.5:
                      ip_location = random.choice([loc for loc in self.config.locations if loc != user_location]) # Force unusual location


            # Impact Score and Cost: Dependent on Severity and Category, often higher for anomalies
            base_impact = 7
            base_cost = 10000
            severity_impact_multiplier = {"Low": 1.5, "Medium": 2.0, "High": 3.0, "Critical": 5.0}.get(severity, 2.0)
            category_impact_multiplier = {"Data Breach": 4.0, "Malware": 3.0, "Unauthorized Access": 3.5}.get(category, 1.5) # Example category impact
            impact_score = max(3, min(10, int(np.random.normal(loc=base_impact * severity_impact_multiplier * category_impact_multiplier * user_profile['risk_tolerance'] * 1.2, scale=4))))
            cost = max(500, np.random.normal(loc=base_cost * severity_impact_multiplier * category_impact_multiplier * department_profile['baseline_risk'] * 1.5, scale=5000))


            # Risk Level Calculation (was missing)
            risk_level = 'Critical' if impact_score > 8 else 'High' if impact_score > 5 else 'Medium' if impact_score > 3 else 'Low'


            # KPI/KRI Calculation (was missing)
            kpi_kri = self.filter_kpi_and_kri(category)


            remediation_steps = f"Steps to resolve {issue_name}" # Remediation Steps (was missing)

            threat_level, threat_score = self.calculate_threat_level(
                severity, impact_score, risk_level, issue_response_time_days,
                login_attempts, num_files_accessed, data_transfer_MB,
                cpu_usage_percent, memory_usage_MB
            )

            row_data = {
                "Severity": severity, "Impact Score": impact_score, "Risk Level": risk_level,
                "Issue Response Time Days": issue_response_time_days, "Login Attempts": login_attempts,
                "Num Files Accessed": num_files_accessed, "Data Transfer MB": data_transfer_MB,
                "CPU Usage %": cpu_usage_percent, "Memory Usage MB": memory_usage_MB,
                "Threat Level": threat_level, "Activity Type": activity_type
            }
            defense_action = self.adaptive_defense_mechanism(row_data)

            anomalous_issues_data.append([
                issue_id, issue_key, issue_name, issue_volume, category, severity, status, reporter, assignee,
                date_reported, date_resolved, issue_response_time_days, impact_score, risk_level, department_affected,
                remediation_steps, cost, kpi_kri, user_id, timestamp, activity_type, user_location, ip_location,
                session_duration, num_files_accessed, login_attempts, data_transfer_MB,
                cpu_usage_percent, memory_usage_MB, threat_score, threat_level, defense_action
            ])

        df = pd.DataFrame(anomalous_issues_data, columns=self.config.columns)
        return df


    def data_generation_pipeline(self):
        normal_df = self.generate_normal_issues_df(self.config.issue_ids, self.config.issue_keys)
        normal_df["Is Anomaly"] = 0
        anomaly_df = self.generate_anomalous_issues_df(self.anomalous_issue_ids, self.anomalous_issue_keys)
        anomaly_df["Is Anomaly"] = 1
        combined_df = pd.concat([normal_df, anomaly_df], ignore_index=True)
        return normal_df, anomaly_df, combined_df


# =====================================================================
# Processor
# =====================================================================
class DataProcessor:
    def map_threat_severity_to_color(self, df):
        def assign_color(threat, severity):
            if threat == "Critical":
                if severity == "Critical": return "Dark Red"
                elif severity == "High": return "Red"
                elif severity == "Medium": return "Orange-Red"
                else: return "Orange"
            elif threat == "High":
                if severity == "Critical": return "Red"
                elif severity == "High": return "Orange-Red"
                elif severity == "Medium": return "Orange"
                else: return "Yellow-Orange"
            elif threat == "Medium":
                if severity == "Critical": return "Orange"
                elif severity == "High": return "Yellow-Orange"
                elif severity == "Medium": return "Yellow"
                else: return "Light Yellow"
            else:
                if severity == "Critical": return "Yellow"
                elif severity == "High": return "Light Yellow"
                elif severity == "Medium": return "Green-Yellow"
                else: return "Green"
        df["Color"] = df.apply(lambda row: assign_color(row["Threat Level"], row["Severity"]), axis=1)
        return df


# =====================================================================
# Data Display
# =====================================================================
class DataDisplay:
    """Handles displaying dataframes."""
    def display_the_data_frames(self, p_normal_issues_df, p_anomalous_issues_df, p_normal_and_anomalous_df,
                                p_ktis_key_threat_indicators_df, p_scenarios_with_colors_df):
        """Displays info, description, and head for multiple DataFrames."""

        print('Normal_issues_df Data structure\n')
        display(p_normal_issues_df.info())
        print('\nData statistics summary\n')
        display(p_normal_issues_df.describe().transpose())
        print('\nNormal_issues_df\n')
        display(p_normal_issues_df.head())

        print('\nAnomalous_issues_df Data structure\n')
        display(p_anomalous_issues_df.info())
        print('\nAnomalous_issues_df statistics summary\n')
        display(p_anomalous_issues_df.describe().transpose())
        print('\nAnomalous_issues_df\n')
        display(p_anomalous_issues_df.head())

        print('\nNormal & anomalous combined Data structure\n')
        display(p_normal_and_anomalous_df.info())
        print('\nCombined statistics summary\n')
        display(p_normal_and_anomalous_df.describe().transpose())
        print('\nNormal & anomalous combined Data\n')
        display(p_normal_and_anomalous_df.head())

        print('\nKey Threat Indicators\n')
        display(p_ktis_key_threat_indicators_df)

        print('\nScenarios with Colors\n')
        display(p_scenarios_with_colors_df)
        print('\n')
# =====================================================================
# Saver
# =====================================================================

class DataSaver:
    def save_dataframe(self, df, save_path):
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, index=False)
        print(f"✅ Saved to {save_path}")

    def print_summary(self, file_paths):
        summary = []
        for path in file_paths:
            if os.path.exists(path):
                df = pd.read_csv(path)
                size_kb = os.path.getsize(path) / 1024
                summary.append([os.path.basename(path), df.shape[0], df.shape[1], f"{size_kb:.1f} KB"])
        print("\n📊 Dataset Summary")
        print(pd.DataFrame(summary, columns=["File", "Rows", "Columns", "Size"]).to_string(index=False))

    def save_data_option(self, config, no_prompt=False, auto_download=False):
        """Optionally download a ZIP of the datasets."""
        temp_dir = "/tmp/cybersecurity_data"
        zip_path = "/tmp/cybersecurity_data.zip"

        def make_zip():
            os.makedirs(temp_dir, exist_ok=True)
            shutil.copy(config.normal_data_file, temp_dir)
            shutil.copy(config.anomalous_data_file, temp_dir)
            shutil.copy(config.combined_data_file, temp_dir)
            shutil.copy(config.key_threat_indicators_file, temp_dir)
            shutil.copy(config.scenarios_with_colors_file, temp_dir)
            shutil.make_archive("/tmp/cybersecurity_data", 'zip', temp_dir)

        # Auto mode (no user interaction)
        if no_prompt:
            print("Skipping local download (no-prompt mode).")
            return
        if auto_download:
            print("Preparing files for automatic download...")
            make_zip()
            if COLAB:
                files.download(zip_path)
                print("Files downloaded locally as cybersecurity_data.zip")
            else:
                print(f"ZIP created at {zip_path} (please download manually).")
            return

        # Interactive prompt
        while True:
            choice = input("Would you like to download the data files locally as well? (yes/no): ").strip().lower()
            if choice == 'yes':
                print("Preparing files for download...")
                make_zip()
                if COLAB:
                    files.download(zip_path)
                    print("Files downloaded locally as cybersecurity_data.zip")
                else:
                    print(f"ZIP created at {zip_path} (please download manually).")
                break
            elif choice == 'no':
                print("Files saved to repository only. No local download.")
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")


# =====================================================================
# Main pipeline
# =====================================================================
def cybersecurity_data_pipeline(show_data=True, no_prompt=False, auto_download=False):
    config = DataConfig()
    generator = DataGenerator(config)
    processor = DataProcessor()
    saver = DataSaver()
    display_handler = DataDisplay()

    normal_df, anomaly_df, combined_df = generator.data_generation_pipeline()
    combined_df = processor.map_threat_severity_to_color(combined_df)

    # Display if requested
    if show_data:
        display_handler.display_the_data_frames(
            normal_df, anomaly_df, combined_df,
            config.ktis_key_threat_indicators_df,
            config.scenarios_with_colors_df
        )

    # Save all datasets
    saver.save_dataframe(normal_df, config.normal_data_file)
    saver.save_dataframe(anomaly_df, config.anomalous_data_file)
    saver.save_dataframe(combined_df, config.combined_data_file)
    saver.save_dataframe(config.ktis_key_threat_indicators_df, config.key_threat_indicators_file)
    saver.save_dataframe(config.scenarios_with_colors_df, config.scenarios_with_colors_file)

    # Print summary
    saver.print_summary([
        config.normal_data_file,
        config.anomalous_data_file,
        config.combined_data_file,
        config.key_threat_indicators_file,
        config.scenarios_with_colors_file
    ])

    # Prompt or auto ZIP download
    saver.save_data_option(config, no_prompt=no_prompt, auto_download=auto_download)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cybersecurity Data Generator")
    parser.add_argument("--no-prompt", action="store_true", help="Skip download prompt")
    parser.add_argument("--auto-download", action="store_true", help="Auto-download ZIP without prompt")
    parser.add_argument("--no-display", action="store_true", help="Skip DataFrame display")

    args = parser.parse_args()

    cybersecurity_data_pipeline(
        show_data=not args.no_display,
        no_prompt=args.no_prompt,
        auto_download=args.auto_download
    )
