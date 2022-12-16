import random
import time

import requests
import UserData

def date_string(year, month, day):
    return f"{year}%2F{month}%2F{day}"



login_asp = "https://cpa.hosp.ncku.edu.tw/user/user_login2.asp"

#"http://192.168.0.35/user/user_login2.asp"

update_temp = "https://cpa.hosp.ncku.edu.tw/PBT/Body_Temperature_Update.asp"


user_data = {"txt_las110_Value": UserData.ID,
             "userpwd": UserData.PW,
             "submit1": "%B5n%A4J%A8t%B2%CE"}

temp_data = {
    "BT_Area": "A",
    "BT_Date": "2021%2F03%2F04",
    "BT_PNo": "966384",
    "BT_PName": "%25u5468%25u627F%25u7DEF",
    "BT_PMainDep": "8000",
    "BT_PDep": "8250",
    "BT_PDep_Name": "%25u8840%25u5EAB%25u7D44%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520%2520",
    "BT_Data_1": "35.2",
    "BT_KeyinPNo": "966384",
    "BT_Q2": "N",
    # "BT_Q3": "N",
    "BT_Q4": "Y",
    # "BT_Q5": "N",

}
session = requests.session()
response = session.post(login_asp, data=user_data)

print(date_string("2020", "02", 3))

# edit here!!
for d in [25,26,27,28]:

    t = random.randint(350, 369)
    t = t / 10.0

    # edit here
    temp_data["BT_Date"] = date_string(2022, "11", d)


    temp_data["BT_Data_1"] = t
    response = session.post(update_temp, data=temp_data)
    print(response.text)

    time.sleep(1)
