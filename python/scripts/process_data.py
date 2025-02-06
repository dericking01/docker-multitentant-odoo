import pandas as pd # type: ignore
import os

# Define file paths
input_file = "data/input.txt"
output_dir = "data/output"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Manually read and clean the file
data = []
with open(input_file, "r") as file:
    for i, line in enumerate(file):
        try:
            # Split the line by tabs and ensure it has the expected number of columns
            columns = line.strip().split("\t")
            if len(columns) == 12:  # Adjust based on your expected number of columns
                data.append(columns)
        except Exception as e:
            print(f"Skipping malformed row {i + 1}: {e}")

# Convert the cleaned data into a DataFrame
df = pd.DataFrame(data, columns=[
    "MSISDN", "SUB_TYPE", "GENDER", "AGE", "ARPU_SEGMENT", "SMARTPHONE_USER",
    "ACS_CHARGE", "ACS_USER", "VAS_CHARGE", "VAS_USER", "TERRITORY", "COMMERCIAL_REGION"
])

# Define age groups
def categorize_age(age):
    age = int(age)  # Convert age to integer for comparison
    if age < 35:
        return "Young Adult"
    elif 35 <= age < 54:
        return "Older Adult"
    else:
        return "Senior Adult"

# Skip rows where AGE is not numeric
df = df[df["AGE"].str.isnumeric()]
# Apply age categorization
df["AGE_GROUP"] = df["AGE"].apply(categorize_age)

# Explicitly handle UNKNOWN in GENDER
df["GENDER"] = df["GENDER"].replace("UNKNOWN", "Unknown")

# Group by TERRITORY, GENDER, and AGE_GROUP
grouped = df.groupby(["TERRITORY", "GENDER", "AGE_GROUP"])

# Process each group
for group_name, group_data in grouped:
    territory, gender, age_group = group_name

    # Create a descriptive filename
    filename = f"{territory}{gender}{age_group.replace(' ', '_')}.csv"

    # Limit each file to 100k records
    for i, chunk in enumerate(range(0, len(group_data), 100000)):
        chunk_data = group_data.iloc[chunk:chunk + 100000]
        output_filename = os.path.join(output_dir, f"{filename}_{i+1}.csv")
        chunk_data[["MSISDN"]].to_csv(output_filename, index=False)

        print(f"Created file: {output_filename}")

print("Processing complete!")