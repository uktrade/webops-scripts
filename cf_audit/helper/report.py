from tqdm import tqdm


class Report:

    def __init__(self, client, options, fetch):
        self.client = client
        self.options = options
        self.fetch = fetch

    def run(self):
        filter_orgs = []
        filter_spaces = []

        if self.options.organizations:
            filter_orgs = self.options.organizations.split(',')
        if self.options.spaces:
            filter_spaces = self.options.spaces.split(',')

        report_routes = []
        report_services = []

        service_report_headers = ['organization', 'space', 'app', 'services_instance_name',
                                  'service', 'service_plan']

        routes_report_headers = ['organization', 'space', 'app', 'routing_service_name',
                                 'route_url', 'route_service_url']

        progress_bar_pos = 0

        organizations = self.fetch.organizations(
            filter_organizations=filter_orgs)

        organizations_progress_bar = tqdm(total=len(
            organizations), desc='Organizations', position=progress_bar_pos, leave=False)

        for organization in organizations:

            organizations_progress_bar.set_description(
                f"organizations/{organization['name']}")

            spaces_in_organization = self.fetch.spaces(filter_spaces=filter_spaces,
                                                       organization_guid=organization['organization_guid'])

            space_progress_bar = tqdm(
                total=len(spaces_in_organization), desc='spaces', position=progress_bar_pos+1, leave=False)
            for space in spaces_in_organization:

                apps_in_space = self.fetch.apps(
                    filter_apps=[], space_guid=space['space_guid'])

                app_progress_bar = tqdm(
                    total=len(apps_in_space), desc=f'apps', position=progress_bar_pos + 2, leave=False)
                space_progress_bar.set_description(f"spaces/{space['name']}")

                for app in apps_in_space:

                    app_progress_bar.set_description(f"apps/{app['name']}")
                    services = []
                    routes = []

                    if self.options.services_only:
                        for service in self.fetch.services_bound_to_app(app_guid=app['app_guid']):
                            services.append([organization['name'], space['name'], app['name'],
                                             service['service_instance_name'], service['service'], service['service_plan']])

                        report_services += services

                    if self.options.routes_only:
                        for route in self.fetch.routes_bound_to_app(app_guid=app['app_guid']):
                            routes.append([organization['name'], space['name'], app['name'],
                                           route['route_service_instance_name'], route['route_url'], route['route_service_url']])

                        report_routes += routes
                    app_progress_bar.update()

                app_progress_bar.refresh()
                space_progress_bar.update()

            space_progress_bar.refresh()
            organizations_progress_bar.update()

        organizations_progress_bar.close()

        if self.options.services_only:
            report_services.insert(1, service_report_headers)

        if self.options.routes_only:
            report_routes.insert(1, routes_report_headers)

        return {'routes': report_routes, 'services': report_services}
