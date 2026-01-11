import getpass
import os
import shutil
import base64

import requests
from bs4 import BeautifulSoup

from Utils.KMS.DocException import LoginFailedException, ReadDocException
from Utils.KMS.Document import Document

HOST = "https://kms.hosp.ncku.edu.tw/KM/"


class DocServer:
    """
    Controlling KM website
    """
    login_link = HOST + "login.aspx"
    logout_link = HOST + "logout.aspx"
    doc_link = HOST + "readdocument.aspx"
    doc_view_link = HOST + "preview.aspx"
    list_link = HOST + "listfolders.aspx"
    upload_link = HOST + "upload.aspx"

    def __init__(self):
        self._user_data = {}
        self._session = requests.session()
        self._response = self._session.get(DocServer.login_link)

        soup = self.get_soup()
        self._user_data["__VIEWSTATE"] = soup.find('input', {'id': "__VIEWSTATE"}).get("value")
        self._user_data["__VIEWSTATEGENERATOR"] = soup.find('input', {'id': "__VIEWSTATEGENERATOR"}).get("value")
        self._user_data["__EVENTVALIDATION"] = soup.find('input', {'id': "__EVENTVALIDATION"}).get("value")
        self._user_data['LoginButton'] = soup.find('input', {'id': "LoginButton"}).get("value")
        self._user_data['__RequestVerificationToken'] = soup.find('input', {'name': "__RequestVerificationToken"}).get("value")
        self._user_data["__VIEWSTATEENCRYPTED"] = soup.find('input', {'id': "__VIEWSTATEENCRYPTED"}).get("value")

        self._user_data['__EVENTTARGET'] = ""
        self._user_data['__EVENTARGUMENT'] = ""

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            # 'Referer': self.login_link,  # 有些伺服器會檢查來源
            # 'Origin': "http://kms.hosp.ncku.edu.tw/"
        }
        self._session.headers.update(headers)


    def get_soup(self):
        """Get current soup content"""
        return BeautifulSoup(self._response.content, "html.parser")

    def login(self, user, password):
        self._user_data['txtUserName'] = user
        self._user_data['txtPw'] = base64.b64encode(password.encode()).decode()

        self._response = self._session.post(DocServer.login_link, data=self._user_data, allow_redirects=False)

        if self._response.status_code == 200:
            raise LoginFailedException

        return self._response

    def logout(self):
        self._response = self._session.get(DocServer.logout_link)
        soup = self.get_soup()

        if soup.find("a", {"href": "/KM/logout.aspx"}) is None:
            return 404

        return 0

    def read_doc_by_id(self, doc_id):
        """
        Get document information
        :param doc_id:
        :return: Document
        """
        link = DocServer.doc_link + f"?documentId={doc_id}"
        self._response = self._session.get(link)

        soup = self.get_soup()
        error_msg = soup.find("div", {"class": "errorMessage"})
        if error_msg is not None:
            raise ReadDocException(error_msg.get_text().strip())

        doc = Document(soup)
        return doc

    def download_view_url(self, url):
        """
        Download image from online pdf viewer
        """
        self._response = self._session.get(url)
        soup = self.get_soup()

        links = soup.find_all("a", {"class": "page-data-link"})
        title = (str(soup.title.string).strip()).split(".")[0]

        print(os.getcwd(), title)

        try:
            os.makedirs(f"export/{title}/")
        except FileExistsError:
            shutil.rmtree(f"export/{title}/")
            os.makedirs(f"export/{title}/")

        page_number = 1
        for i in links:
            img_link = HOST + i.get("href")

            content = self._session.get(img_link).content

            with open(f"export/{title}/{page_number:03}.jpg", "wb") as f:
                f.write(content)
                page_number += 1

    def download_file_url(self, f_name, url):
        """
        Download file
        :param f_name: file name to save
        :param url:  file link
        """
        content = self._session.get(url).content
        with open(f"export/{f_name}", "wb") as f:
            f.write(content)

    def create_document(self, folder_id="104011"):
        """
        Create new document in KM
        """
        upload_url = DocServer.upload_link + f"?folderId={folder_id}"
        self._response = self._session.get(upload_url)
        soup = self.get_soup()

        hidden_tags = soup.find_all("input", {"type": "hidden"})

        hidden_param ={}

        for tag in hidden_tags:
            id_name = tag.get('id')
            if id_name:
                hidden_param[id_name] = tag.get('value')

        return soup

    def save_draft(self):
        """
        Save draft document in KM
        """
        pass

    def attach_files(self):
        """
        Attach files to a document in KM
        """
        pass

    def publish(self):
        """
        Publish document in KM
        """
        pass


if __name__ == "__main__":
    user = input("User:")
    password = getpass.getpass()

    server = DocServer()
    result = server.login(user, password)

    # with open("download_urls.txt", "r") as f:
    #     for url in f.readlines():
    #         server.download_view_url(url)
