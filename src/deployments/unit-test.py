# UNIT TESTING
import json
from numpy import float32
from model_service import svc

if __name__ == "__main__":
    # Initialize all runners of the service locally
    for runner in svc.runners:
        runner.init_local()

    # Prepare input data
    input_data = {
        "Store": 1005,
        "DayOfWeek": 6,
        "Date": "2014-04-04",
        "Customers": 3000,
        "Open": 1,
        "Promo": 1,
        "StateHoliday": "0",
        "SchoolHoliday": 0,
    }
    result = svc.apis["predict"].func(input_data)

    print(f"\nINPUT: {json.dumps(input_data, indent=4)}\n")
    print(f"OUTPUT: {result}\n")

    assert result["status"] == 200
    assert type(result["sales"]) == float32
