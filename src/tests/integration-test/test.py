import os
import requests
import json
from requests_aws4auth import AWS4Auth


def test_endpoint(url, input, auth):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    print(f"URL: {url}")
    print(f"Input: {input}")

    try:
        res = requests.post(url, headers=headers, data=json.dumps(input), auth=auth)
        res.raise_for_status()
        print(f"Response: {res.text}")

        assert res.status_code == 200

    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else", err)


if __name__ == "__main__":
    aws_access_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION")
    aws_auth = AWS4Auth(aws_access_id, aws_access_key, aws_region, "sagemaker")

    model_name = "rsmn-sales-xgbr-endpoint"

    url = f"https://runtime.sagemaker.{aws_region}.amazonaws.com/endpoints/{model_name}/invocations"

    # REQUIRED: Please check input data if correct
    data = {
        "Store": 1111,
        "DayOfWeek": 4,
        "Date": "2014-07-10",
        "Customers": 410,
        "Open": 1,
        "Promo": 0,
        "StateHoliday": "0",
        "SchoolHoliday": 1,
    }
    test_endpoint(url=url, input=data, auth=aws_auth)
