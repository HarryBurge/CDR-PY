__authour__ = 'Harry Burge'
__date_created__ = '10/06/2020'
__last_updated_by__ = 'Harry Burge'
__last_updated_date__ = '23/06/2020'

from UI.Screens.add_cluster_screen import AddClusterScreen
from UI.Screens.add_host_screen import AddHostScreen
from UI.Screens.add_sql_instance_server import AddSQLInstanceScreen
from UI.Screens.searchscreen import SearchScreen


# ScreenManager
class ScreenManager:

    def __init__(self, open_new_window_menu=False):
        '''
        params:-
            open_new_window_menu : True if you want the menu to spawn windows when 
                clicked in the context menu
        '''
        self.current_open_screens = []
        #TODO: Can be modifyied so if you want to be able to open multiple search
        #   screens or screens then just change this to a array and change the functions accordingly
        self.screens = []
        self.popups = []

        self.open_new_window_menu = open_new_window_menu

    # def addScreens(self, Screens):
    #     '''
    #     params:-
    #         Screens : [Screen_subClass, ...] : Screens to be added to the screenmanager
    #     '''
    #     for screen in Screens:
    #         self.screens[screen.name] = screen

    # def is_screen_open(self, name):
    #     if name in self.current_open_screens:
    #         return True
    #     return False

    def show_screen(self, name):
        '''
        params:-
            name : str : Name of the screen to open
        returns:-
            None : Displays screen with given name
        '''
        if name == 'Add Cluster Screen':
            self.screens.append(AddClusterScreen(self, 'Add Cluster Screen'))
        elif name == 'Add Host Screen':
            self.screens.append(AddHostScreen(self, 'Add Host Screen'))
        elif name == 'Add SQL Server Instance Screen':
            self.screens.append(AddSQLInstanceScreen(self, 'Add SQL Server Instance Screen'))
        elif name == 'CDR':
            self.screens.append(SearchScreen(self, 'CDR'))
        else:
            raise RuntimeError('Wrong name passed into show screen')

        self.screens[-1].show()

        self.current_open_screens.append(name)

    # def close_screen(self, name):
    #     '''
    #     params:-
    #         name : str : Name of the screen to close
    #     returns:-
    #         None : Closes the screen that you are viewing
    #     '''
    #     self.screens[name].close()

    #     if name in self.current_open_screens:
    #         del self.current_open_screens[self.current_open_screens.index(name)]

    # def close_all_screens(self):
    #     '''
    #     returns:-
    #         None : Closes all screens that are curently open
    #     '''
    #     for name in self.current_open_screens:
    #         self.screens[name].close()

    #     self.current_open_screens = []

    #TODO: Can lead to memeory overflow so if becomes a problem make sure that you actually untrack the closed popups (Might not be an issue)
    def add_popup(self, popup):
        '''
        params:-
            popup : Popup_subClass : Popup to be displayed
        returns:-
            None : Displays the popup screen
        '''
        self.popups.append(popup)
        self.popups[-1].show()
