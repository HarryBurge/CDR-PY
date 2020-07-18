__authour__ = 'Harry Burge'
__date_created__ = '24/06/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '24/06/2020'

# Imports
from PyQt5.QtWidgets import QGridLayout, QPushButton, QScrollArea

from UI.DetailsPopup.host_details_screen import HostDetailsScreen
from UI.details_popup_class import DetailsPopup
from Utils import config


class StandaloneDetailsScreen(DetailsPopup):

    def __init__(self, master, name, width=config.minimum_width(), height=config.minimum_height()):
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
        screen.addLayout(self.top_bar(), 0,0)

        # Scrollable area
        scroll = QScrollArea()

        table = self.get_sql_info_fields()

        # Puts table into scroll area
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.layout_to_QWidget(table))

        screen.addWidget(scroll, 1, 0)

        # Adds the more info buttons
        screen.addLayout(self.extra_info_buttons(), 2,0)

        return screen

    
    def extra_info_buttons(self):
        '''
        returns:-
            QGridLayout() : Returns the buttons needed to do more info section
        '''
        screen = QGridLayout()
        buttonnodes = []

        for node in ['1','2']:
            # Makes a button for that node
            temp = QPushButton(text=node)
            temp.clicked.connect(lambda: self.button_open_host())
            buttonnodes.append(temp)

        for button in buttonnodes:
            screen.addWidget(button)

        return screen


    def button_open_host(self):
        '''
        returns:-
            None : Opens up a host details popup
        '''
        self.master.add_popup(HostDetailsScreen(self.master, 'HostDetailsScreen'))