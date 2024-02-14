#!/usr/bin/python3

# Licensed under AGPLv3+

from tkinter import *
from tkinter.colorchooser import askcolor
import tkinter.ttk as ttk
import copy
import time

from lib.i18n import _
from lib.config import *


# Internally used class
class counter(object):
    def __init__(self, v=0):
        if type(v) != int:
            v = 0
        self.v = v

    def get(self):
        return self.v

    def inc(self):
        self.v += 1
        return self.v - 1


# GUI configurator class
class guiconfigurator:
    def __init__(self, cfg):
        self.cfg = cfg
        self.__create_window()

    def __close_window(self):
        self.running = False

    # Main function of the class
    def __create_window(self):

        self.savedentcolor = None  # Default entry background color
        self.running = True

        root = Tk()
        root.protocol("WM_DELETE_WINDOW", self.__close_window)
        nb = ttk.Notebook(root)
        nb.pack(side=TOP)

        # Create used tabs
        misctab = ttk.Frame(nb)
        limtab = ttk.Frame(nb)

        nb.add(misctab, text=_("Common settings"))
        nb.add(limtab, text=_("Limits settings"))

        #
        # Common settings
        #
        row = counter()
        Label(misctab, text=_("Camera number")).grid(
                row=row.get(), column=0, sticky=W)
        self.camera_dev = Entry(misctab, width=4)
        self.camera_dev.grid(row=row.inc(), column=1, sticky=W)

        # Once remember default Entry background color
        self.savedentcolor = self.camera_dev.cget("highlightbackground")

        Label(misctab, text=_("Video width")).grid(
                row=row.get(), column=0, sticky=W)
        self.img_w = Entry(misctab, width=4)
        self.img_w.grid(row=row.inc(), column=1, sticky=W)

        Label(misctab, text=_("Video height")).grid(
                row=row.get(), column=0, sticky=W)
        self.img_h = Entry(misctab, width=4)
        self.img_h.grid(row=row.inc(), column=1, sticky=W)

        Label(misctab, text=_("FPS")).grid(row=row.get(), column=0, sticky=W)
        self.fps = Entry(misctab, width=4)
        self.fps.grid(row=row.inc(), column=1, sticky=W)

        self.showcap = BooleanVar()
        Checkbutton(
                misctab, text=_("Show camera picture"), variable=self.showcap,
                onvalue=1, offvalue=0).grid(row=row.inc(), column=0, sticky=W)

        self.writestat = BooleanVar()
        Checkbutton(
                misctab, text=_("Write stat file"), variable=self.writestat,
                onvalue=1, offvalue=0).grid(row=row.inc(), column=0, sticky=W)

        self.beepwarn = BooleanVar()
        Checkbutton(
                misctab, text=_("Beep on warning (depend on system settings)"), variable=self.beepwarn,
                command=self.endis,
                onvalue=1, offvalue=0).grid(row=row.inc(), column=0, sticky=W)

        self.showwarn = BooleanVar()
        Checkbutton(
                misctab, text=_("Show warning"), variable=self.showwarn,
                command=self.endis,
                onvalue=1, offvalue=0).grid(row=row.inc(), column=0, sticky=W)

        Label(misctab, text=_("Warning window size")).grid(
                row=row.get(), column=0, sticky=W)
        self.wsize = Entry(misctab, width=4)
        self.wsize.grid(row=row.inc(), column=1, sticky=W)

        Label(misctab, text=_("Warning window X pos")).grid(
                row=row.get(), column=0, sticky=W)
        self.wx = Entry(misctab, width=4)
        self.wx.grid(row=row.inc(), column=1, sticky=W)

        Label(misctab, text=_("Warning window Y pos")).grid(
                row=row.get(), column=0, sticky=W)
        self.wy = Entry(misctab, width=4)
        self.wy.grid(row=row.inc(), column=1, sticky=W)

        Button(misctab, text=_("Warning color"), command=self.wcolor).grid(
                row=row.inc(), column=0)

        #
        # Limits settings
        #
        row = counter()

        Label(limtab, text=_("Upper limits")).grid(
                row=row.inc(), column=0, columnspan=8, sticky=W+E)

        # Checkbuttons for max limit
        self.wmax = []
        self.wmaxen = []
        column = counter()
        for i, ign in enumerate(self.cfg.wmax):
            self.wmaxen.append(None)
            self.wmaxen[i] = BooleanVar()
            Checkbutton(
                    limtab, text=emotions[i], variable=self.wmaxen[i],
                    onvalue=1, offvalue=0, command=self.endis).grid(
                    row=row.get(), column=column.inc())
        # Scales for max limit
        row.inc()
        column = counter()
        for i, ign in enumerate(self.cfg.wmax):
            self.wmax.append(Scale(
                    limtab, orient=VERTICAL, length=300,
                    from_=5, to=-5, tickinterval=0.0, resolution=0.1))
            self.wmax[i].grid(row=row.get(), column=column.inc())

        row.inc()

        Label(limtab, text=_("Lower limits")).grid(
                row=row.inc(), column=0, columnspan=8, sticky=W+E)
        # Checkbuttons for min limit
        self.wmin = []
        self.wminen = []
        column = counter()
        for i, ign in enumerate(self.cfg.wmin):
            self.wminen.append(None)
            self.wminen[i] = BooleanVar()
            Checkbutton(
                    limtab, text=emotions[i], variable=self.wminen[i],
                    onvalue=1, offvalue=0, command=self.endis).grid(
                    row=row.get(), column=column.inc())
        # Scales for min limit
        row.inc()
        column = counter()
        for i, ign in enumerate(self.cfg.wmin):
            self.wmin.append(Scale(
                    limtab, orient=VERTICAL, length=300, from_=5, to=-5,
                    tickinterval=0.0, resolution=0.1))
            self.wmin[i].grid(row=row.get(), column=column.inc())

        row.inc()

        self.note = Label(root, text="")
        self.note.pack(side=TOP, anchor=W)
        Button(root, text=_("Save"), command=self.save_guicfg).pack(side=LEFT)
        Button(root, text=_("Reset"), command=self.cfg2gui).pack(side=LEFT)

        self.cfg2gui()  # Fill with actual values

        self.endis()  # Update enable/disable status of interface elementes

        while self.running is True:
            root.update_idletasks()
            root.update()
            time.sleep(0.05)

    # Scroll enabler/disabler
    def endis(self,):
        if (self.showwarn.get() is True):
            self.wsize.configure(state=NORMAL)
            self.wx.configure(state=NORMAL)
            self.wy.configure(state=NORMAL)
        else:
            self.wsize.configure(state=DISABLED)
            self.wx.configure(state=DISABLED)
            self.wy.configure(state=DISABLED)

        for i, ign in enumerate(self.cfg.wmax):
            if (self.wmaxen[i].get() is True):
                self.wmax[i].config(state=NORMAL, relief=RAISED)
            else:
                self.wmax[i].config(state=DISABLED, relief=FLAT)

        for i, ign in enumerate(self.cfg.wmin):
            if (self.wminen[i].get() is True):
                self.wmin[i].config(state=NORMAL, relief=RAISED)
            else:
                self.wmin[i].config(state=DISABLED, relief=FLAT)

    # Color chooser
    def wcolor(self,):
        colors = askcolor(initialcolor=self.wcolor, title=_("Color Chooser"))
        self.wcolor = colors[0]

    # Action on save button
    def save_guicfg(self) -> None:
        errorflag, newcfg = self.get_gui_cfg()

        # Show warning if needed
        if errorflag == 0:
            writecfg(newcfg)
            self.cfg = newcfg
            self.note.config(text=_("Config saved"), fg='green')

    # Update cfg structure with configuration from GUI
    def get_gui_cfg(self):
        newcfg = copy.copy(self.cfg)
        errorflag = 0

        # Common settings
        try:
            newcfg.camera_dev = int(self.camera_dev.get())
            self.camera_dev.configure(
                    highlightbackground=self.savedentcolor,
                    highlightcolor=self.savedentcolor)
        except Exception as e:
            self.camera_dev.configure(
                    highlightbackground='red', highlightcolor='red')
            errorflag = 1

        try:
            newcfg.img_w = int(self.img_w.get())
            self.img_w.configure(
                    highlightbackground=self.savedentcolor,
                    highlightcolor=self.savedentcolor)
        except Exception as e:
            self.img_w.configure(
                    highlightbackground='red', highlightcolor='red')
            errorflag = 1

        try:
            newcfg.img_h = int(self.img_h.get())
            self.img_h.configure(
                    highlightbackground=self.savedentcolor,
                    highlightcolor=self.savedentcolor)
        except Exception as e:
            self.img_h.configure(
                    highlightbackground='red', highlightcolor='red')
            errorflag = 1

        try:
            newcfg.fps = float(self.fps.get())
            self.fps.configure(
                    highlightbackground=self.savedentcolor,
                    highlightcolor=self.savedentcolor)
        except Exception as e:
            self.fps.configure(highlightbackground='red', highlightcolor='red')
            errorflag = 1

        newcfg.showcap = self.showcap.get()
        newcfg.writestat = self.writestat.get()
        newcfg.showwarn = self.showwarn.get()
        newcfg.beepwarn = self.beepwarn.get()

        try:
            newcfg.wsize = int(self.wsize.get())
            self.wsize.configure(
                    highlightbackground=self.savedentcolor,
                    highlightcolor=self.savedentcolor)
        except Exception as e:
            self.wsize.configure(
                    highlightbackground='red', highlightcolor='red')
            errorflag = 1

        try:
            newcfg.wx = int(self.wx.get())
            self.wx.configure(
                    highlightbackground=self.savedentcolor,
                    highlightcolor=self.savedentcolor)
        except Exception as e:
            self.wx.configure(
                    highlightbackground='red', highlightcolor='red')
            errorflag = 1

        try:
            newcfg.wy = int(self.wy.get())
            self.wy.configure(
                    highlightbackground=self.savedentcolor,
                    highlightcolor=self.savedentcolor)
        except Exception as e:
            self.wy.configure(highlightbackground='red', highlightcolor='red')
            errorflag = 1

        newcfg.wcolor = self.wcolor

        # Emotion limits
        for i, ign in enumerate(self.cfg.wmax):
            val = self.wmaxen[i].get()
            if val == 1:
                newcfg.wmax[i] = self.wmax[i].get()
            else:
                newcfg.wmax[i] = None

        for i, ign in enumerate(self.cfg.wmin):
            val = self.wminen[i].get()
            if val == 1:
                newcfg.wmin[i] = self.wmin[i].get()
            else:
                newcfg.wmin[i] = None

        # Show warning if needed
        if errorflag == 0:
            self.note.config(text=_("Config validated"), fg='green')
        else:
            self.note.config(text=_("Errors detected"), fg='red')

        return errorflag, newcfg

    # Fill gui fields with the read config
    def cfg2gui(self):
        # Common settings
        self.camera_dev.delete(0, END)
        self.camera_dev.insert(0, str(self.cfg.camera_dev))
        self.img_w.delete(0, END)
        self.img_w.insert(0, str(self.cfg.img_w))
        self.img_h.delete(0, END)
        self.img_h.insert(0, str(self.cfg.img_h))
        self.fps.delete(0, END)
        self.fps.insert(0, str(self.cfg.fps))
        self.showcap.set(1 if self.cfg.showcap else 0)
        self.writestat.set(1 if self.cfg.writestat else 0)
        self.showwarn.set(1 if self.cfg.showwarn else 0)
        self.beepwarn.set(1 if self.cfg.beepwarn else 0)
        self.wsize.delete(0, END)
        self.wsize.insert(0, str(self.cfg.wsize))
        self.wx.delete(0, END)
        self.wx.insert(0, str(self.cfg.wx))
        self.wy.delete(0, END)
        self.wy.insert(0, str(self.cfg.wy))
        self.wcolor = self.cfg.wcolor

        # Emotion limits
        for i, val in enumerate(self.cfg.wmax):
            if val is not None:
                self.wmaxen[i].set(1)
                self.wmax[i].set(val)
            else:
                self.wmaxen[i].set(0)
                self.wmax[i].set(0)

        for i, val in enumerate(self.cfg.wmin):
            if val is not None:
                self.wminen[i].set(1)
                self.wmin[i].set(val)
            else:
                self.wminen[i].set(0)
                self.wmin[i].set(0)

        # Reset note, if it was
        self.note.config(text="")

# vi: tabstop=4 shiftwidth=4 expandtab
