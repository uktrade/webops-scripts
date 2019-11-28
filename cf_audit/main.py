
from auditlib.parse import CommandLine
from auditlib.api import Client
from auditlib.fetch import Fetch
from helper.report import Report
from helper.write import Write

import time


if __name__ == "__main__":
    start_time = time.perf_counter()

    options = CommandLine().options

    if options:
        cf_client = Client()
        if cf_client.oauthToken != 'FAILED':

            fetch = Fetch(cf_client)
            write = Write()

            report = Report(client=cf_client, options=options,
                            fetch=fetch).run()

            for report_name, report_data in report.items():
                if report_data:
                    if not options.quiet:
                        write.to_screen(report=report_data)

                    if options.export_csv:
                        filename = options.routes_filename
                        if report_name == 'services':
                            filename = options.services_filename

                        write.to_file(report=report_data, filename=filename)

            run_time = time.perf_counter() - start_time

            print(f"run time:{run_time}")
