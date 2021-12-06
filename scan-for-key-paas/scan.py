#!/usr/bin/env python
import fire
from cloudfoundry_client.client import CloudFoundryClient


def scan(target_endpoint, token, env_value):
    """
    Scan for value in paas
    """
    client = CloudFoundryClient(target_endpoint)
    client._access_token = token

    for app in client.v2.apps:
        app_name = app["entity"]["name"]
        print(f"checking {app_name}")

        if (
            app["entity"]["environment_json"]
            and env_value in app["entity"]["environment_json"].values()
        ):
            space_name = app.space()["entity"]["name"]
            print(f"Found! {space_name} / {app_name}")

    print("Done.")


if __name__ == "__main__":
    fire.Fire(scan)
