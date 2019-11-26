from optparse import OptionParser, OptionGroup


class CommandLine:

    def __init__(self):
        self.parser = OptionParser()
        self.organizations_options()
        self.space_options()
        self.other_options()

    def other_options(self):

        self.parser.add_option("-l", "--list", dest="list",
                               help="print list of orgs,space and apps")

        self.parser.add_option("-a", "--filter-apps", dest="filter_apps", default=False,
                               help="Restrain out put to comma seperated list if arguments apps")

        self.parser.add_option("-p", "--filter-servicePlans", dest="filter_servicePlans", default=False,
                               help="Restrain out put to comma seperated list if arguments organizations")

        self.parser.add_option("-b", "--filter-services", dest="filter_services", default=False,
                               help="Restrain out put to comma seperated list if arguments services")

        self.parser.add_option("--routes-only", action="store_true", dest="routes_only")
        self.parser.add_option(
            "--services-only", action="store_true", dest="services_only")

        self.parser.add_option("-e", "--export-csv",dest="filename", metavar="FILE")

        self.parser.add_option(
            "-q", "--quiet", action="store_true", dest="quiet")

        self.parser.add_option(
            "--summary", action="store_true", dest="summary")

    def organizations_options(self):
        organizations_group = OptionGroup(self.parser, "Orgnizations options")

        organizations_group.add_option("-o", "--organizations", dest="filter_organizations", default=False,
                                       help="Restrain out put to comma seperated list if arguments organizations")
        organizations_group.add_option("--exclude-orgs", action="store_true", default=False,
                                       dest="exclude_organizations", help="exclude listed organizations")

        self.parser.add_option_group(organizations_group)

    def space_options(self):
        spaces_group = OptionGroup(self.parser, "Spaces options")

        spaces_group.add_option("-s", "--spaces", dest="filter_spaces", default=False,
                                help="Restrain out put to comma seperated list if arguments spaces")
        spaces_group.add_option("--exclude-spaces", action="store_true",
                                default=False, dest="exclude_spaces", help="exclude listed spaces")

        self.parser.add_option_group(spaces_group)

    def validate_options(self):
        (options, args) = self.parser.parse_args()
        program_name = self.parser.get_prog_name()

        if options.exclude_organizations and (not options.filter_organizations):
            print(f"error:Must set --organizatios or -o to use --exclude-orgs, see {program_name} --help")
            return False

        if options.exclude_spaces and (not options.filter_spaces):
            print(f"error:Must set --spaces or -s to use --exclude-spaces, see {program_name} --help")
            return False

        if options.routes_only and options.services_only:
            print("--routes-only and --services-only can't be used together")
            return False

        return True

    @property
    def options(self):
        if self.validate_options():
            return self.parser
