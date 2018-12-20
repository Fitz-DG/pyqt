#-*-coding:utf-8
import sys

from Crawler import Crawler
from Model import PandasModel

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import pandas as pd
from pandas import Series, DataFrame

#form_class = uic.loadUiType('pyqt.ui')[0]

#plt.rcParams["font.family"] = 'NanumGothic'
plt.rcParams["font.family"] = 'H2GTRE'
plt.rcParams["font.size"] =9
plt.rcParams['xtick.labelsize'] = 9.
plt.rcParams['ytick.labelsize'] = 9.
plt.rcParams["figure.figsize"] = (14,4)
plt.rcParams['axes.grid'] = True
plt.rcParams['axes.unicode_minus'] = False

path = r'c:\windows\fonts\malgun.ttf'
font_name = font_manager.FontProperties(fname = path).get_name()
rc('font', family=font_name)

kospi200 = [
            ['005930', '삼성전자'], ['000660', 'SK하이닉스'], ['028260', '삼성물산'], ['015760', '한국전력'], ['005490', 'POSCO'], ['012330', '현대모비스'], ['105560', 'KB금융'], ['032830', '삼성생명'], ['017670', 'SK텔레콤'], ['051910', 'LG화학'], ['034730', 'SK'], ['207940', '삼성바이오로직스'], ['090430', '아모레퍼시픽'], ['033780', 'KT&G'],
            ['051900', 'LG생활건강'], ['096770', 'SK이노베이션'], ['086790', '하나금융지주'], ['003550', 'LG'], ['000810', '삼성화재'], ['034220', 'LG디스플레이'], ['066570', 'LG전자'], ['000030', '우리은행'], ['006400', '삼성SDI'], ['011170', '롯데케미칼'], ['002790', '아모레G'], ['010950', 'S-Oil'], ['009540', '현대중공업'], ['023530', '롯데쇼핑'],
            ['010130', '고려아연'], ['030200', 'KT'], ['036570', '엔씨소프트'], ['004020', '현대제철'], ['024110', '기업은행'], ['161390', '한국타이어'], ['021240', '코웨이'], ['009150', '삼성전기'], ['035250', '강원랜드'], ['006800', '미래에셋대우'], ['032640', 'LG유플러스'], ['139480', '이마트'], ['078930', 'GS'], ['088350', '한화생명'],
            ['086280', '현대글로비스'], ['004800', '효성'], ['047810', '한국항공우주'], ['001040', 'CJ'], ['079160', 'CJ'], ['018880', '한온시스템'], ['008930', '한미사이언스'], ['000720', '현대건설'], ['009830', '한화케미칼'], ['036460', '한국가스공사'], ['010140', '삼성중공업'], ['097950', 'CJ제일제당'],
            ['097955', 'CJ제일제당'], ['002380', 'KCC'], ['029780', '삼성카드'], ['009240', '한샘'], ['005940', 'NH투자증권'], ['128940', '한미약품'], ['000120', 'CJ대한통운'], ['007070', 'GS리테일'], ['071050', '한국금융지주'], ['011070', 'LG이노텍'], ['016360', '삼성증권'], ['012750', '에스원'], ['003490', '대한항공'],
            ['138930', 'BNK금융지주'], ['012630', '현대산업'], ['001450', '현대해상'], ['047040', '대우건설'], ['000210', '대림산업'], ['008560', '메리츠종금증권'], ['000100', '유한양행'], ['047050', '포스코대우'], ['007310', '오뚜기'], ['069960', '현대백화점'], ['060980', '만도'], ['204320', '만도'], ['000150', '두산'],
            ['006260', 'LS'], ['012450', '한화테크윈'], ['028050', '삼성엔지니어링'], ['004170', '신세계'], ['035510', '신세계'], ['008770', '호텔신라'], ['011780', '금호석유'], ['034020', '두산중공업'], ['010620', '현대미포조선'], ['006360', 'GS건설'], ['007070', 'GS리테일'], ['073240', '금호타이어'], ['007310', '오뚜기'],
            ['010620', '현대미포조선'], ['006280', '녹십자'], ['105630', '한세실업'], ['108670', 'LG하우시스'], ['010780', '아이에스동서'], ['003240', '태광산업'], ['001430', '세아베스틸'], ['049770', '동원F&B'], ['002350', '넥센타이어'], ['120110', '코오롱인더'], ['161890', '한국콜마'], ['001120', 'LG상사'], ['069260', '휴켐스'],
            ['003620', '쌍용차'], ['003300', '한일시멘트'], ['011790', 'SKC'], ['003410', '쌍용양회'], ['002270', '롯데푸드'], ['033920', '무학'], ['128940', '한미약품'], ['069620', '대웅제약'], ['002240', '고려제강'], ['005180', '빙그레'], ['020000', '한섬'], ['029530', '신도리코'], ['000070', '삼양홀딩스'], ['170900', '동아에스티'],
            ['005850', '에스엘'], ['025540', '한국단자'], ['064960', 'S&T모티브'], ['115390', '락앤락'], ['000640', '동아쏘시오홀딩스'], ['009290', '광동제약'], ['002960', '한국쉘석유'], ['003000', '부광약품'], ['001230', '동국제강'], ['004490', '세방전지'], ['003030', '세아제강'], ['006650', '대한유화'], ['000480', '조선내화'],
            ['003920', '남양유업'], ['034120', 'SBS'], ['097230', '한진중공업'], ['007570', '일양약품'], ['082740', '두산엔진'], ['008060', '대덕전자'], ['079980', '휴비스'], ['009680', '모토닉'], ['025860', '남해화학'], ['000430', '대원강업'], ['014830', '유니드'], ['016800', '퍼시스'],
            ['005090', '삼광글라스'], ['020150', '일진머티리얼즈'], ['009580', '무림P&P'], ['003570', 'S&T중공업'], ['033530', '세종공업'], ['104700', '한국철강'], ['078520', '에이블씨엔씨'], ['010690', '화신'], ['002020', '코오롱'], ['000140', '하이트진로홀딩스'], ['007690', '국도화학'], ['003520', '영진약품'], ['004130', '대덕GDS'],
            ['093370', '후성'], ['004710', '한솔테크닉스'], ['033240', '자화전자'], ['020760', '일진디스플'], ['007810', '코리아써키트'], ['004430', '송원산업'], ['005950', '이수화학'], ['006380', '카프로'] ]
#['282330', 'BGF리테일'],['282690', '동아타이어'],['213500', '한솔제지'],

#def doGenerate(setValue) :
#    for x2 in range(5):
#        loop = QEventLoop()
#        QTimer.singleShot(1000, loop.quit)
#        loop.exec_()
#        setValue(x2 +1)
#    print('Done')

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()



    def setTopLayout(self):
        self.checkBox1= QCheckBox("매출액", self)
        self.checkBox1.setChecked(True)
        self.spinBox1 = QSpinBox(self)
        #self.spinBox1.setValue(2000)
        self.spinBox1.setSingleStep(1000)
        self.spinBox1.setRange(0,10000000)

        self.spinBox1.setMinimumWidth(100)
        self.Label1 = QLabel("이상   ", self)
        #self.spinBox1.valueChanged.connect(self, spinBoxChanged)

        self.checkBox2= QCheckBox("PER", self)
        self.checkBox2.setChecked(True)
        self.spinBox2 = QSpinBox(self)
        self.spinBox2.setSingleStep(1)
        self.spinBox2.setMinimumWidth(100)
        self.spinBox2.setMinimum(0)
        self.spinBox2.setMaximum(100)
        self.Label2 = QLabel("미만   ", self)

        self.checkBox3= QCheckBox("최근 3년 당기순이익 점차 증가", self)
        self.checkBox3.setChecked(True)

        self.checkBox4= QCheckBox("최근 3년 매출액 점차 항상", self)
        self.checkBox4.setChecked(True)
        self.pushButton5= QPushButton("검색", self)
        self.pushButton5.clicked.connect(self.onClickButton)

        self.TopLayout  = QHBoxLayout()
        self.TopRightLayout  = QHBoxLayout()
        self.TopLeftLayout  = QHBoxLayout()
        self.TopLayout.addLayout(self.TopRightLayout)
        self.TopLayout.addLayout(self.TopLeftLayout)
        self.TopGroupBox = QGroupBox(' 검색조건 ')
        self.TopGroupBox.setLayout(self.TopLayout)

        self.TopLeftLayout.addWidget(self.checkBox1)
        self.TopLeftLayout.addWidget(self.spinBox1)
        self.TopLeftLayout.addWidget(self.Label1)
        self.TopLeftLayout.addSpacing(5)
        self.TopLeftLayout.addWidget(self.checkBox2)
        self.TopLeftLayout.addWidget(self.spinBox2)
        self.TopLeftLayout.addWidget(self.Label2)
        self.TopLeftLayout.addSpacing(5)
        self.TopLeftLayout.addWidget(self.checkBox3)
        self.TopLeftLayout.addSpacing(5)
        self.TopLeftLayout.addWidget(self.checkBox4)
        self.TopLeftLayout.addWidget(self.pushButton5)
        #self.TopLeftLayout.addSpacing(5)
        self.TopLeftLayout.setAlignment(Qt.AlignLeft )

        self.spinBox1.setValue(100000)
        self.spinBox2.setValue(10)

    def onClickButton(self):
        machul = self.spinBox1.value()
        PER = self.spinBox2.value()
        print( 'Gross = '+str(machul))
        print( 'PER = '+str(PER))
        self.SearchResultDict = self.List200_Dict.copy()

        SelectedKeys = []
        if ( self.checkBox1.isChecked() == True ) :
            Gross = self.spinBox1.value()
            for i in self.SearchResultDict :
                CompanyTable = self.SearchResultDict[str(i)]

                if CompanyTable['매출액'][-3] >  int(Gross) :
                    pass
                    #print("Dict Added "+str(i))
                    #self.SearchResultDict[i] = CompanyTable
                else :
                    print("Dict Deleted "+str(i))
                    SelectedKeys.append(str(i))
            for i in SelectedKeys :
                if i in self.SearchResultDict :
                    del( self.SearchResultDict[i])

        SelectedKeys = []
        if ( self.checkBox2.isChecked() == True ) :
            PER = self.spinBox2.value()
            for i in self.SearchResultDict :
                CompanyTable = self.SearchResultDict[str(i)]

                #if CompanyTable['PER(배)'][-3] <  int(PER) :
                if CompanyTable['PER(배)'][-3] <  int(PER) and CompanyTable['PER(배)'][-3] >  0 :
                    print("Dict Added by PER"+str(i))
                    pass
                    #self.SearchResultDict[i] = CompanyTable
                else :
                    print("Dict Deleted by PER"+str(i))
                    SelectedKeys.append(str(i))
            for i in SelectedKeys :
                if i in self.SearchResultDict :
                    del( self.SearchResultDict[i])

        SelectedKeys = []
        if ( self.checkBox3.isChecked() == True ) :
            for i in self.SearchResultDict :
                CompanyTable = self.SearchResultDict[str(i)]

                if CompanyTable['당기순이익'][-5] <  CompanyTable['당기순이익'][-4] and \
                   CompanyTable['당기순이익'][-4] <  CompanyTable['당기순이익'][-3] :
                    print("Dict Added by Profit"+str(i))
                    pass
                    #self.SearchResultDict[i] = CompanyTable
                else :
                    print("Dict Deleted by Profit"+str(i))
                    SelectedKeys.append(str(i))
            for i in SelectedKeys :
                if i in self.SearchResultDict :
                    del( self.SearchResultDict[i])

        SelectedKeys = []
        if ( self.checkBox4.isChecked() == True ) :
            for i in self.SearchResultDict :
                CompanyTable = self.SearchResultDict[str(i)]

                if CompanyTable['매출액'][-5] <  CompanyTable['매출액'][-4] and \
                        CompanyTable['매출액'][-4] <  CompanyTable['매출액'][-3] :
                    print("Dict Added by Gross"+str(i))
                    pass
                    #self.SearchResultDict[i] = CompanyTable
                else :
                    print("Dict Deleted by Gross"+str(i))
                    SelectedKeys.append(str(i))
            for i in SelectedKeys :
                if i in self.SearchResultDict :
                    del( self.SearchResultDict[i])

        self.setTable0WidgetData(self.SearchResultDict)


    def setTableLayout(self):
        self.Tab0Layout  = QVBoxLayout()
        self.Tab1Layout  = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab1, "배당률 기반 검색 결과")
        self.tabs.addTab(self.tab2, "해당 종목 제무재표")

        self.table0Widget = QTableWidget(self)
        self.table0Widget.setMinimumWidth(700)
        self.table0Widget.setRowCount(200)
        self.table0Widget.setColumnCount(len(self.df.columns))
        print( self.df.columns)
        self.setTable0WidgetData(self.List200_Dict)
        self.table0Widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table0Widget.setSelectionBehavior(QTableWidget.SelectRows)

        self.table1Widget = QTableWidget(self)
        self.table1Widget.setMinimumWidth(700)
        self.table1Widget.setRowCount(len(self.df.index))
        self.table1Widget.setColumnCount(len(self.df.columns))
        self.table1Widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.setTable1WidgetData()

        self.Tab0Layout.addWidget(self.table0Widget)
        self.Tab1Layout.addWidget(self.table1Widget)
        self.tab1.setLayout(self.Tab0Layout)
        self.tab2.setLayout(self.Tab1Layout)

    def setBotLayout(self):
        self.BotLayout  = QHBoxLayout()

        self.fig0 = plt.Figure()
        self.ax0 = self.fig0.add_subplot(1, 1, 1)  # fig0를 1행 1칸으로 나누어 1칸안에 넣어줍니다
        self.ax0.grid()
        self.canvas0 = FigureCanvas(self.fig0)
        self.canvas0.resize(500,500)
        self.canvas0.draw()

        self.fig1 = plt.Figure()
        self.ax1 = self.fig1.add_subplot(1, 1, 1)  # fig1를 1행 1칸으로 나누어 1칸안에 넣어줍니다
        self.ax1.grid()
        self.canvas1 = FigureCanvas(self.fig1)
        self.canvas1.resize(500,500)
        self.canvas1.draw()

        self.fig2 = plt.Figure()
        self.ax2 = self.fig2.add_subplot(1, 1, 1)  # fig2를 1행 1칸으로 나누어 1칸안에 넣어줍니다
        self.ax2.grid()
        self.canvas2 = FigureCanvas(self.fig2)
        self.canvas2.resize(500,500)
        self.canvas2.draw()

        self.fig3 = plt.Figure()
        self.ax3 = self.fig3.add_subplot(1, 1, 1)  # fig3를 1행 1칸으로 나누어 1칸안에 넣어줍니다
        self.ax3.grid()
        self.canvas3 = FigureCanvas(self.fig3)
        self.canvas3.resize(100,100)
        self.canvas3.draw()


        self.BotLayout.addWidget(self.canvas0)
        self.BotLayout.addWidget(self.canvas1)
        self.BotLayout.addWidget(self.canvas2)
        self.BotLayout.addWidget(self.canvas3)
        #self.updatePlot()

    def updatePlot(self,cmp_code):
        #print("cmp_code="+cmp_code)
        self.ax0.clear()
        self.ax0.set_title('현금DPS(원)')
        self.List200_Dict[cmp_code]['현금DPS(원)'].plot(ax=self.ax0)
        self.canvas0.draw()

        self.ax1.clear()
        self.ax1.set_title('당기순이익')
        self.List200_Dict[cmp_code]['당기순이익'].plot(ax=self.ax1)
        self.canvas1.draw()

        self.ax2.clear()
        self.ax2.set_title('PER(배)')
        self.List200_Dict[cmp_code]['PER(배)'].plot(ax=self.ax2)
        self.canvas2.draw()

        self.ax3.clear()
        self.ax3.set_title('매출액')
        self.List200_Dict[cmp_code]['매출액'].plot(ax=self.ax3)
        self.canvas3.draw()

    def setupUI(self):
        self.setWindowTitle("배당검색기반 종목검색 v0.1")
        self.setGeometry(50,50,1800,900)

        self.List200_Dict = {}
        cr = Crawler()
        for  i, v in enumerate(kospi200) :
            self.cmp_code = v[0]
            self.cmp_name = v[1]
            #print("self.cmp_code = "+str(self.cmp_code))
            #print("self.cmp_name = "+str(self.cmp_name))
            self.df = cr.getFStatementsFromNaverFinance(self.cmp_code)
            self.df['종목코드'] = self.cmp_code
            self.df['종목'] = str(self.cmp_name)
            self.df = self.df[ ['종목코드', '종목', '매출액', '영업이익', '당기순이익', '자산총계', '부채총계', '자본총계','영업이익률', '순이익률', 'ROE(%)', 'ROA(%)', '부채비율', '자본유보율', 'EPS(원)', 'PER(배)',
                                 'BPS(원)', 'PBR(배)', '현금DPS(원)', '현금배당수익률', '현금배당성향(%)'
                                ] ]
            #, '발행주식수(보통주)'
            self.List200_Dict[self.cmp_code] = self.df
        #print(self.df.columns)

        self.setTopLayout()
        self.setTableLayout()
        self.setBotLayout()

        # 레이아웃 설정
        self.WholeLayout = QVBoxLayout()
        self.WholeLayout.addWidget(self.TopGroupBox)
        self.WholeLayout.addWidget(self.tabs)
        self.WholeLayout.addLayout(self.BotLayout)
        self.setLayout(self.WholeLayout)

        self.table0Widget.cellClicked.connect(self.process_cellClicked)

    def setTable0WidgetData(self, Dict):
        self.table0Widget.clear()
        column_headers = self.df.columns
        row_headers = []
        print('Column Headers = '+str(column_headers))
        print('Row Headers = '+ str(row_headers))
        for i in range(len(Dict)) :
            row_headers.append( str(i) )

        self.table0Widget.setVerticalHeaderLabels(row_headers)
        self.table0Widget.setHorizontalHeaderLabels(column_headers)

        rowCnt = len(Dict)
        print('len(Dict)'+str(rowCnt))
        colCnt = len(self.df.columns)

        for i, item in enumerate( Dict.items()) :
            #print('i , item = '+str(i)+' '+str(item))
            for j in range(colCnt) :
                #print( str(i)+' '+str(j)+' '+str(Dict[item[0]].loc['2018-12-01'][j]) )
                Item = QTableWidgetItem( str(Dict[item[0]].loc['2018-12-01'][j]) )
                Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.table0Widget.setItem(i, int(j), Item )
                #self.table0Widget.setItem(i, int(j), QTableWidgetItem( str(Dict[item[0]].loc['2018-12-01'][j]) ) )
                #self.table0Widget.setTextAlignment(Qt.AlignRight)

        self.table0Widget.resizeColumnsToContents()
        self.table0Widget.resizeRowsToContents()
        #self.table0Widget.cellClicked.connect(self.process_cellClicked)

    @pyqtSlot(int, int)
    def process_cellClicked(self, row, col):
        #print("self.table0Widget.rowCount = "+str(self.table0Widget.rowCount()) )
        #if( row < self.table0Widget.rowCount() ) :
        cmp_code = self.table0Widget.item(row,0).text()
        print("process_cellClicked = " +cmp_code)
        self.updatePlot(cmp_code)
        self.setTable1WidgetData(cmp_code)

    def setTable1WidgetData(self, cmp_code):
        Tab1_df = self.List200_Dict[cmp_code]
        column_headers = Tab1_df.columns
        row_headers = []
        for i in Tab1_df.index:
            row_headers.append( str(i).split(' ')[0] )

        self.table1Widget.setVerticalHeaderLabels(row_headers)
        self.table1Widget.setHorizontalHeaderLabels(column_headers)

        rowCnt = len(Tab1_df.index)
        colCnt = len(Tab1_df.columns)

        for i in range(rowCnt) :
            for j in range(colCnt) :
                #print(self.df.values[i][j])
                #print( self.df.values[i][j] )
                Item = QTableWidgetItem( str(Tab1_df.values[i][j]))
                Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.table1Widget.setItem(i, j,  Item)

        self.table1Widget.resizeColumnsToContents()
        self.table1Widget.resizeRowsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()




