# Usage
```bash
Usage: report.py [OPTIONS] MONTH

Runs a report for MONTH

month can be specified in any format dateutil understands. e.g "1 feb 2022"
or even just "feb" will work.

If a day other than the first of the month is given it will automatically be
reset to the first of the month

Options:
--help  Show this message and exit.
```

## Development
This script uses [poetry] to manage requirements. Ensure you have that installed
then CD to the directory this README is in and run `poetry shell` to have the requirements
installed and a shell activated.

In this shell you can export a PINGDOM API TOKEN:
```bash
export PINGDOM_TOKEN="example"
```

then you can run the script e.g. if you wanted to run it for the month of July
you could do the following:
```bash
python report.py "1 july 2022"
```

The output will look something like:

```bash
name                     uptime %
-----------------------  ----------
datahub                  100.00%
digital workspace        100.00%
great.gov.uk             100.00%
selling online overseas  100.00%
export opps              100.00%
horizon (events)         100.00%
invest in gb             100.00%
market access            100.00%
datahub legacy           100.00%
trade remedies public    100.00%
```


[poetry]: https://python-poetry.org/docs/#installation
