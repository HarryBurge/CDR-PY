__authour__ = 'Harry Burge'
__date_created__ = '03/07/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '06/07/2020'

# Imports
from PyQt5.QtWidgets import QGridLayout, QPushButton, QScrollArea
from Utils import config, sqlcommands, util
from UI.screen_class import Screen


class SQLServerDetailsScreen(Screen):

    def __init__(self, master, name, identifier, width=config.minimum_width(), height=config.minimum_height()):
        self.identifier = identifier
        super().__init__(self, master, name, width, height, True)


    def get_layout(self):
        '''
        returns:-
            QGridLayout : Anything that needs to be displayed as a popup, this 
            is used in tandom with the popup class for inheritance
        '''
        # Update Button
        update_button = QPushButton('Save&Close')
        update_button.setFixedSize(80, 40)
        update_button.clicked.connect(lambda: self.update())

        # Top bar buttons <- Update Button
        topbar_buttons = QGridLayout()
        topbar_buttons.addWidget(update_button, 0,0)

        # Preset layout
        data_labels = config.sqlserver_details_screen_layout()
        dropdown = self.get_dropdowns()

        # Gets values with SQL Command
        data_values = self.get_sql_server()

        # Makes table
        table = self.popup_table(data_labels, dropdown, data_values)

        # Scrollable area <- Table
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(util.layout_to_QWidget(table))

        # Screen <- Topbar and Scroll Table
        screen = QGridLayout()
        screen.setRowStretch(1, 1)
        screen.addLayout(super().top_bar(topbar_buttons, data_values[0]['Host Name'] + ('\\' + data_values[0]['Instance Name'] if data_values[0]['Instance Name'] != 'MSSQLSERVER' else '')), 0,0)
        screen.addWidget(scroll, 1, 0)

        return screen
        
    
    def get_sql_server(self):
        '''
        params:-
            identifier : str : Used to get the info to put into the table
        returns:-
            {str:str, ...} : Data format for table above
        '''
        return sqlcommands.get_sqlserver_info(*self.identifier)

    def get_dropdowns(self):
        return {'CommVault?':['Yes', 'No'], 'Monitored by SentryOne?':['Yes', 'No', 'None'], 'Server State':['Commissioned', 'Decommissioned'], 'Business Unit':sqlcommands.get_business_units(), 'Environment':sqlcommands.get_enviroments()}

    
    def update(self):
        instance = self.get_sql_server()[0]

        # Adds thing into extras if non in there already
        sqlcommands.insert_instance_extras(*self.identifier)

        # LineEdit Fields
        if self.data_fields['DNS Alias'].text() != str(instance['DNS Alias']):
            sqlcommands.update_instance_dnsAlias(*self.identifier, self.data_fields['DNS Alias'].text())

        if self.data_fields['Commissioned Date'].text() != str(instance['Commissioned Date']):
            sqlcommands.update_instance_commissionedDate(*self.identifier, self.data_fields['Commissioned Date'].text())

        if self.data_fields['Built By'].text() != str(instance['Built By']):
            sqlcommands.update_instance_builtBy(*self.identifier, self.data_fields['Built By'].text())

        if self.data_fields['Reviewed By'].text() != str(instance['Reviewed By']):
            sqlcommands.update_instance_reviewedBy(*self.identifier, self.data_fields['Reviewed By'].text())

        if self.data_fields['Notes'].toPlainText() != str(instance['Notes']):
            pass

        # Need dropdown
        if self.data_fields['CommVault?'].currentText() != str(instance['CommVault?']):
            sqlcommands.update_instance_commVault(*self.identifier, self.data_fields['CommVault?'].currentText())

        if self.data_fields['Monitored by SentryOne?'].currentText() != str(instance['Monitored by SentryOne?']):
            sqlcommands.update_instance_sentryOne(*self.identifier, self.data_fields['Monitored by SentryOne?'].currentText())

        if self.data_fields['Server State'].currentText() != str(instance['Server State']):
            # Decomm server
            if self.data_fields['Server State'].currentText() == 'Decommissioned':
                sqlcommands.decomm_instance(
                    source= self.identifier[0], 
                    instanceName= self.data_fields['Instance Name'].text(),
                    hostname= self.data_fields['Host Name'].text(),
                    sqlclustername= self.data_fields['Windows Cluster Name'].text() if self.data_fields['Windows Cluster Name'].text() != 'None' else 'NULL'
                )
            elif self.data_fields['Server State'].currentText() == 'Commissioned':
                sqlcommands.update_instance_serverState(*self.identifier, self.data_fields['Server State'].currentText())

        if self.data_fields['Business Unit'].currentText() != str(instance['Business Unit']):
            sqlcommands.update_instance_businessUnit(*self.identifier, self.data_fields['Business Unit'].currentText())

        if self.data_fields['Environment'].currentText() != str(instance['Environment']):
            sqlcommands.update_instance_enviroment(*self.identifier, self.data_fields['Environment'].currentText())

        self.close()