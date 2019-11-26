
from argparse import ArgumentParser


class CommandLine:

    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument("--organizations", '-o', dest="organizations",
                                 type=str, help="Show report for comma seperated list of organizations")

        self.parser.add_argument("--spaces", '-s', dest="spaces", type=str,
                                 help="Show report for comma seperated list of spaces")

        self.parser.add_argument("--quiet", '-q', dest="quiet", action="store_true",
                                 default=False, help="Do not show anything on screen")

        selective_report_group = self.parser.add_mutually_exclusive_group()
        selective_report_group.add_argument("--routes-only", "-ro", action="store_false",
                                            dest="services_only", default=True, help="Show routes report only")
        selective_report_group.add_argument("--services-only", "-so", action="store_false",
                                            dest="routes_only", default=True, help="Show services report only")

        export_report_group = self.parser.add_argument_group()
        export_report_group.add_argument(
            "--export-csv", dest="export_csv", action="store_true", default=False, help="Export reports")
        export_report_group.add_argument("--routes-report", dest="routes_filename",
                                         default="routes.csv", help="name of the routes report file")
        export_report_group.add_argument("--services-report", dest="services_filename",
                                         default="services.csv", help="name of the services report file")

    def validate_options(self):
        prog = self.parser.prog
        options = self.parser.parse_args()

        if options.quiet and (not options.export_csv):
            self.parser.print_usage()
            print(f'{prog} error: --quiet/-q is not allowed without --export-csv')
            return False

        return True

    @property
    def options(self):
        if self.validate_options():
            return self.parser.parse_args()
        return False
