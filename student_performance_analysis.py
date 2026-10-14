"""
Student Performance Analysis
Beginner-friendly Python project.

Requirements:
    pip install pandas matplotlib

Run:
    python student_performance_analysis.py

Input:
    student_performance.csv (in the same folder)

Outputs:
    charts/01_subject_averages.png
    charts/02_result_distribution.png
    charts/03_study_hours_vs_marks.png
    charts/04_class_comparison.png
    charts/05_attendance_vs_marks.png
    analysis_summary.txt
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "student_performance.csv"
CHARTS_DIR = BASE_DIR / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

def main():
    # 1. Load the CSV dataset
    data = pd.read_csv(DATA_FILE)
    print("First five rows:")
    print(data.head())

    # 2. Basic data checks and preprocessing
    print("\nDataset shape (rows, columns):", data.shape)
    print("\nMissing values by column:")
    print(data.isnull().sum())

    # Remove duplicate rows, if any
    data = data.drop_duplicates()

    # Fill missing numeric values with each column's median
    numeric_columns = data.select_dtypes(include="number").columns
    data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].median())

    # Recalculate average marks from subject marks so the average is consistent
    subject_columns = ["Maths_Marks", "Science_Marks", "English_Marks", "Computer_Marks"]
    data["Average_Marks"] = data[subject_columns].mean(axis=1).round(1)
    data["Result"] = data["Average_Marks"].apply(
        lambda mark: "Pass" if mark >= 40 else "Needs Support"
    )

    # 3. Print descriptive statistics
    print("\nSummary statistics:")
    print(data[["Study_Hours_Per_Day", "Attendance_Percent"] + subject_columns + ["Average_Marks"]].describe().round(2))

    # 4. Subject-wise average marks
    subject_names = ["Maths", "Science", "English", "Computer"]
    subject_averages = data[subject_columns].mean()
    plt.figure(figsize=(8, 5))
    plt.bar(subject_names, [subject_averages[c] for c in subject_columns])
    plt.title("Average Marks by Subject")
    plt.xlabel("Subject")
    plt.ylabel("Average marks (out of 100)")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "01_subject_averages.png", dpi=160)
    plt.close()

    # 5. Result distribution (pie chart)
    result_counts = data["Result"].value_counts().reindex(["Pass", "Needs Support"], fill_value=0)
    plt.figure(figsize=(6, 6))
    plt.pie(result_counts.values, labels=result_counts.index, autopct="%1.1f%%", startangle=90)
    plt.title("Student Result Distribution")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "02_result_distribution.png", dpi=160)
    plt.close()

    # 6. Study hours versus marks (line of points/scatter plot)
    plt.figure(figsize=(8, 5))
    for class_name in sorted(data["Class"].dropna().unique()):
        group = data[data["Class"] == class_name]
        plt.scatter(group["Study_Hours_Per_Day"], group["Average_Marks"], label=class_name, alpha=0.75)
    plt.title("Study Hours vs Average Marks")
    plt.xlabel("Study hours per day")
    plt.ylabel("Average marks (out of 100)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "03_study_hours_vs_marks.png", dpi=160)
    plt.close()

    # 7. Compare class performance
    class_averages = data.groupby("Class")["Average_Marks"].mean().sort_index()
    plt.figure(figsize=(8, 5))
    plt.bar(class_averages.index, class_averages.values)
    plt.title("Average Performance by Class")
    plt.xlabel("Class")
    plt.ylabel("Average marks (out of 100)")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "04_class_comparison.png", dpi=160)
    plt.close()

    # 8. Attendance versus marks
    plt.figure(figsize=(8, 5))
    plt.scatter(data["Attendance_Percent"], data["Average_Marks"], alpha=0.75)
    plt.title("Attendance vs Average Marks")
    plt.xlabel("Attendance (%)")
    plt.ylabel("Average marks (out of 100)")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "05_attendance_vs_marks.png", dpi=160)
    plt.close()

    # 9. Simple correlation values (correlation is not proof of cause)
    study_corr = data["Study_Hours_Per_Day"].corr(data["Average_Marks"])
    attendance_corr = data["Attendance_Percent"].corr(data["Average_Marks"])
    summary = [
        "STUDENT PERFORMANCE ANALYSIS — SUMMARY",
        f"Number of students: {len(data)}",
        f"Overall average marks: {data['Average_Marks'].mean():.1f}/100",
        f"Average attendance: {data['Attendance_Percent'].mean():.1f}%",
        f"Average study hours/day: {data['Study_Hours_Per_Day'].mean():.1f}",
        f"Pass (average marks >= 40): {(data['Result'] == 'Pass').sum()}",
        f"Needs support: {(data['Result'] == 'Needs Support').sum()}",
        f"Correlation: study hours and average marks = {study_corr:.2f}",
        f"Correlation: attendance and average marks = {attendance_corr:.2f}",
        "",
        "Note: This project uses a sample dataset. Correlation does not prove causation."
    ]
    summary_path = BASE_DIR / "analysis_summary.txt"
    summary_path.write_text("\\n".join(summary), encoding="utf-8")
    print("\\n" + "\\n".join(summary))
    print(f"\\nCharts saved to: {CHARTS_DIR}")

if __name__ == "__main__":
    main()
