__authour__ = 'Harry Burge'
__date_created__ = '10/06/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '23/06/2020'

# Imports
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QMenu, QLabel, QComboBox, QLineEdit, QTextEdit

from Utils import config


# Screen
class Screen(QWidget):
    '''
    Super class of all screens that needs to inherit the menu bar, or other utility
    '''

    def __init__(self, child, master, name, width, height, popup=False):
        '''
        params:-
            child : Screen_SubClasss : Screen that needs to inherit code from this screen class
            master : ScreenManager : The thing that controlls this screen
            width : int : Minimum width of window
            height : int : Minimum height of the window
            name : str : Name to be given to the screen
        '''
        # Makes the child into a QWidget but due to this being a 
        # middle man, the child inherits code from it
        QWidget.__init__(child)

        # Links the screen manager of the screen
        self.master = master

        # Child is the screen inheriting code from screen
        self.child = child

        # Name of the screen, used in screen manager to be able to show screens
        self.name = name

        # Holds the data fields of things that need to be recorded
        self.data_fields = {}

        # Changing window decisions
        self.child.setMinimumSize(width, height)
        self.setWindowTitle(name)

        # Inherited design
        screen = QGridLayout()
        screen.setContentsMargins(0,0,0,0)
        screen.setSpacing(0)
        screen.setColumnStretch(1, 1)
        # screen.setRowStretch(1, 1)

        if popup == False:
            screen.addLayout(self.side_bar(), 0, 0)

        # Gets childs layout and puts into the screen
        screen.addLayout(self.child.get_layout(), 0,1)

        # Sets screen as layout of QWidget
        self.setLayout(screen)


    # Utils
    def side_bar(self):
        # Menu Button also uses context menu to change screens
        self.menu_button = QPushButton('Menu')
        self.menu_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.menu_button.setFixedSize(40, 40)
        self.menu_button.setStyleSheet("background-color: {}".format(config.bar_colour()))
        self.menu_button.clicked.connect(self.contextMenuEvent)

        # Fill up the rest of the bar with a label
        sidebar = QLabel('')
        sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sidebar.setFixedWidth(40)
        sidebar.setStyleSheet("background-color: {}".format(config.bar_colour()))

        screen = QGridLayout()
        screen.setContentsMargins(0,0,0,0)
        screen.setSpacing(0)
        # screen.setColumnStretch(1, 1)
        screen.setRowStretch(1, 1)

        screen.addWidget(self.menu_button, 0,0)
        screen.addWidget(sidebar, 1,0)

        return screen


    def top_bar(self, buttons_grid=QGridLayout(), extra_text=None):
        '''
        params:-
            buttons_grid : QGridLayout : Buttons to be added to the right of the topbar
        returns:-
            QGridLayout : Layout for a top bar that is called by children screens that want one
        '''
        spacer = QLabel()
        spacer.setFixedSize(10, 40)
        spacer.setStyleSheet("background-color: {};".format(config.bar_colour()))

        # Creates a bar for the top a of a screen
        title = QLabel(self.name if extra_text == None else self.name + ' - ' + extra_text)
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        title.setFixedHeight(40)
        title.setStyleSheet("font-size: {}; qproperty-alignment: AlignJustify; font-family: {}; background-color: {}; font-weight: bold;".format(
            config.title_font_size(), config.title_font_family(), config.bar_colour()))

        screen = QGridLayout()
        screen.addWidget(spacer, 0,0)
        screen.addWidget(title, 0,1)
        screen.addLayout(buttons_grid, 0,2)

        return screen


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

    
    def button_input(self, label, function):
        self.data_fields[label] = QPushButton()
        self.data_fields[label].clicked.connect(function)

        return QLabel(label), self.data_fields[label]


    def text_input(self, label):
        self.data_fields[label] = QTextEdit()
        return QLabel(label), self.data_fields[label]


    def popup_table(self, data_labels, dropdown, data_values):
        # Table to put into the scroll area
        table = QGridLayout()
        table.setHorizontalSpacing(10)
        table.setVerticalSpacing(0)

        if len(data_values) == 1:

            # Adds that data
            for data_label, column, row, column_span, row_span, enable, buttonb in data_labels:

                try:
                    if buttonb != False:
                        label, inputter = self.typer_input('Failure')

                        if data_label == 'Host Name':
                            label, inputter = self.button_input(data_label, buttonb.button_open_host(str(data_values[0]['source']), str(data_values[0]['nodeID'])))
                            inputter.setText(str(data_values[0]['Host Name']))

                    # Inputbox <- Value
                    elif data_label not in dropdown.keys():
                        label, inputter = self.typer_input(data_label)

                        if data_label == 'Notes':
                            label, inputter = self.text_input(data_label)
                            inputter.setFixedHeight(100)

                        inputter.setText(str(data_values[0][data_label]))
                        if enable: inputter.textChanged.connect(self.something_changed(inputter, str(data_values[0][data_label])))

                    # Dropdown <- Value
                    else:
                        label, inputter = self.dropdown_input(data_label, dropdown[data_label])
                        for i in range(inputter.count()):
                            if inputter.itemText(i) == str(data_values[0][data_label]):
                                inputter.setCurrentIndex(i)
                        
                        if enable: inputter.currentTextChanged.connect(self.something_changed(inputter, str(data_values[0][data_label])))

                    if type(inputter) in [QComboBox, QPushButton]:
                        inputter.setEnabled(enable)
                        if enable:
                            inputter.setStyleSheet("background-color: {};".format(config.searchtable_background()))

                    else:
                        inputter.setReadOnly(not enable)
                        if not enable:
                            inputter.setStyleSheet("background-color: {};".format(config.popup_readonly_colour()))


                    # Add to table
                    table.addWidget(label, row, column*2, row_span, column_span*2-1)
                    table.addWidget(inputter, row, column*2+1, row_span, column_span*2-1)

                    # table.setColumnMinimumWidth(column*2, 100)
                    table.setColumnStretch(column*2+1, 1)

                except KeyError:
                    pass

        return table


    # Funcs
    def contextMenuEvent(self):
        '''
        returns:-
            None : Checks based on event what needs to be done
        '''
        contextMenu = QMenu(self)

        # Creates clickable buttons
        addHost = contextMenu.addAction("Add New Host")
        addCluster = contextMenu.addAction("Add New Cluster")
        addSqlInstance = contextMenu.addAction("Add New SQL Server Instance")
        search = contextMenu.addAction("Search")

        # Makes an action equal to what you click on the context menu
        action = contextMenu.exec_(self.mapToGlobal(self.menu_button.pos()))

        # Does action based on what was pressed
        if action == addHost:
            self.master.show_screen('Add Host Screen')

        elif action == addCluster:
            self.master.show_screen('Add Cluster Screen')

        elif action == addSqlInstance:
            self.master.show_screen('Add SQL Server Instance Screen')

        elif action == search:
            self.master.show_screen('CDR')

    # Button
    def something_changed(self, inputter, key):
        def temp():
            if (type(inputter) == QLineEdit and inputter.text() != key) or (type(inputter) == QTextEdit and inputter.toPlainText() != key) or (type(inputter) == QComboBox and inputter.currentText() != key):

                inputter.setStyleSheet("background-color: {};".format(config.popup_changed_colour()))
            else:
                inputter.setStyleSheet("background-color: {};".format(config.searchtable_background()))
        return temp