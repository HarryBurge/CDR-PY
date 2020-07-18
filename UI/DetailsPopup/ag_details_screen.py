__authour__ = 'Harry Burge'
__date_created__ = '07/07/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '07/07/2020'

# Imports
from PyQt5.QtWidgets import QGridLayout, QPushButton, QScrollArea

from UI.DetailsPopup.host_details_screen import HostDetailsScreen
from UI.screen_class import Screen
from Utils import config, sqlcommands, util


class AGDetailsScreen(Screen):

    def __init__(self, master, name, identifier, width=config.minimum_width(), height=config.minimum_height()):
        self.identifier = identifier
        super().__init__(self, master, name, width, height, True)


    def get_layout(self):
        '''
        returns:-
            QGridLayout : Anything that needs to be displayed as a popup, this 
            is used in tandom with the popup class for inheritance
        '''
        # Update Button
        update_button = QPushButton('Update')
        update_button.setFixedSize(80, 40)
        update_button.clicked.connect(lambda: self.update())

        # Top bar buttons <- Update Button
        topbar_buttons = QGridLayout()
        topbar_buttons.addWidget(update_button, 0,0)

        # Gets values with SQL Command
        data_values = self.get_ag()

        if len(data_values) != 0:
            testag = data_values[0]
            diffrent = False

            for ag in data_values:
                for tag in ['AG Name', 'Listener', 'Port', 'AG role']:
                    if ag[tag] != testag[tag]:
                        diffrent = True

        if len(data_values) != 0 and not diffrent:
            # Preset layout
            data_labels = [('serverID', 0,0, 1,1, False, False), ('AG Name', 0,1, 1,1,False, False), ('Listener', 1,1, 1,1, False, False), ('Port', 2,1, 1,1, False, False), ('AG role', 3,1, 1,1, False, False)]
            dropdown = self.get_dropdowns()

            databases_labels = [('Database Name', 0,0, 1,1, False, False)]
            databases_dropdowns = {}
        else:
            # Preset layout
            data_labels = [('serverID', 0,0, 1,1, False, False)]
            dropdown = self.get_dropdowns()

            databases_labels = [('Database Name', 0,1, 1,1, False, False), ('AG Name', 0,0, 1,1, False, False), ('Listener', 1,0, 1,1, False, False), ('Port', 2,0, 1,1, False, False), ('AG role', 3,0, 1,1, False, False)]
            databases_dropdowns = {}

        # Makes table
        table = QGridLayout()
        for i, node in enumerate(data_values):
            table.addLayout(self.popup_table(databases_labels, databases_dropdowns, [node]), i+1, 0)

        table.addLayout(self.popup_table(data_labels, dropdown, data_values[:1]), 0, 0)

        # Scrollable area <- Table
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(util.layout_to_QWidget(table))

        # Screen <- Topbar and Scroll Table
        screen = QGridLayout()
        screen.setRowStretch(1, 1)
        screen.addLayout(super().top_bar(topbar_buttons, data_values[0]['Server Name']), 0,0)
        screen.addWidget(scroll, 1, 0)

        return screen
    
    def get_ag(self):
        '''
        params:-
            identifier : str : Used to get the info to put into the table
        returns:-
            {str:str, ...} : Data format for table above
        '''
        return sqlcommands.get_ag_info(*self.identifier)

    def get_dropdowns(self):
        return {}

    
    def update(self):
        print('Update')