import requests


class Database:
    def __init__(self):
        self.dbUrl = "http://jeld.mohammadmirzaaee.com/api/"

    def addConetest(self,title,description, award1, award2,award3, award4,
                    registrationFee, startTime, endTime, startable,
                    customerReferenceID, dealingValue, dealingDescription):
        request = {"Description": description,
                   "Award1": award1,
                   "title": title,
                   "Award2": award2,
                   "Award3": award3,
                   "Award4": award4,
                   "RegistrationFee": registrationFee,
                   "StartTime": startTime,
                   "EndTime": endTime,
                   "StartAble": startable,
                   "CustomerRefId": customerReferenceID,
                   "DealingValue": dealingValue,
                   "DealingDescription": dealingDescription}
        print(request)
        response = requests.post(self.dbUrl+'Contest/AddContest', json=request)
        return response.json()

    def showcontests(self, pagenum):
        req = {"pageNumber": pagenum}
        print(req)
        resp = requests.post(self.dbUrl + 'Contest/ContestsList', json=req)
        revised = resp.json()
        for contest in revised['ContestsList']:
            if 'علامه' in str(contest['Title']):
                print("Do!")
                contest["Title"]=contest["Title"].replace("علامه ی","دانشمند")
                #contest["Title"]=contest["Title"].replace("علامه","دانشمند")
                print(contest["Title"])
        return revised

    def passwordCheck(self,username, hashedpassword):
        if username == "ali" and hashedpassword == '098f6bcd4621d373cade4e832627b4f6':
            return True

        else: return False

    def signup(self,email="shit@gmail.com", username="", password=""):
        return True


