
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

        self.parser.add_argument("--service-versions", "-sv", dest="service_versions",
                                 type=str, help="Report for comma seperated matching service plan(s)")

        self.parser.add_argument("--exclude-service-versions", "-esv", dest="exclude_service_versions",
                                 type=str, default=False, help="Exclude matching plans from the report")

        self.parser.add_argument("--scan-env-variables", '-senvs',
                                 type=str, help="scan for the environment variable in app(s)")

        self.parser.add_argument("--scan-env-values", '-senv-values',
                                 type=str, help="scan for the environment variable values app(s)")

        selective_report_group = self.parser.add_argument_group()
        selective_report_group.add_argument(
            "--services-only", dest="services_only", action="store_true", default=False, help="process only service reports")
        selective_report_group.add_argument(
            "--routes-only", dest="routes_only", action="store_true", default=False, help="process only routes reports")
        selective_report_group.add_argument(
            "--scan-env-only", dest="scanenv_only", action="store_true", default=False, help="process only scanning env variables/values reports")

        export_report_group = self.parser.add_argument_group()
        export_report_group.add_argument(
            "--export-csv", dest="export_csv", action="store_true", default=False, help="Export reports")
        export_report_group.add_argument("--routes-report", dest="routes_filename",
                                         default="routes.csv", help="name of the routes report file")
        export_report_group.add_argument("--services-report", dest="services_filename",
                                         default="services.csv", help="name of the services report file")
        export_report_group.add_argument("--scan-env-vars-report", dest="scan_env_vars_filename",
                                         default="scanned_env_variables.csv", help="name of the scanned env vraibles report file")
        export_report_group.add_argument("--scan-env-values-report", dest="scan_env_values_filename",
                                         default="scanned_env_values.csv", help="name of the scanned env value report file")

    def validate_options(self):
        prog = self.parser.prog
        options = self.parser.parse_args()

        if options.quiet and (not options.export_csv):
            self.parser.print_usage()
            print(f'{prog} error: --quiet/-q is not allowed without --export-csv')
            return False

        if options.exclude_service_versions and (options.service_versions):
            self.parser.print_usage()
            print(
                f'{prog} error: --service-version/-sv and, --exclude-services-versions/-esv are mutually exclusive')
            return False

        if (
            (options.services_only and options.routes_only) or
            (options.services_only and options.scanenv_only) or
            (options.routes_only and options.scanenv_only)
        ):
            print(
                f'{prog} error: --services-only , --routes-only and --scanenv--only are mutually exclusive')
            return False

        #error if scanenv_only is set but, scan_env value or scan env_variable is not set
        if options.scanenv_only and ( not ( options.scan_env_values or options.scan_env_variables )):
            print(
                f'{prog} error: --scanenv--only can only be used with --scan-env-variables/-senv OR --scan-env-values/-senv-values')
            return False

        if options.scan_env_variables and options.scan_env_values:
            self.parser.print_usage()
            print(
                f'{prog} error: --scan-env-variables/-senv and --scan-env-value/-senv-value are mutually exclusive')
            return False

        return options

    @property
    def options(self):
        return self.validate_options()
