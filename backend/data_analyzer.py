import pandas as pd


def analyze_csv(csv_path, question, llm):
    try:
        # 1. Load the dataset
        df = pd.read_csv(csv_path)

        # 2. Basic dataset information
        rows, columns = df.shape
        column_names = list(df.columns)
        data_types = df.dtypes.astype(str).to_dict()

        # 3. Data quality checks
        missing_values = df.isnull().sum()
        missing_values = missing_values[missing_values > 0]

        duplicate_rows = int(df.duplicated().sum())

        # 4. Statistical summary
        numeric_columns = df.select_dtypes(include="number")
        categorical_columns = df.select_dtypes(
            include=["object", "category", "bool"]
        )

        if not numeric_columns.empty:
            statistics = numeric_columns.describe().round(2).to_string()

            # Detect potential outliers using the IQR method
            outlier_counts = {}

            for column in numeric_columns.columns:
                values = numeric_columns[column].dropna()

                if values.empty:
                    outlier_counts[column] = 0
                    continue

                q1 = values.quantile(0.25)
                q3 = values.quantile(0.75)
                iqr = q3 - q1

                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr

                outlier_counts[column] = int(
                    ((values < lower_bound) | (values > upper_bound)).sum()
                )

        else:
            statistics = "No numeric columns available."
            outlier_counts = {}

        # 5. Categorical summaries
        categorical_summary = {}

        for column in categorical_columns.columns:
            categorical_summary[column] = (
                df[column].value_counts().head(5).to_dict()
            )

        # 6. Build a reliable analysis report
        dataset_info = f"""
DATASET OVERVIEW
Rows: {rows}
Columns: {columns}
Column names: {column_names}

DATA TYPES
{data_types}

MISSING VALUES
{missing_values.to_dict() if not missing_values.empty else "No missing values found."}

DUPLICATE ROWS
{duplicate_rows}

NUMERIC STATISTICS
{statistics}

POTENTIAL OUTLIERS (IQR METHOD)
{outlier_counts}

TOP CATEGORICAL VALUES
{categorical_summary}
"""

        # 7. Ask the AI to interpret the calculated results
        prompt = f"""
You are InsightFlow AI, an intelligent data analyst.

Answer the user's question using the dataset report below.

DATASET REPORT:
{dataset_info}

USER QUESTION:
{question}

RULES:
- Use the supplied statistics as the source of truth.
- Do not invent numbers or claim to have performed calculations
  that are not included in the report.
- Explain important patterns in simple language.
- Give practical recommendations when relevant.
- Mention limitations when the available information is insufficient.
- Use clear headings and bullet points.
- Explain that IQR-detected outliers are potential outliers,
  not automatically errors.
"""

        response = llm.invoke(prompt)
        return response.content

    except FileNotFoundError:
        return "Error: The CSV file was not found. Please check the file path."

    except pd.errors.EmptyDataError:
        return "Error: The CSV file is empty."

    except pd.errors.ParserError:
        return "Error: The CSV file could not be parsed. Please check its format."

    except Exception as e:
        return f"An error occurred during analysis: {e}"