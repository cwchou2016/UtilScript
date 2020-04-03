import getpass

from Utils.BOS.BloodServer import BloodServer

edi = []

with open("EDI.txt", "r") as f:
    for line in f.readlines():
        edi.append(line.strip())

user = input("user:")
password = getpass.getpass()

bs = BloodServer()
r = bs.login(user, password)

for i in edi:
    if not bs.verify_edi(i):
        continue

    r = bs.confirm_order(i)
    print(r.text)
    bs.download_edi(i)

r = bs.logout()
print(r.text)
