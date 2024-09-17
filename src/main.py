import tkinter as tk  # user interface constructor
import tkinter.font as tkFont  # for ease of use
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt  # calculations / graphing and
import pandas as pd  # dealing with datasets

pd.set_option('display.max_rows', None,  # visual enhancements for user
              'display.max_columns', None,  # quality of use. prevents program
              'display.width', None)  # condensing lines

from scipy.optimize import curve_fit
from scipy import stats
import datetime as dt
import numpy as np

from tkinter.filedialog import askopenfile  # only used for importing files
import os.path
import platform

from Class_Tk_Widgets_Cur_3 import *  # My widgets classes


########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################

class Program():
    def __init__(self):
        # tk interface setup
        self.window = self.window()
        self.menubar = self.menubar()

        # tk management vars
        self.currentScreen = ''
        self.fontOptions = list(tkFont.families())
        self.fontOptions.insert(0, 'TkDefaultFont')
        self.fontColours = ['black', 'blue', 'red', 'green', 'white']
        self.bgOptions = ['white', '#CFCFCF', '#A9A9A9', 'grey', '#404040', '#5A5A5A', 'black']
        self.defaultStyles = ['TkDefaultFont', 'Black', 10, 'White', 'CFCFCF']
        self.userFont = 'TkDefaultFont'
        self.userFontColour = 'Black'
        self.userFontSize = 10
        self.userBGOption = 'white'
        self.userWBGOption = '#CFCFCF'

        # universal vars:
        self.datapath = os.path.join('AutoImportDataSheetsFile.xlsx')  # avoid system specific input using path object
        self.importedData = []
        self.importingData = ''
        self.importingDataPages = []

        self.dateFormat = ['Day', 'Month', 'Year', 'Year/Month/Day', 'Month/Day', 'Year/Month']
        self.timeFormat = ['24hr 00:00:00', 'Hour/Min 00:00:_', 'Min/Sec _:00:00', 'Hour 00:_:_', 'Min _:00:_',
                           'Sec _:_:00']
        self.tFunctions = []
        self.tFunctionsDisplay = []

        self.linesList = []
        self.compiledLines = []

        self.autoImportData()

    def window(self):
        w = tk.Tk()
        w.title('Data Analysis Program')
        w.geometry('2000x1050')
        return w

    def menubar(self):
        mb = tk.Menu(self.window)  # initialise the Menubar
        self.window.config(menu=mb)  # assign menubar to window
        if platform.system() != 'Windows':
            cas_mb = tk.Menu(mb)
            mb.add_cascade(label='Select Screen', menu=cas_mb)
            return cas_mb
        else:
            return mb

    def autoImportData(self):
        if os.path.exists(self.datapath):
            autoFile = pd.ExcelFile(self.datapath)
            sheetNames = sorted(autoFile.sheet_names)
            for sheet in sheetNames:
                self.importedData.append([sheet, autoFile.parse(sheet_name=sheet)])
        else:
            pass

    def parseElement(self, element):
        if len(element) == 2:
            return f'{element[0]}t^{element[1]}'

        if len(element) == 1:
            return f'{element[0]}'


p = Program()


########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################

class Screen():
    def __init__(self, framesList, scrlabel):
        if platform.system() == 'Windows':
            p.menubar.add_command(label=scrlabel, command=lambda: self.screenSwitch(self))
        else:
            p.menubar.add_cascade(label=scrlabel, command=lambda: self.screenSwitch(self))

        self.framesList = framesList

    def screenSwitch(self, switchto):
        if p.currentScreen != '':
            self.unload(p.currentScreen.framesList)
        p.currentScreen = switchto
        self.load(switchto.framesList)

    def load(self, frames):
        try:
            for frame in frames:
                for widget in frame:
                    widget.usefont(p.userFont, p.userFontColour, p.userFontSize, p.userBGOption)
                    widget.load()
        except:
            for widget in frames:
                widget.usefont(p.userFont, p.userFontColour, p.userFontSize, p.userBGOption)
                widget.load()

    def unload(self, frames):
        try:
            for frame in frames:
                for widget in frame:
                    widget.unload()
        except:
            for widget in frames:
                widget.unload()


########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################

class ConstructSettingsScreen(Screen):
    def __init__(self):
        framesList = [self.constructFSF()]
        super().__init__(framesList, 'Settings')

    def constructFSF(self):
        # Font Settings Frame
        frame = [FrameWidget(p.window, 0, 0, 'nsew', 1, 1)]
        root = frame[0].body

        frame.append(LabelWidget(root, 0, 0, '', 1, 1, 'Font Style:'))
        frame.append(OptionMenuWidget(root, 0, 1, '', 1, 1, p.fontOptions, self.userfont))
        frame.append(LabelWidget(root, 1, 0, '', 1, 1, 'Font Colour:'))
        frame.append(OptionMenuWidget(root, 1, 1, '', 1, 1, p.fontColours, self.fontColour))
        frame.append(LabelWidget(root, 2, 0, '', 1, 1, 'Font Size:'))
        frame.append(EntryWidget(root, 2, 1, '', 1, 1, '10', 'p_int', self.fontSize))
        frame.append(LabelWidget(root, 3, 0, '', 1, 1, 'Frame Background Colour:'))
        frame.append(OptionMenuWidget(root, 3, 1, '', 1, 1, p.bgOptions, self.fbgTheme))
        frame.append(LabelWidget(root, 4, 0, '', 1, 1, 'Window Background Colour:'))
        frame.append(OptionMenuWidget(root, 4, 1, '', 1, 1, p.bgOptions, self.wbgTheme))
        frame.append(ButtonWidget(root, 0, 3, '', 1, 1, 'Reload Screen', self.reloadScreen))
        return frame

    def userfont(self, *args):
        p.userFont = self.framesList[0][2].var.get()

    def fontColour(self, *args):
        p.userFontColour = self.framesList[0][4].var.get()

    def fontSize(self, *args):
        p.userFontSize = self.framesList[0][6].var.get()

    def fbgTheme(self, *args):
        p.userBGOption = self.framesList[0][8].var.get()

    def wbgTheme(self, *args):
        p.userWBGOption = self.framesList[0][10].var.get()

    def reloadScreen(self):
        self.unload(self.framesList)
        p.window.config(bg=p.userWBGOption)
        self.load(self.framesList)


ConstructSettingsScreen()


########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################

class ConstructImportDataScreen(Screen):
    def __init__(self):
        self.normFig, self.normAxis = plt.subplots(1, 1, figsize=(6, 3), dpi=100)
        self.normFig.tight_layout(rect=[0.1, 0, 0.8, 0.9], pad=1.5)
        self.normAxis.tick_params(axis='x', labelsize=6)
        self.normAxis.tick_params(axis='y', labelsize=6)
        self.normAxis.locator_params(axis='x', nbins=20)
        self.normAxis.locator_params(axis='y', nbins=20)

        self.path = ''
        self.columns = []
        self.usecols = ''
        self.fileType = ''

        self.mean = 0
        self.stdev = 1
        self.cleandata = []
        self.anomalies = []
        self.posInAnom = 0
        self.tempdtvals = []
        self.olddtvals = []
        self.newtvals = []
        self.newdvals = []
        self.oldtvals = []
        self.olddvals = []

        framesList = [self.constructDFF(), self.constructPTF(), self.constructMIF(), self.constructMTDF(),
                      self.constructNDA(), self.constructNDGF(), self.constructMTPF()]
        super().__init__(framesList, 'Import Data')

    def constructDFF(self):
        # data file finder
        frame = [FrameWidget(p.window, 0, 0, 'nsew', 1, 1)]
        root = frame[0].body

        frame.append(ButtonWidget(root, 0, 0, '', 1, 1, 'Import File', self.fileFinder))
        frame.append(LabelWidget(root, 0, 1, '', 1, 1, 'Set File Name:'))
        frame.append(EntryWidget(root, 0, 2, '', 1, 1, f'Data Set {len(p.importedData) + 1}', 'c_str'))
        frame.append(ButtonWidget(root, 0, 3, '', 1, 1, 'Confirm Import', self.confirmImport))
        frame.append(LabelWidget(root, 0, 4, '', 1, 1, 'Auto Import on Program Load:'))
        frame.append(CheckbuttonWidget(root, 0, 5, '', 1, 1))
        return frame

    def constructPTF(self):
        # Preview Text Frame
        frame = [FrameWidget(p.window, 2, 0, 'ewns', 1, 1)]
        root = frame[0].body

        frame.append(TextWidget(root, 1, 1, 'ewns', 1, 1, '', 75, 25, 'disabled', 'none'))
        frame.append(ScrollbarWidget(root, 0, 1, 'ew', 1, 1, 'horizontal', frame[1].body))
        frame.append(ScrollbarWidget(root, 1, 0, 'ns', 1, 1, 'vertical', frame[1].body))
        return frame

    def constructMIF(self):
        # Manage Import Frame
        frame = [FrameWidget(p.window, 1, 0, 'nsew', 1, 1)]
        root = frame[0].body

        frame.append(LabelWidget(root, 0, 0, '', 1, 1, 'Select Sheet:'))
        frame.append(OptionMenuWidget(root, 0, 1, '', 1, 1, ['No Sheets'], self.updateImport))
        frame.append(LabelWidget(root, 2, 0, '', 1, 1, 'Apply Header:'))
        frame.append(EntryWidget(root, 2, 1, '', 1, 1, '0', 'p_int', self.updateImport))
        frame.append(LabelWidget(root, 3, 0, '', 1, 1, 'Apply Footer:'))
        frame.append(EntryWidget(root, 3, 1, '', 1, 1, '0', 'p_int', self.updateImport))
        return frame

    def constructMTDF(self):
        # Manage Time Data Frame
        frame = [FrameWidget(p.window, 0, 1, 'ewns', 2, 1)]
        root = frame[0].body

        frame.append(LabelWidget(root, 0, 0, '', 1, 1, 'Select Column:'))
        frame.append(OptionMenuWidget(root, 0, 1, '', 1, 1, ['No Columns'], self.selectedDTcolumn))
        frame.append(LabelWidget(root, 1, 0, '', 1, 1, 'Date Object Formatting:'))
        frame.append(OptionMenuWidget(root, 1, 1, '', 1, 1, p.dateFormat, self.updateDateTimeFormat))
        frame.append(LabelWidget(root, 2, 0, '', 1, 1, 'Time Object conversion:'))
        frame.append(OptionMenuWidget(root, 2, 1, '', 1, 1, p.timeFormat, self.updateDateTimeFormat))
        frame.append(LabelWidget(root, 1, 2, '', 1, 1, 'Remove Time Component:'))
        frame.append(CheckbuttonWidget(root, 1, 3, '', 1, 1))
        frame.append(LabelWidget(root, 2, 2, '', 1, 1, 'Remove Date Component:'))
        frame.append(CheckbuttonWidget(root, 2, 3, '', 1, 1))
        frame.append(ButtonWidget(root, 0, 3, '', 1, 1, 'Apply Changes', self.applyDTchanges))
        return frame

    def constructNDA(self):
        # normal distribution anomalies
        frame = [FrameWidget(p.window, 3, 0, 'ewns', 1, 1)]
        root = frame[0].body

        frame.append(LabelWidget(root, 0, 0, '', 1, 1, 'Create Normal For:'))
        frame.append(OptionMenuWidget(root, 0, 1, '', 1, 1, ['No Columns'], self.normalGraph))
        frame.append(LabelWidget(root, 1, 0, '', 1, 3, 'Detect Anomylous Results'))
        frame.append(LabelWidget(root, 2, 0, '', 1, 1, 'Max Deviation:'))
        frame.append(EntryWidget(root, 2, 1, '', 1, 1, '2', 'p_int', self.obtainAnomalies))
        frame.append(ButtonWidget(root, 3, 0, '', 1, 1, '< Prev', self.prevAnom))
        frame.append(TextWidget(root, 3, 1, '', 1, 1, 'None', 15, 1, 'disabled', 'none'))
        frame.append(ButtonWidget(root, 3, 2, '', 1, 1, 'Next >', self.nextAnom))
        frame.append(ButtonWidget(root, 4, 1, '', 1, 1, 'Replace with Mean', self.removeAnomaly))
        frame.append(LabelWidget(root, 0, 4, '', 1, 1, f'Found {len(self.anomalies)}\nPotential Instances'))
        frame.append(LabelWidget(root, 1, 4, '', 1, 1, f'Current Mean:\n{self.mean}'))
        frame.append(LabelWidget(root, 2, 4, '', 1, 1, f'Current Standard Deviation:\n{self.mean}'))
        return frame

    def constructNDGF(self):
        # normal distribution graph frame
        frame = [FrameWidget(p.window, 3, 1, 'ewns', 1, 1)]
        root = frame[0].body

        frame.append(GraphFigWidget(root, 0, 1, '', 2, 1, self.normFig))
        return frame

    def constructMTPF(self):
        # manage time preview frame
        frame = [FrameWidget(p.window, 2, 1, 'ewns', 1, 1)]
        root = frame[0].body

        frame.append(TextWidget(root, 1, 1, 'ewns', 1, 1, '', 75, 25, 'disabled', 'none'))
        frame.append(ScrollbarWidget(root, 1, 0, 'ns', 1, 1, 'vertical', frame[1].body))
        return frame

    def normalGraph(self, *args):
        self.normAxis.clear()
        columndata = p.importingData[self.framesList[4][2].var.get()]
        self.cleandata = []
        try:
            for data in columndata:
                self.cleandata.append(float(data))
        except:
            return False

        if len(self.cleandata) < 25:
            bins = len(self.cleandata)
        else:
            bins = 25
        self.normAxis.hist(self.cleandata, bins=bins, density=True, color='b')

        self.mean, self.stdev = stats.norm.fit(self.cleandata)
        x = np.linspace(min(self.cleandata), max(self.cleandata), 100)
        self.normAxis.plot(x, stats.norm.pdf(x, self.mean, self.stdev), 'k', '--')
        self.normAxis.title.set_text(f'Normal of {self.framesList[4][2].var.get()}')
        self.normFig.canvas.draw()
        self.obtainAnomalies()

    def obtainAnomalies(self, *args):
        maxdev = int(self.framesList[4][5].var.get())
        self.anomalies = []
        upperlimit = (self.mean + (maxdev * self.stdev))
        lowerlimit = (self.mean - (maxdev * self.stdev))
        for value in self.cleandata:
            if value > upperlimit or value < lowerlimit:
                self.anomalies.append(value)

        if len(self.anomalies) > 0:
            self.framesList[4][7].replace(self.anomalies[0])
            self.framesList[4][10].body.config(text=f'Found {len(self.anomalies)}\nPotential Instances')
            self.framesList[4][11].body.config(text=f'Current Mean:\n{self.mean}')
            self.framesList[4][12].body.config(text=f'Current Standard Deviation:\n{self.stdev}')
            self.posInAnom = 0

    def prevAnom(self):
        if self.posInAnom > 0:
            self.posInAnom -= 1
            self.framesList[4][7].replace(self.anomalies[self.posInAnom])
        else:
            return False

    def nextAnom(self):
        if self.posInAnom < len(self.anomalies) - 1:
            self.posInAnom += 1
            self.framesList[4][7].replace(self.anomalies[self.posInAnom])
        else:
            return False

    def removeAnomaly(self):
        colid = self.framesList[4][2].var.get()
        anomaly = self.anomalies[self.posInAnom]
        index = self.cleandata.index(anomaly)

        newcol = []
        for val in p.importingData[colid]:
            if val == anomaly:
                newcol.append(self.mean)
            else:
                newcol.append(val)

        newcoldict = {f'{colid}': newcol}
        newcoldf = pd.DataFrame(newcoldict)
        p.importingData[colid] = newcoldf[colid]
        self.anomalies.pop(self.posInAnom)
        self.framesList[4][10].body.config(text=f'Found {len(self.anomalies)}\nPotential Instances')
        self.framesList[1][1].replace(p.importingData)
        if self.posInAnom > len(self.anomalies) - 1:
            self.prevAnom()
        else:
            self.nextAnom()

    def selectedDTcolumn(self, *args):
        column = self.framesList[3][2].var.get()
        self.olddtvals = p.importingData[column]
        self.oldtvals = []
        self.olddvals = []
        self.newtvals = []
        self.newdvals = []
        self.tempdtvals = []
        for i, val in enumerate(self.olddtvals):
            if isinstance(val, dt.datetime):
                d, t = val.strftime('%d/%m/%Y %X').split(' ')
                d = dt.datetime.strptime(d, '%d/%m/%Y')
                t = dt.datetime.strptime(t, '%H:%M:%S')
            else:
                if i > 0:
                    d, t = self.olddvals[i - 1], self.oldtvals[i - 1]
                else:
                    d, t = self.olddvals[i], self.oldtvals[i]
            self.olddvals.append(d)
            self.oldtvals.append(t)
        self.updateDateTimeFormat()

    def updateDateTimeFormat(self, *args):
        self.tempdtvals = []
        self.newdvals = []
        self.newtvals = []
        dformat = self.framesList[3][4].var.get()
        tformat = self.framesList[3][6].var.get()
        # ['Day', 'Month', 'Year', 'Day/Month/Year', 'Day/Month', 'Month/Year', 'x-axis (from 0)', 'Remove Date Element']
        if len(self.olddtvals) == 0:
            return False
        incdate = self.framesList[3][10].var.get()  # 1=no, 0=yes
        inctime = self.framesList[3][8].var.get()
        if incdate == 1 and inctime == 1:
            return False
        for i, datetime in enumerate(self.olddvals):
            if dformat == 'Day':
                self.newdvals.append(datetime.strftime('%d'))
            elif dformat == 'Month':
                self.newdvals.append(datetime.strftime('%m'))
            elif dformat == 'Year':
                self.newdvals.append(datetime.strftime('%Y'))
            elif dformat == 'Year/Month/Day':
                self.newdvals.append(datetime.strftime('%Y/%m/%d'))
            elif dformat == 'Month/Day':
                self.newdvals.append(datetime.strftime('%m/%d'))
            elif dformat == 'Year/Month':
                self.newdvals.append(datetime.strftime('%Y/%m'))
            elif tformat == '24hr 00:00:00':
                self.newtvals.append(datetime.strftime('%H:%M:%S'))
            elif tformat == 'Hour/Min 00:00:_':
                self.newtvals.append(datetime.strftime('%H:%M'))
            elif tformat == 'Min/Sec _:00:00':
                self.newtvals.append(datetime.strftime('%M:%S'))
            elif tformat == 'Hour 00:_:_':
                self.newtvals.append(datetime.strftime('%H'))
            elif tformat == 'Min _:00:_':
                self.newtvals.append(datetime.strftime('%M'))
            elif tformat == 'Sec _:_:00':
                self.newtvals.append(datetime.strftime('%S'))

        if inctime == 1 or len(self.newtvals) == 0:
            self.tempdtvals = self.newdvals
        elif incdate == 1 or len(self.newdvals) == 0:
            self.tempdtvals = self.newtvals
        else:
            for i in range(len(self.newdvals)):
                self.tempdtvals.append(f'{self.newdvals[i]} {self.newtvals[i]}')

        dateDict = {'Old Values:': self.olddtvals, 'New Values:': self.tempdtvals}
        comparison = pd.DataFrame(dateDict)
        self.framesList[6][1].replace(comparison)

    def applyDTchanges(self):
        newdtdict = {f'{self.framesList[3][2].var.get()}': self.tempdtvals}
        newdtdf = pd.DataFrame(newdtdict)
        p.importingData[self.framesList[3][2].var.get()] = newdtdf[self.framesList[3][2].var.get()]
        self.framesList[1][1].replace(p.importingData)

    def fileFinder(self):
        file = askopenfile(mode='r')
        if file:
            self.path = os.path.join(file.name)
            file, extension = os.path.splitext(file.name)
            if '.csv' in extension:
                self.fileType = 'csv'
                p.importingData = pd.read_csv(self.path)
                self.columns = p.importingData.columns.tolist()
                self.framesList[3][2].changeOptions(self.columns)
                self.framesList[4][2].changeOptions(self.columns)
                self.framesList[1][1].replace(p.importingData)

            elif '.xls' in extension:
                self.fileType = 'xls'
                sheets = sorted(pd.ExcelFile(self.path).sheet_names)
                self.framesList[2][2].changeOptions(sheets)
                self.columns = []

            else:
                pass

    def updateImport(self, *args):
        if self.fileType == 'xls':
            p.importingData = pd.read_excel(self.path,
                                            sheet_name=self.framesList[2][2].var.get(),
                                            header=self.framesList[2][4].var.get(),
                                            skipfooter=self.framesList[2][6].var.get())
            self.columns = p.importingData.columns.tolist()
            self.framesList[3][2].changeOptions(self.columns)
            self.framesList[4][2].changeOptions(self.columns)
            self.framesList[1][1].replace(p.importingData)

    def confirmImport(self):
        data = p.importingData
        dataName = self.framesList[0][3].var.get().strip()
        if dataName == '':
            return False
        else:
            p.importedData.append([dataName, data])
            if self.framesList[0][6].var.get() == 1:
                if os.path.exists(p.datapath):
                    with pd.ExcelWriter(p.datapath, engine='openpyxl', mode='a') as writer:
                        data.to_excel(writer, sheet_name=dataName, index=False)
                else:
                    with pd.ExcelWriter(p.datapath, engine='openpyxl', mode='w') as writer:
                        data.to_excel(writer, sheet_name=dataName, index=False)


ConstructImportDataScreen()


########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################

class ConstructFunctionDataScreen(Screen):
    def __init__(self):
        self.elements = []
        self.positionInFunction = 0
        self.xValues = []
        self.yValues = []
        self.presetFunctions = ['sin(t)', 'cos(t)', 'tan(t)', 'e^(t)', 'e^(t^2)', 'ln(t)']
        framesList = [self.constructSET(), self.constructFOE(), self.constructTRF(), self.constructXYV()]
        super().__init__(framesList, 'Creating Function Data ')

    def constructSET(self):
        # simultenous Equations in T
        frame = [FrameWidget(p.window, 0, 0, 'ewns', 1, 1)]
        root = frame[0].body

        frame.append(LabelWidget(root, 0, 0, '', 1, 1, 'Construct Simultenous Equations:'))
        frame.append(ButtonWidget(root, 0, 1, '', 1, 1, 'Update Function Lists', self.updateFunctionLists))
        frame.append(LabelWidget(root, 1, 0, '', 1, 1, 'Y Function:'))
        frame.append(OptionMenuWidget(root, 1, 1, '', 1, 1, ['Functions'], self.createYValues))
        frame.append(LabelWidget(root, 2, 0, '', 1, 1, 'X Function:'))
        frame.append(OptionMenuWidget(root, 2, 1, '', 1, 1, ['Functions'], self.createXValues))

        frame.append(EntryWidget(root, 3, 0, '', 1, 1, f'DatasetName {len(p.importedData)}', 'c_str', None))
        frame.append(ButtonWidget(root, 3, 1, '', 1, 1, 'Confirm Data', self.confirmData))
        frame.append(LabelWidget(root, 3, 2, '', 1, 1, 'Import Data on Program Load:'))
        frame.append(CheckbuttonWidget(root, 3, 3, '', 1, 1))
        return frame

    def constructFOE(self):
        # Function Of Elements
        frame = [FrameWidget(p.window, 0, 1, 'ewns', 1, 1)]
        root = frame[0].body

        frame.append(ButtonWidget(root, 0, 1, '', 1, 1, '< Prev Element', self.scrollFunctionR))
        frame.append(ButtonWidget(root, 0, 2, '', 1, 1, 'Remove Element', self.removeElement))
        frame.append(ButtonWidget(root, 0, 3, '', 1, 1, 'Next Element >', self.scrollFunctionL))

        frame.append(LabelWidget(root, 1, 0, '', 1, 1, 'Function:'))
        frame.append(TextWidget(root, 1, 1, '', 1, 1, '', 50, 5, 'disabled', None))
        frame.append(TextWidget(root, 1, 2, '', 1, 1, '', 25, 5, 'disabled', None))
        frame.append(TextWidget(root, 1, 3, '', 1, 1, '', 50, 5, 'disabled', None))

        frame.append(ButtonWidget(root, 2, 0, '', 1, 1, 'Add Power Element', self.addPowerElement))
        frame.append(EntryWidget(root, 2, 1, '', 1, 1, '1', 'p_float', None))
        frame.append(LabelWidget(root, 2, 2, '', 1, 1, 't^'))
        frame.append(EntryWidget(root, 2, 3, '', 1, 1, '0', 'p_float', None))

        frame.append(ButtonWidget(root, 3, 0, '', 1, 1, 'Add Function Element', self.addFunctionElement))
        frame.append(OptionMenuWidget(root, 3, 1, '', 1, 1, self.presetFunctions, None))

        frame.append(ButtonWidget(root, 4, 0, '', 1, 1, 'Store Function', self.confirmFunction))
        return frame

    def constructTRF(self):
        # t range frame
        frame = [FrameWidget(p.window, 0, 2, 'ewns', 1, 1)]
        root = frame[0].body

        frame.append(LabelWidget(root, 6, 0, '', 1, 1, 't start:'))
        frame.append(EntryWidget(root, 6, 1, '', 1, 1, '0', 'p_float', None))
        frame.append(LabelWidget(root, 7, 0, '', 1, 1, 't end:'))
        frame.append(EntryWidget(root, 7, 1, '', 1, 1, '100', 'p_float', None))
        frame.append(LabelWidget(root, 8, 0, '', 1, 1, 't step:'))
        frame.append(EntryWidget(root, 8, 1, '', 1, 1, '1', 'p_float', None))
        return frame

    def constructXYV(self):
        # X Y values
        frame = [FrameWidget(p.window, 1, 0, 'ew', 1, 3)]
        root = frame[0].body

        frame.append(LabelWidget(root, 1, 0, '', 1, 1, 'Y values:'))
        frame.append(TextWidget(root, 1, 1, 'ew', 1, 1, '', 250, 1, 'disabled', 'none'))
        frame.append(ScrollbarWidget(root, 0, 1, 'ew', 1, 1, 'horizontal', frame[2].body))
        frame.append(LabelWidget(root, 2, 0, '', 1, 1, 'X values:'))
        frame.append(TextWidget(root, 2, 1, 'ew', 1, 1, '', 250, 1, 'disabled', 'none'))
        frame.append(ScrollbarWidget(root, 3, 1, 'ew', 1, 1, 'horizontal', frame[5].body))
        return frame

    def parseElement(self, element):
        if len(element) == 2:
            return f'{element[0]}t^{element[1]}'

        if len(element) == 1:
            return f'{element[0]}'

    def displayFunctionElements(self):
        L, R, C = '', '', ''
        for i, element in enumerate(self.elements):
            if i < self.positionInFunction:
                L += f'{self.parseElement(element)} + '
            if i == self.positionInFunction:
                C += f'{self.parseElement(element)} + '
            if i > self.positionInFunction:
                R += f'{self.parseElement(element)} + '

        self.framesList[1][5].replace(L)
        self.framesList[1][6].replace(C)
        self.framesList[1][7].replace(R)

    def scrollFunctionR(self):
        if self.positionInFunction > 0:
            self.positionInFunction += -1
        self.displayFunctionElements()

    def scrollFunctionL(self):
        if self.positionInFunction < len(self.elements) - 1:
            self.positionInFunction += 1
        self.displayFunctionElements()

    def addPowerElement(self):
        elementToAdd = [float(self.framesList[1][9].var.get()), float(self.framesList[1][11].var.get())]
        for i, val in enumerate(elementToAdd):
            if int(val) == val:
                elementToAdd[i] = int(val)
        newElementList = []

        if len(self.elements) == 0:
            newElementList.append(elementToAdd)
        else:
            for i, element in enumerate(self.elements):
                if i == self.positionInFunction:
                    newElementList.append(element)
                    newElementList.append(elementToAdd)
                else:
                    newElementList.append(element)
            self.positionInFunction += 1
        self.elements = newElementList
        self.displayFunctionElements()

    def addFunctionElement(self):
        elementToAdd = [self.framesList[1][13].var.get()]
        newElementList = []
        if len(self.elements) == 0:
            newElementList.append(elementToAdd)
        else:
            for i, element in enumerate(self.elements):
                if i == self.positionInFunction:
                    newElementList.append(element)
                    newElementList.append(elementToAdd)
                else:
                    newElementList.append(element)
            self.positionInFunction += 1
        self.elements = newElementList
        self.displayFunctionElements()

    def removeElement(self):
        for i, element in enumerate(self.elements):
            if i == self.positionInFunction:
                self.elements.pop(i)
        if self.positionInFunction > len(self.elements) - 1:
            self.positionInFunction -= 1
        self.displayFunctionElements()

    def confirmFunction(self):
        p.tFunctions.append(self.elements)
        elementsName = ''
        for element in self.elements:
            elementsName += f'{self.parseElement(element)}'
        p.tFunctionsDisplay.append(elementsName)
        self.updateFunctionLists()

    def evaluateFunction(self, functionElements, t):
        pfDict = {'sin(t)': np.sin, 'cos(t)': np.cos, 'tan(t)': np.tan,
                  'e^(t)': np.exp, 'e^(t^2)': np.exp, 'ln(t)': np.log}
        value = 0
        for element in functionElements:
            if len(element) == 2:
                value += element[0] * (t ** element[1])
            else:
                if element[0] == 'e^(t^2)':
                    value += pfDict[element[0]](t ** 2)
                else:
                    value += pfDict[element[0]](t)
        return value

    def updateFunctionLists(self):
        self.framesList[0][4].changeOptions(p.tFunctionsDisplay)
        self.framesList[0][6].changeOptions(p.tFunctionsDisplay)

    def obtainSSS(self):
        values = []
        multipliers = []
        intvalues = []
        for s in range(3):
            values.append(str(self.framesList[2][2 + (2 * s)].var.get()))
            intval, decval = values[s].split('.')
            if decval != '0':
                multipliers.append(len(decval))
            else:
                multipliers.append(0)
            values[s] = float(values[s])
        x10 = max(multipliers)
        for s in range(3):
            intvalues.append(int(values[s] * (10 ** x10)))
        return intvalues, values

    def createXValues(self, *args):
        index = p.tFunctionsDisplay.index(self.framesList[0][6].var.get())
        self.XfunctionElements = p.tFunctions[index]
        self.xValues = []

        # start, stop, step
        intvals, decvals = self.obtainSSS()
        t, step = decvals[0], decvals[2]
        for i in range(intvals[0], intvals[1], intvals[2]):
            value = self.evaluateFunction(self.XfunctionElements, t)
            self.xValues.append(value)
            t += step
        self.framesList[3][5].replace(self.xValues)

    def createYValues(self, *args):
        index = p.tFunctionsDisplay.index(self.framesList[0][4].var.get())
        self.YfunctionElements = p.tFunctions[index]
        self.yValues = []

        # start, stop, step
        intvals, decvals = self.obtainSSS()
        t, step = decvals[0], decvals[2]
        for i in range(intvals[0], intvals[1], intvals[2]):
            value = self.evaluateFunction(self.YfunctionElements, t)
            self.yValues.append(value)
            t += step
        self.framesList[3][2].replace(self.yValues)

    def confirmData(self):
        name = self.framesList[0][7].var.get().strip()
        if name != '':
            data = {'Yvalues': self.yValues, 'Xvalues': self.xValues}
            data = pd.DataFrame(data)
            p.importedData.append([name, data])
            if self.framesList[0][10].var.get() == 1:
                if os.path.exists(p.datapath):
                    with pd.ExcelWriter(p.datapath, engine='openpyxl', mode='a') as writer:
                        data.to_excel(writer, sheet_name=name, index=False)
                else:
                    with pd.ExcelWriter(p.datapath, engine='openpyxl', mode='w') as writer:
                        data.to_excel(writer, sheet_name=name, index=False)


ConstructFunctionDataScreen()


########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################

class Line():
    def __init__(self, xvals, yvals, root, rootfig, name, lineid, linecol, linestyle, markerstyle, markersize):
        p.linesList.append(self)
        self.xvals = xvals
        self.yvals = yvals
        self.removed = False
        if xvals == 'axis':
            for i in range(len(yvals)):
                self.xvals.append(i)
        if yvals == 'axis':
            for i in range(len(xvals)):
                self.xvals.append(i)
        self.workingArgs = [self.xvals, self.yvals, root, rootfig, name, lineid, linecol, linestyle, markerstyle,
                            int(markersize)]
        self.confirmedArgs = []  # rootaxis, rootfig, name, id, linecol, linestyle, markerstyle, markercol
        self.markersize = int(markersize)

    def graph(self, vals):
        # xvals, yvals, root, rootfig, name, lineid, linecol, linestyle, markerstyle, markersize
        vals[2].plot(vals[0], vals[1],
                     label=f'{vals[4]}\nid:{vals[5]}',
                     color=vals[6],
                     marker=vals[8],
                     markersize=vals[9],
                     linestyle=vals[7])

    def update(self, linecol, linestyle, markerstyle, markersize):
        self.workingArgs = [self.workingArgs[0], self.workingArgs[1], self.workingArgs[2], self.workingArgs[3],
                            self.workingArgs[4], self.workingArgs[5],
                            linecol, linestyle, markerstyle, int(markersize)]

    def remove(self):
        self.removed = True

    def delete(self):
        del self


########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################

class ConstructDataGraphScreen(Screen):
    def __init__(self):
        self.graphFig, self.graphAxis = plt.subplots(2, 1, figsize=(9, 6), dpi=100)
        self.graphFig.tight_layout(rect=[0.1, 0, 0.8, 0.9], pad=1.5)
        # axis0 for completed, axis1 for working
        self.graphAxis[0].tick_params(axis='x', labelsize=6)
        self.graphAxis[0].tick_params(axis='y', labelsize=6)
        self.graphAxis[1].tick_params(axis='x', labelsize=6)
        self.graphAxis[1].tick_params(axis='y', labelsize=6)

        self.bflineid = ''
        self.linetofit = ''

        self.storedGraphInfo = []
        self.tempStoredGraphInfo = []
        self.colour = ['red', 'blue', 'green', 'cyan', 'magenta', 'black']
        self.marker = ['point', 'circle', 'triangle', 'cross']
        self.style = ['solid', 'dashed', 'dotted', 'dot/dash', 'none']
        self.colourDict = {'red': 'r', 'blue': 'b', 'green': 'g', 'cyan': 'c', 'magenta': 'm', 'black': 'k'}
        self.markerDict = {'point': '.', 'circle': 'o', 'triangle': 'v', 'cross': 'x'}
        self.styleDict = {'solid': '-', 'dashed': '--', 'dotted': ':', 'dot/dash': '-.', 'none': 'none'}
        framesList = [self.constructDPF(), self.constructMGF(), self.constructMDF(), self.constructGraphs(),
                      self.constructLBF()]
        super().__init__(framesList, 'Graph Data')

    def constructDPF(self):
        # data plotter frame
        frame = [FrameWidget(p.window, 0, 0, 'ewns', 1, 1)]
        root = frame[0].body

        frame.append(LabelWidget(root, 0, 0, '', 2, 1, 'Plot Data to Frame:'))
        frame.append(LabelWidget(root, 0, 1, '', 1, 1, 'Dataset:'))
        frame.append(LabelWidget(root, 0, 2, '', 1, 1, 'Y-axis:'))
        frame.append(LabelWidget(root, 0, 3, '', 1, 1, 'X-axis:'))
        frame.append(OptionMenuWidget(root, 1, 1, '', 1, 1, ['No Datasets'], self.updateDataSelection))
        frame.append(OptionMenuWidget(root, 1, 2, '', 1, 1, ['No Columns'], None))
        frame.append(OptionMenuWidget(root, 1, 3, '', 1, 1, ['No Columns'], None))
        frame.append(ButtonWidget(root, 0, 4, '', 2, 1, 'Load Stored Data', self.updateDataOptions))
        frame.append(EntryWidget(root, 0, 5, '', 2, 1, 'Line Label', 'c_str', None))
        frame.append(ButtonWidget(root, 2, 0, '', 1, 1, 'Add to Graph', self.addGraphElement))
        return frame

    def constructMGF(self):
        # manage graph frame
        frame = [FrameWidget(p.window, 0, 1, 'ewns', 1, 1)]
        root = frame[0].body

        frame.append(LabelWidget(root, 0, 0, '', 1, 1, 'Graph Title:'))
        frame.append(LabelWidget(root, 1, 0, '', 1, 1, 'X-axis Title:'))
        frame.append(LabelWidget(root, 2, 0, '', 1, 1, 'Y-axis Title:'))
        frame.append(EntryWidget(root, 0, 1, '', 1, 1, 'Title', 'c_str', self.applyTitles))
        frame.append(EntryWidget(root, 1, 1, '', 1, 1, 'X-axis', 'c_str', self.applyTitles))
        frame.append(EntryWidget(root, 2, 1, '', 1, 1, 'Y-axis', 'c_str', self.applyTitles))
        frame.append(ButtonWidget(root, 0, 2, '', 3, 1, 'Save Graph as PDF', self.saveImage))
        return frame

    def constructMDF(self):
        # manage data frame
        frame = [FrameWidget(p.window, 1, 1, 'ewns', 1, 1)]
        root = frame[0].body

        frame.append(LabelWidget(root, 0, 0, '', 1, 1, 'Update Line ID:'))
        frame.append(EntryWidget(root, 0, 1, '', 1, 1, '0', 'p_int', None))
        frame.append(ButtonWidget(root, 0, 2, '', 1, 1, 'Remove Line', self.removeLine))
        frame.append(LabelWidget(root, 1, 0, '', 1, 1, 'Line Colour'))
        frame.append(OptionMenuWidget(root, 1, 1, '', 1, 1, self.colour, self.updateLine))
        frame.append(LabelWidget(root, 2, 0, '', 1, 1, 'Line Style'))
        frame.append(OptionMenuWidget(root, 2, 1, '', 1, 1, self.style, self.updateLine))
        frame.append(LabelWidget(root, 3, 0, '', 1, 1, 'Marker Style'))
        frame.append(OptionMenuWidget(root, 3, 1, '', 1, 1, self.marker, self.updateLine))
        frame.append(LabelWidget(root, 4, 0, '', 1, 1, 'Marker Size'))
        frame.append(EntryWidget(root, 4, 1, '', 1, 1, '0', 'p_int', self.updateLine))
        frame.append(LabelWidget(root, 5, 0, '', 1, 1, 'Change Label:'))
        frame.append(EntryWidget(root, 5, 1, '', 1, 1, 'Label Name', 'c_str', None))
        frame.append(ButtonWidget(root, 5, 2, '', 1, 1, 'Change Label', self.updateLabel))
        return frame

    def constructGraphs(self):
        # make graph widget
        frame = [FrameWidget(p.window, 1, 0, 'ewns', 1, 1)]
        root = frame[0].body

        frame.append(GraphFigWidget(root, 0, 1, '', 2, 1, self.graphFig))
        frame.append(ButtonWidget(root, 0, 0, '', 1, 1, 'Confirm Changes', self.confirmChanges))
        frame.append(ButtonWidget(root, 1, 0, '', 1, 1, 'Clear Changes', self.clearChanges))
        return frame

    def constructLBF(self):
        # line of best fit
        frame = [FrameWidget(p.window, 2, 0, 'ewns', 1, 2)]
        root = frame[0].body

        frame.append(LabelWidget(root, 0, 0, '', 1, 1, 'Construct Best Fit to Line ID:'))
        frame.append(EntryWidget(root, 0, 1, '', 1, 1, '0', 'p_int', None))
        frame.append(LabelWidget(root, 1, 0, '', 1, 1, 'Max Poly Order:'))
        frame.append(EntryWidget(root, 1, 1, '', 1, 1, '5', 'p_int', None))
        frame.append(LabelWidget(root, 2, 0, '', 1, 1, 'Label:'))
        frame.append(EntryWidget(root, 2, 1, '', 2, 1, 'Best Fit Line', 'c_str', None))
        frame.append(ButtonWidget(root, 3, 0, '', 1, 1, 'Add Best Fit', self.addBestFit))
        return frame

    def updateDataOptions(self, *args):
        options = []
        for data in p.importedData:
            options.append(data[0])
        self.framesList[0][5].changeOptions(options)

    def updateDataSelection(self, *args):
        names = []
        for data in p.importedData:
            names.append(data[0])
        index = names.index(self.framesList[0][5].var.get())
        dataset = p.importedData[index][1]
        columns = list(dataset.columns)
        columns.append('axis')
        self.framesList[0][6].changeOptions(columns)
        self.framesList[0][7].changeOptions(columns)

    def addGraphElement(self):
        # xvals, yvals, root, rootfig, name, lineid, linecol, linestyle, markerstyle, markersize
        dataname = self.framesList[0][5].var.get()
        yid = self.framesList[0][6].var.get()
        xid = self.framesList[0][7].var.get()
        dataid = -1
        for i, data in enumerate(p.importedData):
            if data[0] == dataname:
                dataid = i

        yvals = []
        xvals = []
        if xid == 'axis' and yid == 'axis':
            return False
        elif xid == 'axis':
            for val in p.importedData[dataid][1][yid]:
                yvals.append(val)
            for i in range(len(yvals)):
                xvals.append(i)
        elif yid == 'axis':
            for val in p.importedData[dataid][1][xid]:
                xvals.append(val)
            for i in range(len(xvals)):
                yvals.append(i)
        else:
            for val in p.importedData[dataid][1][xid]:
                xvals.append(val)
            for val in p.importedData[dataid][1][yid]:
                yvals.append(val)

        root = self.graphAxis[1]
        rootfig = self.graphFig
        name = self.framesList[0][9].var.get()
        lineid = len(p.linesList)
        linecol = self.colourDict[self.framesList[2][5].var.get()]
        linestyle = self.styleDict[self.framesList[2][7].var.get()]
        markerstyle = self.markerDict[self.framesList[2][9].var.get()]
        markersize = self.framesList[2][11].var.get()
        Line(xvals, yvals, root, rootfig, name, lineid, linecol, linestyle, markerstyle, markersize)
        self.updateGraphAxis(self.graphAxis[1], self.graphFig, p.linesList)

    def applyTitles(self, *args):
        self.graphAxis[0].set_xlabel(self.framesList[1][5].var.get())
        self.graphAxis[0].set_ylabel(self.framesList[1][6].var.get())
        self.graphAxis[1].set_xlabel(self.framesList[1][5].var.get())
        self.graphAxis[1].set_ylabel(self.framesList[1][6].var.get())
        self.graphAxis[0].title.set_text(self.framesList[1][4].var.get())
        self.graphFig.canvas.draw()

    def updateLine(self, *args):
        colourDict = {'red': 'r', 'blue': 'b', 'green': 'g', 'cyan': 'c', 'magenta': 'm', 'black': 'k'}
        markerDict = {'point': '.', 'circle': 'o', 'triangle': 'v', 'cross': 'x'}
        styleDict = {'solid': '-', 'dashed': '--', 'dotted': ':', 'dot/dash': '-.', 'none': 'none'}
        # linecol, linestyle, markerstyle, markersize
        lineid = int(self.framesList[2][2].var.get())
        line = p.linesList[lineid]

        linecol = colourDict[self.framesList[2][5].var.get()]
        linestyle = styleDict[self.framesList[2][7].var.get()]
        markerstyle = markerDict[self.framesList[2][9].var.get()]
        markersize = self.framesList[2][11].var.get()
        line.update(linecol, linestyle, markerstyle, markersize)
        self.updateGraphAxis(self.graphAxis[1], self.graphFig, p.linesList)

    def updateLabel(self, *args):
        label = self.framesList[2][13].var.get()
        lineid = int(self.framesList[2][2].var.get())
        line = p.linesList[lineid]
        line.workingArgs[4] = label
        self.updateGraphAxis(self.graphAxis[1], self.graphFig, p.linesList)

    def updateGraphAxis(self, axis, fig, lines):
        axis.clear()
        print(len(lines), lines)
        xvalslen = []
        for line in lines:
            print('line')
            if line.removed == False:
                if axis == self.graphAxis[0]:
                    line.graph(line.confirmedArgs)
                else:
                    line.graph(line.workingArgs)
        axis.legend(bbox_to_anchor=(1.04, 1), loc='upper left', borderaxespad=0)
        axis.locator_params(axis='both', nbins=15)
        self.applyTitles()
        fig.canvas.draw()

    def removeLine(self):
        lineid = int(self.framesList[2][2].var.get())
        line = p.linesList[lineid]
        line.remove()
        self.updateGraphAxis(self.graphAxis[1], self.graphFig, p.linesList)

    def confirmChanges(self):
        for line in p.linesList:
            line.confirmedArgs = []
            if line.removed == True:
                removeid = 0
                for i, linetoshift in enumerate(p.linesList):
                    if linetoshift.workingArgs[5] > line.workingArgs[5]:
                        linetoshift.workingArgs[5] -= 1
                    if line == linetoshift:
                        removeid = i
                p.linesList.pop(removeid)
                del line
            else:
                if len(p.linesList) == 0:
                    break

                for element in line.workingArgs:
                    line.confirmedArgs.append(element)
                line.confirmedArgs[2] = self.graphAxis[0]
        self.updateGraphAxis(self.graphAxis[0], self.graphFig, p.linesList)

    def clearChanges(self):
        for line in p.linesList:
            if line.confirmedArgs == []:
                del p.linesList[line.workingArgs[5]]
            else:
                if line.removed == True:
                    line.removed = False
                line.workingArgs = []
                for element in line.confirmedArgs:
                    line.workingArgs.append(element)
                line.workingArgs[2] = self.graphAxis[1]
        self.updateGraphAxis(self.graphAxis[1], self.graphFig, p.linesList)

    def saveImage(self):
        title = self.framesList[1][4].var.get().strip()
        title = f'{title}.pdf'
        try:
            bounds = self.graphAxis[0].get_window_extent().transformed(self.graphFig.dpi_scale_trans.inverted())
            self.graphFig.savefig(title, bbox_inches=bounds.expanded(1.45, 1.5))
        except:
            print('file name error')

    def orderFunction(self, x, *coeffs):
        function = 0
        for order, coeff in enumerate(coeffs):
            function += coeff * (x ** order)
        return function

    def addBestFit(self):

        lineid = int(self.framesList[4][2].var.get())
        self.linetofit = p.linesList[lineid]
        linename = self.framesList[4][6].var.get()
        xvals = self.linetofit.confirmedArgs[0]
        yvals = self.linetofit.confirmedArgs[1]
        maxpoly = int(self.framesList[4][4].var.get())

        # create Best Fit Line
        # create function for best fit line:
        for f in range(maxpoly):
            coeffs, _ = curve_fit(self.orderFunction, xvals, yvals, p0=[0] * (f + 1))

        # determine (x,y) values
        bfxvals = np.arange(min(xvals), max(xvals), 1)
        bfyvals = self.orderFunction(bfxvals, *coeffs)

        # create line object:
        # xvals, yvals, root, rootfig, name, lineid, linecol, linestyle, markerstyle, markersize
        self.bflineid = len(p.linesList)
        Line(bfxvals, bfyvals, self.graphAxis[1], self.graphFig, linename, self.bflineid, 'r', '--', '.', '0')
        self.updateGraphAxis(self.graphAxis[1], self.graphFig, p.linesList)


ConstructDataGraphScreen()

########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################

