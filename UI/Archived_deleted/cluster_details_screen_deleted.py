__authour__ = 'Harry Burge'
__date_created__ = '10/06/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '23/06/2020'

# Imports
from PyQt5.QtWidgets import QGridLayout, QPushButton, QScrollArea

from UI.popup_class import Popup
from Utils import config


class ClusterDetailsScreen(Popup):

    def __init__(self, master, name, identifier, width=config.minimum_width(), height=config.minimum_height()):
        # Will be used later to identify which Cluster to look at
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

        data_labels = ['SQL Access Point', 'Windows Cluster', 'Num Of Nodes', 'Clustering Method', 'Added To CDR', 'Updated In CDR', 'Host-1', 'Install Date-1', 'Commissioned?-1', 'Host-2', 'Install Date-2', 'Commissioned?-2', 'Notes']
        dropdown = {'Commissioned?-1':['True', 'False'], 'Commissioned?-2':['True','False']}

        # Gets the values to put into above table
        data_values = self.get_cluster(self.identifier)

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
        
    
    def get_cluster(self, identifier):
        '''
        params:-
            identifier : str : Used to get the info to put into the table
        returns:-
            {str:str, ...} : Data format for table above
        '''
        #TODO: Use SQL to get this data
        return {'SQL Access Point':'Point1', 'Windows Cluster':'sure', 'Num Of Nodes':'2', 'Clustering Method':'tom', 'Added To CDR':'24-06-1999', 'Updated In CDR':'one day', 'Host-1':'tim', 'Install Date-1':'This is a date', 'Commissioned?-1':'dkljw', 'Host-2':'hiefbw', 'Install Date-2':'hgfwjkh', 'Commissioned?-2':'fiejh', 'Notes':'this is a test'}
