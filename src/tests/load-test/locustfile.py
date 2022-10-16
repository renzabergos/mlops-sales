from locust import HttpUser, task, between
from requests_aws4auth import AWS4Auth
import os


class Testing(HttpUser):
    wait_time = between(1, 2)

    @task
    def login_site_access(self):
        aws_access_id = os.environ.get("AWS_ACCESS_KEY_ID")
        aws_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        aws_region = os.environ.get("AWS_REGION")

        self.client.post(
            "/invocations",
            auth=AWS4Auth(aws_access_id, aws_access_key, aws_region, "sagemaker"),
            json={
                "Store": 1111,
                "DayOfWeek": 4,
                "Date": "2014-07-10",
                "Customers": 410,
                "Open": 1,
                "Promo": 0,
                "StateHoliday": "0",
                "SchoolHoliday": 1,
            },
        )
