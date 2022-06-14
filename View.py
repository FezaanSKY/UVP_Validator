import PySimpleGUI as sg

class View:
    window = None

    def __init__(self, controller):
        self.controller = controller

    def __setupwindow__(self):
        sg.theme("DarkTeal2")

        layout = [[sg.T("")],
                  [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-")],
                  [sg.Combo(self.controller.DisplayProvider(), size=(40, 40), default_value='Select Provider', key="-Provider_In-")],
                  [sg.Button("Submit")],
                  [sg.Push(), sg.Text('', auto_size_text=True, justification='center', key="-Output_Untar-"), sg.Push()] ,
                  [sg.Push(), sg.Text('', auto_size_text=True, justification='center', key="-Output_xsd-"), sg.Push()],
                  [sg.Push(), sg.Text('', size=(80, 50), auto_size_text=True, justification='center', key="-Output_parse-"), sg.Push()],
                  [sg.Push(), sg.Text('', auto_size_text=True, justification='center', key="-Database_Check-"), sg.Push()],
                  [sg.Push(), sg.Text('', auto_size_text=True, justification='center', key="-Genre_Check-"), sg.Push()],
                  [sg.Push(), sg.Text('', auto_size_text=True, justification='center', key="-DPL_Playlist_Check-"), sg.Push()],
                  [sg.Push(), sg.Text('', auto_size_text=True, justification='center', key="-Offer_Type-"), sg.Push()],
                  [sg.Push(), sg.Text('', size=(20,20), justification='center', key="-Provider_Check-"), sg.Push()]]

        ###Building Window
        self.window = sg.Window('UVP Validator', resizable=True, finalize=True, auto_size_text=True).Layout(
            [[sg.Column(layout, size=(900, 600), scrollable=True, )]])


    def start(self):
        self.__setupwindow__()
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == "Exit":
                self.controller.onclose()
                break
            file_location = str(values[0]).replace(".uvp", ".UVP_Extracted")
            if event == "Submit":
                self.controller.OnSubmitClicked(values["-IN-"], values["-Provider_In-"])
                self.window.refresh()
        self.window.close()

    def UpdateUntar(self, data):
        self.window['-Output_Untar-'].update(data)

    def Update_Authenticate(self, data):
        self.window['-Output_xsd-'].update(data)

    def Update_pars(self, data):
        self.window['-Output_parse-'].update(data)

    def Update_database_check(self):
        self.window['-Database_Check-'].update('#######Database Checks#######')

    def Update_ProviderCheck(self, data):
        if data > 0:
            self.window['-Provider_Check-'].update( "Provider Selected matched with Provider listed in the ADI")
        else:
            self.window['-Provider_Check-'].update("Provider found in the ADI does not match database records")

    def Update_GenreCheck(self, data):
        if data > 0:
            self.window['-Genre_Check-'].update( "Genre matched with DB ")
        else:
            self.window['-Genre_Check-'].update("Genre did not match")

    def Update_PlaylistCheck(self, data):
        if data > 0:
            self.window['-DPL_Playlist_Check-'].update( "Playlist matched with DB ")
        else:
            self.window['-DPL_Playlist_Check-'].update("Playlist did not match")

    def Update_OfferTypeCheck(self, data):
        if data > 0:
            self.window['-Offer_Type-'].update( "OfferType is valid")
        else:
            self.window['-Offer_Type-'].update("Offer Type is not valid")


