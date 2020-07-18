__authour__ = 'Harry Burge'
__date_created__ = '10/06/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '23/06/2020'

# Imports
from PyQt5.QtWidgets import QGridLayout, QPushButton, QScrollArea

from UI.popup_class import Popup
from Utils import config


class HostDetailsScreen(Popup):

    def __init__(self, master, name, identifier, width=config.minimum_width(), height=config.minimum_height()):
        # Will be used later to identify which Host to look at
        self.identifier = identifier

        super().__init__(self, master, name, width, height)


    def get_layout(self):
        '''
        returns:-
            QGridLayout : Anything that needs to be displayed as a popup, this 
            is used in tandom with the popup class for inheritance
        '''
        # Sets up a top bar and another section underneath
        screen = QGridLayout()
        screen.setRowStretch(1, 1)

        # Top Bar
        screen.addLayout(super().top_bar(), 0,0)

        # Scrollable area
        scroll = QScrollArea()

        # Table to put into the scroll area
        table = QGridLayout()
        table.setHorizontalSpacing(10)
        table.setVerticalSpacing(0)

        data_labels = ['Host', 'Domain', 'Is Cluster?', 'Last Reboot', 'SQL AP', 'Install Date', 'Model', 'Commissioned Date', 'OS Bit', 'Decomm Date', 'OS Edition', 'Cluster?', 'OS Build', 'Processors', 'Reviewed By', 'Cores', 'DR Tier', 'OS Memory', 'Primary Bu', 'Added to CDR', 'Host Location', 'Updated By', 'SolarWinds?', 'Updated in CDR', 'Commissioned', 'IP Addresses', 'Notes']
        dropdown = {'Is Cluster?':['True','False'], 'Cluster?':['True','False'], 'SolarWinds?':['True','False']}


        # Gets the values to put into above table
        data_values = self.get_host(self.identifier)

        # Adds that data
        for index, i in enumerate(data_labels):

            if i not in dropdown.keys():
                label, inputter = self.typer_input(i)
                inputter.setText(data_values[i])
                table.addWidget(label, index, 0)
                table.addWidget(inputter, index, 1)

            else:
                label, inputter = self.dropdown_input(i, dropdown[i])
                table.addWidget(label, index, 0)
                table.addWidget(inputter, index, 1)

        # Puts table into scroll area
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.layout_to_QWidget(table))

        screen.addWidget(scroll, 1, 0)

        return screen
        
    
    def get_host(self, identifier):
        '''
        params:-
            identifier : str : Used to get the info to put into the table
        returns:-
            {str:str, ...} : Data format for table above
        '''
        #TODO: Use SQL to get this data
        return {'Host':'tom', 'Domain':'tom', 'Last Reboot':'tom', 'SQL AP':'tom', 'Install Date':'tom', 'Model':'tom', 'Commissioned Date':'tom', 'OS Bit':'tom', 'Decomm Date':'tom', 'OS Edition':'tom', 'OS Build':'tom', 'Processors':'tom', 'Reviewed By':'tom', 'Cores':'tom', 'DR Tier':'tom', 'OS Memory':'tom', 'Primary Bu':'tom', 'Added to CDR':'tom', 'Host Location':'tom', 'Updated By':'tom', 'Updated in CDR':'tom', 'Commissioned':'tom', 'IP Addresses':'tom', 'Notes':'tom'}
