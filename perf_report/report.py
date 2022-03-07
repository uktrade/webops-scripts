import os
from datetime import datetime

import click
import httpx
from dateutil.parser import parse as parse_dt
from dateutil.relativedelta import relativedelta
from tabulate import tabulate

CHECKS = {
    "datahub": 4946807,
    "digital workspace": 4052929,
    "great.gov.uk": 6846102,
    "selling online overseas": 2358391,
    "export opps": 2650384,
    "horizon (events)": 6846199,
    "invest in gb": 4814386,
    "market access": 6846108,
    "datahub legacy": 4052947,
    "trade remedies public": 5100473,
}

TOKEN = os.environ.get("PINGDOM_TOKEN")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
BASE_URL = "https://api.pingdom.com/api/3.1"


def parse_month(ctx, param, value):
    if value:
        return parse_dt(value).replace(day=1)


def fetch_report(check_id: int, from_: datetime, to: datetime):
    params = {"includeuptime": "true", "from": from_.timestamp(), "to": to.timestamp()}
    resp = httpx.get(
        f"{BASE_URL}/summary.average/{check_id}", params=params, headers=HEADERS
    )
    return resp.json()


def get_uptime_percent(report):
    total_up = report["summary"]["status"]["totalup"]
    total_down = report["summary"]["status"]["totaldown"]
    return 1 - (total_down / total_up)


@click.command()
@click.argument("month", callback=parse_month)
def main(month: datetime):
    """
    Runs a report for MONTH

    month can be specified in any format dateutil understands. e.g "1 feb 2022"
    or even just "feb" will work.

    If a day other than the first of the month is given it will automatically
    be reset to the first of the month
    """
    next_month = month + relativedelta(months=1)
    table = []
    for check_name, check_id in CHECKS.items():
        r = fetch_report(check_id, month, next_month)
        uptime = get_uptime_percent(r)
        table.append([check_name, f"{uptime:.2%}"])
    print(tabulate(table, headers=["name", "uptime %"]))


if __name__ == "__main__":
    main()
