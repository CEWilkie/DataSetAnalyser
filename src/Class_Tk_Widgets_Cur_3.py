import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Widget():
    def __init__(self, root, rpos, cpos, sticky, rspan, cspan, *args):
        self.root = root
        self.rpos = rpos
        self.cpos = cpos
        self.sticky = sticky
        self.rspan = rspan
        self.cspan = cspan

    def usefont(self, ff, fc, fs, bg):
        try:
            self.body.config(font=(ff, fs), fg=fc)
        except:
            pass

        self.body.config(bg=bg)

    def load(self):
        self.body.grid(row=self.rpos,
                       column=self.cpos,
                       sticky=self.sticky,
                       rowspan=self.rspan,
                       columnspan=self.cspan)

    def unload(self):
        self.body.grid_forget()


class FrameWidget(Widget):
    def __init__(self, root, rpos, cpos, sticky, rspan, cspan):
        super().__init__(root, rpos, cpos, sticky, rspan, cspan)
        self.body = tk.Frame(root, relief='raised', borderwidth=3)


class LabelWidget(Widget):
    def __init__(self, root, rpos, cpos, sticky, rspan, cspan, text='NoTagProvided'):
        super().__init__(root, rpos, cpos, sticky, rspan, cspan)
        self.body = tk.Label(root, text=text)


class ButtonWidget(Widget):
    def __init__(self, root, rpos, cpos, sticky, rspan, cspan, text='', command=None):
        super().__init__(root, rpos, cpos, sticky, rspan, cspan)
        self.body = tk.Button(root, text=text, command=command)


class TextWidget(Widget):
    def __init__(self, root, rpos, cpos, sticky, rspan, cspan, text, width=10, height=2, state='normal', wrap='none'):
        super().__init__(root, rpos, cpos, sticky, rspan, cspan)
        self.body = tk.Text(root, state=state, width=width, height=height, wrap=wrap)
        self.body.insert('1.0', text)
        self.body.config(state=state)
        self.state = state

    def add(self, text):
        if self.state == 'disabled':
            self.body.config(state='normal')
            self.body.insert('1.0', text)
            self.body.config(state='disabled')
        else:
            self.body.insert('1.0', text)

    def replace(self, text):
        if self.state == 'disabled':
            self.body.config(state='normal')
            self.body.delete('1.0', 'end')
            self.body.insert('1.0', text)
            self.body.config(state='disabled')
        else:
            self.body.delete('1.0', 'end')
            self.body.insert('1.0', text)


class EntryWidget(Widget):
    def __init__(self, root, rpos, cpos, sticky, rspan, cspan, text, vartype='c_str', tr_cmd=None):
        super().__init__(root, rpos, cpos, sticky, rspan, cspan)
        if vartype == 'p_int':
            self.var = tk.IntVar()
            self.prevValue = 0
            self.var.trace('w', self.EntryWidgetIntTrace)
        elif vartype == 'p_str':
            self.var = tk.StringVar()
            self.prevValue = 'a'
            self.var.trace('w', self.EntryWidgetStrTrace)
        elif vartype == 'p_float':
            self.var = tk.StringVar()
            self.prevValue = 0.0
            self.var.trace('w', self.EntryWidgetFloatTrace)
        elif vartype == 'c_str':
            self.var = tk.StringVar()
            self.prevValue = 'a'
        self.body = tk.Entry(root, textvariable=self.var)
        self.body.insert(0, text)
        if tr_cmd != None:
            self.var.trace('w', tr_cmd)
        self.var.set(text)

    def EntryWidgetIntTrace(self, *args):
        try:
            self.var.get()
        except:
            if self.prevValue == '':
                self.prevValue = 0
            self.var.set(self.prevValue)
        if isinstance(self.var.get(), int) == False:
            self.var.set(self.prevValue)
        self.prevValue = (self.var.get())

    def EntryWidgetStrTrace(self, *args):
        try:
            self.var.get()
        except:
            if self.prevValue == '':
                self.prevValue = 'a'
            self.var.set(self.prevValue)
        if self.var.get().isalpha() == False:
            self.var.set(self.prevValue)
        self.prevValue = (self.var.get())

    def EntryWidgetFloatTrace(self, *args):
        try:
            self.var.get()
        except:
            if self.prevValue == '':
                self.prevValue = 0.0
            self.var.set(self.prevValue)
        try:
            self.var.set(float(self.var.get()))
        except:
            self.var.set(self.prevValue)
            self.var.set(float(self.var.get()))
        self.prevValue = self.var.get()


class OptionMenuWidget(Widget):
    def __init__(self, root, rpos, cpos, sticky, rspan, cspan, options=['No Options'], tr_cmd=None):
        super().__init__(root, rpos, cpos, sticky, rspan, cspan)
        self.var = tk.StringVar()
        if tr_cmd != None:
            self.var.trace('w', tr_cmd)
        self.body = tk.OptionMenu(root, self.var, *options)
        self.var.set(options[0])

    def changeOptions(self, options=['No Options']):
        self.body['menu'].delete(0, 'end')
        for item in options:
            self.body['menu'].add_command(label=item, command=tk._setit(self.var, item))
        self.var.set(options[0])
        self.load()


class CheckbuttonWidget(Widget):
    def __init__(self, root, rpos, cpos, sticky, rspan, cspan, tr_cmd=None):
        super().__init__(root, rpos, cpos, sticky, rspan, cspan)
        self.var = tk.IntVar()
        if tr_cmd != None:
            self.var.trace('w', tr_cmd)
        self.body = tk.Checkbutton(root, variable=self.var)


class ScrollbarWidget(Widget):
    def __init__(self, root, rpos, cpos, sticky, rspan, cspan, orient='vertical', target=None):
        super().__init__(root, rpos, cpos, sticky, rspan, cspan)
        if orient == 'vertical':
            self.body = tk.Scrollbar(root, orient=orient, command=target.yview)
            target.config(yscrollcommand=self.body.set)
        elif orient == 'horizontal':
            self.body = tk.Scrollbar(root, orient=orient, command=target.xview)
            target.config(xscrollcommand=self.body.set)


class GraphFigWidget(Widget):
    def __init__(self, root, rpos, cpos, sticky, rspan, cspan, figure):
        super().__init__(root, rpos, cpos, sticky, rspan, cspan)
        self.body = FigureCanvasTkAgg(figure, root).get_tk_widget()
