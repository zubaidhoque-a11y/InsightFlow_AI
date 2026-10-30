import os
import pandas as pd
import matplotlib.pyplot as plt


BACKEND_FOLDER = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BACKEND_FOLDER, "generated_charts")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def generate_charts(csv_path):
    chart_paths = []

    df = pd.read_csv(csv_path)

    if df.empty:
        return chart_paths

    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    text_columns = df.select_dtypes(include=["object", "category"]).columns.tolist()

    def save_chart(filename):
        path = os.path.abspath(os.path.join(OUTPUT_FOLDER, filename))
        plt.savefig(path, bbox_inches="tight", dpi=150)
        plt.close()
        chart_paths.append(path)

    if numeric_columns:
        column = (
            "temperature"
            if "temperature" in numeric_columns
            else numeric_columns[0]
        )

        values = df[column].dropna()

        if not values.empty:
            plt.figure(figsize=(8, 5))
            plt.hist(values, bins=20, edgecolor="black")
            plt.title(f"Distribution of {column}")
            plt.xlabel(column)
            plt.ylabel("Frequency")
            plt.tight_layout()
            save_chart("histogram.png")

    if "machine_failure" in df.columns:
        counts = (
            df["machine_failure"]
            .fillna("Missing")
            .astype(str)
            .value_counts()
            .sort_index()
        )
        column = "machine_failure"
    elif text_columns:
        column = text_columns[0]
        counts = (
            df[column]
            .fillna("Missing")
            .astype(str)
            .value_counts()
            .head(10)
        )
    else:
        counts = None

    if counts is not None and not counts.empty:
        plt.figure(figsize=(8, 5))
        plt.bar(counts.index.astype(str), counts.values)
        plt.title(f"Counts for {column}")
        plt.xlabel(column)
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        save_chart("bar_chart.png")

        plt.figure(figsize=(7, 7))
        plt.pie(
            counts.values,
            labels=counts.index.astype(str),
            autopct="%1.1f%%",
            startangle=140,
        )
        plt.title(f"Proportion of {column}")
        plt.tight_layout()
        save_chart("pie_chart.png")

    if len(numeric_columns) >= 2:
        x_col = numeric_columns[0]
        y_col = numeric_columns[1]
        subset = df[[x_col, y_col]].dropna()

        if not subset.empty:
            plt.figure(figsize=(8, 5))
            plt.scatter(subset[x_col], subset[y_col], alpha=0.6, edgecolor="k")
            plt.title(f"{y_col} vs {x_col}")
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.tight_layout()
            save_chart("scatter_plot.png")

    if len(numeric_columns) >= 2:
        correlation = df[numeric_columns].corr()

        plt.figure(figsize=(10, 8))
        plt.imshow(
            correlation,
            cmap="coolwarm",
            vmin=-1,
            vmax=1,
            aspect="auto",
        )
        plt.colorbar(label="Correlation")

        plt.xticks(
            range(len(correlation.columns)),
            correlation.columns,
            rotation=45,
            ha="right",
        )
        plt.yticks(
            range(len(correlation.columns)),
            correlation.columns,
        )

        plt.title("Correlation Heatmap")
        plt.tight_layout()
        save_chart("heatmap.png")

    return chart_paths


if __name__ == "__main__":
    csv_path = input("Enter your CSV file path: ").strip().strip("'\"")
    paths = generate_charts(csv_path)

    for path in paths:
        print(path)
