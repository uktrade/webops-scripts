from tqdm import tqdm

from pprint import pprint


class Report:

    def __init__(self, client, options, fetch):
        self.client = client
        self.options = options
        self.fetch = fetch

    def run(self):
        filter_orgs = []
        filter_spaces = []
        filter_services = []
        filter_service_plans = []
        filter_env_variables = []

        if self.options.organizations:
            filter_orgs = self.options.organizations.split(',')
        if self.options.spaces:
            filter_spaces = self.options.spaces.split(',')
        if self.options.services:
            filter_services = self.options.services.split(',')
        if self.options.service_plans:
            filter_service_plans = self.options.service_plans.split(',')
        if self.options.scan_env_variables:
            filter_env_variables = self.options.scan_env_variables.split(',')

        report_routes = []
        report_services = []
        report_env_variables = []

        service_report_headers = ['organization', 'space', 'app', 'services_instance_name',
                                  'service', 'service_plan']

        routes_report_headers = ['organization', 'space', 'app', 'routing_service_name',
                                 'route_url', 'route_service_url']

        scan_env_variables_report_header = ['organization', 'space']
        for env_variable in filter_env_variables:
            scan_env_variables_report_header.append(env_variable)

        progress_bar_pos = 0

        organizations = self.fetch.organizations(
            filter_organizations=filter_orgs)

        organizations_progress_bar = tqdm(total=len(
            organizations), position=progress_bar_pos, leave=False)

        for organization in organizations:

            organization_name = organization['entity']['name']
            organization_guid = organization['metadata']['guid']

            organizations_progress_bar.set_description(
                f"organizations/{organization_name}")

            spaces_in_organization = self.fetch.spaces(filter_spaces=filter_spaces,
                                                       organization_guid=organization_guid)

            space_progress_bar = tqdm(
                total=len(spaces_in_organization), position=progress_bar_pos + 1, leave=False)

            for space in spaces_in_organization:
                space_name = space['entity']['name']
                space_guid = space['metadata']['guid']

                space_progress_bar.set_description(f"spaces/{space_name}")

                apps_in_space = self.fetch.apps(
                    filter_apps=[], space_guid=space_guid)

                app_progress_bar = tqdm(
                    total=len(apps_in_space), position=progress_bar_pos + 2, leave=False)

                # if scaning for env varaibles, do not generate route and service report at all
                if not self.options.scan_env_variables:
                    report_routes, report_services = self.__routes_and_services(
                        apps_in_space=apps_in_space,
                        app_progress_bar=app_progress_bar,
                        organization_name=organization_name,
                        space_name=space_name,
                        filter_services=filter_services,
                        filter_service_plans=filter_service_plans,
                        exclue_service_plans=self.options.exclude_service_plans
                    )

                else:
                    report_env_variables += self.__scan_env_variables(
                        apps_in_space=apps_in_space,
                        app_progress_bar=app_progress_bar,
                        organization_name=organization_name,
                        space_name=space_name,
                        filter_env_variables=filter_env_variables
                    )

                app_progress_bar.refresh()
                space_progress_bar.update()

            space_progress_bar.refresh()
            organizations_progress_bar.update()

        organizations_progress_bar.close()

        # if scaning for env varaibles, do not generate route and service report at all
        if not self.options.scan_env_variables:
            if self.options.services_only:
                report_services.insert(0, service_report_headers)

            if self.options.routes_only:
                report_routes.insert(0, routes_report_headers)
        else:
            report_env_variables.insert(0, scan_env_variables_report_header)

        return {'routes': report_routes, 'services': report_services, 'env_variables': report_env_variables}

    def __routes_and_services(self, apps_in_space, app_progress_bar, organization_name, space_name, filter_services, filter_service_plans, exclue_service_plans):
        report_routes = []
        report_services = []
        for app in apps_in_space:
            app_name = app['entity']['name']
            app_guid = app['metadata']['guid']
            app_progress_bar.set_description(f"apps/{app_name}")
            services = []
            routes = []
            if self.options.services_only:
                for bound_service in self.fetch.bound_services(app_guid=app_guid, filter_services=filter_services,
                                                               filter_service_plans=filter_service_plans, exclude_service_plans=exclue_service_plans):

                    service_instance_name = bound_service['service_instance']['entity']['name']
                    service_name = "N/A"
                    service_plan = "N/A"

                    if bound_service['service']:
                        service_name = bound_service['service']['entity']['label']
                    else:
                        if 'type' in bound_service['service_instance']['entity']:
                            service_name = bound_service['service_instance']['entity']['type']

                    if bound_service['service_plan']:
                        service_plan = bound_service['service_plan']['entity']['name']
                    services.append([organization_name, space_name, app_name,
                                     service_instance_name, service_name, service_plan])
                report_services += services
            if self.options.routes_only:
                for mapping in self.fetch.mapped_routes(app_guid=app_guid):
                    route_url = f"{mapping['route']['entity']['host']}.{mapping['domain']['entity']['name']}{mapping['route']['entity']['path']}"
                    route_service_url = ''
                    route_service_instance_name = ''
                    if mapping['route_service_instance']:
                        route_service_instance_name = mapping['route_service_instance']['entity']['name']
                        if 'route_service_url' in mapping['route_service_instance']['entity']:
                            route_service_url = mapping['route_service_instance']['entity']['route_service_url']
                    routes.append([organization_name, space_name, app_name,
                                   route_service_instance_name, route_url, route_service_url])
                report_routes += routes
                app_progress_bar.update()

        return (report_routes, report_services)

    def __scan_env_variables(self, apps_in_space, app_progress_bar, organization_name, space_name, filter_env_variables):
        report_env_variables = []
        for app in apps_in_space:
            app_name = app['entity']['name']
            app_guid = app['metadata']['guid']
            app_progress_bar.set_description(f"apps/{app_name}")

            app_env_variables = app['entity']['environment_json']
            report = [organization_name, space_name, app_name]

            if app_env_variables is None:
                app_env_variables = {}

            for env_var in filter_env_variables:
                value = "None"
                if env_var in app_env_variables.keys():
                    value = app_env_variables[env_var]
                report = report + [value]

            report_env_variables.append(report)
            app_progress_bar.update()
        return report_env_variables
