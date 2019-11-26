
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

        servive_report_title = ['Services Report', '', '', '', '', '']
        service_report_headers = ['organization', 'space', 'app', 'services_instance_name',
                                  'service', 'service_plan']

        route_report_title = ['Routes Report', '', '', '', '', '']
        routes_report_headers = ['organization', 'space', 'app', 'routing_service_name',
                                 'route_url', 'route_service_url']

        for organization in self.fetch.organizations(filter_organizations=filter_orgs):

            for space in self.fetch.spaces(filter_spaces=filter_spaces,
                                           organization_guid=organization['organization_guid']):

                for app in self.fetch.apps(filter_apps=[], space_guid=space['space_guid']):

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

            if self.options.services_only:
                report_services.insert(0, servive_report_title)
                report_services.insert(1, service_report_headers)

            if self.options.routes_only:
                report_routes.insert(0, route_report_title)
                report_routes.insert(1, routes_report_headers)

        return {'routes': report_routes, 'services': report_services}
