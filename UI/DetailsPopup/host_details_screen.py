__authour__ = 'Harry Burge'
__date_created__ = '10/06/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '06/07/2020'

# Imports
from PyQt5.QtWidgets import QGridLayout, QPushButton, QScrollArea
from Utils import config, sqlcommands, util
from UI.screen_class import Screen


class HostDetailsScreen(Screen):

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
        data_labels = config.host_details_screen_layout()
        dropdown = self.get_dropdowns()

        # Gets values with SQL Command
        data_values = self.get_host()

        # Makes table
        table = self.popup_table(data_labels, dropdown, data_values)

        # Scrollable area <- Table
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(util.layout_to_QWidget(table))

        # Screen <- Topbar and Scroll Table
        screen = QGridLayout()
        screen.setRowStretch(1, 1)
        screen.addLayout(super().top_bar(topbar_buttons, data_values[0]['Host']), 0,0)
        screen.addWidget(scroll, 1, 0)

        return screen
        
    
    def get_host(self):
        '''
        params:-
            identifier : str : Used to get the info to put into the table
        returns:-
            {str:str, ...} : Data format for table above
        '''
        return sqlcommands.get_host_info(*self.identifier)


    def get_dropdowns(self):
        return {'Dr Tier':sqlcommands.get_drtiers(), 'Primary BU':sqlcommands.get_business_units(), 'Host Location':sqlcommands.get_locations(), 'SolarWinds':['Yes', 'No', 'None'], 'Commissioned':['Decommissioned','Commissioned']}

    
    def update(self):
        instance = self.get_host()[0]

        # Blank into extras if needed
        sqlcommands.insert_host_extras(*self.identifier)

        # LineEdit Fields
        if self.data_fields['Built By'].text() != str(instance['Built By']):
            sqlcommands.update_host_builtBy(*self.identifier, self.data_fields['Built By'].text())
        
        if self.data_fields['Reviewed By'].text() != str(instance['Reviewed By']):
            sqlcommands.update_host_builtByPeerReviewedBy(*self.identifier, self.data_fields['Reviewed By'].text())

        if self.data_fields['Notes'].toPlainText() != str(instance['Notes']):
            sqlcommands.update_host_notes(*self.identifier, self.data_fields['Notes'].toPlainText())

        # Need dropdown
        if self.data_fields['Dr Tier'].currentText() != str(instance['Dr Tier']):
            sqlcommands.update_host_drTier(*self.identifier, self.data_fields['Dr Tier'].currentText())

        if self.data_fields['Primary BU'].currentText() != str(instance['Primary BU']):
            sqlcommands.update_host_primaryBU(*self.identifier, self.data_fields['Primary BU'].currentText())

        if self.data_fields['Host Location'].currentText() != str(instance['Host Location']):
            sqlcommands.update_host_location(*self.identifier, self.data_fields['Host Location'].currentText())

        if self.data_fields['SolarWinds'].currentText() != str(instance['SolarWinds']):
            sqlcommands.update_host_solarWinds(*self.identifier, self.data_fields['SolarWinds'].currentText())

        if self.data_fields['Commissioned'].currentText() != str(instance['Commissioned']):
            if self.data_fields['Commissioned'].currentText() == 'Decommissioned':
                # Decommission host thing
                sqlcommands.decomm_host(
                    source= self.identifier[0], 
                    hostname= self.data_fields['Host'].text()
                    )
            elif self.data_fields['Commissioned'].currentText() == 'Commissioned':
                sqlcommands.update_host_commissioned(*self.identifier, self.data_fields['Commissioned'].currentText())

        self.close()