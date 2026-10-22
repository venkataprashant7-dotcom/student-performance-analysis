import pandas as pd
import numpy as np
df = pd.read_csv("students.csv")
print("STUDENT PERFORMANCE ANALYTICS SYSTEM")
print("------------------------------------")
print(df.head())
print("\nTotal students:", len(df))
print("Columns:", list(df.columns))

subjects = ["Python", "SQL", "Maths", "AI", "English"]
df["Total"] = df[subjects].sum(axis=1)
df["Average"] = df[subjects].mean(axis=1)
print("\nSTUDENT MARKS SUMMARY")
print("---------------------")
print(df[["Name", "Total", "Average"]].to_string(index=False))

def calculate_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    elif avg >= 50:
        return "E"
    else:
        return "F"
df["Grade"] = df["Average"].apply(calculate_grade)

df["Result"] = np.where(
    (df[subjects] >= 35).all(axis=1),
    "Pass",
    "Fail"
)
print("\nGRADE AND PASS/FAIL REPORT")
print("--------------------------")
print(
    df[["Name", "Average", "Grade", "Result"]]
    .to_string(index=False)
)

print("\n===== OVERALL CLASS ANALYSIS =====")
class_average = df["Average"].mean()
print("Class Average:", round(class_average, 2))

highest_student = df.loc[df["Average"].idxmax()]
lowest_student = df.loc[df["Average"].idxmin()]
print("\nHighest Performing Student:")
print(highest_student["Name"],
      "-", highest_student["Average"])
print("\nLowest Performing Student:")
print(lowest_student["Name"],
      "-", lowest_student["Average"])

pass_count = (df["Result"] == "Pass").sum()
fail_count = (df["Result"] == "Fail").sum()
print("\nTotal Students:", len(df))
print("Passed Students:", pass_count)
print("Failed Students:", fail_count)
print("\nSubject-wise Average Marks:")
subject_averages = df[subjects].mean()
print(subject_averages.round(2))

print("\n===== TOP 3 STUDENTS =====")
top_students = df.nlargest(3, "Average")
print(
    top_students[["Name", "Average", "Grade"]]
    .to_string(index=False)
)
# Data Validation
print("\n===== DATA VALIDATION =====")

missing_values = df.isnull().sum()
print("Missing values in each column:")
print(missing_values)

valid_marks = df[subjects].apply(
    lambda column: column.between(0, 100).all()
).all()

if valid_marks:
    print("Subject marks validation: Passed")
else:
    print("Subject marks validation: Failed")

duplicate_ids = df["StudentID"].duplicated().sum()
print("Duplicate Student IDs:", duplicate_ids)

report_columns = [
    "StudentID",
    "Name",
    "Department",
    "Total",
    "Average",
    "Grade",
    "Result",
    "Attendance"
]

df[report_columns].to_csv(
    "student_performance_report.csv",
    index=False
)
print("\nFinal report saved successfully!")
print("File: student_performance_report.csv")

print("\n===== DEPARTMENT-WISE ANALYSIS =====")
department_average = df.groupby("Department")["Average"].mean()
print("\nAverage marks by department:")
print(department_average.round(2))
print("\nNumber of students in each department:")
print(df["Department"].value_counts())
print("\nPass percentage by department:")
for department in df["Department"].unique():
    department_data = df[df["Department"] == department]
    total_students = len(department_data)
    passed_students = (department_data["Result"] == "Pass").sum()
    pass_percentage = (passed_students / total_students) * 100

    print(
        department,
        ":", round(pass_percentage, 2), "%"
    )

import matplotlib.pyplot as plt
print("\n===== GENERATING PERFORMANCE CHART =====")
top_10 = df.nlargest(10, "Average")
plt.figure(figsize=(10, 5))
plt.bar(top_10["Name"], top_10["Average"])
plt.title("Top 10 Students - Average Marks")
plt.xlabel("Student Name")
plt.ylabel("Average Marks")
plt.ylim(0, 100)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_students_chart.png")
plt.show()
print("Chart saved as top_students_chart.png")