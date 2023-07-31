import datetime as dt
import json
import os
import shutil

import requests

from Utils.BOS import Data

if os.getenv("TEST_H") is None:
    HOST = Data.HOST
else:
    # Add this into environment variable.
    # TEST_H=https://122.147.48.137/
    HOST = os.getenv("TEST_H")


class BloodTypeErrorException(Exception):
    pass


class LoginErrorException(Exception):
    pass


class BloodServer:
    Host = HOST
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
    _queryOrderList = HOST + "tbsf-api/bs/bldSupOrdMService/queryBldSupOrdMList"
    _checkToken = HOST + "tbsf-api/check_token"

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
		
        #self._headers["Origin"] = HOST
        self._headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        #self._headers["HOST"] ="dh.blood.org.tw"

    def login(self, user_id, user_pw):
        """
        Login website. Acquiring token and modified headers

        :return: requests.response
        """
        self.user['username'] = user_id
        self.user['password'] = user_pw

        response = requests.request("POST", self._loginAPI, headers=self._headers, data=self.user, verify=False)

        if response.json().get("statusCode") != 1060:
            raise LoginErrorException("Username or password might be wrong!")

        self._token = response.json()['access_token']
        self._headers['authorization'] = "Bearer " + self._token
        return response

    def logout(self):
        data = {"access_token": self._token}
        response = requests.request("POST", self._logoutAPI, headers=self._headers, data=data, verify=False)
        return response

    def check_token(self) -> requests.Response:
        data = {"access_token": self._token}
        response = requests.post(self._checkToken, data=data, headers=self._headers)
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
        self._headers['Content-Type'] = "application/json"

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

    def query_order(self, order_number) -> requests.Response:
        payload = {
            "bagNoType": "1",
            "bldSupOrdNo": order_number,
            "bldSupOrdShipDate": "",
            "bldSupOrdStatus": "",
            "iDisplayStart": "0",
            "iDisplayLength": 10
        }
        self._headers['Content-Type'] = "application/x-www-form-urlencoded"

        response = requests.post(self._queryOrderList,
                                 headers=self._headers,
                                 params=payload,
                                 verify=False)
        return response

    def verify_edi(self, order_number) -> bool:
        r = self.query_order(order_number)
        if r.json().get("responseData").get("totalCount") != 1:
            return False

        if self.check_edi(order_number).json().get("responseData").get("isCut"):
            return False

        return True

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
        self._headers['Content-Type'] = "application/json"
        response = requests.post(self._checkEDI,
                                 headers=self._headers,
                                 data=json.dumps(payload),
                                 verify=False)

        return response

    def download_edi(self, order_number, path="."):
        """
        Download EDI file
        """
        url = self._downloadEDI + f"?bldSupOrdNo={order_number}&access_token={self._token}"

        response = requests.get(url, headers=self._headers, verify=False)
        with open(f"{order_number}.txt", "w") as f:
            f.write(response.text)

        open(os.path.join(path, f"{order_number}.txt"), "a").close()
        shutil.move(f"{order_number}.txt", os.path.join(path, f"{order_number}.txt"))

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
