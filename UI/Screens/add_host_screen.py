__authour__ = 'Harry Burge'
__date_created__ = '10/06/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '10/06/2020'

# Imports
from PyQt5.QtWidgets import QGridLayout, QScrollArea, QPushButton, QComboBox, QLineEdit
from UI.screen_class import Screen

from Utils import config, util, sqlcommands


class AddHostScreen(Screen):
    '''
    Screen to show user when adding a new Host to the CDR database
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

        # Update Button
        create_host_button = QPushButton('Create&Close')
        create_host_button.setFixedSize(80, 40)
        create_host_button.clicked.connect(lambda: self.create_host_button())

        # Top bar buttons <- Update Button
        topbar_buttons = QGridLayout()
        topbar_buttons.addWidget(create_host_button, 0,0)

        # Top Bar
        self.screen.addLayout(super().top_bar(topbar_buttons), 0,0)

        # Scrollable area
        scroll = QScrollArea()

        # Table to put into the scroll area
        self.table = QGridLayout()
        self.table.setHorizontalSpacing(10)
        self.table.setVerticalSpacing(0)

        self.data_labels = [('domain', '', 0,0, 1,1, True), ('hostName', '', 1,0, 1,1, True), ('vsr', 'N/A', 2,0, 1,1, True), ('region', 'EU', 3,0, 1,1, True), ('location', 'LN', 4,0, 1,1, True), ('primaryBU', '', 5,0, 1,1, True), ('description', '', 0,1, 1,1, True), ('maintenanceWindow', '18:00-08:00(GMT)', 1,1, 1,1, True), ('builtBy', 'Server Team', 2,1, 1,1, True), ('builtByPeerReviewedBy', '', 3,1, 1,1, False), ('hostState', 'Commissioned', 4,1, 1,1, True), ('commissionedDate', '', 5,1, 1,1, False), ('temporaryStateExpirydate', '', 6,1, 1,1, False), ('DRTier', '', 7,1, 1,1, True), ('SentryOne?', '', 8,1, 1,1, True), ('Notes', '', 9,0, 1,3, False)]
        dropdown = {'location':[None] + sqlcommands.get_locations(), 'primaryBU':[None] + sqlcommands.get_business_units(), 'hostState':['Commissioned', 'Decommissioned'], 'domain':['.hiscox.com', '.hiscox.nonprod'], 'region':sqlcommands.get_regions(), 'DRTier':sqlcommands.get_drtiers(), 'SentryOne?':['Yes', 'No']}

        # Create a textinput or dropdown for all data_labels
        for i, default, row, col, row_s, col_s, null_not_allowed in self.data_labels:

            if i not in dropdown.keys():
                label, inputter = self.typer_input(i if not null_not_allowed else str(i) + '*')
                inputter.setText(default)
                self.table.addWidget(label, row, col*2, row_s, col_s)
                self.table.addWidget(inputter, row, col*2+1, row_s, col_s)

            else:
                label, inputter = self.dropdown_input(i if not null_not_allowed else str(i) + '*', dropdown[i])
                self.table.addWidget(label, row, col*2, row_s, col_s)
                self.table.addWidget(inputter, row, col*2+1, row_s, col_s)

        # Puts table into scroll area
        scroll.setWidgetResizable(True)
        scroll.setWidget(util.layout_to_QWidget(self.table))

        # Put scroll area into the screen
        self.screen.addWidget(scroll, 1, 0)

        return self.screen
        
    
    def create_host_button(self):
        # Need to do check for nulls and see if they all have values
        for label, default, row, col, row_s, col_s, null_not_allowed in self.data_labels:
            temp = self.data_fields[label if not null_not_allowed else str(label + '*')]

            if null_not_allowed:
                if type(temp) == QLineEdit and temp.text() == '':
                    break
                elif type(temp) == QComboBox and temp.currentText() in [None, '']:
                    break
            else:
                if type(temp) == QLineEdit and temp.text() == '':
                    temp.setText('NULL')
                elif type(temp) == QLineEdit:
                    temp.setText('\''+temp.text()+'\'')

        else:
            sqlcommands.upsert_host(
                source= 'P' if self.data_fields['domain*'].currentText() == '.hiscox.com' else 'N',
                hostname= '\''+self.data_fields['hostName*'].text() + self.data_fields['domain*'].currentText()+'\'',
                vsr= self.data_fields['vsr*'].text(),
                region= '\''+self.data_fields['region*'].currentText()+'\'', 
                location= '\''+self.data_fields['location*'].currentText()+'\'', 
                primaryBU= '\''+self.data_fields['primaryBU*'].currentText()+'\'', 
                description= self.data_fields['description*'].text(), 
                maintenanceWindow= self.data_fields['maintenanceWindow*'].text(), 
                builtBy= self.data_fields['builtBy*'].text(), 
                builtByPeerReviewedBy= self.data_fields['builtByPeerReviewedBy'].text(), 
                hostState= '\''+self.data_fields['hostState*'].currentText()+'\'', 
                commissionedDate= self.data_fields['commissionedDate'].text(), 
                temporaryStateExpiryDate= self.data_fields['temporaryStateExpirydate'].text(), 
                refreshData= '\'N\''
            )

            sqlcommands.upsert_host_extras(
                source= 'P' if self.data_fields['domain*'].currentText() == '.hiscox.com' else 'N',
                hostname= '\''+self.data_fields['hostName*'].text() + self.data_fields['domain*'].currentText()+'\'',
                drtier= '\''+self.data_fields['DRTier*'].currentText()+'\'',
                sentryone= '\''+self.data_fields['SentryOne?*'].currentText()+'\'',
                notes= self.data_fields['Notes'].text()
            )
            self.close()
            return

        print('Failed Search')

        
