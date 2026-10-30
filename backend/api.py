
import os
import uuid

import pandas as pd
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.main import workflow


app = FastAPI(title="InsightFlow AI")

# Allow React to connect to FastAPI

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BACKEND_FOLDER = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BACKEND_FOLDER, "uploads")
CHART_FOLDER = os.path.join(BACKEND_FOLDER, "generated_charts")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)

app.mount(
    "/charts",
    StaticFiles(directory=CHART_FOLDER),
    name="charts",
)


@app.get("/")
def home():
    return {"message": "InsightFlow AI backend is running!"}


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    question: str = Form(...),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file.",
        )

    if not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a question.",
        )

    filename = f"{uuid.uuid4().hex}.csv"
    csv_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        file_content = await file.read()

        with open(csv_path, "wb") as saved_file:
            saved_file.write(file_content)

        df = pd.read_csv(csv_path)

        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="The CSV file has no data rows.",
            )

        result = workflow.invoke({
            "question": question,
            "answer": "",
            "csv_path": csv_path,
            "chart_paths": [],
        })

        chart_urls = []

        for chart_path in result.get("chart_paths", []):
            chart_name = os.path.basename(chart_path)
            actual_path = os.path.join(CHART_FOLDER, chart_name)

            # Only return files that really exist in the chart folder
            if os.path.isfile(actual_path):
                chart_urls.append(
                    f"http://localhost:8000/charts/{chart_name}"
                )

        print("Charts returned by API:", chart_urls)

        return {
            "filename": file.filename,
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": df.columns.tolist(),
            "answer": result.get("answer", ""),
            "charts": chart_urls,
        }

    except HTTPException:
        raise

    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=400,
            detail="The uploaded CSV file is empty or invalid.",
        )

    except pd.errors.ParserError:
        raise HTTPException(
            status_code=400,
            detail="Could not read the CSV. Please check its format.",
        )

    except Exception:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Analysis failed. Check the backend terminal.",
        )

    finally:
        await file.close()



