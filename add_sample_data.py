#!/usr/bin/env python3
"""
Add sample data to test the Results dashboard
"""
import pandas as pd
from datetime import datetime, timedelta
import random

# Sample data to add
sample_responses = [
    {
        "SubmissionID": "SAMPLE_001",
        "Timestamp": datetime.now() - timedelta(days=5),
        "User_Name": "John Doe",
        "User_Role": "Title Clerk",
        "CSC": "Richmond",
        "User_Email": "john.doe@dmv.virginia.gov",
        "Title_Class_Skills_Important": "All of the above",
        "Title_Class_Confidence": 4,
        "AI_Survey_Experience_Rating": 5,
        "AI_Survey_Experience_Comments": "Great experience with the AI survey!",
        "Recommend_Survey_App": "Yes"
    },
    {
        "SubmissionID": "SAMPLE_002", 
        "Timestamp": datetime.now() - timedelta(days=3),
        "User_Name": "Jane Smith",
        "User_Role": "Driver Examiner",
        "CSC": "Norfolk",
        "User_Email": "jane.smith@dmv.virginia.gov",
        "Driver_Examiner_Skills_Important": "All of the above",
        "Driver_Examiner_Confidence": 3,
        "AI_Survey_Experience_Rating": 4,
        "AI_Survey_Experience_Comments": "Very helpful tool",
        "Recommend_Survey_App": "Yes"
    },
    {
        "SubmissionID": "SAMPLE_003",
        "Timestamp": datetime.now() - timedelta(days=1),
        "User_Name": "Bob Johnson", 
        "User_Role": "Compliance Officer",
        "CSC": "Virginia Beach",
        "User_Email": "bob.johnson@dmv.virginia.gov",
        "Compliance_Skills_Important": "All of the above",
        "Compliance_Confidence": 5,
        "AI_Survey_Experience_Rating": 5,
        "AI_Survey_Experience_Comments": "Excellent survey design",
        "Recommend_Survey_App": "Yes"
    }
]

# Read existing CSV
csv_file = "Updated_Training_Feedback_Survey_Template.csv"
df = pd.read_csv(csv_file)

# Add sample data
for response in sample_responses:
    # Create a row with all columns from the original CSV
    new_row = {col: "" for col in df.columns}  # Initialize all columns
    new_row.update(response)  # Update with sample data
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# Save back to CSV
df.to_csv(csv_file, index=False)
print(f"Added {len(sample_responses)} sample responses to {csv_file}")
print("Sample data preview:")
print(df.tail(3)[["User_Name", "User_Role", "CSC", "Timestamp"]].to_string())