import platform

HOST = "https://dh.blood.org.tw/"

if platform.system() == "Windows":
    PATH = r"C:\blood"
else:
    PATH = r"~"

special_rbc_form = {"bldOrderDate": "2019-07-20",  # 訂血日期
                    "hospGetBldMtd": "SUPY",
                    "bldSupCenterSiteId": "6_S61",
                    "bldUserSeqNo": "6848296c4362498b8f5df4c2ef5ffa61",  # 病人資料庫編碼
                    "bldOrdRemark": "test",  # 備註
                    "spReqRbcAgneg": "1",
                    "spReqRbcAgpos": "0",
                    "spBldTyp": "0",
                    "spReqHla": "0",
                    "spReqHpa": "0",
                    "spReqPltXMat": "0",
                    "spReqElse": "0",
                    "spReqElseDesc": "",
                    "spReqBldTypSame": "1",
                    "rbcAgneg1": "002001",  # 特殊抗原
                    "rbcAgneg2": "002002",  # 特殊抗原
                    "rbcAgneg3": "002003",  # 特殊抗原
                    "rbcAgneg4": "002004",  # 特殊抗原
                    "rbcAgneg5": "002007",  # 特殊抗原
                    "rbcAgneg6": "",  # 特殊抗原
                    "rbcAgneg7": "",  # 特殊抗原
                    "rbcAgneg8": "",  # 特殊抗原
                    "rbcAgneg9": "",  # 特殊抗原
                    "rbcAgneg10": "",  # 特殊抗原
                    "rbcAgpos1": "",
                    "rbcAgpos2": "",
                    "rbcAgpos3": "",
                    "rbcAgpos4": "",
                    "rbcAgpos5": "",
                    "rbcAgpos6": "",
                    "rbcAgpos7": "",
                    "rbcAgpos8": "",
                    "rbcAgpos9": "",
                    "rbcAgpos10": "",
                    "spReqHlaA1": "",
                    "spReqHlaA2": "",
                    "spReqHlaB1": "",
                    "spReqHlaB2": "",
                    "spReqHlaC1": "",
                    "spReqHlaC2": "",
                    "spReqHlaBw1": "",
                    "spReqHlaBw2": "",
                    "spReqHpa1_1": "",
                    "spReqHpa1_2": "",
                    "spReqHpa2_1": "",
                    "spReqHpa2_2": "",
                    "spReqHpa3_1": "",
                    "spReqHpa3_2": "",
                    "spReqHpa4_1": "",
                    "spReqHpa4_2": "",
                    "spReqHpa5_1": "",
                    "spReqHpa5_2": "",
                    "spReqHpa6_1": "",
                    "spReqHpa6_2": "",
                    "spReqHpa15_1": "",
                    "spReqHpa15_2": "",
                    "spReqBldTypName": "",
                    "spReqBldTyp": ""}

SP_TYPE = {"M": "002001",
           "N": "002002",
           "S": "002003",
           "s'": "002004",
           "Mia": "002007",
           "P1": "003001",
           "C": "004002",
           "E": "004003",
           "c'": "004004",
           "e": "004005",
           "K": "006001",
           "k'": "006002",
           "Lea": "007001",
           "Leb": "007002",
           "Fya": "008001",
           "Fyb": "008002",
           "Jka": "009001",
           "Jkb": "009002",
           "Dia": "010001"}
