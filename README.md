### Microsoft Meetings Scheduler

# About

This program is meant to provide online meeting scheduling from a Microsoft Azure application. The users must have an Azure application registered with the permissions to access users within the application and schedule calendar meetings. The required packages for this are included within requirements.txt.

Start this program by running the main.py script within the command line. This version requires environment variables set for all sensitive data (see auth.py).

Once the application is started, you can log in with an email that is part of the Azure Active Directory associated with the app. From here you can easily add other users from the organization, or manually add anyone else. Meeting parameters must be entered, such as the subject, the content, location, start and end time, etc. You can choose whether to have the meeting be rescheduleable, and you can select whether an online video call link will be created along with the meeting.

# Disclaimers

- If the account used to sign into this application does not have permissions within the app it likely will not work. 
- Issues may arise if the account used to sign into the app does not have the online meeting provider that is programmed into the meeting request (see req.py).