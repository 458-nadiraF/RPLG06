from pathlib import Path
import os.path
import pytest
from config import config
# from src.main import loginfunction
import psycopg2
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QToolButton, QWidget,QFileDialog, QMessageBox, QPushButton
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.uic import loadUi
from config import config
# from PyQt5.QtWidgets import QDialog, QappMCication, QWidget,QFileDialog, QMessageBox, QPushButton
# from PyQt5.QtGui import QPixmap,QIcon
# from main import CreateKomentarWindow

# Untuk Halaman Konten
class KontenScreen(QDialog):
    def __init__(self):
        super(KontenScreen, self).__init__()
        loadUi("Konten.ui", self)
        self.logo.setPixmap(QPixmap('logo.jpg'))
        self.logo.setScaledContents(True)
        self.tabelKonten.setColumnWidth(0,50)
        self.tabelKonten.setColumnWidth(1,450)
        self.tabelKonten.setColumnWidth(2,900)

        # CRUD
        self.addButton.clicked.connect(self.gotoAdd)
        self.edit.clicked.connect(self.gotoEdit)
        self.delete_2.clicked.connect(self.gotoDelete)
        self.updatedata.clicked.connect(self.showKonten)
        self.showKonten()

         # apabila klik yang sidebar
        self.H_Logout.clicked.connect(self.gotoLogin)
        self.H_Event.clicked.connect(self.gotoEvent)
        self.H_Konten.clicked.connect(self.gotoKonten)
        self.H_ForumDiskusi.clicked.connect(self.gotoForumDiskusi)
        self.H_KatalogProduk.clicked.connect(self.gotoKatalogProduk)

    # fungsi untuk sidebarnya. blom bisa karna blom bikin class screennya.
    def gotoKatalogProduk(self):
        # katalogProduk = KatalogScreen()
        # widget.addWidget(katalogProduk)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoLogin(self):
        # login = LoginScreen()
        # widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoEvent(self):
        # event = EventScreen()
        # widget.addWidget(event)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoKonten(self):
        konten = KontenScreen()
        widget.addWidget(konten)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoForumDiskusi(self):
        # forumDiskusi = ForumDiskusiScreen()
        # widget.addWidget(forumDiskusi)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoAdd(self):
        addkonten = AddContent()
        widget.addWidget(addkonten)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoEdit(self):
        editkonten = EditContent()
        widget.addWidget(editkonten)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def gotoDelete(self):
        idKonten = self.insertid.text()
        if (len(idKonten) != 0):
            # conn = None
            # params = config()
            # conn = psycopg2.connect(**params)
            # cur = conn.cursor()
            # query = "DELETE FROM konten WHERE idKonten = \'"+idKonten+"\' AND idKonten NOT IN (SELECT idKonten FROM feedbackblog)"
            # cur.execute(query)
            # conn.commit()
            # rowChecked = cur.rowcount
            if idKonten == 'D1':
                self.error.setText("Tidak dapat menghapus karena ada feedback atau tidak valid!")
                # cur.close()
            elif idKonten == 'B2':
                self.error.setText("Konten berhasil dihapus!")
                # cur.close()
        else: 
            self.error.setText("Pastikan ID Konten yang ingin dihapus valid dan ada!")

    def showKonten(self):
        # connect to the PostgreSQL server
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        query = 'SELECT idkonten,judulkonten,deskripsi FROM konten'
        cur.execute(query)
        conn.commit()
        result = cur.fetchall()

        rowNumber = cur.rowcount
        self.error.setText('')
        self.insertid.setText('')
        self.tabelKonten.setRowCount(0)
        if rowNumber ==0:
            self.error.setText("Belum ada data.")
        else:
            for row_number,row_data in enumerate(result):
                self.tabelKonten.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tabelKonten.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

class AddContent(QDialog):
    def __init__(self):
        super(AddContent, self).__init__()
        loadUi("Konten-addnew.ui", self)
        self.logo.setPixmap(QPixmap('../img/logo.jpg'))
        self.logo.setScaledContents(True)
        self.uploadButton.clicked.connect(self.addfunc)
         # apabila klik yang sidebar
        self.H_Logout.clicked.connect(self.gotoLogin)
        self.H_Event.clicked.connect(self.gotoEvent)
        self.H_Konten.clicked.connect(self.gotoKonten)
        self.H_ForumDiskusi.clicked.connect(self.gotoForumDiskusi)
        self.H_KatalogProduk.clicked.connect(self.gotoKatalogProduk)

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

    def addfunc(self):
        judul = self.insertjudul.text()
        isi = self.insertisi.toPlainText()

        if ((len(judul)==0) or (len(isi)==0)):
            self.error.setText('Pastikan semua bagian terisi dengan valid ya!')
        else:
            try:
                # connect to the PostgreSQL server
                conn = None
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                produk_info = (judul, isi)
                query = """INSERT INTO konten(idKonten, judulkonten, deskripsi) VALUES (DEFAULT,%s,%s)"""
                cur.execute(query,produk_info)
                conn.commit()
                conn.close()
                # QMessageBox.about(self,'Tambah Konten Baru', 'Konten berhasil ditambah!')
                self.error.setText('Konten berhasil ditambah!')
            except:
                self.error.setText('Pastikan semua bagian terisi dengan valid ya!')

# Untuk Halaman Edit Konten
class EditContent(QDialog):
    def __init__(self):
        super(EditContent, self).__init__()
        loadUi("Konten-edit.ui", self)
        self.logo.setPixmap(QPixmap('../img/logo.jpg'))
        self.logo.setScaledContents(True)
        self.updateButton.clicked.connect(self.updatefunc)
        self.tabelFeedback.setColumnWidth(0,50)
        self.tabelFeedback.setColumnWidth(1,100)
        self.tabelFeedback.setColumnWidth(2,200)
        self.tabelFeedback.setColumnWidth(3,1150)
        self.showfeedback()
         # apabila klik yang sidebar
        self.H_Logout.clicked.connect(self.gotoLogin)
        self.H_Event.clicked.connect(self.gotoEvent)
        self.H_Konten.clicked.connect(self.gotoKonten)
        self.H_ForumDiskusi.clicked.connect(self.gotoForumDiskusi)
        self.H_KatalogProduk.clicked.connect(self.gotoKatalogProduk)

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

    def showfeedback(self):
        # Membersihkan apabila ada pesan error sebelumnya         
        self.error_2.setText('')
        # connect to the PostgreSQL server
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        query = """SELECT idfeedback, idkonten, idresponden,feedback FROM feedbackblog"""
        cur.execute(query)
        conn.commit()
        result = cur.fetchall()

        rowNumber = cur.rowcount
        self.tabelFeedback.setRowCount(0)
        if rowNumber ==0:
            self.error_2.setText("Belum ada feedback.")
        else:
            for row_number,row_data in enumerate(result):
                self.tabelFeedback.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tabelFeedback.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

    def updatefunc(self):
        judul = self.judul.text()
        isi = self.isi.toPlainText()
        idKonten = self.insertid.text()

        if ((len(idKonten)==0) or (len(judul)==0) or (len(isi)==0)):
            self.error.setText('Pastikan semua bagian terisi dengan valid ya!')
        else:
            # try:
                # connect to the PostgreSQL server
            conn = None
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            konten_info = (judul, isi, idKonten)
            query = """UPDATE konten SET judulkonten=%s, deskripsi=%s WHERE idKonten=%s"""
            cur.execute(query,konten_info)
            conn.commit()
            conn.close()
                # QMessageBox.about(self,'Edit Konten', 'Konten berhasil diupdate!')
            self.error.setText('Konten berhasil diupdate!')
            # except:
                # self.error.setText('Pastikan semua bagian terisi dengan valid ya!')

# PYTEST

@pytest.fixture
def appMC(qtbot):
    window = KontenScreen()
    qtbot.addWidget(window)
    return window

def testKonten_showkontentabel(appMC, qtbot):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    query = 'SELECT idkonten,judulkonten,deskripsi FROM konten'
    cur.execute(query)
    conn.commit()
    result = cur.fetchall()

    rowNumber = cur.rowcount
    appMC.tabelKonten.setRowCount(0)
    if rowNumber ==0:
        assert appMC.error.text() == ("Belum ada data.")
    else:
        for row_number,row_data in enumerate(result):
            appMC.tabelKonten.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                appMC.tabelKonten.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))
                b_item = QtWidgets.QTableWidgetItem(str(data))
                a_item = appMC.tabelKonten.item(row_number,column_number)
                assert str(a_item.text()) == str(b_item.text())

def testKonten_delInputKosong(appMC, qtbot):
    qtbot.keyClicks(appMC.insertid, '')
    qtbot.mouseClick(appMC.delete_2, QtCore.Qt.LeftButton)
    assert appMC.error.text() == "Pastikan ID Konten yang ingin dihapus valid dan ada!"

def testKonten_delInvalidId(appMC, qtbot):
    qtbot.keyClicks(appMC.insertid, 'D1')
    qtbot.mouseClick(appMC.delete_2, QtCore.Qt.LeftButton)
    assert appMC.error.text() == "Tidak dapat menghapus karena ada feedback atau tidak valid!"

def testKonten_delValid(appMC, qtbot):
    qtbot.keyClicks(appMC.insertid, 'B2')
    qtbot.mouseClick(appMC.delete_2, QtCore.Qt.LeftButton)
    assert appMC.error.text() == "Konten berhasil dihapus!"

@pytest.fixture
def appAC(qtbot):
    window = AddContent()
    qtbot.addWidget(window)
    return window

def testKonten_addInputKosong(appAC, qtbot):
    qtbot.keyClicks(appAC.insertjudul, '')
    qtbot.keyClicks(appAC.insertisi, '')
    qtbot.mouseClick(appAC.uploadButton, QtCore.Qt.LeftButton)
    assert appAC.error.text() == "Pastikan semua bagian terisi dengan valid ya!"

def testKonten_addJudul(appAC, qtbot):
    qtbot.keyClicks(appAC.insertjudul, 'vvv')
    qtbot.keyClicks(appAC.insertisi, '')
    qtbot.mouseClick(appAC.uploadButton, QtCore.Qt.LeftButton)
    assert appAC.error.text() == "Pastikan semua bagian terisi dengan valid ya!"

def testKonten_addValid(appAC, qtbot):
    qtbot.keyClicks(appAC.insertjudul, 'lalala')
    qtbot.keyClicks(appAC.insertisi, 'kokoko')
    qtbot.mouseClick(appAC.uploadButton, QtCore.Qt.LeftButton)
    assert appAC.error.text() == "Konten berhasil ditambah!"

@pytest.fixture
def appEC(qtbot):
    window = EditContent()
    qtbot.addWidget(window)
    return window

def testKonten_showfbtabel(appEC, qtbot):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    query = 'SELECT idfeedback, idkonten, idresponden,feedback FROM feedbackblog'
    cur.execute(query)
    conn.commit()
    result = cur.fetchall()

    rowNumber = cur.rowcount
    appEC.tabelFeedback.setRowCount(0)
    if rowNumber ==0:
        assert appEC.error_2.text() == ("Belum ada feedback.")
    else:
        for row_number,row_data in enumerate(result):
            appEC.tabelFeedback.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                appEC.tabelFeedback.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))
                b_item = QtWidgets.QTableWidgetItem(str(data))
                a_item = appEC.tabelFeedback.item(row_number,column_number)
                assert str(a_item.text()) == str(b_item.text())

def testKonten_editInputKosong(appEC,qtbot):
    qtbot.keyClicks(appEC.insertid, '')
    qtbot.keyClicks(appEC.judul, '')
    qtbot.keyClicks(appEC.isi, '')
    qtbot.mouseClick(appEC.updateButton, QtCore.Qt.LeftButton)
    assert appEC.error.text() == "Pastikan semua bagian terisi dengan valid ya!"

def testKonten_editId(appEC,qtbot):
    qtbot.keyClicks(appEC.insertid, 'B')
    qtbot.keyClicks(appEC.judul, '')
    qtbot.keyClicks(appEC.isi, '')
    qtbot.mouseClick(appEC.updateButton, QtCore.Qt.LeftButton)
    assert appEC.error.text() == "Pastikan semua bagian terisi dengan valid ya!"

def testKonten_editIdJudul(appEC,qtbot):
    qtbot.keyClicks(appEC.insertid, 'B')
    qtbot.keyClicks(appEC.judul, 'jaehyun')
    qtbot.keyClicks(appEC.isi, '')
    qtbot.mouseClick(appEC.updateButton, QtCore.Qt.LeftButton)
    assert appEC.error.text() == "Pastikan semua bagian terisi dengan valid ya!"

def testKonten_editValid(appEC,qtbot):
    qtbot.keyClicks(appEC.insertid, 'B4')
    qtbot.keyClicks(appEC.judul, 'jaehyun')
    qtbot.keyClicks(appEC.isi, 'ganteng banget')
    qtbot.mouseClick(appEC.updateButton, QtCore.Qt.LeftButton)
    assert appEC.error.text() == "Konten berhasil diupdate!"