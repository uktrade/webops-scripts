
from argparse import ArgumentParser


class CommandLine:

    def __init__(self):
        self.parser = ArgumentParser()

        self.parser.add_argument("--organizations", '-o', dest="organizations",
                                 type=str, help="Report for comma seperated list of organizations")

        self.parser.add_argument("--spaces", '-s', dest="spaces", type=str,
                                 help="Report for comma seperated list of spaces")

        self.parser.add_argument("--quiet", '-q', dest="quiet", action="store_true",
                                 default=False, help="Do not show anything on screen")

        self.parser.add_argument("--services", "-se", dest="services",
                                 type=str, help="Report for comma seperated list of services")

        self.parser.add_argument("--service-plans", "-sp", dest="service_plans",
                                 type=str, help="Report for comma seperated matching service plan(s)")

        self.parser.add_argument("--exclude-service-plans", "-esp", dest="exclude_service_plans",
                                 action="store_true", default=False, help="Exclude matching plans from the report")

        self.parser.add_argument("--scan-env-variables", '-senvs',
                                 type=str, help="scan for the environment variable in app(s)")

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
        export_report_group.add_argument("--scan-env-vars-report", dest="scan_env_vars_filename",
                                         default="scanned_env_variables.csv", help="name of the scanned env vraibles report file")

    def validate_options(self):
        prog = self.parser.prog
        options = self.parser.parse_args()

        if options.quiet and (not options.export_csv):
            self.parser.print_usage()
            print(f'{prog} error: --quiet/-q is not allowed without --export-csv')
            return False

        if options.exclude_service_plans and (not options.service_plans):
            self.parser.print_usage()
            print(
                f'{prog} error: --exclude-services-plans/-esp is not allowed without --service-plans/-sp')
            return False

        if options.routes_only and options.services:
            self.parser.print_usage()
            print(
                f'{prog} error: --services/-se and --routes-only/-ro are mutually exclusive')
            return False
        if options.scan_env_variables:
            options.routes_only = False
            options.services_only = False

        # if options.scan_env_variables and (options.services or options.service_plans or options.routes_only or options.services_only):
        #     self.parser.print_usage()
        #     print(f'{prog} error: --scan-env-variables/-sev can only be used with --organization/-o and/or --space/-s')
        #     return False

        return True

    @property
    def options(self):
        if self.validate_options():
            return self.parser.parse_args()
        return False
