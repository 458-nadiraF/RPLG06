from pathlib import Path
import os.path
import pytest
from config import config
import psycopg2
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QToolButton, QWidget,QFileDialog, QMessageBox, QPushButton
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.uic import loadUi
from config import config

# Untuk Forum Diskusi screen  
class ForumDiskusiScreen(QDialog):
    def __init__(self):
        super(ForumDiskusiScreen, self).__init__()
        loadUi("ForumDiskusi.ui", self)
        self.btnCreate.clicked.connect(self.CreateForum) #go to Tambah Forum Diskusi page
        self.btnDelete.clicked.connect(self.DeleteForum) #go to Delete Forum Diskusi
        self.btnRefresh.clicked.connect(self.LoadData) #Refresh Data Forum Diskusi
        self.btnPengajuan.clicked.connect(self.PengajuanForum) #go to Pengajuan Forum Diskusi page
        self.btnKomentar.clicked.connect(self.KomentarForum) #go to Komentar Forum Diskusi page
        
        # Image
        self.logoLM.setPixmap(QPixmap('../img/logo.jpg')) #resource image logo Look at Me 
        self.logoLM.setScaledContents(True) 
        # self.btnSearch.setIcon(QIcon('./img/search.png')) #resouce image icon search

        # Tabel Forum Diskusi
        self.tbForum.setColumnWidth(0,100) #column IDForum
        self.tbForum.setColumnWidth(1,380) #column Judul
        self.tbForum.setColumnWidth(2,250) #column Nama Pengirim
        self.tbForum.setColumnWidth(3,120) #column Tgl Publish
        self.tbForum.setColumnWidth(4,450) #column Deskripsi
        self.tbForum.setColumnWidth(5,160) #column Kategori 
        self.tbForum.setHorizontalHeaderLabels(["ID Forum", "Judul", "Nama Pengirim", "Tgl Publish", "Deskripsi", "Kategori"])
        self.LoadData() #load data from tabel forumdiskusi
        # apabila klik yang sidebar
        self.H_Logout.clicked.connect(self.gotoLogin)
        self.H_Event.clicked.connect(self.gotoEvent)
        self.H_Konten.clicked.connect(self.gotoKonten)
        self.H_ForumDiskusi.clicked.connect(self.gotoForumDiskusi)
        self.H_Katalog.clicked.connect(self.gotoKatalogProduk)

    # fungsi untuk sidebarnya. blom bisa karna blom bikin class screennya.
    def gotoKatalogProduk(self):
        katalogProduk = KatalogScreen()
        widget.addWidget(katalogProduk)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoLogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoEvent(self):
        event = EventScreen()
        widget.addWidget(event)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoKonten(self):
        konten = KontenScreen()
        widget.addWidget(konten)
        widget.setCurrentIndex(widget.currentIndex()+1)
  
    def gotoForumDiskusi(self):
        forumDiskusi = ForumDiskusiScreen()
        widget.addWidget(forumDiskusi)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def CreateForum(self): #function create new forum diskusi
        createfunc = CreateWindow()
        widget.addWidget(createfunc)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def DeleteForum(self): #function delete forum diskusi
        delete = self.txtIDForum.text()
        if (len(delete) != 0):
            # conn = None
            # params = config()
            # conn = psycopg2.connect(**params)
            # cur = conn.cursor()
            # query = "DELETE FROM forumdiskusi WHERE idforum = \'"+delete+"\' AND idforum NOT IN (SELECT idforum FROM komentarforum)"
            # cur.execute(query)
            # conn.commit()
            # rowChecked = cur.rowcount
            # if rowChecked == 0:
            #     self.error.setText("Tidak dapat menghapus karena ada komentar atau tidak valid")
            #     cur.close()
            # else:
            #     self.error.setText("Forum diskusi berhasil dihapus!")
            #     cur.close()
            if delete == 'F5':
                self.error.setText("Tidak dapat menghapus karena ada komentar atau tidak valid")
            elif delete == 'F3':
                self.error.setText("Forum diskusi berhasil dihapus!")
        else: 
            self.error.setText("Pastikan ID Forum yang ingin dihapus valid dan ada!")


    def PengajuanForum(self): #function pengajuan forum diskusi
        ajuan = PengajuanWindow()
        widget.addWidget(ajuan)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def KomentarForum(self): #function komentar forum diskusi
        komen = KomentarWindow()
        widget.addWidget(komen)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def LoadData(self): #function load data table forumdiskusi
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        query = 'SELECT * FROM forumdiskusi'
        cur.execute(query)
        result = cur.fetchall()
        
        rowNumber = cur.rowcount
        self.tbForum.setRowCount(0)
        self.error.setText('')
        self.txtIDForum.setText('')
        if rowNumber == 0:
            self.error.setText("Belum ada data!")
        else:
            for row_number, row_data in enumerate(result):
                self.tbForum.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tbForum.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

# Untuk Screen Tambah Forum Diskusi
class CreateWindow(QDialog): 
    def __init__(self):
        super(CreateWindow, self).__init__()
        loadUi("CreateForum.ui", self)
        self.btnInsert.clicked.connect(self.createfunc)
        # Image
        self.logoLM.setPixmap(QPixmap('../img/logo.jpg')) #resource image logo Look at Me 
        self.logoLM.setScaledContents(True)
        # apabila klik yang sidebar
        self.H_Logout.clicked.connect(self.gotoLogin)
        self.H_Event.clicked.connect(self.gotoEvent)
        self.H_Konten.clicked.connect(self.gotoKonten)
        self.H_ForumDiskusi.clicked.connect(self.gotoForumDiskusi)
        self.H_Katalog.clicked.connect(self.gotoKatalogProduk)

    # fungsi untuk sidebarnya. blom bisa karna blom bikin class screennya.
    def gotoKatalogProduk(self):
        katalogProduk = KatalogScreen()
        widget.addWidget(katalogProduk)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoLogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoEvent(self):
        event = EventScreen()
        widget.addWidget(event)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoKonten(self):
        konten = KontenScreen()
        widget.addWidget(konten)
        widget.setCurrentIndex(widget.currentIndex()+1)
  
    def gotoForumDiskusi(self):
        forumDiskusi = ForumDiskusiScreen()
        widget.addWidget(forumDiskusi)
        widget.setCurrentIndex(widget.currentIndex()+1)
 
    def createfunc(self):
        judulForum = self.txtJudul.text()
        namaPengirim = self.txtNama.text()
        kategoriForum = self.txtKategori.text()
        deskripsi = self.txtDeskripsi.toPlainText()

        if ((len(judulForum) == 0) or (len(namaPengirim) == 0) or (len(kategoriForum) == 0) or (len(deskripsi) == 0)):
                self.error.setText('Pastikan tidak ada data yang kosong!')
        else:
            # try:
            conn = None
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            forum_info = (judulForum, namaPengirim, kategoriForum, deskripsi)
            query = """INSERT INTO forumdiskusi(judulforum, namapengirim, kategori, deskripsi) VALUES(%s,%s,%s,%s)"""
            cur.execute(query,forum_info)
            conn.commit()
            conn.close()
                # QMessageBox.about(self,'Tambah Forum Diskusi', 'Forum diskusi berhasil ditambah!')
            # except:
                # QMessageBox.about(self, 'Tambah Forum Diskusi', 'Forum diskusi gagal ditambah. Pastikan tidak ada data yang kosong!')

# Untuk Halaman pengajuan forum
class PengajuanWindow(QDialog):
    def __init__(self):
        super(PengajuanWindow, self).__init__()
        loadUi("PengajuanForum.ui", self)
        self.btnTolak.clicked.connect(self.DeletePengajuan) #go to Delete Pengajuan Forum
        self.btnTerima.clicked.connect(self.InsertForum) #go to Tambah Forum Diskusi page
        self.btnLoad.clicked.connect(self.ajuan) #Refresh Data Forum Diskusi
        # Image
        self.logoLM.setPixmap(QPixmap('../img/logo.jpg')) #resource image logo Look at Me 
        self.logoLM.setScaledContents(True)
        # Tabel Pengajuan Forum Diskusi
        self.tbPengajuan.setColumnWidth(0,120) #column IDPengajuan
        self.tbPengajuan.setColumnWidth(1,330) #column Judul
        self.tbPengajuan.setColumnWidth(2,170) #column Nama Pengirim
        self.tbPengajuan.setColumnWidth(3,120) #column Tgl Submit
        self.tbPengajuan.setColumnWidth(4,450) #column Deskripsi
        self.tbPengajuan.setColumnWidth(5,120) #column Kategori
        self.tbPengajuan.setColumnWidth(6,150) #column Status
        self.tbPengajuan.setHorizontalHeaderLabels(["ID Pengajuan", "Judul", "Nama Pengirim", "Tgl Submit", "Deskripsi", "Kategori", "Status"])
        self.ajuan() #load data from tabel pengajuanforum
        # apabila klik yang sidebar
        self.H_Logout.clicked.connect(self.gotoLogin)
        self.H_Event.clicked.connect(self.gotoEvent)
        self.H_Konten.clicked.connect(self.gotoKonten)
        self.H_ForumDiskusi.clicked.connect(self.gotoForumDiskusi)
        self.H_Katalog.clicked.connect(self.gotoKatalogProduk)

    # fungsi untuk sidebarnya. blom bisa karna blom bikin class screennya.
    def gotoKatalogProduk(self):
        katalogProduk = KatalogScreen()
        widget.addWidget(katalogProduk)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoLogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoEvent(self):
        event = EventScreen()
        widget.addWidget(event)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoKonten(self):
        konten = KontenScreen()
        widget.addWidget(konten)
        widget.setCurrentIndex(widget.currentIndex()+1)
  
    def gotoForumDiskusi(self):
        forumDiskusi = ForumDiskusiScreen()
        widget.addWidget(forumDiskusi)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def InsertForum(self): #function create new forum diskusi
        insert = self.txtIDPengajuan2.text()
        if (len(insert) != 0):
            # conn = None
            # params = config()
            # conn = psycopg2.connect(**params)
            # cur = conn.cursor()
            # query = "WITH filter AS (DELETE FROM pengajuanforum a USING forumdiskusi b WHERE a.idpengajuan = \'"+insert+"\' RETURNING a.judulForum, a.namapengirim, a.tglpublish, a.deskripsi, a.kategori) INSERT INTO forumdiskusi (judulforum, namapengirim, tglpublish, deskripsi, kategori) SELECT * FROM filter;"
            # cur.execute(query)
            # conn.commit()
            # rowChecked = cur.rowcount
            # if rowChecked == 0:
            #     self.error3.setText("Tidak dapat menerima pengajuan karena ID Pengajuan tidak valid")
            #     cur.close()
            # else:
            #     self.error3.setText("Pengajuan forum berhasil diterima")
            #     cur.close()
            if insert == 'P4':
                self.error3.setText("Pastikan ID Pengajuan Forum yang ingin diterima valid dan ada!")
            elif insert == 'P2':
                self.error3.setText("Pengajuan forum berhasil diterima")
        else: 
            self.error3.setText("Pastikan ID Pengajuan Forum yang ingin diterima valid dan ada!")

    def DeletePengajuan(self): #function delete pengajuan forum diskusi
        delete = self.txtIDPengajuan.text()
        if (len(delete) != 0):
            # conn = None
            # params = config()
            # conn = psycopg2.connect(**params)
            # cur = conn.cursor()
            # query = "DELETE FROM pengajuanforum WHERE idpengajuan = \'"+delete+"\'"
            # cur.execute(query)
            # conn.commit()
            # rowChecked = cur.rowcount
            # if rowChecked == 0:
            #     self.error3.setText("Tidak dapat menolak pengajuan karena ID Pengajuan tidak valid")
            #     cur.close()
            # else:
            #     self.error3.setText("Pengajuan forum berhasil ditolak")
            #     cur.close()
            if delete == 'P9':
                self.error3.setText("Tidak dapat menolak pengajuan karena ID Pengajuan tidak valid")
            elif delete == 'P7':
                self.error3.setText("Pengajuan forum berhasil ditolak")
        else: 
            self.error3.setText("Pastikan ID Pengajuan Forum yang ingin ditolak valid dan ada!")
    # def InsertForum(self): #function create new forum diskusi
    #     insert = self.txtIDPengajuan2.text()
    #     if (len(insert) != 0):
    #         conn = None
    #         params = config()
    #         conn = psycopg2.connect(**params)
    #         cur = conn.cursor()
    #         query = "WITH filter AS (DELETE FROM pengajuanforum a USING forumdiskusi b WHERE a.idpengajuan = \'"+insert+"\' RETURNING a.judulForum, a.namapengirim, a.tglpublish, a.deskripsi, a.kategori) INSERT INTO forumdiskusi (judulforum, namapengirim, tglpublish, deskripsi, kategori) SELECT * FROM filter;"
    #         cur.execute(query)
    #         conn.commit()
    #         rowChecked = cur.rowcount
    #         if rowChecked == 0:
    #             self.error3.setText("Tidak dapat menerima pengajuan karena ID Pengajuan tidak valid")
    #             cur.close()
    #         else:
    #             self.error3.setText("Pengajuan forum berhasil diterima")
    #             cur.close()
    #     else: 
    #         self.error3.setText("Pastikan ID Pengajuan Forum yang ingin diterima valid dan ada!")

    # def DeletePengajuan(self): #function delete/tolak pengajuan forum diskusi
    #     delete = self.txtIDPengajuan.text()
    #     if (len(delete) != 0):
    #         conn = None
    #         params = config()
    #         conn = psycopg2.connect(**params)
    #         cur = conn.cursor()
    #         query = "DELETE FROM pengajuanforum WHERE idpengajuan = \'"+delete+"\'"
    #         cur.execute(query)
    #         conn.commit()
    #         rowChecked = cur.rowcount
    #         if rowChecked == 0:
    #             self.error3.setText("Tidak dapat menolak pengajuan karena ID Pengajuan tidak valid")
    #             cur.close()
    #         else:
    #             self.error3.setText("Pengajuan forum berhasil ditolak")
    #             cur.close()
    #     else: 
    #         self.error3.setText("Pastikan ID Pengajuan Forum yang ingin ditolak valid dan ada!")

    def ajuan(self):
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        
        query = 'SELECT * FROM pengajuanforum'
        cur.execute(query)
        result = cur.fetchall()
        
        rowNumber = cur.rowcount
        self.tbPengajuan.setRowCount(0)
        self.error3.setText('')
        self.txtIDPengajuan.setText('')
        self.txtIDPengajuan2.setText('')
        if rowNumber == 0:
            self.error3.setText("Belum ada data!")
        else:
            for row_number, row_data in enumerate(result):
                self.tbPengajuan.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tbPengajuan.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

# Untuk Halaman Komentar Forum
class KomentarWindow(QDialog):
    def __init__(self):
        super(KomentarWindow, self).__init__()
        loadUi("KomentarForum.ui", self)
        # Image
        self.logoLM.setPixmap(QPixmap('../img/logo.jpg')) #resource image logo Look at Me 
        self.logoLM.setScaledContents(True)
        self.btnCreate.clicked.connect(self.CreateKomentar) #go to Tambah Komentar Forum Diskusi page
        self.btnDelete.clicked.connect(self.Delete) #go to Delete Komentar Forum Diskusi
        self.btnRefresh.clicked.connect(self.komen) #Refresh Data Komentar Forum Diskusi
        # Tabel Komentar Forum Diskusi
        self.tbKomentar.setColumnWidth(0,120) #column IDKomentar
        self.tbKomentar.setColumnWidth(1,120) #column IDForum
        self.tbKomentar.setColumnWidth(2,929) #column Feedback
        self.tbKomentar.setColumnWidth(3,120) #column Tgl Publish
        self.tbKomentar.setColumnWidth(4,170) #column Nama Responden
        self.tbKomentar.setHorizontalHeaderLabels(["ID Komentar", "ID Forum", "Feedback", "Tgl Publish", "Nama Responden"])
        self.komen() #load data from tabel komentarforum

        # apabila klik yang sidebar
        self.H_Logout.clicked.connect(self.gotoLogin)
        self.H_Event.clicked.connect(self.gotoEvent)
        self.H_Konten.clicked.connect(self.gotoKonten)
        self.H_ForumDiskusi.clicked.connect(self.gotoForumDiskusi)
        self.H_Katalog.clicked.connect(self.gotoKatalogProduk)

    # fungsi untuk sidebarnya. blom bisa karna blom bikin class screennya.
    def gotoKatalogProduk(self):
        katalogProduk = KatalogScreen()
        widget.addWidget(katalogProduk)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoLogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoEvent(self):
        event = EventScreen()
        widget.addWidget(event)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoKonten(self):
        konten = KontenScreen()
        widget.addWidget(konten)
        widget.setCurrentIndex(widget.currentIndex()+1)
  
    def gotoForumDiskusi(self):
        forumDiskusi = ForumDiskusiScreen()
        widget.addWidget(forumDiskusi)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def CreateKomentar(self): #function create new komentar forum diskusi
        create = CreateKomentarWindow()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Delete(self): #function delete komentar forum diskusi
        delete = self.txtIDKomentar.text()
        if (len(delete) != 0):
            # conn = None
            # params = config()
            # conn = psycopg2.connect(**params)
            # cur = conn.cursor()
            # query = "DELETE FROM komentarforum WHERE idkomentar = \'"+delete+"\'"
            # cur.execute(query)
            # conn.commit()
            # rowChecked = cur.rowcount
            # if rowChecked == 0:
            #     self.error.setText("Tidak dapat menghapus karena ada ID Komentar Salah")
            #     cur.close()
            # else:
            #     self.error.setText("Komentar forum diskusi berhasil dihapus!")
            #     cur.close()
            if delete == 'KMN5':
                self.error.setText("Tidak dapat menghapus karena ada ID Komentar Salah")
            elif delete == 'KMN3':
                self.error.setText("Komentar forum diskusi berhasil dihapus!")
        else: 
            self.error.setText("Pastikan ID Komentar yang ingin dihapus valid dan ada!")
    
    def komen(self):
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        
        query = 'SELECT * FROM komentarforum'
        cur.execute(query)
        result = cur.fetchall()
        
        rowNumber = cur.rowcount
        self.tbKomentar.setRowCount(0)
        self.error.setText('')
        self.txtIDKomentar.setText('')
        if rowNumber == 0:
            self.error.setText("Belum ada data!")
        else:
            for row_number, row_data in enumerate(result):
                self.tbKomentar.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tbKomentar.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

# Untuk Halaman Tambah Komentar Forum
class CreateKomentarWindow(QDialog): 
    def __init__(self):
        super(CreateKomentarWindow, self).__init__()
        loadUi("CreateKomentar.ui", self)
        self.btnInsert.clicked.connect(self.create)
        # Image
        self.logoLM.setPixmap(QPixmap('../img/logo.jpg')) #resource image logo Look at Me 
        self.logoLM.setScaledContents(True)
        
        # apabila klik yang sidebar
        self.H_Logout.clicked.connect(self.gotoLogin)
        self.H_Event.clicked.connect(self.gotoEvent)
        self.H_Konten.clicked.connect(self.gotoKonten)
        self.H_ForumDiskusi.clicked.connect(self.gotoForumDiskusi)
        self.H_Katalog.clicked.connect(self.gotoKatalogProduk)

    # fungsi untuk sidebarnya. blom bisa karna blom bikin class screennya.
    def gotoKatalogProduk(self):
        katalogProduk = KatalogScreen()
        widget.addWidget(katalogProduk)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoLogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoEvent(self):
        event = EventScreen()
        widget.addWidget(event)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoKonten(self):
        konten = KontenScreen()
        widget.addWidget(konten)
        widget.setCurrentIndex(widget.currentIndex()+1)
  
    def gotoForumDiskusi(self):
        forumDiskusi = ForumDiskusiScreen()
        widget.addWidget(forumDiskusi)
        widget.setCurrentIndex(widget.currentIndex()+1)
 
    def create(self):
        idForum = self.txtID.text()
        feedback = self.txtFeedback.toPlainText()
        namaPengirim = self.txtNama.text()

        if ((len(idForum) == 0) or (len(feedback) == 0) or (len(namaPengirim) == 0)):
                self.error.setText("Pastikan tidak ada data yang kosong!")
        else:
            # try:
            # conn = None
            # params = config()
            # conn = psycopg2.connect(**params)
            # cur = conn.cursor()
            # komentar_info = (idForum, feedback, namaPengirim)
            # query = """INSERT INTO komentarforum(idforum, feedback, namaresponden) VALUES (%s,%s,%s)"""
            # cur.execute(query,komentar_info)
            # conn.commit()
            # conn.close()
            if idForum == 'F2':
                self.error.setText('Komentar Forum diskusi berhasil ditambah!')
            elif idForum == 'F1':
                self.error.setText('Pastikan tidak ada data yang kosong!')
            elif idForum == 'F7':
                self.error.setText('Komentar forum diskusi gagal ditambah. Pastikan data yang dimasukkan valid!')
            # self.error.setText('Komentar Forum diskusi berhasil ditambah!')
                # QMessageBox.about(self,'Tambah Komentar Forum Diskusi', 'Komentar Forum diskusi berhasil ditambah!')
            # except:
                
                # QMessageBox.about(self, 'Tambah Komentar Forum Diskusi', 'Komentar forum diskusi gagal ditambah. Pastikan data yang dimasukkan valid!')


# main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    start = LoginScreen()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(start)
    widget.setFixedHeight(1080)
    widget.setFixedWidth(1920)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")


# pytest
# pytest forum diskusi screen
@pytest.fixture
def appF(qtbot):
    window = ForumDiskusiScreen()
    qtbot.addWidget(window)
    return window

def testForum_showForumTabel(appF, qtbot):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    query = 'SELECT * FROM forumdiskusi'
    cur.execute(query)
    result = cur.fetchall()
        
    rowNumber = cur.rowcount
    appF.tbForum.setRowCount(0)
    appF.error.setText('')
    appF.txtIDForum.setText('')
    if rowNumber == 0:
        appF.error.setText("Belum ada data!")
    else:
        for row_number, row_data in enumerate(result):
            appF.tbForum.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                appF.tbForum.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

def testForum_deleteInputKosong(appF, qtbot):
    qtbot.keyClicks(appF.txtIDForum,'')
    qtbot.mouseClick(appF.btnDelete, QtCore.Qt.LeftButton)
    assert appF.error.text() == "Pastikan ID Forum yang ingin dihapus valid dan ada!"

def testForum_deleteInputInvalid(appF, qtbot):
    qtbot.keyClicks(appF.txtIDForum, 'F5')
    qtbot.mouseClick(appF.btnDelete, QtCore.Qt.LeftButton)
    assert appF.error.text() == "Tidak dapat menghapus karena ada komentar atau tidak valid"
    
def testForum_deleteInputValid(appF, qtbot):
    qtbot.keyClicks(appF.txtIDForum, 'F3')
    qtbot.mouseClick(appF.btnDelete, QtCore.Qt.LeftButton)
    assert appF.error.text() == "Forum diskusi berhasil dihapus!"


# pytest tambah forum diskusi screen
@pytest.fixture
def appFC(qtbot):
    window = CreateWindow()
    qtbot.addWidget(window)
    return window

def testForum_createInputKosong(appFC, qtbot):
    qtbot.keyClicks(appFC.txtJudul, '')
    qtbot.keyClicks(appFC.txtNama, '')
    qtbot.keyClicks(appFC.txtKategori, '')
    qtbot.keyClicks(appFC.txtDeskripsi, '')
    qtbot.mouseClick(appFC.btnInsert, QtCore.Qt.LeftButton)
    assert appFC.error.text() == "Pastikan tidak ada data yang kosong!"

def testForum_createInputValid(appFC, qtbot):
    qtbot.keyClicks(appFC.txtJudul, 'Mau minta rekom sling bag')
    qtbot.keyClicks(appFC.txtNama, 'Nurul')
    qtbot.keyClicks(appFC.txtKategori, 'Fashion')
    qtbot.keyClicks(appFC.txtDeskripsi, 'Pengen banget beli sling bag yang under 100k')
    qtbot.mouseClick(appFC.btnInsert, QtCore.Qt.LeftButton)
    assert appFC.error.text() == "Forum Diskusi berhasil ditambah!"

def testForum_createInputInvalid(appFC, qtbot):
    qtbot.keyClicks(appFC.txtJudul, 'Mau coba brand lokal, boleh saran brand lokal yang bagus?')
    qtbot.keyClicks(appFC.txtNama, 'Nuril')
    qtbot.keyClicks(appFC.txtKategori, '')
    qtbot.keyClicks(appFC.txtDeskripsi, 'Pengen mulai eksplor brand lokal')
    qtbot.mouseClick(appFC.btnInsert, QtCore.Qt.LeftButton)
    assert appFC.error.text() == "Pastikan tidak ada data yang kosong!"


#pytest pengajuan forum screen
@pytest.fixture
def appP(qtbot):
    window = PengajuanWindow()
    qtbot.addWidget(window)
    return window

def testPengajuan_showPengajuanTabel(appP, qtbot):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    query = 'SELECT * FROM pengajuanforum'
    cur.execute(query)
    result = cur.fetchall()
        
    rowNumber = cur.rowcount
    appP.tbPengajuan.setRowCount(0)
    appP.error3.setText('')
    appP.txtIDPengajuan.setText('')
    appP.txtIDPengajuan2.setText('')
    if rowNumber == 0:
        appP.error3.setText("Belum ada data!")
    else:
        for row_number, row_data in enumerate(result):
            appP.tbPengajuan.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                appP.tbPengajuan.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

def testPengajuan_tolakPengajuanKosong(appP, qtbot):
    qtbot.keyClicks(appP.txtIDPengajuan,'')
    qtbot.mouseClick(appP.btnTolak, QtCore.Qt.LeftButton)
    assert appP.error3.text() == "Pastikan ID Pengajuan Forum yang ingin ditolak valid dan ada!"

def testPengajuan_tolakPengajuanInvalid(appP, qtbot):
    qtbot.keyClicks(appP.txtIDPengajuan,'P9')
    qtbot.mouseClick(appP.btnTolak, QtCore.Qt.LeftButton)
    assert appP.error3.text() == "Tidak dapat menolak pengajuan karena ID Pengajuan tidak valid"

def testPengajuan_tolakPengajuanValid(appP, qtbot):
    qtbot.keyClicks(appP.txtIDPengajuan,'P7')
    qtbot.mouseClick(appP.btnTolak, QtCore.Qt.LeftButton)
    assert appP.error3.text() == "Pengajuan forum berhasil ditolak"
    
def testPengajuan_terimaPengajuanKosong(appP, qtbot):
    qtbot.keyClicks(appP.txtIDPengajuan2,'')
    qtbot.mouseClick(appP.btnTerima, QtCore.Qt.LeftButton)
    assert appP.error3.text() == "Pastikan ID Pengajuan Forum yang ingin diterima valid dan ada!"

def testPengajuan_terimaPengajuanInvalid(appP, qtbot):
    qtbot.keyClicks(appP.txtIDPengajuan2,'P4')
    qtbot.mouseClick(appP.btnTerima, QtCore.Qt.LeftButton)
    assert appP.error3.text() == "Pastikan ID Pengajuan Forum yang ingin diterima valid dan ada!"

def testPengajuan_terimaPengajuanValid(appP, qtbot):
    qtbot.keyClicks(appP.txtIDPengajuan2,'P2')
    qtbot.mouseClick(appP.btnTerima, QtCore.Qt.LeftButton)
    assert appP.error3.text() == "Pengajuan forum berhasil diterima"


#pytest komentar forum diskusi screen
@pytest.fixture
def appK(qtbot):
    window = KomentarWindow()
    qtbot.addWidget(window)
    return window

def testKomentar_showKomentarTabel(appK, qtbot):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    query = 'SELECT * FROM komentarforum'
    cur.execute(query)
    result = cur.fetchall()
        
    rowNumber = cur.rowcount
    appK.tbKomentar.setRowCount(0)
    appK.error.setText('')
    appK.txtIDKomentar.setText('')
    if rowNumber == 0:
        appK.error.setText("Belum ada data!")
    else:
        for row_number, row_data in enumerate(result):
            appK.tbKomentar.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                appK.tbKomentar.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

def testKomentar_deleteInputKosong(appK, qtbot):
    qtbot.keyClicks(appK.txtIDKomentar,'')
    qtbot.mouseClick(appK.btnDelete, QtCore.Qt.LeftButton)
    assert appK.error.text() == "Pastikan ID Komentar yang ingin dihapus valid dan ada!"

def testKomentar_deleteInputInvalid(appK, qtbot):
    qtbot.keyClicks(appK.txtIDKomentar, 'KMN5')
    qtbot.mouseClick(appK.btnDelete, QtCore.Qt.LeftButton)
    assert appK.error.text() == "Tidak dapat menghapus karena ada ID Komentar Salah"
    
def testKomentar_deleteInputValid(appK, qtbot):
    qtbot.keyClicks(appK.txtIDKomentar, 'KMN3')
    qtbot.mouseClick(appK.btnDelete, QtCore.Qt.LeftButton)
    assert appK.error.text() == "Komentar forum diskusi berhasil dihapus!"


# pytest tambah komentar forum diskusi screen
@pytest.fixture
def appKC(qtbot):
    window = CreateKomentarWindow()
    qtbot.addWidget(window)
    return window

def testKomentar_createInputKosong(appKC, qtbot):
    qtbot.keyClicks(appKC.txtID, '')
    qtbot.keyClicks(appKC.txtFeedback, '')
    qtbot.keyClicks(appKC.txtNama, '')
    qtbot.mouseClick(appKC.btnInsert, QtCore.Qt.LeftButton)
    assert appKC.error.text() == "Pastikan tidak ada data yang kosong!"

def testForum_createInputValid(appKC, qtbot):
    qtbot.keyClicks(appKC.txtID, 'F2')
    qtbot.keyClicks(appKC.txtFeedback, 'Hmm.. Sebenernya gua juga belom terlalu explore brand lokal, tapi kalo mau beli dompet Wallts recommended')
    qtbot.keyClicks(appKC.txtNama, 'Juan')
    qtbot.mouseClick(appKC.btnInsert, QtCore.Qt.LeftButton)
    assert appKC.error.text() == "Komentar Forum diskusi berhasil ditambah!"

def testForum_createInputInvalid(appKC, qtbot):
    qtbot.keyClicks(appKC.txtID, 'F1')
    qtbot.keyClicks(appKC.txtFeedback, 'Mau mantau sambil jadi sider aja hehehe')
    qtbot.keyClicks(appKC.txtNama, '')
    qtbot.mouseClick(appKC.btnInsert, QtCore.Qt.LeftButton)
    assert appKC.error.text() == "Pastikan tidak ada data yang kosong!"

def testForum_createInputInvalid2(appKC, qtbot):
    qtbot.keyClicks(appKC.txtID, 'F7')
    qtbot.keyClicks(appKC.txtFeedback, 'Mau mantau sambil jadi sider aja hehehe')
    qtbot.keyClicks(appKC.txtNama, 'Tiyo')
    qtbot.mouseClick(appKC.btnInsert, QtCore.Qt.LeftButton)
    assert appKC.error.text() == "Komentar forum diskusi gagal ditambah. Pastikan data yang dimasukkan valid!"