import boto3
import csv
from sys import stderr

from enum import Enum

class TermColours(Enum):
    FAIL = '\033[91m'
    ENDC = '\033[0m'


"""Boto3 way to grab and list all profiles from aws config file aka ~/.awa/credentials """
profiles = boto3.session.Session().available_profiles

for profile in profiles:
    """stores extracted data used to generate csv"""
    data = [['CF_DOMAIN','CNAME','Min TLS Version']]
    """ store the distribution data as received from aws"""
    distributions_data = []

    session = boto3.session.Session(profile_name=profile)
    cloud_front = session.client('cloudfront')
  
    """ starting with blank marker so we can loop through next marker in response"""
    nextMarker = ''

    while True:
        try:
            distributions = cloud_front.list_distributions(Marker=nextMarker)
            distributions_data += distributions['DistributionList']['Items']

            if 'NextMarker' not in distributions['DistributionList'].keys():
                break;

            nextMarker = distributions['DistributionList']['NextMarker']

        except Exception as e:
            print(f'{TermColours.FAIL.value}Error Profile:{TermColours.ENDC.value}{profile} {TermColours.FAIL.value}Error:{TermColours.ENDC.value} {e}',file=stderr)
            break

    """Extract data of interest from distributions"""
    for distribution_info in distributions_data:
        cloud_front_domain = distribution_info['DomainName']

        cloud_front_cname = 'None' 
        if distribution_info['Aliases']['Quantity'] > 0:
            if distribution_info['Aliases']['Quantity'] > 1:
                cloud_front_cname = "|".join(distribution_info['Aliases']['Items'])
            else:
                cloud_front_cname = distribution_info['Aliases']['Items'][0]

        cloud_front_min_tls = distribution_info['ViewerCertificate']['MinimumProtocolVersion']

        data.append([cloud_front_domain,cloud_front_cname,cloud_front_min_tls])


    """Create one csv per profile """
    if (len(data) > 1):
        filename = f'{profile}.csv'
        filename.replace(" ","_")
        with open(filename, mode="w") as report_file:
            report_writer = csv.writer(report_file, delimiter=',', quotechar='"')
            for raw in data:
                report_writer.writerow(raw)