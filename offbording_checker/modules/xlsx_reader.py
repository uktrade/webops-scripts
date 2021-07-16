
import pandas as pd
import sys

class ReadExcel:

    def data(self,file,sheet,upto_this_date):
        data  = pd.read_excel(file,sheet)

        headers = []
        users = {}
        for index,info in data.iterrows():
            if index == 0:
                for col in info:
                    headers.append(col.strip())
                continue

            temp_data = {}

            for col_index,col_value in enumerate(info):
                temp_data.update({headers[col_index]:col_value})
                    
            users.update({index:temp_data})

            #filtet leaver with date greater than todays date
            keys_to_delete = []
            for index,user in users.items():
                try:
                    if user['Leave Date'] > upto_this_date:
                        keys_to_delete.append(index)
                except Exception as e:
                    if type(user['Leave Date']) is str:
                        user['Leave Date'] = (user['Leave Date']).strip('\n')
                    print(f"Row:{index}\tLeave Date:{user['Leave Date']}\tError:{e}")
                    continue

            for key in keys_to_delete:
                users.pop(key,None)

        return users
    