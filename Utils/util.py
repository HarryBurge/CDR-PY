from PyQt5.QtWidgets import QWidget

import pandas as pd

def layout_to_QWidget(layout):
    '''
    params:-
        layout : QLayout : Layout to be converted to a QWidget
    returns:-
        QWidget : Layout as a widget
    '''
    widget = QWidget()
    widget.setLayout(layout)
    return widget


def sqlreturn_to_tabledata_for_search(sqlreturn):
    '''
    params:-
        str, pandas.dataframe : First str is the type of things returned by the
            sql for example cluster, host. the data frame is the data passed by the sql command
    returns:-
        [str, ...] : Headers to the table
        [(str, {str:str, ...}), ...] : Data to populate the table with
    '''
    headers = []
    object_data = []

    # Add the header if it doesn't exist yet
    for head in list(sqlreturn.columns):
        if head not in headers: headers.append(head)

    dataset = sqlreturn.to_dict('records')

    # Add the data in, setting its type for a link
    for data in dataset:
        object_data.append(data)

    return headers, object_data


def tuple_to_string_for_sql(items):
    stringitems = '(\''

    if type(items) not in [tuple, list]:
        stringitems += str(items)

    else:
        for item in items:
            stringitems += str(item) + '\',\''
        stringitems = stringitems[:-3]

    stringitems += '\')'

    return stringitems