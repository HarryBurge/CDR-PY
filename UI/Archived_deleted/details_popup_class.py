__authour__ = 'Harry Burge'
__date_created__ = '10/06/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '24/06/2020'

# Imports
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QLabel, QComboBox, QLineEdit, QScrollArea

from Utils import config

# Popup
class DetailsPopup(QWidget):
    '''
    Super class of all popups
    '''

    def __init__(self, child, master, name, width, height):
        '''
        params:-
            child : Popup_SubClasss : Popup that needs to inherit code from this Popup class
            master : ScreenManager : The thing that controlls this popup
            width : int : Minimum width of window
            height : int : Minimum height of the window
            name : str : Name to be given to the popup
        '''
        # Makes the child into a QWidget but due to this being a 
        # middle man, the child inherits code from it
        QWidget.__init__(child)

        # Links the screen manager of the popup
        self.master = master

        # Child is the popup inheriting code from popup
        self.child = child

        # Name of the popup, used in screen manager to be able to show screens
        self.name = name

        # Holds the data fields of things that need to be recorded
        self.data_fields = {}

        # Changing window decisions
        self.child.setMinimumSize(width, height)
        self.setWindowTitle(name)

        # Defining Screen
        screen = QGridLayout()
        screen.setContentsMargins(0,0,0,0)
        screen.setSpacing(0)
        screen.setColumnStretch(1, 1)
        screen.setRowStretch(1, 1)

        # Gets layout and puts into the popup
        screen.addLayout(self.child.get_layout(), 0,1,2,1)

        # Sets screen as layout of QWidget
        self.setLayout(screen)


    # Utils
    def top_bar(self, buttons_grid=QGridLayout()):
        '''
        params:-
            buttons_grid : QGridLayout : Buttons to be added to the right of the topbar
        returns:-
            QGridLayout : Layout for a top bar that is called by children screens that want one
        '''
        spacer = QLabel()
        spacer.setFixedSize(10, 40)
        spacer.setStyleSheet("background-color: {};".format(config.bar_colour()))

        # Creates a bar for the top a of a popup
        title = QLabel(self.name)
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        title.setFixedHeight(40)
        title.setStyleSheet("font-size: {}; qproperty-alignment: AlignJustify; font-family: {}; background-color: {}; font-weight: bold;".format(
            config.title_font_size(), config.title_font_family(), config.bar_colour()))

        screen = QGridLayout()
        screen.addWidget(spacer, 0,0)
        screen.addWidget(title, 0,1)
        screen.addLayout(buttons_grid, 0,2)

        return screen

    
    # def get_sql_info_fields(self):
    #     '''
    #     returns:-
    #         QGridLayout : Table of info on that SQL instance, collected with get_sql_instance
    #     '''
    #     # Table to put into the scroll area
    #     table = QGridLayout()
    #     table.setHorizontalSpacing(10)
    #     table.setVerticalSpacing(0)

    #     data_labels = ['Cluster/Host', ' Application', ' Is Cluster?', ' Business Owner', ' Instance', ' Technical Owner', ' SQL Server', ' Maintecnance Window', ' SQL Edition', ' Technical Expert', ' SQL SP', ' SQL Licence VSR', ' SQL Build', ' Decomm Date', ' Collation', ' DNS Alias', ' Max Memory', ' Commissioned Date', ' Min Memory', ' Built By', ' Port', ' Reviewed By', ' Startup Params', ' Business Unit', ' AWE Enabled', ' Enviroment', ' Added to CDR', ' CommVault?', ' Updated By', ' Idera?', ' Updated in CDR', ' Commissioned']
    #     dropdown = {}

    #     # Gets the values to put into above table
    #     data_values = self.get_sqlinstance()

    #     # Adds that data
    #     for index, i in enumerate(data_labels):

    #         if i not in dropdown.keys():
    #             label, inputter = self.typer_input(i)
    #             inputter.setText(data_values[i])
    #             table.addWidget(label, index, 0)
    #             table.addWidget(inputter, index, 1)

    #         else:
    #             label, inputter = self.dropdown_input(i, dropdown[i])
    #             table.addWidget(label, index, 0)
    #             table.addWidget(inputter, index, 1)

    #     return table

    def typer_input(self, label):
        '''
        params:-
            label : str : Text to put into the label
        returns:-
            QLabel : A label with text equal to label param
            QLineEdit : A Editable Line
        '''
        # Puts into the data fields for future reading
        self.data_fields[label] = QLineEdit()

        return QLabel(label), self.data_fields[label]


    def dropdown_input(self, label, options):
        '''
        params:-
            label : str : Text to put into the label
            options : [str, ...] : A List of options that can be choose from
        returns:-
            QLabel : A label with text equal to label param
            QComboBox : A dropdown box
        '''
        # Creates combo box and makes it able for future reading
        self.data_fields[label] = QComboBox()
        self.data_fields[label].addItems(options)

        return QLabel(label), self.data_fields[label]