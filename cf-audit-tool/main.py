

from lib.api import Client
from lib.parse import CommandLine
from helper.report import Report
from tabulate import tabulate
import csv
import time

if __name__ == "__main__":
    start_time = time.perf_counter()
    (options, args) = CommandLine().options.parse_args()
    cf_client = Client()
    reports = Report(client=cf_client, options=options).run()
    
    for report in reports:
        if report:
            if not options.quiet:
                print(tabulate(report, headers="firstrow"))
            if options.filename:
                with open(options.filename, mode="w") as report_file:
                    report_writer = csv.writer(report_file, delimiter=',', quotechar='"')

                    for raw in report:
                        report_writer.writerow(raw)

    run_time = time.perf_counter() - start_time

    print(f"run time:{run_time}")

    
