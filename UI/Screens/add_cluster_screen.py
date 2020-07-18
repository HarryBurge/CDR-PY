__authour__ = 'Harry Burge'
__date_created__ = '10/06/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '10/06/2020'

# Imports
from PyQt5.QtWidgets import QGridLayout, QScrollArea, QPushButton, QLineEdit, QComboBox
from UI.screen_class import Screen

from Utils import config, util, sqlcommands
import copy


class AddClusterScreen(Screen):
    '''
    Screen to show user when adding a new Cluster to the CDR database
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
        create_cluster_button = QPushButton('Create&Close')
        create_cluster_button.setFixedSize(80, 40)
        create_cluster_button.clicked.connect(lambda: self.create_cluster_button())

        # Top bar buttons <- Update Button
        topbar_buttons = QGridLayout()
        topbar_buttons.addWidget(create_cluster_button, 0,0)

        # Top Bar
        self.screen.addLayout(super().top_bar(topbar_buttons), 0,0)

        # Scrollable area
        scroll = QScrollArea()

        # Table to put into the scroll area
        self.table = QGridLayout()
        self.table.setHorizontalSpacing(10)
        self.table.setVerticalSpacing(0)

        self.data_labels = [('domain', '', 0,0, 1,1, True), ('SQL Acess Point', '', 1,0, 1,1, True), ('Windows Cluster Name', '', 2,0, 1,1, True), ('Clustering Method', '', 3,0, 1,1, True), ('Number of Nodes', '', 0,1, 1,1, True), ('Notes', '', 5,0, 1,1, True), ('Cluster Node 1', '', 1,1, 1,1, False), ('Related SQL Server 1', '', 2,1, 1,1, False), ('Cluster Node 2', '', 3,1, 1,1, False), ('Related SQL Server 2', '', 4,1, 1,1, False), ('Cluster Node 3', '', 5,1, 1,1, False), ('Related SQL Server 3', '', 6,1, 1,1, False), ('Cluster Node 4', '', 7,1, 1,1, False), ('Related SQL Server 4', '', 8,1, 1,1, False)]
        node_options = [None] + sqlcommands.get_host_name()
        sql_options = [None]+sqlcommands.get_instance_name()
        dropdown = {'domain':['.hiscox.com', '.hiscox.nonprod'], 'Related SQL Server 1':sql_options, 'Related SQL Server 2':sql_options, 'Related SQL Server 3':sql_options, 'Related SQL Server 4':sql_options, 'Clustering Method':['MSCS', 'AlwaysOn'], 'Number of Nodes':['1','2','3','4'], 'Cluster Node 1':node_options, 'Cluster Node 2':node_options, 'Cluster Node 3':node_options, 'Cluster Node 4':node_options}

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
                if i == 'Number of Nodes':
                    self.temp = inputter
                    self.temp.currentTextChanged.connect(lambda: self.num_nodes_changed(int(self.temp.currentText())))
                    self.table.addWidget(self.temp, row, col*2+1, row_s, col_s)
                else:
                    self.table.addWidget(inputter, row, col*2+1, row_s, col_s)

        # Puts table into scroll area
        scroll.setWidgetResizable(True)
        scroll.setWidget(util.layout_to_QWidget(self.table))

        # Put scroll area into the screen
        self.screen.addWidget(scroll, 1, 0)

        # Make sure things changed
        self.num_nodes_changed(int(self.temp.currentText()))

        return self.screen

    def num_nodes_changed(self, num):
        values = [self.data_fields['Cluster Node {}'.format(i)] for i in [1,2,3,4]]
        others = [self.data_fields['Related SQL Server {}'.format(i)] for i in [1,2,3,4]]
        num = int(num)

        for index, thing in enumerate(values):
            if index+1 <= num:
                thing.setEnabled(True)
                others[index].setEnabled(True)
            else:
                thing.setEnabled(False)
                thing.setCurrentIndex(0)
                others[index].setEnabled(False)
                others[index].setCurrentIndex(0)
        
    
    def create_cluster_button(self):
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

            if label.split(' ')[0] == 'Cluster' and label.split(' ')[1] == 'Node':
                if int(label.split(' ')[2]) <= int(self.data_fields['Number of Nodes*'].currentText()):
                    if temp.currentText() == '':
                        break

        else:
            sqlcommands.upsert_cluster(
                source= 'P' if self.data_fields['domain*'].currentText() == '.hiscox.com' else 'N', 
                sqlclustername= '\''+self.data_fields['SQL Acess Point*'].text()+'\'', 
                windowsclustername= '\''+self.data_fields['Windows Cluster Name*'].text()+'\'', 
                numofnodes= self.data_fields['Number of Nodes*'].currentText(), 
                clusteringmethod= '\''+self.data_fields['Clustering Method*'].currentText()+'\''
            )

            sqlcommands.upsert_cluster_extras(
                source= 'P' if self.data_fields['domain*'].currentText() == '.hiscox.com' else 'N', 
                sqlclustername= '\''+self.data_fields['Windows Cluster Name*'].text()+'\'', 
                notes= '\''+self.data_fields['Notes*'].text()+'\''
            )

            for i in range(int(self.data_fields['Number of Nodes*'].currentText())):
                sqlcommands.upsert_cluster_node(
                    source= 'P' if self.data_fields['domain*'].currentText() == '.hiscox.com' else 'N', 
                    sqlclustername= '\''+self.data_fields['SQL Acess Point*'].text()+'\'', 
                    nodename= '\''+self.data_fields['Cluster Node {}'.format(i+1)].currentText()+'\'', 
                    sqlserverid= 'NULL' if (self.data_fields['Related SQL Server {}'.format(i+1)].currentText() == '') else (str(sqlcommands.get_instance_names_serverID( self.data_fields['Related SQL Server {}'.format(i+1)].currentText() )))
                )
            self.close()
            return
        print('Failed Search')