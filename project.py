from ttPython import Ui_MainWindow
from matplotlib import style
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import numpy as np

plt.style.use('seaborn-v0_8-bright')
plt.style.use('seaborn-v0_8-notebook')
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_win=QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        
        self.uic.load.clicked.connect(self.getCSV)
        self.uic.exit.clicked.connect(self.Exit)
        
    def show(self):
        self.main_win.show()
        #print(plt.style.available)
    def Exit(self):
        self.main_win.close()
        print("Exit Successful, thank for use :3")

    def getCSV(self):
        self.openFile = QFileDialog.getOpenFileName(filter="CSV (*.csv)")[0]
        self.df = pd.read_csv(self.openFile, encoding='utf-8').fillna(0)
        print("Load Successful !")
        self.uic.visual.clicked.connect(self.show_chart)

    def show_chart(self):
        if self.uic.screen.isEmpty():
            self.uic.screen.addWidget(show_Hist(self.df))
        if self.uic.screen_2.isEmpty():
            self.uic.screen_2.addWidget(show_Line(self.df))
        if self.uic.screen_3.isEmpty():
            self.uic.screen_3.addWidget(show_Scatter(self.df))
        if self.uic.screen_4.isEmpty():
            self.uic.screen_4.addWidget(show_Bar(self.df))

class show_Hist(FigureCanvas):
    def __init__(self ,df):
        self.fig, self.ax=plt.subplots()
        super().__init__(self.fig)

        df['Month'] = pd.to_datetime(df['Month'])
        self.ax.hist(df['New_deaths'],bins='auto',ec='#00A06B',color='#A2007C',alpha=0.3)
        self.fig.suptitle("Histogram")
        
class show_Line(FigureCanvas):
    def __init__(self ,df):
        self.fig, self.ax=plt.subplots()
        super().__init__(self.fig) 

        df['Month'] = pd.to_datetime(df['Month'])
        self.ax.plot(df['Month'], df['New_deaths']-0.2,dashes=[6,2],color='#0000CD',
                        label='New_deaths')
        self.ax.set_xlabel('Month')
        self.ax.set_ylabel('Amount_Death')
        self.fig.suptitle('Line')
        self.ax.legend(['New_deaths'])

class show_Bar(FigureCanvas):
    def __init__(self ,df):
        self.fig, self.ax=plt.subplots()
        super().__init__(self.fig) 
        
        xpos=np.arange(1,len(df['Month'])+1)
        df['Month'] = pd.to_datetime(df['Month'])
       
        #self.ax.set_xticks(df['Month'])
        self.ax.bar(xpos,df['New_deaths'],color='#F4A460')

        self.fig.suptitle('Bar')

class show_Scatter(FigureCanvas):
    def __init__(self ,df):
        
        self.fig, self.ax=plt.subplots()
        super().__init__(self.fig)
        
        self.rng=np.random.RandomState(0)
        colors=self.rng.rand(12)

        df['Month'] = pd.to_datetime(df['Month'])
        self.ax.scatter(df['Month'], df['New_deaths'],c=colors, s=df['New_deaths'],
                        cmap='viridis',alpha=0.7)

        self.ax.set_ylabel('Death')
        self.ax.set_xlabel('Month')
        self.fig.suptitle('Scatter')  

        death_range=[50,500,1000,2000]
        for i in death_range:
            self.ax.scatter([],[],s=i,label='>'+str(i)+'person',alpha=0.5)
        self.fig.legend(labelspacing=3,title='Amout Death',loc='lower right')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

