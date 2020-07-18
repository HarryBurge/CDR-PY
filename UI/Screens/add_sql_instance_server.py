__authour__ = 'Harry Burge'
__date_created__ = '10/06/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '10/06/2020'

# Imports
from PyQt5.QtWidgets import QGridLayout, QScrollArea, QPushButton, QComboBox, QLineEdit
from UI.screen_class import Screen

from Utils import config, util, sqlcommands


class AddSQLInstanceScreen(Screen):
    '''
    Screen to show user when adding a new SQL Instance to the CDR database
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
        create_host_button.clicked.connect(lambda: self.create_server_button())

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

        self.data_labels = [('domain', '', 4,0, 1,1, True), ('instanceName', 'MSSQLSERVER', 1,0, 1,1, True), ('clusterName', '', 3,0, 1,1, False), ('Enviroment', '', 0,1, 1,1, True), ('postConfigBy', '', 1,1, 1,1, False), ('postConfigByPeerReviewedBy', '', 2,1, 1,1, False), ('ServerState', 'Commissioned', 3,1, 1,1, True), ('Host Type', 'Cluster', 0,0, 1,1, True), ('SQL Host', 'Failed', 5,1, 1,1, True), ('Business Unit', '', 6,1, 1,1, True), ('thirdPartybackups', '', 7,1, 1,1, True), ('SQL Monitoring', '', 8,1, 1,1, True), ('Commissioned Date', '', 9,1, 1,1, False), ('Decommissioned Date', '', 10,1, 1,1, False), ('DNSAlias', '', 11,1, 1,1, False)]
        dropdown = {'ServerState':['Commissioned', 'Decommissioned'], 'Host Type':['Standalone','Cluster'], 'SQL Host':['Failed'], 'hostName':[None] + sqlcommands.get_host_name(), 'domain':['.hiscox.com', '.hiscox.nonprod'], 'Business Unit':sqlcommands.get_business_units(), 'thirdPartybackups':['Yes', 'No'], 'SQL Monitoring':['Yes', 'No'], 'Enviroment':sqlcommands.get_enviroments()}

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
                if i == 'Host Type':
                    temp = inputter
                    temp.currentTextChanged.connect(lambda: self.host_type_changed(temp.currentText()))
                    self.table.addWidget(temp, row, col*2+1, row_s, col_s)
                else:
                    self.table.addWidget(inputter, row, col*2+1, row_s, col_s)

        # Puts table into scroll area
        scroll.setWidgetResizable(True)
        scroll.setWidget(util.layout_to_QWidget(self.table))

        # Put scroll area into the screen
        self.screen.addWidget(scroll, 1, 0)

        # Update the data field
        self.data_fields['SQL Host*'].clear()
        self.host_type_changed(self.data_fields['Host Type*'].currentText())

        return self.screen


    def host_type_changed(self, text):
        self.data_fields['SQL Host*'].clear()

        if text == 'Cluster':
            self.data_fields['SQL Host*'].addItems(sqlcommands.get_cluster_hosts())
            self.data_fields['clusterName'].setEnabled(True)
        else:
            self.data_fields['SQL Host*'].addItems(sqlcommands.get_standalone_hosts())
            self.data_fields['clusterName'].setEnabled(False)
            self.data_fields['clusterName'].setText('')


    def create_server_button(self):
        pass
        # Need to do check for nulls and see if they all have values
        for label, default, row, col, row_s, col_s, null_not_allowed in self.data_labels:
            temp = self.data_fields[label if not null_not_allowed else str(label + '*')]

            if null_not_allowed:
                if type(temp) == QLineEdit and temp.text() == '':
                    break
            else:
                if type(temp) == QLineEdit and temp.text() == '':
                    temp.setText('NULL')
                elif type(temp) == QLineEdit:
                    temp.setText('\''+temp.text()+'\'')

        else:
            sqlcommands.upsert_server(
                source= 'P' if self.data_fields['domain*'].currentText() == '.hiscox.com' else 'N', 
                instanceName= self.data_fields['instanceName*'].text(), 
                hostName= '\''+self.data_fields['SQL Host*'].currentText()+'\'', 
                clusterName= self.data_fields['clusterName'].text(), 
                status= '\''+sqlcommands.get_enviroment_code(self.data_fields['Enviroment*'].currentText())+'\'', 
                postConfigBy= self.data_fields['postConfigBy'].text(), 
                postConfigPeerReviewedBy= self.data_fields['postConfigByPeerReviewedBy'].text(), 
                serverState= '\''+self.data_fields['ServerState*'].currentText()+'\'', 
                refreshData= '\'N\''
            )

            sqlcommands.upsert_server_extras(
                source= 'P' if self.data_fields['domain*'].currentText() == '.hiscox.com' else 'N', 
                instanceName= self.data_fields['instanceName*'].text(), 
                hostname= '\''+self.data_fields['SQL Host*'].currentText()+'\'', 
                sqlclustername= self.data_fields['clusterName'].text(), 
                businessunit= '\''+self.data_fields['Business Unit*'].currentText()+'\'', 
                thirdpartybackup= '\''+self.data_fields['thirdPartybackups*'].currentText()+'\'', 
                sqlmonitoring= '\''+self.data_fields['SQL Monitoring*'].currentText()+'\'', 
                commissionedDate= self.data_fields['Commissioned Date'].text(), 
                decommissioneddate= self.data_fields['Decommissioned Date'].text(), 
                dnsalias= self.data_fields['DNSAlias'].text()
            )
            self.close()
            return

        print('Failed Search')