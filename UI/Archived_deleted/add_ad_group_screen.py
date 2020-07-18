__authour__ = 'Harry Burge'
__date_created__ = '11/06/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '11/06/2020'

# Imports
from PyQt5.QtWidgets import QGridLayout, QScrollArea
from UI.screen_class import Screen

from Utils import config, util


class AddADGroupScreen(Screen):
    '''
    Screen to show user when adding a new AD Group to the CDR database
    '''

    def __init__(self, master, name, width=config.minimum_width(), height=config.minimum_height()):
        super().__init__(self, master, name, width, height)


    def get_layout(self):
        '''
        returns:-
            QGridLayout : Anything that needs to be displayed as a screen, this 
            is used in tandom with the screen class to make inheritance of the menu bar
        '''
        # Sets up a top bar and another section underneath
        self.screen = QGridLayout()
        self.screen.setRowStretch(1, 1)

        # Top Bar
        self.screen.addLayout(super().top_bar(), 0,0)

        # Scrollable area
        scroll = QScrollArea()

        # Table to put into the scroll area
        self.table = QGridLayout()
        self.table.setHorizontalSpacing(10)
        self.table.setVerticalSpacing(0)

        #TODO: Will need to collect data labels if there is variable data fields needed
        data_labels = ['Not Yet Complete']
        dropdown = {}

        # Create a textinput or dropdown for all data_labels
        for index, i in enumerate(data_labels):

            if i not in dropdown.keys():
                label, inputter = self.typer_input(i)
                self.table.addWidget(label, index, 0)
                self.table.addWidget(inputter, index, 1)

            else:
                label, inputter = self.dropdown_input(i, dropdown[i])
                self.table.addWidget(label, index, 0)
                self.table.addWidget(inputter, index, 1)

        # Puts table into scroll area
        scroll.setWidgetResizable(True)
        scroll.setWidget(util.layout_to_QWidget(self.table))

        # Put scroll area into the screen
        self.screen.addWidget(scroll, 1, 0)

        return self.screen