import datetime as dt
import json
import os
import shutil

import requests

import Data

if os.getenv("TEST_H") is None:
    HOST = Data.HOST
else:
    # https://122.147.48.137/
    HOST = os.getenv("TEST_H")


class BloodTypeErrorException(Exception):
    pass


class LoginErrorException(Exception):
    pass


class BloodServer:
    _loginAPI = HOST + "tbsf-api/login"
    _queryPatientDetail = HOST + "tbsf-api/bs/patientsDetailService/queryPatientsDetail"
    _queryPatientDetailInfo = HOST + "tbsf-api/bs/patientsDetailService/queryPatientsDetailInfo"
    _addSpecialBloodOrderMaster = HOST + "tbsf-api/bs/specialbloodOrderMasterService/addSpecialBloodOrderMaster"
    _savePatient = HOST + "tbsf-api/bs/patientsDetailService/savePatientsDetail"
    _tokenCheck = HOST + "tbsf-api/check_token"
    _downloadEDI = HOST + "tbsf-api/bs/bldSupOrdMService/downloadEDI"
    _checkEDI = HOST + "tbsf-api/bs/bldSupOrdMService/checkEDI"
    _confirmAPI = HOST + "tbsf-api/bs/bldSupOrdMService/confirm"
    _logoutAPI = HOST + "tbsf-api/logout"

    queryData = {
        "bldUserHistoryNo": "",
        "bldUserIdNo": "",
        "bldUserName": "",
        "bldUserOthId": "",
        "iDisplayStart": "0",
        "iDisplayLength": "1000"
    }

    def __init__(self):
        self.user = {
            'orgCode': '0421040011',
            'username': '',
            'password': '',
            'type': 'HOS'
        }
        self._token = ""
        self._headers = {}

    def login(self, user_id, user_pw):
        """
        Login website. Acquiring token and modified headers

        :return: requests.response
        """
        self.user['username'] = user_id
        self.user['password'] = user_pw

        response = requests.request("POST", self._loginAPI, data=self.user, verify=False)

        if response.json().get("statusCode") != 1060:
            raise LoginErrorException("Username or password might be wrong!")

        self._token = response.json()['access_token']
        self._headers['authorization'] = "Bearer " + self._token
        return response

    def logout(self):
        data = {"access_token": self._token}
        response = requests.request("POST", self._logoutAPI, data=data, verify=False)
        return response

    def query_patients_detail(self, ptid):
        """
        search patient by patient's ID

        :param ptid: patient's ID
        :return: dictionary of patient's detail if it exists
        """
        self.queryData['bldUserHistoryNo'] = ptid
        response = requests.request("POST", self._queryPatientDetail,
                                    headers=self._headers,
                                    params=self.queryData,
                                    verify=False)

        patients_result = response.json().get("responseData").get("results")
        for patient in patients_result:
            if patient['bldUserHistoryNo'] == ptid:
                patient_query = {'bldUserSeqNo': patient.get('bldUserSeqNo')}

                response = requests.request("POST", self._queryPatientDetailInfo,
                                            headers=self._headers,
                                            params=patient_query,
                                            verify=False)

                patient = response.json().get("responseData")
                return patient

        return None

    def save_patient(self, patient):
        """
        Save patient's data on server

        :param patient: dictionary of patient data
        :return: response
        """
        BloodServer.validate_patient_data(patient)

        patient = json.dumps(patient).strip(" ")
        self._headers['content-type'] = "application/json"

        response = requests.request("POST", self._savePatient,
                                    headers=self._headers,
                                    data=patient,
                                    verify=False)
        return response

    def create_sp_order(self):
        """
        create a new special blood order
        :return: response
        """
        date_str = dt.datetime.today().strftime("%Y-%m-%d")

        # To-do: customized Data.special_rbc_form

        payload = json.dumps(Data.special_rbc_form).strip(" ")
        response = requests.request("POST", self._addSpecialBloodOrderMaster,
                                    headers=self._headers,
                                    data=payload,
                                    verify=False)

        return response

    def confirm_order(self, order_number):
        payload = f"pkAk={order_number}"
        self._headers['Content-Type'] = "application/x-www-form-urlencoded"

        print(payload)

        response = requests.post(self._confirmAPI,
                                 headers=self._headers,
                                 data=payload,
                                 verify=False)

        return response

    def check_edi(self, order_number):
        payload = {'bldSupOrdNo': order_number}
        self._headers['content-type'] = "application/json"
        response = requests.post(self._checkEDI,
                                 headers=self._headers,
                                 data=json.dumps(payload),
                                 verify=False)

        return response

    def download_edi(self, order_number):
        """
        Download EDI file
        """
        url = self._downloadEDI + f"?bldSupOrdNo={order_number}&access_token={self._token}"

        response = requests.get(url, verify=False)
        with open(f"{order_number}.txt", "w") as f:
            f.write(response.text)

        open(os.path.join(Data.PATH, f"{order_number}.txt"), "a").close()
        shutil.move(f"{order_number}.txt", os.path.join(Data.PATH, f"{order_number}.txt"))

    @classmethod
    def validate_patient_data(cls, patient):
        """
        clean up patient data
        raise BloodTypeErrorException when patient doesn't have blood type

        :param patient: dictionary of patient data
        """
        if (patient["bldUserBldTyp"] is None) or (patient["bldUserRhBldTyp"] is None):
            raise BloodTypeErrorException("blood type error")

        patient['bldUserSex'] = "1"
        patient["isBldUserEnable"] = "1"

        for key in patient:
            if patient[key] is None:
                patient[key] = ""
