__authour__ = 'Harry Burge'
__date_created__ = '10/06/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '23/06/2020'

# Imports
from PyQt5.QtWidgets import QGridLayout, QPushButton, QScrollArea

from UI.popup_class import Popup
from Utils import config


class SQLInstanceDetailsScreen(Popup):

    def __init__(self, master, name, identifier, width=config.minimum_width(), height=config.minimum_height()):
        # Will be used later to identify which SQLInstance to look at
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

        data_labels = ['Cluster/Host', ' Application', ' Is Cluster?', ' Business Owner', ' Instance', ' Technical Owner', ' SQL Server', ' Maintecnance Window', ' SQL Edition', ' Technical Expert', ' SQL SP', ' SQL Licence VSR', ' SQL Build', ' Decomm Date', ' Collation', ' DNS Alias', ' Max Memory', ' Commissioned Date', ' Min Memory', ' Built By', ' Port', ' Reviewed By', ' Startup Params', ' Business Unit', ' AWE Enabled', ' Enviroment', ' Added to CDR', ' CommVault?', ' Updated By', ' Idera?', ' Updated in CDR', ' Commissioned']
        dropdown = {}

        # Gets the values to put into above table
        data_values = self.get_sqlinstance(self.identifier)

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
        
    
    def get_sqlinstance(self, identifier):
        '''
        params:-
            identifier : str : Used to get the info to put into the table
        returns:-
            {str:str, ...} : Data format for table above
        '''
        #TODO: Use SQL to get this data
        return {'Cluster/Host': 'tim',  ' Application': 'tim',  ' Is Cluster?': 'tim',  ' Business Owner': 'tim',  ' Instance': 'tim',  ' Technical Owner': 'tim',  ' SQL Server': 'tim',  ' Maintecnance Window': 'tim',  ' SQL Edition': 'tim',  ' Technical Expert': 'tim',  ' SQL SP': 'tim',  ' SQL Licence VSR': 'tim',  ' SQL Build': 'tim',  ' Decomm Date': 'tim',  ' Collation': 'tim',  ' DNS Alias': 'tim',  ' Max Memory': 'tim',  ' Commissioned Date': 'tim',  ' Min Memory': 'tim',  ' Built By': 'tim',  ' Port': 'tim',  ' Reviewed By': 'tim',  ' Startup Params': 'tim',  ' Business Unit': 'tim',  ' AWE Enabled': 'tim',  ' Enviroment': 'tim',  ' Added to CDR': 'tim',  ' CommVault?': 'tim',  ' Updated By': 'tim',  ' Idera?': 'tim',  ' Updated in CDR': 'tim',  ' Commissioned': 'tim'}
