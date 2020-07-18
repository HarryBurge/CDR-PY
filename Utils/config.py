# Colour options
def bar_colour():
    return "#FFFF00"

def search_screen_table_line_colour():
    return "#000000"

def searchtable_background():
    return "#FFFFFF"

def search_screen_top_bar_line_colour():
    return "#000000"

def popup_changed_colour():
    return "#FF5500"

def popup_readonly_colour():
    return "#BAC3D1"


# Window size
def minimum_width():
    return 1200

def minimum_height():
    return 500


# Fonts
def title_font_size():
    return "30px"

def title_font_family():
    return "Courier New"

def searching_results_font_size():
    return "30px"

def searching_results_font_family():
    return "Courier New"

def searchtable_font_size():
    return "12px"

def searchtable_font_family():
    return "Courier New"


# Search Table options
def searchtable_spacing():
    return 3

def search_screen_table_columns_to_show_and_order():
    return ['Host/Listener Name','Instance Name','Environment', 'Server Type','Windows Cluster Name', 'SQL Cluster Name', 'Port','Type','Edition','Host State','Server State']

def search_screen_table_columns_to_show_and_order_for_hosts():
    return ['host Name', 'Windows Cluster Name', 'SQL Cluster Name', 'Host State', 'Commissioned Date', 'Decommissioned Date', 'Model', 'No Of Logical Processors', 'Total Physical Memory', 'Create Date', 'Update Date']


# Popup options - (str name, row, col, row_span, col_span, bool enable, object|False button_object)
def sqlserver_details_screen_layout():
    return [('hostID', 0,0, 1,1, False, False), ('Host Name', 0,1, 1,1, False, False), ('serverID', 0,2, 1,1, False, False), ('Instance Name', 0,3, 1,1, False, False), ('clusterID', 0,4, 1,1, False, False), ('Windows Cluster Name', 0,5, 1,1, False, False), ('Type', 0,6, 1,1, False, False), ('Edition', 0,7, 1,1, False, False), ('Service Pack', 0,8, 1,1, False, False), ('Version', 0,9, 1,1, False, False), ('Collation', 0,10, 1,1, False, False), ('Min Memory (Mb)', 0,11, 1,1, False, False), ('Max Memory (Mb)', 0,12, 1,1, False, False), ('Tcp Port', 0,13, 1,1, False, False), ('AWE Enabled', 0,14, 1,1, False, False), ('Create Date', 0,15, 1,1, False, False), ('Supplied User Details', 0,16, 1,1, False, False), ('Update Date', 0,17, 1,1, False, False), ('Application', 1,0, 1,1, False, False), ('Business Owner', 1,1, 1,1, False, False), ('Technical Owner', 1,2, 1,1, False, False), ('Core Db Maintenance Window', 1,3, 1,1, False, False), ('Technical Expert', 1,4, 1,1, False, False), ('VSR', 1,5, 1,1, False, False), ('DNS Alias', 1,6, 1,1, True, False), ('Commissioned Date', 1,7, 1,1, True, False), ('Built By', 1,8, 1,1, True, False), ('Reviewed By', 1,9, 1,1, True, False), ('Business Unit', 1,10, 1,1, True, False), ('Environment', 1,11, 1,1, True, False), ('CommVault?', 1,12, 1,1, True, False), ('Monitored by SentryOne?', 1,13, 1,1, True, False), ('Server State', 1,14, 1,1, True, False), ('Notes', 0,18, 2,1, True, False), ('Startup Parameters', 0,19, 2,1, True, False)]

def host_details_screen_layout():
    return [('HostID', 0,0, 1,1, False, False), ('Host', 0,1, 1,1, False, False), ('Model', 0,2, 1,1, False, False), ('Bit', 0,3, 1,1, False, False), ('OS', 0,4, 1,1, False, False), ('Build', 0,5, 1,1, False, False), ('Processors', 0,6, 1,1, False, False), ('Cores', 0,7, 1,1, False, False), ('Memory (Mb)', 0,8, 1,1, False, False), ('Create Date', 0,9, 1,1, False, False), ('Updated By', 0,10, 1,1, False, False), ('Update Date', 0,11, 1,1, False, False), ('Domain', 1,0, 1,1, False, False), ('Last Boot Time', 1,1, 1,1, False, False), ('Install Date', 1,2, 1,1, False, False), ('Commissioned Date', 1,3, 1,1, False, False), ('Decommissioned Date', 1,4, 1,1, False, False), ('Built By', 1,5, 1,1, True, False), ('Reviewed By', 1,6, 1,1, True, False), ('Dr Tier', 1,7, 1,1, True, False), ('Primary BU', 1,8, 1,1, True, False), ('Host Location', 1,9, 1,1, True, False), ('SolarWinds', 1,10, 1,1, True, False), ('Commissioned', 1,11, 1,1, True, False), ('VSR', 1,12, 1,1, False, False), ('Notes', 0,13, 2,1, False, False)]

def cluster_details_screen_layout():
    return [('ClusterID', 0,0, 1,1, False, False), ('SQL ClusterName', 0,1, 1,1, False, False), ('Windows Cluster Name', 0,2, 1,1, False, False), ('No Of Nodes', 0,3, 1,1, False, False), ('Cluster Method', 0,4, 1,1, False, False), ('Create Date', 0,5, 1,1, False, False), ('Update Date', 0,6, 1,1, False, False)]

def cluster_nodes_screen_layout(self):
    return [('nodeID', 0,0, 1,1, False, False), ('Host Name', 0,1, 1,1, True, self), ('Host State', 0,2, 1,1, False, False), ('Install Date', 0,3, 1,1, False, False), ('Description', 1,0, 1,1, False, False), ('Primary BU', 1,1, 1,1, False, False), ('Domain', 1,2, 1,1, False, False), ('Notes', 0,4, 2,1, False, False)]