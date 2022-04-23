from time import time
import requests as req, json # make API requests and format json response

from auth import Service

class Api(Service):
    """
    This class inherits Service, allowing for the authentication of the application
    The API class contains methods to query the API

    """

    def __init__(self):
        super().__init__() # runs the super class constructor
        self.base_url = "https://graph.microsoft.com/{0}".format(self.version)
        self.header = {"Authorization": "Bearer " + self.token}

    def get_users(self):

        """
        User details

        - displayName
        - givenName
        - mail
        - id
        - jobTitle
        - businessPhone

        
        """
        url = self.base_url + "/users"

        users = {}
        res = req.get(url, headers=self.header)
        if res.status_code == 200:
            res = res.json()
            for user in res["value"]:
                if user["mail"] == None: user["mail"] == ""
                users[user["id"]] = (user["displayName"], user["mail"], user["jobTitle"], user["mobilePhone"])
                
        else: print("Error querying users")
        return users

    def create_meeting(self, user_id, subject, content, start_time, end_time, location, attendees, is_online_meeting=False, new_time_proposals=False):
        """
        This request assumes that the application host user has 
        teamsForBusiness as an online meeting provider
        
        """
        url = "{0}/users/{1}/calendar/events".format(self.base_url, user_id)

        # date is YYYY-MM-DDT23:59
        # attendees should be email and names
        payload = {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": content
            },
            "start": {
                "dateTime": start_time,
                "timeZone": "Eastern Standard Time"
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "Eastern Standard Time"
            },
            "location":{
                "displayName": location
            },
            "attendees": attendees,
            "allowNewTimeProposals": new_time_proposals,
            "isOnlineMeeting": is_online_meeting,
            "onlineMeetingProvider": "teamsForBusiness"
        }
        res = req.post(url, headers=self.header, json=payload)
        print("\n", res.status_code)

""" Example Package
    {
  "subject": "Let's go for lunch",
  "body": {
    "contentType": "HTML",
    "content": "Does noon work for you?"
  },
  "start": {
      "dateTime": "2017-04-15T12:00:00",
      "timeZone": "Pacific Standard Time"
  },
  "end": {
      "dateTime": "2017-04-15T14:00:00",
      "timeZone": "Pacific Standard Time"
  },
  "location":{
      "displayName":"Harry's Bar"
  },
  "attendees": [
    {
      "emailAddress": {
        "address":"samanthab@contoso.onmicrosoft.com",
        "name": "Samantha Booth"
      },
      "type": "required"
    }
  ],
  "allowNewTimeProposals": true,
  "transactionId":"7E163156-7762-4BEB-A1C6-729EA81755A7"
}
"""