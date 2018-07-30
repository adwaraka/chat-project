import time, wx, sys, subprocess
import json
import requests
from threading import *

ID_FRAME = wx.NewId()
ID_PANEL = wx.NewId()
ID_LOG = wx.NewId()
ID_START = wx.NewId()
ID_TEXT = wx.NewId()

class RedirectText:
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)

class ClientApp(wx.Frame):

    def __init__(self):
        # The main frame
        wx.Frame.__init__(self, None, ID_FRAME, "Chat App", size=(600,400))
 
        # Add a panel
        panel = wx.Panel(self, ID_PANEL)
        log = wx.TextCtrl(panel, ID_LOG, size=(600, 400), style = wx.TE_MULTILINE|wx.TE_READONLY)

        #message panel
        message_txt = wx.TextCtrl(panel, ID_TEXT, size=(400, -1))

        # Add the send button
        start_btn = wx.Button(panel, ID_START, 'Send')
        self.Bind(wx.EVT_BUTTON, self.onRun, start_btn)
 
        # Add widgets to a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(log, 1, wx.ALL|wx.EXPAND, 5)
        sizer.Add(message_txt, 0, wx.ALL|wx.EXPAND, 10)

        # Add buttons to the GUI
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        button_box.Add(start_btn, 0, wx.ALL|wx.CENTER, 10)
        sizer.Add(button_box, 0, wx.ALL|wx.CENTER)

        # Adding the sizer to the panel
        panel.SetSizer(sizer)

        # Redirect text here
        sys.stdout = RedirectText(log)

    def onRun(self, event):
        print "TODO"
    
def main():
    print "Please enter your login name :-"
    usr_name = sys.stdin.readline()
    print "Please enter your password   :-"
    password = sys.stdin.readline()
    '''
    Login format
    {
        "username": "string",
        "password": "pa$$word"
    }
    '''
    payload = {}
    payload["username"], payload["password"] = usr_name.strip(), password.strip()
    login_url = "http://localhost:8080/login"
    result = requests.post(url = login_url, data = json.dumps(payload))
    print result
    if result.status_code == 200:
        app = wx.App()
        frame = ClientApp().Show()
        app.MainLoop()

if __name__== "__main__":
    main()
