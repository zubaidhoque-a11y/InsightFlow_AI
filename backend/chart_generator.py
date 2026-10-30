import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


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
        if path not in chart_paths:
            chart_paths.append(path)

    for i, col in enumerate(numeric_columns[:4]):
        values = df[col].dropna()
        if not values.empty:
            plt.figure(figsize=(8, 5))
            plt.hist(values, bins=25, edgecolor="black", color="#4f46e5", alpha=0.8)
            plt.title(f"Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            plt.tight_layout()
            save_chart(f"histogram_{i}_{col}.png")

    for i, col in enumerate(text_columns[:3]):
        counts = df[col].fillna("Missing").astype(str).value_counts().head(10)
        if not counts.empty:
            plt.figure(figsize=(9, 5))
            plt.bar(counts.index.astype(str), counts.values, color="#06b6d4", alpha=0.85)
            plt.title(f"Top Categories for {col}")
            plt.xlabel(col)
            plt.ylabel("Count")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            save_chart(f"bar_chart_{i}_{col}.png")

            plt.figure(figsize=(7, 7))
            plt.pie(
                counts.values,
                labels=counts.index.astype(str),
                autopct="%1.1f%%",
                startangle=140,
            )
            plt.title(f"Proportion of {col}")
            plt.tight_layout()
            save_chart(f"pie_chart_{i}_{col}.png")

    if len(numeric_columns) >= 2:
        for i in range(min(3, len(numeric_columns) - 1)):
            x_col = numeric_columns[i]
            y_col = numeric_columns[i + 1]
            subset = df[[x_col, y_col]].dropna()
            if not subset.empty:
                plt.figure(figsize=(8, 5))
                plt.scatter(subset[x_col], subset[y_col], alpha=0.6, color="#ec4899", edgecolor="k")
                plt.title(f"{y_col} vs {x_col}")
                plt.xlabel(x_col)
                plt.ylabel(y_col)
                plt.tight_layout()
                save_chart(f"scatter_{i}_{x_col}_vs_{y_col}.png")

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
        save_chart("correlation_heatmap.png")

    return chart_paths


if __name__ == "__main__":
    csv_path = input("Enter your CSV file path: ").strip().strip("'\"")
    paths = generate_charts(csv_path)

    for path in paths:
        print(path)
