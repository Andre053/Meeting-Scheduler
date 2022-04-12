import PySimpleGUI as sg

class GuiBuilder:
    def __init__(self):
        print("GuiBuilder initialized")

    def build_users(self, selected, users, current_user):
        if not selected: selected = "Selected Participants"
        else: selected = [users[id][0] for id in selected]
        layout = self.users_layout(selected, users, current_user)
        return sg.Window('Users', layout)

    def users_layout(self, selected, users, current_user):
        treeData = sg.TreeData()
        for user in users:
            if user == current_user: continue # do not add current user to the tree data
            treeData.Insert(parent="", key=user, text=users[user][0], values=[user, users[user][1], users[user][2], users[user][3]])

        return [[
                sg.Tree(
                    data=treeData, 
                    key='-TREE-',
                    headings=['ID', 'Email', 'Job Title', 'Mobile Phone' ],
                    auto_size_columns=True,
                    num_rows=20,
                    col0_width=30,
                    show_expanded=False,
                    enable_events=True,
                    expand_x=True,
                    expand_y=True)
            ], 
            [
                sg.Text(selected, key='-CHOSEN-')
            ],
            [sg.Button('Select', key='-SELECT-'), sg.Button('Confirm', key='-OK-'), sg.Button('Clear', key='-QUIT-')]
            ]
    
    def build_adder(self, added):
        layout = self.adder_layout(added)
        return sg.Window('Add Participant', layout)

    def adder_layout(self, added_users):
        vals = [x[0] + ": " + x[1] for x in added_users]

        return [
            [
                sg.Text("Name"), sg.Input(key='-PART_NAME-')
            ],
            [
                sg.Text("Email"), sg.Input(key='-PART_EMAIL-')
            ],
            [
                sg.Text("Added participants"), sg.Listbox(values=vals, key='-EXTERNAL_PARTICIPANTS-', size=(30, 3))
            ],
            [
                sg.Button('Add', key='-OK-'), sg.Button('Remove', key='-REMOVE-'), sg.Button('Done', key='-QUIT-')
            ]
        ]
    
    def build_remove(self, added):
        layout = self.remove_layout(added)
        return sg.Window('Remove Participant', layout)

    def remove_layout(self, added_users):
        return [
            [
                sg.Text("Email"), sg.Input(key='-REMOVE_EMAIL-')
            ],
            [
                sg.Text("Current participants"), sg.Text(';'.join([','.join(x) for x in added_users]), key='-CURRENT_PARTICIPANTS-')
            ],
            [
                sg.Button('Remove', key='-OK-'), sg.Button('CLOSE', key='-QUIT-')
            ]
        ] 

    def build_sched(self):
        layout = self.sched_layout()
        return sg.Window('Scheduler', layout)

    def sched_layout(self):
        hours = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
        minutes = ['00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55']
        
        # TODO: Make spin buttons loop
        return [
            [sg.Column(
                [
                    [sg.Text('Please choose the meeting parameters.')],
                    [sg.Text('Subject'), sg.Input(key='-SUBJECT-', size=50)],
                    [sg.Text('Content'), sg.Multiline(key='-CONTENT-', size=(48,5))],
                    [sg.Text('Location'), sg.Input(key='-LOCATION-', size=50)],
                    [
                        sg.Text('Select Date', key='-DATE-'), sg.CalendarButton(button_text='Date', format='%Y-%m-%d'),
                        sg.Text('Start'), sg.Spin(values=hours, key='-START_HOUR-', initial_value='00', readonly=True, text_color='#FFFFFF'), sg.Spin(values=minutes, key='-START_MIN-', initial_value='00', readonly=True, text_color='#FFFFFF'), 
                        sg.Text('End'), sg.Spin(values=hours, key='-END_HOUR-', initial_value='00', readonly=True, text_color='#FFFFFF'), sg.Spin(values=minutes, key='-END_MIN-', initial_value='00', readonly=True, text_color='#FFFFFF')
                    ],
                    [sg.Text('Choose Participants'), sg.Button('Select', key='-CHOOSE_PARTICIPANTS-'), sg.Button('Add External', key='-ADD_PARTICIPANTS-')],
                    [sg.Checkbox('Can Reschedule', key="-RESCHED-", default=True, checkbox_color='white'), sg.Checkbox('Online Meeting', key="-ONLINE_MEETING-", default=True)],
                    [sg.Button('Submit', key='-OK-'), sg.Button('Clear All', key='-CLEAR-'), sg.Button('Exit', key='-QUIT-')]
                ],
                element_justification='r')],
        ]

    def build_auth(self):
        layout = self.auth_layout()
        return sg.Window('Authentication', layout)
        
    def auth_layout(self):
        return [
            [sg.Text('Please enter your email')],
            [sg.Input(default_text='mentor@vbbmentoring.onmicrosoft.com', key='-AUTH-')],
            [sg.Button('Ok', key='-OK-'), sg.Button('Quit', key='-QUIT-')]
        ]

    