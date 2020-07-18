__authour__ = 'Harry Burge'
__date_created__ = '11/06/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '23/06/2020'

# Imports
from PyQt5.QtWidgets import QGridLayout, QSizePolicy, QPushButton, QLabel, QScrollArea, QWidget, QLineEdit, QCheckBox, QComboBox
from PyQt5.QtCore import Qt
from Utils import config, sqlcommands, util

from UI.DetailsPopup.host_details_screen import HostDetailsScreen
from UI.DetailsPopup.sqlserver_details_screen import SQLServerDetailsScreen
from UI.DetailsPopup.cluster_details_screen import ClusterDetailsScreen
from UI.DetailsPopup.ag_details_screen import AGDetailsScreen
from UI.screen_class import Screen


# SearchScreen
class SearchScreen(Screen):
    '''
    Screen to show search results and to create the search term
    '''

    def __init__(self, master, name, width=config.minimum_width(), height=config.minimum_height()):
        super().__init__(self, master, name, width, height)


    def get_layout(self):
        '''
        returns:-
            QGridLayout : Anything that needs to be displayed as a screen, this 
            is used in tandom with the screen class to make inheritance of the menu bar
        '''
        # View Options
        server_filter = QLabel('Server Type Filter:')
        server_filter.setFixedSize(100, 40)
        server_filter.setStyleSheet("background-color: {};".format(config.bar_colour()))

        self.view_standalone_check = QCheckBox(text='Standalone')
        self.view_standalone_check.setFixedSize(75, 20)
        self.view_standalone_check.setStyleSheet("background-color: {};".format(config.bar_colour()))
        self.view_standalone_check.setChecked(True)

        self.view_alwayson_check = QCheckBox(text='AlwaysON')
        self.view_alwayson_check.setFixedSize(75, 20)
        self.view_alwayson_check.setStyleSheet("background-color: {};".format(config.bar_colour()))
        self.view_alwayson_check.setChecked(True)

        self.view_failover_check = QCheckBox(text='Failover')
        self.view_failover_check.setFixedSize(80, 20)
        self.view_failover_check.setStyleSheet("background-color: {};".format(config.bar_colour()))
        self.view_failover_check.setChecked(True)

        # Search On Cluster Nodes
        self.search_clusternodes_check = QComboBox()
        self.search_clusternodes_check.setFixedSize(80, 40)
        self.search_clusternodes_check.addItems(['Instances', 'Hosts'])
        self.search_clusternodes_check.currentTextChanged.connect(lambda: self.button_search_options(self.search_clusternodes_check.currentText()))

        # Decommission Options
        self.search_hoststate_check = QComboBox()
        self.search_hoststate_check.addItems(['Either','Decommissioned', 'Commissioned'])
        self.search_hoststate_check.setFixedSize(170, 20)
        self.search_hoststate_check.setCurrentText('Commissioned')

        self.search_serverstate_check = QComboBox()
        self.search_serverstate_check.addItems(['Either','Decommissioned', 'Commissioned'])
        self.search_serverstate_check.setFixedSize(170, 20)
        self.search_serverstate_check.setCurrentText('Commissioned')

        # Decommision labels
        hoststate = QLabel('Host Filter:')
        hoststate.setFixedSize(80, 20)
        hoststate.setStyleSheet("background-color: {};".format(config.bar_colour()))

        serverstate = QLabel('Server Filter:')
        serverstate.setFixedSize(80, 20)
        serverstate.setStyleSheet("background-color: {};".format(config.bar_colour()))

        # Editable line
        edit_host = QLabel('Host Name:')
        edit_host.setFixedSize(70, 20)
        edit_host.setStyleSheet("background-color: {};".format(config.bar_colour()))

        self.search_line_edit_host = QLineEdit()
        self.search_line_edit_host.setFixedSize(170, 20)

        edit_instance = QLabel('Instance Name:')
        edit_instance.setFixedSize(80, 20)
        edit_instance.setStyleSheet("background-color: {};".format(config.bar_colour()))

        self.search_line_edit_instance = QLineEdit()
        self.search_line_edit_instance.setFixedSize(170, 20)

        edit_cluster = QLabel('Cluster Name:')
        edit_cluster.setFixedSize(80, 20)
        edit_cluster.setStyleSheet("background-color: {};".format(config.bar_colour()))

        self.search_line_edit_cluster = QLineEdit()
        self.search_line_edit_cluster.setFixedSize(170, 20)

        self.search_line_edit_host.returnPressed.connect(lambda: self.search(self.search_line_edit_host.text(), 
                                                                        self.view_standalone_check.isChecked(), 
                                                                        self.view_alwayson_check.isChecked(), 
                                                                        self.view_failover_check.isChecked(),
                                                                        True,
                                                                        True,
                                                                        True,
                                                                        self.search_hoststate_check.currentText(),
                                                                        self.search_serverstate_check.currentText(),
                                                                        self.search_clusternodes_check.currentText(),
                                                                        self.search_line_edit_instance.text(),
                                                                        self.search_line_edit_cluster.text()) )
        self.search_line_edit_instance.returnPressed.connect(lambda: self.search(self.search_line_edit_host.text(), 
                                                                        self.view_standalone_check.isChecked(), 
                                                                        self.view_alwayson_check.isChecked(), 
                                                                        self.view_failover_check.isChecked(),
                                                                        True,
                                                                        True,
                                                                        True,
                                                                        self.search_hoststate_check.currentText(),
                                                                        self.search_serverstate_check.currentText(),
                                                                        self.search_clusternodes_check.currentText(),
                                                                        self.search_line_edit_instance.text(),
                                                                        self.search_line_edit_cluster.text()) )
        self.search_line_edit_cluster.returnPressed.connect(lambda: self.search(self.search_line_edit_host.text(), 
                                                                        self.view_standalone_check.isChecked(), 
                                                                        self.view_alwayson_check.isChecked(), 
                                                                        self.view_failover_check.isChecked(),
                                                                        True,
                                                                        True,
                                                                        True,
                                                                        self.search_hoststate_check.currentText(),
                                                                        self.search_serverstate_check.currentText(),
                                                                        self.search_clusternodes_check.currentText(),
                                                                        self.search_line_edit_instance.text(),
                                                                        self.search_line_edit_cluster.text()) )

        labels = [QLabel(), QLabel(), QLabel(), QLabel(), QLabel(), QLabel(), QLabel()]
        for i in labels:
            i.setFixedSize(5, 20)
            i.setStyleSheet("background-color: {};".format(config.bar_colour()))

        label40 = [QLabel(), QLabel()]
        for i in label40:
            i.setFixedSize(5, 40)
            i.setStyleSheet("background-color: {};".format(config.bar_colour()))

        # Topbar buttons <- All buttons needed
        top_bar_buttons = QGridLayout()

        top_bar_buttons.addWidget(label40[0], 0,0, 2,1)
        top_bar_buttons.addWidget(self.search_clusternodes_check, 0,2, 2,1)
        top_bar_buttons.addWidget(server_filter, 0,1, 2,1)
        top_bar_buttons.addWidget(label40[1], 0,3, 2,1)

        searchoptions = QGridLayout()
        searchoptions.addWidget(self.view_standalone_check, 0,2)
        searchoptions.addWidget(labels[0], 0, 3)
        searchoptions.addWidget(self.view_failover_check, 0,4)
        searchoptions.addWidget(labels[1], 0, 5)
        searchoptions.addWidget(self.view_alwayson_check, 0,6)

        searchoptions.addWidget(labels[2], 0, 7)
        searchoptions.addWidget(hoststate, 0,8)
        searchoptions.addWidget(self.search_hoststate_check, 0,9)
        searchoptions.addWidget(labels[3], 0, 10)
        searchoptions.addWidget(serverstate, 0,11)
        searchoptions.addWidget(self.search_serverstate_check, 0,12)


        searchbarline = QGridLayout()
        searchbarline.addWidget(edit_host, 0,0)
        searchbarline.addWidget(self.search_line_edit_host, 0,1)
        searchbarline.addWidget(labels[4], 0,2)
        searchbarline.addWidget(edit_instance, 0,3)
        searchbarline.addWidget(self.search_line_edit_instance, 0,4)
        searchbarline.addWidget(labels[5], 0,5)
        searchbarline.addWidget(edit_cluster, 0,6)
        searchbarline.addWidget(self.search_line_edit_cluster, 0,7)

        top_bar_buttons.addLayout(searchbarline, 1,4)
        top_bar_buttons.addLayout(searchoptions, 0,4)


        # Scrollable area <- Blank table
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.headers = QScrollArea()
        self.headers.setWidgetResizable(True)
        self.headers.setFixedHeight(55)
        self.headers.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.change_table(self.blank_table())

        # Screen <- Topbar and Scroll blank table
        screen = QGridLayout()
        screen.setRowStretch(1, 1)
        screen.addWidget(self.scroll, 2,0)
        screen.addWidget(self.headers, 1,0)
        screen.addLayout(super().top_bar(top_bar_buttons), 0,0)

        return screen


    def search(self, text, standaloneb, alwaysonb, failoverb, hostnameb, instancenameb, clusternameb, hoststateo, serverstateo, clusternodeo, text2='', text3=''):
        # Non-cluster node search
        if clusternodeo == 'Instances':
            hoststate = '\''+hoststateo+'\'' if hoststateo != 'Either' else '\'Decommissioned\', \'Commissioned\''
            serverstate = '\''+serverstateo+'\'' if serverstateo != 'Either' else '\'Decommissioned\', \'Commissioned\''

            if text == '' and text2 == '' and text3 == '':
                hostname = text
                instancename = text2
                clustername = text3
            else:
                hostname = text if text != '' else None
                instancename = text2 if text2 != '' else None
                clustername = text3 if text3 != '' else None

            servertypes = []
            if standaloneb:
                servertypes.append('Standalone')
            if alwaysonb:
                servertypes.append('AlwaysON')
            if failoverb:
                servertypes.append('Failover Cluster')
            servertypes = util.tuple_to_string_for_sql(servertypes)

            if ( not(standaloneb) and not(alwaysonb) and not(failoverb) ) or ( not(hostnameb) and not(instancenameb) and not(clusternameb) ):
                print('Failed Search')
            else:
                sql_results = sqlcommands.get_all_servers_like(servertypes, hoststate, serverstate, hostname, instancename, clustername)

                headers = sql_results[0]
                data = sql_results[1]

                self.change_table(*self.search_table(headers, data))
        
        # Cluster node search
        else:
            hoststate = '\''+hoststateo+'\'' if hoststateo != 'Either' else '\'Decommissioned\', \'Commissioned\''

            sql_results = sqlcommands.get_all_hosts_like(text, hoststate)

            headers = sql_results[0]
            data = sql_results[1]

            self.change_table(*self.search_table(headers, data, True))


    # Tables
    def blank_table(self):
        '''
        returns:-
            QGridLayout : A table with text in middle saying its searching for results
        '''
        table = QGridLayout()
        table.setHorizontalSpacing(0)
        table.setVerticalSpacing(0)

        text = QLabel(text='Please search for results')
        text.setStyleSheet("font-size: {}; qproperty-alignment: AlignJustify; font-family: {}".format(
            config.searching_results_font_size(), config.searching_results_font_family()))

        table.addWidget(text)
        table.setAlignment(Qt.AlignCenter)

        return table


    def search_table(self, headers, object_data, hosts=False):
        '''
        params:-
            headers : [str, ...] : Headers of the columns wanted
            object_data : [(str, {str:str, ...}), ...] : First str is the type of object
                this is used to make the button link. The key in the dictonary needs to be
                a header in headers so that value can be put in that column
        returns:-
            None : Table is changed to objects passed
        '''
        table = QGridLayout()
        table.setHorizontalSpacing(config.searchtable_spacing())
        table.setVerticalSpacing(0)

        order_list = config.search_screen_table_columns_to_show_and_order() if not hosts else config.search_screen_table_columns_to_show_and_order_for_hosts()
        headers_ordered = [header for header in order_list if header in headers]


        table_headers = QGridLayout()
        table_headers.setHorizontalSpacing(config.searchtable_spacing())
        table_headers.setVerticalSpacing(0)
        # Table <- Headers
        for i, header in enumerate(headers_ordered):
            headerbutton = QPushButton(header)
            headerbutton.setFixedHeight(40)
            table_headers.addWidget(headerbutton, 0, i)

        # Table <- Data labels and Linkings
        for i, data in enumerate(object_data):

            for key in data.keys():
                
                # Make sure key header is in the table headers
                if key in headers_ordered:

                    # Special columns
                    if key in ['Host Name', 'Windows Cluster Name', 'Instance Name', 'Server Type']:
                        field = QPushButton(str(data[key]))
                        field.setStyleSheet("font-size: {}; font-family: {}; background-color: {}".format(
                            config.searchtable_font_size(), config.searchtable_font_family(), config.searchtable_background()))

                        if key == 'Host Name':
                            field.clicked.connect(self.button_open_host(str(data['source']), str(data['hostID']))) if str(data['hostID']) != '0' else field.setEnabled(False)

                        elif key == 'Windows Cluster Name':
                            field.clicked.connect(self.button_open_cluster(str(data['source']), str(data['clusterID']))) if str(data['clusterID']) != '0' else field.setEnabled(False)

                        elif key == 'Instance Name':
                            field.clicked.connect(self.button_open_instance(str(data['source']), str(data['serverID']))) if str(data['serverID']) != '0' else field.setEnabled(False)

                        elif key == 'Server Type':
                            if str(data['Server Type']) == 'AlwaysON' and str(data['serverID']) != '0':
                                field.clicked.connect(self.button_open_ag(str(data['source']), str(data['serverID'])))
                            else:
                                field.setEnabled(False)

                    # Data columns
                    else:
                        field = QLabel(str(data[key]))
                        field.setStyleSheet("font-size: {}; qproperty-alignment: AlignJustify; font-family: {}; background-color: {}".format(
                            config.searchtable_font_size(), config.searchtable_font_family(), config.searchtable_background()))

                    field.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
                    table.addWidget(field, i+1, headers_ordered.index(key))

        # Add in a filler Qlabel if there is to smaller table
        if (len(object_data)+10)*20 < config.minimum_height():
            filler = QLabel()
            filler.setFixedHeight(10)
            table.addWidget(filler, 1000, 0, len(headers_ordered), 1)

        return table, table_headers


    # Funcs
    def change_table(self, table, headers=QGridLayout()):
        self.scroll.setWidget(util.layout_to_QWidget(table))
        self.headers.setWidget(util.layout_to_QWidget(headers))

    # Buttons
    def button_open_cluster(self, source, data):
        def temp():
            '''
            params:-
                data : Misc : Will be used to specify which data point should be shown
            returns:-
                None : Creates a popup with the info on
            '''
            self.master.add_popup(ClusterDetailsScreen(self.master, 'ClusterDetailsScreen', (source, data)))
        return temp


    def button_open_instance(self, source, data):
        def temp():
            '''
            params:-
                data : Misc : Will be used to specify which data point should be shown
            returns:-
                None : Creates a popup with the info on
            '''
            self.master.add_popup(SQLServerDetailsScreen(self.master, 'SQLServerDetailsScreen', (source, data)))
        return temp


    def button_open_host(self, source, data):
        def temp():
            '''
            params:-
                data : Misc : Will be used to specify which data point should be shown
            returns:-
                None : Creates a popup with the info on
            '''
            self.master.add_popup(HostDetailsScreen(self.master, 'HostDetailsScreen', (source, data)))
        return temp

    
    def button_open_ag(self, source, data):
        def temp():
            '''
            params:-
                data : Misc : Will be used to specify which data point should be shown
            returns:-
                None : Creates a popup with the info on
            '''
            self.master.add_popup(AGDetailsScreen(self.master, 'AGDetailsScreen', (source, data)))
        return temp


    def button_search_options(self, text):
        values = [self.view_standalone_check, self.view_alwayson_check, self.view_failover_check, self.search_line_edit_instance, self.search_line_edit_cluster, self.search_serverstate_check]
        
        for i in values:
            if self.search_clusternodes_check.currentText() == 'Hosts':
                i.setEnabled(False)
            else:
                i.setEnabled(True)

            if type(i) == QCheckBox:
                i.setChecked(False)
            elif type(i) == QLineEdit:
                i.setText('')
            elif type(i) == QComboBox:
                i.setCurrentIndex(0)
