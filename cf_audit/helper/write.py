from tabulate import tabulate
import csv


class Write:

    def to_screen(self, report):
        print(tabulate(report, headers="firstrow", tablefmt='grid'))
        print("\n\n")

    def to_file(self, report, filename):
        with open(filename, mode="w") as report_file:
            report_writer = csv.writer(
                report_file, delimiter=',', quotechar='"')
            del report[0]
            for raw in report:
                report_writer.writerow(raw)
