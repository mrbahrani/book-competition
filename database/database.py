import requests


class Database:
    def __init__(self):
        self.dbUrl = "http://jeld.mohammadmirzaaee.com/"

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
        print("FUck")
        for contest in revised['ContestsList']:
            if 'علامه' in str(contest['Title']):
                print("Do!")
                contest["Title"]=contest["Title"].replace("علامه ی","دانشمند")
                #contest["Title"]=contest["Title"].replace("علامه","دانشمند")
                print(contest)
        return revised

    def login(self,email, username, hashedpassword):
        print(hashedpassword)
        LoginRequest = {"UserName":username,"Password":hashedpassword,"Email":email}
        print(LoginRequest)
        response = requests.post(self.dbUrl + 'DaAuth/Login', json=LoginRequest).json()
        print(response)
        if response["Status"] == 1:
            return response["CustomerId"]
        else:
            return False

    def signup(self,email="shit@gmail.com", username="", password=""):
        signUpRequest = {"Email": email,"UserName":username, "Password":password}
        response = requests.post(self.dbUrl + 'DaAuth/AddCustomer', json=signUpRequest).json()
        print(response,"Hell fuck minaee")
        return response["status"]

    def getprofile(self,userid):
        pass

    def editprofile(self):
        pass

    def joincontest(self,contestid,userid):
        pass

    def getcontest(self,contestid):
        ReadContestRequest = {"ContestId": contestid}
        response = requests.post(self.dbUrl + 'Contest/QuestionsListByContestId', json=ReadContestRequest).json()
        print (response,"Zinab")
        return response["QuestionsList"]

    def getResults(self,contestid):
        ReadContestRequest = {"ContestId": contestid}
        response = requests.post(self.dbUrl + 'Contest/CorrectChoices', json=ReadContestRequest).json()
        return response

    def viewinformation(self,contestid):
        ReadContestRequest = {"ContestId": contestid}
        response = requests.post(self.dbUrl + 'Contest/ReadContest', json=ReadContestRequest).json()
        print(response,"a shoker")
        return response

    def viewranking(self):
        return [{"user":"Ali","point":200},{"user":"Mahhii","point":540},
                {"user":"Ehsan","point":900}, {"user":"Behrooz","point":0} ]
