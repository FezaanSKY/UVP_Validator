import PySimpleGUI as sg
import XML_PARSE as xp

sg.theme("DarkTeal2")

layout = [[sg.T("")], [sg.Text("Choose a file: "), sg.Input(),  sg.FileBrowse(key="-IN-")], [sg.Button("Submit")],
          [sg.Text('Untar', auto_size_text=True, justification='right', key="-OUTPUT3-")],
          [sg.Text('XSD Validation', auto_size_text=True, justification='right', key="-OUTPUT-")],
          [sg.Text('XMLPARSE',size=(80,80),  auto_size_text=True, justification='left', key="-OUTPUT2-")]]

###Building Window
window = sg.Window('My File Browser', resizable=True, finalize=True, auto_size_text=True).Layout([[sg.Column(layout, scrollable=True,)]])

while True:
    event, values = window.read()
    # print("debug")
    # print(str(values[0]).replace(".tar",".tar_Extracted"))
    file_location = str(values[0]).replace(".uvp",".UVP_Extracted")
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event == "Submit":
        window['-OUTPUT3-'].update(xp.untar(values["-IN-"]))
        window['-OUTPUT-'].update(xp.xsd_validation(values["-IN-"]))
        window['-OUTPUT2-'].update(xp.xml_parse(values["-IN-"]))

