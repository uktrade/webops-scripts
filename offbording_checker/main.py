# from auditlib.parse import CommandLine
# from auditlib.api import Client
# from auditlib.fetch import Fetch
# from helper.report import Report
# from helper.write import Write

# import time


# if __name__ == "__main__":
#     start_time = time.perf_counter()

#     options = CommandLine().options

#     if options:
#         cf_client = Client()
#         store_file = '.audit_data'
#         timeformat = '%d/%m/%y %H:%M:%S'

#         if cf_client.oauthToken != 'FAILED':

#             fetch = Fetch(client=cf_client,store_file=store_file,timeformat=timeformat)
#             write = Write()

#             report = Report(client=cf_client, options=options,
#                             fetch=fetch, store_file=store_file,timeformat=timeformat).run()

#             for report_name, report_data in report.items():
#                 if report_data:
#                     if not options.quiet:
#                         write.to_screen(report=report_data)

#                     if options.export_csv:
#                         if report_name == 'routes':
#                             filename = options.routes_filename
#                         if report_name == 'services':
#                             filename = options.services_filename
#                         if report_name == 'scanenv':
#                             if options.scan_env_vars_filename:
#                                 filename = options.scan_env_vars_filename
#                             else:
#                                 filename = options.scan_env_values_filename

#                         write.to_file(report=report_data, filename=filename)

#             run_time = time.perf_counter() - start_time

#             print(f"run time:{run_time}")


from modules.xlsx_reader import ReadExcel
from modules.atlassian_admin import AtlassianAdmin

from datetime import datetime
from envs import env

import time


def getOffboardingUsers():
    now = datetime.now()
    filter_date = datetime(now.year,now.month,now.day,0,0)
    users = ReadExcel().data(file='Offboarding.xlsx',sheet='Completed',upto_this_date=filter_date)

    #appened guessed emails
    for index,user in users.items():
        email_name = f"{(user['First Name']).lower()}.{(user['Surname']).lower()}"
        user.update({'digital_email': f'{email_name}@digital.trade.gov.uk' , 'trade_email': f'{email_name}@trade.gov.uk'})


    return users


def getAtlassinUsers():
    url = (env('ATLASSIAN_ADMIN_API_ENDPOINT')).strip('\r')
    token = (env('ATLASSIAN_ADMIN_AUTH_TOKEN')).strip('\r')
    orgName = (env('ATLASSIAN_ORG_NAME')).strip('\r')

    atlassianAdmin = AtlassianAdmin(url=url,token=token)
    atlassianUsers = atlassianAdmin.getOrgUsers(orgName='uktrade')

    return atlassianUsers

if __name__ == "__main__":
    start_time = time.perf_counter()


    users = getOffboardingUsers()
    atlassianUsers = getAtlassinUsers()

    #start checking!


    
    run_time = time.perf_counter() - start_time
    print(f"run time:{run_time}")
