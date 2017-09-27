import os
import socket
import subprocess
import tkinter as tk

from tkinter.ttk import Frame
from tkinter import messagebox


ROOT_WIDTH = 800  # width for the Tk root
ROOT_HEIGHT = 650  # height for the Tk root
DEFAULT_TEXT = "Enter the List of server or IP\'s"


def center_align_root(root):
    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (ROOT_WIDTH / 2)
    y = (hs / 2) - (ROOT_HEIGHT / 2)

    # set the dimensions of the screen
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (ROOT_WIDTH, ROOT_HEIGHT, x, y))


def _validate_input(function_):
    def wrapper(self):
        data = self._retrieve_input_from_text_area()
        if data is not None:
            function_(self, data.split())
    return wrapper


def get_forward_dns(hostname):
    try:
        ip = socket.gethostbyname(hostname)
    except (socket.gaierror, socket.herror):
        ip = "No Ip Address"

    return "%s  %s" % (hostname, ip)


def get_reverse_dns(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except (socket.gaierror, socket.herror):
        hostname = "No hostname"

    return "%s  %s" % (ip, hostname)


def find_ping_response(hostname_or_ip):
    with open(os.devnull, 'w') as DEVNULL:
        try:
            subprocess.check_call(
                ['ping', '-c', '3', hostname_or_ip],
                stdout=DEVNULL,  # suppress output
                stderr=DEVNULL
            )
            ping_status = "Active"
        except subprocess.CalledProcessError:
            ping_status = "Unreachable"

    return "%s  %s" % (hostname_or_ip, ping_status)



class Application(Frame):
    def __init__(self, parent):
        Frame.__init__(self, master=parent)
        self.parent = parent
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        self.winfo_toplevel().title("Pre-Requisite Check")

        # Text area to get the items list
        self.text_area = tk.Text(self.parent, height=35, width=80, bg="yellow")
        self.text_area.pack()
        self.text_area.insert(tk.END, DEFAULT_TEXT)

        # Buttons
        buttons = {"Forward DNS": self.find_forward_dns, "Reverse DNS": self.find_backward_dns, "Ping": self.find_ping,
                   "Clear": self._clear_data}
        x = 100
        for button, action in buttons.items():
            button = tk.Button(self.parent, text=button, command=action)
            button.pack()
            button.place(x=x, y=600)
            x += 200

    def _retrieve_input_from_text_area(self):
        input_ = self.text_area.get("1.0", tk.END)
        self._clear_data()
        if input_.strip() in (DEFAULT_TEXT, ''):
            self._show_warning()
        else:
            return input_

    def _clear_data(self):
        self.text_area.delete("1.0", tk.END)

    def _insert_data(self, text):
        self.text_area.insert("1.0", text)

    @staticmethod
    def _show_warning():
        messagebox.showwarning("Warning", "You have not entered the proper data yet!")

    @_validate_input
    def find_forward_dns(self, data):
        result = map(get_forward_dns, data)
        final = "\n".join(i for i in result)
        self._insert_data(final)

    @_validate_input
    def find_backward_dns(self, data):
        result = map(get_reverse_dns, data)
        final = "\n".join(i for i in result)
        self._insert_data(final)

    @_validate_input
    def find_ping(self, data):
        result = map(find_ping_response, data)
        final = "\n".join(i for i in result)
        self._insert_data(final)


def main():
    root = tk.Tk()  # create a Tk root window

    # Align root window to the center of the screen
    center_align_root(root)
    _ = Application(root)

    root.mainloop()

if __name__ == '__main__':
    main()
