import pandas as pd
import pyodbc
from Utils.util import sqlreturn_to_tabledata_for_search
# from util import sqlreturn_to_tabledata_for_search

conn = pyodbc.connect()

cursor = conn.cursor()


# Search Functions
def get_all_servers_like(servertypes, hoststates, serverstates, hostname, instancename, clustername, order_by):
    sqlhostname = ''
    sqlinstancename = ''
    sqlclustername = ''

    if hostname != None:
        sqlhostname = '[Host/Listener Name] like \'%{}%\' {}\n'.format(hostname, 'and' if (instancename != None or clustername != None) else '')

    if instancename != None:
        sqlinstancename = '[Instance Name] like \'%{}%\' {}\n'.format(instancename, 'and' if (clustername != None) else '')

    if clustername != None:
        sqlclustername = '[Windows Cluster Name] like \'%{}%\'\n'.format(clustername)

    sql_command = '''
    select * 
        from [dbo].[vw_PythonPortal_InstanceList] 
        where [Server Type] in {} and 
        (
        {}{}{}
        ) and 
        [Host State] in ({}) and 
        [Server State] in ({})
        order by [{}]
    '''.format(servertypes, sqlhostname, sqlinstancename, sqlclustername, hoststates, serverstates, order_by)
    sql_query = pd.read_sql_query(sql_command,conn)

    # Ensure ID's are integers and not null
    sql_query[["hostID", "clusterID", "serverID"]] = sql_query[["hostID", "clusterID", "serverID"]].fillna(0.0).astype(int)

    return sqlreturn_to_tabledata_for_search(sql_query)

def get_all_hosts_like(hostname, hoststates, order_by):
    sql_command = '''
    select *
        from [dbo].[vw_PythonPortal_HostList]
        where [host Name] like '%{}%' and [Host State] in ({})
        order by [{}]
    '''.format(hostname, hoststates, order_by)
    sql_query = pd.read_sql_query(sql_command,conn)

    # Ensure ID's are integers and not null
    sql_query[["hostID", "clusterID"]] = sql_query[["hostID", "clusterID"]].fillna(0.0).astype(int)

    return sqlreturn_to_tabledata_for_search(sql_query)


# Detailed info
def get_host_info(source, hostname):
    sql_command = '''
    select *
    from dbo.vw_PythonPortal_HostInfo
    where source = '{}' and HostID = '{}'
    '''.format(source, hostname)
    sql_query = pd.read_sql_query(sql_command,conn)

    return sql_query.to_dict('records')


def get_sqlserver_info(source, serverID):
    sql_command = '''
    select *
    from [dbo].[vw_PythonPortal_InstanceInfo]
    where source='{}' and serverID = '{}'
    '''.format(source, serverID)
    sql_query = pd.read_sql_query(sql_command,conn)

    return sql_query.to_dict('records')


def get_cluster_info(source, clusterID):
    sql_command = '''
    select *
    from [dbo].[vw_PythonPortal_ClusterInfo]
    where source = '{}' and ClusterID = '{}'
    '''.format(source, clusterID)
    sql_query = pd.read_sql_query(sql_command,conn)

    return sql_query.to_dict('records')


def get_ag_info(source, serverID):
    sql_command = '''
    select *
    from [dbo].[vw_PythonPortal_AG_Info]
    where source = '{}' and serverID = '{}'
    '''.format(source, serverID)
    sql_query = pd.read_sql_query(sql_command,conn)

    return sql_query.to_dict('records')


# Popdown vlookup
def get_instance_names_serverID(name):
    sql_command = '''
    select source, serverID, case when [Instance Name] = 'MSSQLSERVER' then [Host/Listener Name] else [Host/Listener Name] + '\\' + [Instance Name] end as [Instance Name]
    from [vw_PythonPortal_InstanceList] where [Server State] = 'Commissioned'
    order by [Instance Name]
    '''
    instancenames_lookup = pd.read_sql_query(sql_command,conn)
    value = instancenames_lookup.loc[instancenames_lookup['Instance Name'] == name.replace('\'', '')]['serverID'].to_list()[0]
    return value

def get_enviroment_code(environment):
    sql_command = '''
    Select * from [dbo].[Environments] order by Environment
    '''
    enviroments_lookup = pd.read_sql_query(sql_command,conn)
    value = enviroments_lookup.loc[enviroments_lookup['Environment'] == environment.replace('\'', '')]['ShortCode'].to_list()[0]
    return value


# Combo box info
def get_business_units():
    sql_command= "SELECT TOP 1000 BUID, BusinessUnit FROM [dbo].[BusinessUnits] order by BusinessUnit"
    sql_query = pd.read_sql_query(sql_command,conn)
    return sql_query['BusinessUnit'].to_list()

def get_drtiers(drid=False):
    sql_command= "SELECT TOP 1000 DRID, DRTier, SLAWorkingHours FROM [dbo].[DRTier] ORDER BY DRTier"
    sql_query = pd.read_sql_query(sql_command,conn)
    if not drid:
        return sql_query['DRTier'].to_list()
    return sql_query[['DRID','DRTier']]

def get_locations(shortcode=False):
    sql_command= "SELECT TOP 1000 LocationID, Location, ShortCode FROM [dbo].[Locations] order by Location"
    sql_query = pd.read_sql_query(sql_command,conn)
    if not shortcode:
        return sql_query['Location'].to_list()
    return sql_query[['Location','ShortCode']]

def get_enviroments():
    sql_command= "Select * from [dbo].[Environments] order by Environment"
    sql_query = pd.read_sql_query(sql_command,conn)
    return sql_query['Environment'].to_list()

def get_instance_name():
    sql_command = '''
    select source, serverID, case when [Instance Name] = 'MSSQLSERVER' then [Host/Listener Name] else [Host/Listener Name] + '\\' + [Instance Name] end as [Instance Name]
    from [vw_PythonPortal_InstanceList] where [Server State] = 'Commissioned'
    order by [Instance Name]
    '''
    sql_query = pd.read_sql_query(sql_command,conn)
    return sql_query['Instance Name'].to_list()

def get_host_name():
    sql_command = '''
    select distinct source, hostID, [host Name] from [vw_PythonPortal_HostList] where [Host State] = 'Commissioned'
    order by [host Name]
    '''
    sql_query = pd.read_sql_query(sql_command,conn)
    return sql_query['host Name'].to_list()

def get_standalone_hosts():
    sql_command='''
    select distinct [host name] as [SQL Host] from [vw_PythonPortal_HostList] where clusterid is null and [Host State] = 'Commissioned'  order by [host name]
    '''
    sql_query = pd.read_sql_query(sql_command,conn)
    return sql_query['SQL Host'].to_list()

def get_cluster_hosts():
    sql_command='''
    select distinct [SQL CLuster Name] as [SQL Host] from [vw_PythonPortal_HostList] where clusterid is not null and [SQL CLuster Name] is not null and [Host State] = 'Commissioned'  order by [SQL CLuster Name]
    '''
    sql_query = pd.read_sql_query(sql_command,conn)
    return sql_query['SQL Host'].to_list()

def get_regions():
    sql_command='''
    select *
    from [dbo].[Regions]
    '''
    sql_query = pd.read_sql_query(sql_command,conn)
    return sql_query['ShortCode'].to_list()


# Upsert functions
def upsert_host(source, hostname, vsr, region, location, primaryBU, description, maintenanceWindow, builtBy, builtByPeerReviewedBy, hostState, commissionedDate, temporaryStateExpiryDate, refreshData):
    domain = '[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]'
    sql_command= "exec {}.[uspUpsertHostToCDR] {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(domain, hostname, vsr, region, location, primaryBU, description, maintenanceWindow, builtBy, builtByPeerReviewedBy, hostState, commissionedDate, temporaryStateExpiryDate, refreshData)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def upsert_host_extras(source, hostname, drtier, sentryone, notes):
    domain = '[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]'
    drtier_lookup = get_drtiers(True)
    drtier = drtier_lookup.loc[drtier_lookup['DRTier'] == drtier.replace('\'', '')]['DRID'].to_list()[0]
    sql_command= "exec {}.[usp_CDRPortal_UpsertExtrasHost] {}, {}, {}, {}".format(domain, hostname, drtier, sentryone, notes)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()


def upsert_server(source, instanceName, hostName, clusterName, status, postConfigBy, postConfigPeerReviewedBy, serverState, refreshData):
    domain = '[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]'
    sql_command= "exec {}.[uspUpsertServerToCDR] {}, {}, {}, {}, {}, {}, {}, {}".format(domain, instanceName, hostName, clusterName, status, postConfigBy, postConfigPeerReviewedBy, serverState, refreshData)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def upsert_server_extras(source, instanceName, hostname, sqlclustername, businessunit, thirdpartybackup, sqlmonitoring, commissionedDate, decommissioneddate, dnsalias):
    domain = '[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]'
    sql_command= "exec {}.[usp_CDRPortal_UpsertExtrasInstance] {}, {}, {}, {}, {}, {}, {}, {}, {}".format(domain, instanceName, hostname, sqlclustername, businessunit, thirdpartybackup, sqlmonitoring, commissionedDate, decommissioneddate, dnsalias)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()


def upsert_cluster(source, sqlclustername, windowsclustername, numofnodes, clusteringmethod):
    domain = '[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]'
    sql_command="exec {}.[uspUpsertClusters] {}, {}, {}, {}".format(domain, sqlclustername, windowsclustername, numofnodes, clusteringmethod)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def upsert_cluster_extras(source, sqlclustername, notes):
    domain = '[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]'
    sql_command= '''
    exec {}.[usp_CDRPortal_UpsertExtrasCluster] {}, {}
    '''.format(domain, sqlclustername, notes)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def upsert_cluster_node(source, sqlclustername, nodename, sqlserverid):
    domain = '[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]'
    sql_command="exec {}.[uspUpsertClusterNodes_from_Python] {},{},{}".format(domain, sqlclustername, nodename, sqlserverid)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()


# Decommissioning
# Host
def decomm_host(source, hostname):
    domain = '[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]'
    sql_command= "exec {}.[uspDecommissionHostFromCDR] '{}', null, null".format(domain, hostname)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

# Server
def decomm_instance(source, instanceName, hostname, sqlclustername):
    domain = '[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]'
    sql_command= "exec {}.[uspDecommissionServerFromCDR] '{}', '{}', {}".format(domain, instanceName, hostname, sqlclustername)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()



# Updater functions
# Sql Server instance
def update_instance_reviewedBy(source, serverID, value):
    sql_command = '''
    Update {}.servers set [postConfigPeerReviewedBy] = '{}' where serverID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, serverID)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()
    
def update_instance_serverState(source, serverID, value):
    sql_command = '''
    update {}.servers set [serverState] = '{}' where serverID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, serverID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def update_instance_commVault(source, serverID, value):
    sql_command = '''
    update {}.[Extras_Instance] set ThirdPartyBackups = '{}' where serverID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, serverID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def update_instance_sentryOne(source, serverID, value):
    sql_command = '''
    update {}.[Extras_Instance] set SQLMonitoring = '{}' where serverID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, serverID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def update_instance_enviroment(source, serverID, value):
    sql_command = '''
    update {}.servers set status = (select ShortCode from Environments where Environment = '{}') where serverID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, serverID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def update_instance_businessUnit(source, serverID, value):
    sql_command = '''
    update {}.[Extras_Instance] set BusinessUnit = '{}' where serverID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, serverID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def update_instance_builtBy(source, serverID, value):
    sql_command = '''
    Update {}.servers set [postConfigBy] = '{}' where serverID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, serverID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def update_instance_commissionedDate(source, serverID, value):
    sql_command = '''
    update {}.[Extras_Instance] set CommissionedDate = '{}' where serverID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, serverID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def update_instance_dnsAlias(source, serverID, value):
    sql_command = '''
    update {}.[Extras_Instance] set DNSAlias = '{}' where serverID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, serverID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def insert_instance_extras(source, serverID):
    sql_command = '''
    if not exists(select 1 from {0}.[Extras_Instance] where ServerID = '{1}')
    insert into {0}.[Extras_Instance] values ('{1}',NULL,NULL,NULL,getdate(),NULL,NULL)
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', serverID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()


#Host
def update_host_builtBy(source, hostID, value):
    sql_command = '''
    update {}.hosts set [BuiltBy] = '{}' where hostID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, hostID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def update_host_builtByPeerReviewedBy(source, hostID, value):
    sql_command = '''
    update {}.hosts set [BuiltByPeerReviewedBy] = '{}' where hostID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, hostID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def update_host_drTier(source, hostID, value):
    drtier_lookup = get_drtiers(True)
    value = drtier_lookup.loc[drtier_lookup['DRTier'] == value]['DRID'].to_list()[0]
    sql_command = '''
    update {}.[Extras_Host] set DRID = '{}' where hostID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, hostID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def update_host_primaryBU(source, hostID, value):
    sql_command = '''
    update {}.hosts set [primaryBU] = '{}' where hostID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, hostID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def update_host_location(source, hostID, value):
    sql_command = '''
    update {}.Hosts set location = (select ShortCode from Locations where Location = '{}') where hostId = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, hostID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def update_host_solarWinds(source, hostID, value):
    sql_command = '''
    update {}.[Extras_Host] set InfMonitoring = '{}' where hostID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, hostID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def update_host_commissioned(source, hostID, value):
    sql_command = '''
    update {}.hosts set [hostState] = '{}' where hostID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, hostID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def update_host_vsr(source, hostID, value):
    sql_command = '''
    update {}.hosts set [VSR] = '{}' where hostID = '{}'
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, hostID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def update_host_notes(source, hostID, value):
    sql_command = '''
    update {}.[Extras_Host] set Notes = '{}' where hostID = '{}
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', value, hostID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()

def insert_host_extras(source, hostID):
    sql_command = '''
    if not exists(select 1 from {0}.[Extras_Host] where hostID = '{1}')
    insert into {0}.[Extras_Host] values ('{1}',NULL,NULL,NULL)
    '''.format('[dbo]' if source=='P' else '[CDR_NONPROD].[SQL_Inventory].[dbo]', hostID)
    print(sql_command)
    cursor.execute(sql_command)
    cursor.commit()
    conn.commit()