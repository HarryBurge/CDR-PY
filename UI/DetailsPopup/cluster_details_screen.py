__authour__ = 'Harry Burge'
__date_created__ = '03/07/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '03/07/2020'

# Imports
from PyQt5.QtWidgets import QGridLayout, QPushButton, QScrollArea

from UI.DetailsPopup.host_details_screen import HostDetailsScreen
from UI.screen_class import Screen
from Utils import config, sqlcommands, util


class ClusterDetailsScreen(Screen):

    def __init__(self, master, name, identifier, width=config.minimum_width(), height=config.minimum_height()):
        self.identifier = identifier
        super().__init__(self, master, name, width, height, True)


    def get_layout(self):
        '''
        returns:-
            QGridLayout : Anything that needs to be displayed as a popup, this 
            is used in tandom with the popup class for inheritance
        '''
        # Top bar buttons <- Update Button
        topbar_buttons = QGridLayout()

        # Preset layout
        data_labels = config.cluster_details_screen_layout()
        dropdown = self.get_dropdowns()

        node_labels = config.cluster_nodes_screen_layout(self)
        node_dropdowns = {}

        # Gets values with SQL Command
        data_values = self.get_cluster()

        # Makes table
        table = QGridLayout()
        for i, node in enumerate(data_values):
            table.addLayout(self.popup_table(node_labels, node_dropdowns, [node]), i+1, 0)
        table.addLayout(self.popup_table(data_labels, dropdown, data_values[:1]), 0, 0)

        # Scrollable area <- Table
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(util.layout_to_QWidget(table))

        # Screen <- Topbar and Scroll Table
        screen = QGridLayout()
        screen.setRowStretch(1, 1)
        screen.addLayout(super().top_bar(topbar_buttons, data_values[0]['Windows Cluster Name']), 0,0)
        screen.addWidget(scroll, 1, 0)

        return screen
    
    def get_cluster(self):
        '''
        params:-
            identifier : str : Used to get the info to put into the table
        returns:-
            {str:str, ...} : Data format for table above
        '''
        return sqlcommands.get_cluster_info(*self.identifier)

    def get_dropdowns(self):
        return {}

    
    def update(self):
        print('Update')


    def button_open_host(self, source, data):
        def temp():
            '''
            params:-
                data : Misc : Will be used to specify which data point should be shown
            returns:-
                None : Creates a popup with the info on
            '''
            self.master.add_popup(HostDetailsScreen(self.master, 'Host Details Screen', (source, data)))
        return temp