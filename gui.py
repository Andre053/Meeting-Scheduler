import PySimpleGUI as sg
from gui_builder import GuiBuilder

class Gui:
    """
    The GUI class contains all initializations of graphical windows and the program loops
    The constructor takes a list of users that are part of the Azure Active Directory, it 
    also takes an instance of the API class so that it can make the API calls internally
    
    """

    def __init__(self, users, api_instance):
        self.theme = sg.theme()   # Add a touch of color  
        self.users = users
        self.emails = {users[key][1]:key for key in users}
        self.api = api_instance
        self.current_user = None
        self.added = []
        self.gui_builder = GuiBuilder()
        self.program_loop()


    def program_loop(self):
        running = True
        while True: 
            a_window = self.gui_builder.build_auth()
            while True: 
                event, values = a_window.read()
                if event == sg.WIN_CLOSED or event == '-QUIT-':
                    running = False
                    break
                if event == '-OK-':
                    email = a_window['-AUTH-'].get()
                    if email in self.emails:
                        authorized = True
                        self.current_user = self.emails[email] # current user id
                        break
            a_window.close()
            if not running: break
            self.event_loop()


    def event_loop(self):
        s_window = self.gui_builder.build_sched()
        selected = [] # empty array so if never set it does not cause an error when iteration is attempted
        while True:
            event, values = s_window.read()
            if event == sg.WIN_CLOSED or event == '-QUIT-': # if user closes window or clicks cancel
                break
            if event == '-CHOOSE_PARTICIPANTS-':
                u_window = self.gui_builder.build_users(selected, self.users, self.current_user)

                # start user window
                while True: 
                    u_event, u_values = u_window.read()
                    if u_event == sg.WIN_CLOSED or u_event == '-QUIT-': # if user closes window or clicks cancel
                        selected = None
                        break
                    if u_event == '-OK-':
                        if u_window['-CHOSEN-'].get() == 'Selected': continue
                        break
                    if u_event == '-SELECT-':
                        selected_names = [self.users[key][0] for key in u_values['-TREE-']]
                        u_window['-CHOSEN-'].update(selected_names)
                        selected = u_values['-TREE-']
                u_window.close()


            if event == '-ADD_PARTICIPANTS-':
                e_window = self.gui_builder.build_adder(self.added)
                

                while True:
                    e_event, e_values = e_window.read()
                    if e_event == sg.WIN_CLOSED or e_event == '-QUIT-':
                        break

                    if e_event == '-OK-':
                        name = e_window['-PART_NAME-'].get()
                        email = e_window['-PART_EMAIL-'].get()
                        print(f"Added participant {name} with email {email}")
                        if name and email:
                            self.added.append((name, email))
                            display = [x[0] + ": " + x[1] for x in self.added]
                            e_window['-EXTERNAL_PARTICIPANTS-'].update(display)
                        else: print("Input is invalid")
                        e_window['-PART_NAME-'].update(None)
                        e_window['-PART_EMAIL-'].update(None)

                    if e_event == '-REMOVE-':
                        # loop through all selected users
                        i = 0 # counter in the self.added list
                        for val in e_values['-EXTERNAL_PARTICIPANTS-']:
                            while True:
                                if self.added[i] == val: 
                                    self.added.pop(i)
                                    i += 1
                                    break
                                i += 1
                        e_window['-EXTERNAL_PARTICIPANTS-'].update(self.added)


                e_window.close()

            # helper function

            def clear(s_window):
                s_window['-SUBJECT-'].update('')
                s_window['-CONTENT-'].update('')
                s_window['-LOCATION-'].update('')
                s_window['-DATE-'].update('Select Date')
                s_window['-START_HOUR-'].update('00')
                s_window['-START_MIN-'].update('00')
                s_window['-END_HOUR-'].update('00')
                s_window['-END_HOUR-'].update('00')
                s_window['-RESCHED-'].update(True)
                s_window['-ONLINE_MEETING-'].update(True)
                self.added = []

            if event == '-CLEAR-':
                clear(s_window)
                selected = None


                
            if event == '-OK-':
                
                subject = s_window['-SUBJECT-'].get()
                content = s_window['-CONTENT-'].get()
                location = s_window['-LOCATION-'].get()

                print("Selected:", selected, "Added:", self.added)

                # add error handling for if selected is empty
                names = [self.users[key][0] for key in selected] + [x[0] for x in self.added]
                emails = [self.users[key][1] for key in selected] + [x[1] for x in self.added]
                resched_permitted = s_window['-RESCHED-'].get()
                has_online_meeting = s_window['-ONLINE_MEETING-'].get()
                
                attendees = []

                # error check
                if len(emails) != len(names):
                    print("Emails and names do not match")
                    continue

                for i in range(len(emails)):
                    email = emails[i]
                    name = names[i]
                    attendees.append({
                        "emailAddress": {
                            "address": email,
                            "name": name
                        },
                        "type": "required"
                    })
                date = s_window['-DATE-'].get()
                start = date + 'T' + s_window['-START_HOUR-'].get() + ":" + s_window['-START_MIN-'].get()
                end = date + 'T' + s_window['-END_HOUR-'].get() + ":" + s_window['-END_MIN-'].get()

                if not selected or not emails or not location or not subject or not content or not attendees: continue
                
                
                result = sg.popup_yes_no(
                    f"""
                    Confirm the following details
                    User = {self.current_user}
                    Subject = {subject}
                    Content = {content}\n
                    Start time = {start}
                    End time = {end}
                    Location = {location}\n
                    Emails = {', '.join(emails)}
                    Names = {', '.join(names)}\n
                    New Time Proposals = {resched_permitted}
                    Online Meeting = {has_online_meeting}
                    
                    """,
                    title="Confirm your meeting parameters",
                    line_width=100)

                if result == "Yes": # clear before calling create_meeting
                    clear(s_window)
                    selected = None

                if result == "Yes": # could make this an async call so we do not wait for the window to clear if the request is slow
                    self.api.create_meeting(
                        user_id=self.current_user, 
                        subject=subject, 
                        content=content, 
                        start_time=start, 
                        end_time=end, 
                        location=location, 
                        attendees=attendees,
                        is_online_meeting=has_online_meeting,
                        new_time_proposals=resched_permitted
                    )
                

                

        s_window.close()