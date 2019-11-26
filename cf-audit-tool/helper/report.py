from lib.fetch import Fetch


class Report:

    def __init__(self, client, options):
        self.client = client
        self.options = options
        self.fetch = Fetch(client=client)

    def run(self):
        filter_orgs = []
        filter_spaces = []

        if self.options.filter_organizations:
            filter_orgs = self.options.filter_organizations.split(',')
        if self.options.filter_spaces:
            filter_spaces = self.options.filter_spaces.split(',')
        
        report_routes = []
        report_services = []

        service_report_headers = ['organization', 'space', 'app', 'services_instance_name',
                          'service', 'service_plan']

        routes_report_headers = ['organization', 'space', 'app', 'routing_service_name',
                                  'route_url', 'route_service_url']
        
        for organization in self.fetch.organizations(filter_organizations=filter_orgs):

            for space in self.fetch.spaces(filter_spaces=filter_spaces,
                                           organization_guid=organization['organization_guid']):

                for app in self.fetch.apps(filter_apps=[], space_guid=space['space_guid']):

                    services = []
                    routes = []

                    if not self.options.routes_only:
                        for service in self.fetch.services_bound_to_app(app_guid=app['app_guid']):
                            services.append([organization['name'], space['name'], app['name'],
                                         service['service_instance_name'], service['service'], service['service_plan']])

                        report_services += services

                    if not self.options.services_only:
                        for route in self.fetch.routes_bound_to_app(app_guid=app['app_guid']):
                            routes.append([organization['name'], space['name'], app['name'],
                                           route['route_service_instance_name'], route['route_url'], route['route_service_url']])
                            
                        report_routes += routes


            if not self.options.routes_only:
                report_services.insert(0, service_report_headers)
                
            if not self.options.services_only:
                report_routes.insert(0, routes_report_headers)
       
     
        return (report_routes,report_services)
