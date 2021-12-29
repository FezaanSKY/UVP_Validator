import PySimpleGUI as sg
from Controller import Controller

class View:
    window = None

    def __init__(self):
        self.__setupwindow__()

    def __setupwindow__(self):
        sg.theme("DarkTeal2")

        layout = [[sg.T("")], [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-")], [sg.Button("Submit")],
                  [sg.Text('Untar', auto_size_text=True, justification='right', key="-Output_Untar-")],
                  [sg.Text('XSD Validation', auto_size_text=True, justification='left', key="-Output_xsd-")],
                  [sg.Text('XMLPARSE', size=(80, 80), auto_size_text=True, justification='left', key="-Output_parse-")]]

        ###Building Window
        self.window = sg.Window('My File Browser', resizable=True, finalize=True, auto_size_text=True).Layout(
            [[sg.Column(layout, size=(900, 600), scrollable=True, )]])

    def start(self):

        while True:
            event, values = self.window.read()
            file_location = str(values[0]).replace(".uvp", ".UVP_Extracted")
            if event == sg.WIN_CLOSED or event == "Exit":
                break
            elif event == "Submit":
                controller = Controller(values["-IN-"])
                self.window['-Output_Untar-'].update(controller.untarResult)
                self.window['-Output_xsd-'].update(controller.validate())
                self.window['-Output_parse-'].update(controller.parse())



