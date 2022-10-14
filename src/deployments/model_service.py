import bentoml
from bentoml.io import JSON

# model imports
import pandas as pd
from xgboost import XGBRegressor


class CustomRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("cpu",)  # or "nvidia.com/gpu"
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        # Load XGBoostRegression Model
        self.model = XGBRegressor()
        self.model.load_model("./xgbr-1_0.json")

    @bentoml.Runnable.method(batchable=False)
    def predict(self, input_df: pd.DataFrame) -> list:
        # Call XGBoost predict function
        return self.model.predict(input_df)[0]


custom_runner = bentoml.Runner(CustomRunnable)
svc = bentoml.Service("rsmn-sales-xgbr-1_0", runners=[custom_runner])


# Custom Functions
def split_date(df: pd.DataFrame):
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df = df.drop("Date", axis=1)
    return df


def categorize_state_holiday(df: pd.DataFrame):
    df["StateHoliday"] = df["StateHoliday"].replace(["0", "a", "b", "c"], [0, 1, 2, 3])
    return df


# BentoML API service logic
@svc.api(input=JSON(), output=JSON())
def predict(input_json):
    # Validate inputs
    # Check if Open, else throw error
    if not input_json["Open"]:
        return {
            "error": f"ERROR: Store {input_json['Store']} should be open. Current value of Open: {input_json['Open']}",
            "status": 400,
        }

    # Convert to DF to easily preprocess in batches
    input_df = pd.DataFrame([input_json])

    # Preprocess Inputs
    input_df = split_date(input_df)
    input_df = categorize_state_holiday(input_df)

    result = custom_runner.predict.run(input_df)
    return {"sales": result, "status": 200}
