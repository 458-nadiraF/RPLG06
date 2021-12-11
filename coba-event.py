from pathlib import Path
import os.path
import pytest
from config import config
# from src.main import loginfunction
import psycopg2
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QToolButton, QWidget,QFileDialog, QMessageBox, QPushButton
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.uic import loadUi
from config import config
# from PyQt5.QtWidgets import QDialog, QApplication, QWidget,QFileDialog, QMessageBox, QPushButton
# from PyQt5.QtGui import QPixmap,QIcon
# from main import CreateKomentarWindow

# Untuk Halaman Login
class LoginScreen(QDialog):
    
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui",self)
        #logoLM.setPixmap(pixmap.scaled(myWidth, myHeight, Qt::KeepAspectRatio, Qt::SmoothTransformation));
        self.logoLM.setPixmap(QPixmap('../img/logo.jpg'))
        self.logoLM.setScaledContents(True)
        self.passwordField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginButton.clicked.connect(self.loginfunction)

    def loginfunction(self):
        user = self.usernameField.text()
        password = self.passwordField.text()

        if len(user)==0 or len(password)==0:
            self.error.setText("Pastikan tidak ada kolom kosong!")

        else:
            conn = None
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            query = 'SELECT password FROM admin WHERE username =\''+user+"\'"
            cur.execute(query)
            rowChecked = cur.rowcount
            # apabila username/ password ga ada
            if rowChecked == 1:
                result_pass = cur.fetchone()[0]
                if result_pass == password:
                    self.error.setText("Successfully logged in.")
                    # self.gotoKatalogProduk()
                    # self.error.setText(result_pass)

                else:
                    self.error.setText("Invalid username or password")
            else:
                self.error.setText("Tidak ditemukan username!")
    # def gotoKatalogProduk(self):
    #     katalogProduk = KatalogScreen()
    #     # widget.addWidget(katalogProduk)
    #     # widget.setCurrentIndex(widget.currentIndex()+1)

class KatalogScreen(QDialog):
    def __init__(self):
        super(KatalogScreen, self).__init__()
        loadUi("katalog.ui",self)
        
        #set gambar
        self.logoLM.setPixmap(QPixmap('../img/logo.jpg'))
        self.logoLM.setScaledContents(True)
        # self.searchButton.setIcon(QIcon('./images/search.png'))

        #redirect clicked button
        self.tambahproduk.clicked.connect(self.gotoadd)
        self.editButton.clicked.connect(self.gotoEditProduk)
        self.hapusButton.clicked.connect(self.gotoHapusProduk)
        self.reloadButton.clicked.connect(self.showProdukfunction)
        self.showProdukfunction()

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

    #fungsi untuk tambah produk
    def gotoadd(self):
        addProduk = AddProdukScreen()
        widget.addWidget(addProduk)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    #fungsi untuk tambah produk
    def gotoEditProduk(self):
        editProduk = EditProdukScreen()
        widget.addWidget(editProduk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    #fungsi untuk hapus produk
    def gotoHapusProduk(self):
        idProdukCRUD = self.inputidProduk.text()
        if (len(idProdukCRUD) != 0):
            try:
                conn = None
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                query = "DELETE FROM produk WHERE idProduk =\'"+idProdukCRUD+"\'"
                cur.execute(query)
                conn.commit()
                rowChecked = cur.rowcount
                if rowChecked == 0:
                    self.error.setText("idProduk tidak valid")    
                else:
                    self.error.setText("Berhasil menghapus produk")
                cur.close()
            except:
                self.error.setText("Pastikan idProduk valid!")
        else: 
            self.error.setText("Anda belum menginput id Produk yang ingin dihapus!")
    
    def showProdukfunction(self):

        # Membersihkan apabila ada pesan error sebelumnya         
        self.error.setText('')

        # connect to the PostgreSQL server
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        query = 'SELECT * FROM produk'
        cur.execute(query)
        conn.commit()
        result = cur.fetchall()

        rowNumber = cur.rowcount
        self.tabelProduk.setRowCount(0)
        if rowNumber ==0:
            self.error.setText("Belum ada data.")
        else:
        # apabila username/ password ga ada
            for row_number,row_data in enumerate(result):
                self.tabelProduk.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tabelProduk.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

# Untuk Halaman Edit Produk
class EditProdukScreen(QDialog):

    def __init__(self):
        super(EditProdukScreen, self).__init__()
        loadUi("editKatalog.ui",self)
        # set gambar
        self.logoLM.setPixmap(QPixmap('../img/logo.jpg'))
        self.logoLM.setScaledContents(True)
        # self.searchButton.setIcon(QIcon('./images/search.png'))

        # redirect clicked button
        self.editButton.clicked.connect(self.editProdukfunction)
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

    def editProdukfunction(self):
        try:
            namaProduk = self.inputNama.text()
            batch = int(self.inputBatch.text())
            kategori = self.inputKategori.text()
            harga = float(self.inputHarga.text())
            quantity = int(self.inputKuantitas.text())
            berat = float(self.inputBerat.text())
            deskripsi = self.inputDeskripsi.toPlainText()
            link = self.inputLink.text()
            idProdukCRUD = self.inputidProduk.text()
            if ((kategori != 'Atasan') and (kategori != 'Bawahan') and (kategori !='Outer') and (kategori !='Masker' ) and (kategori != 'Aksesoris')):
                self.error.setText("Kategori tidak ada. Pilih salah satu diantara 'Atasan', 'Bawahan', 'Outer', 'Masker', dan 'Aksesoris'")
            else: 
                # try: 
                    # connect to the PostgreSQL server
                conn = None
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                    # query = 'SELECT password FROM admin WHERE username =\''+user+"\'"
                    # produk_info = [namaProduk, batch, kategori,harga,quantity,berat,deskripsi,link]
                produk_info = (namaProduk, batch, kategori,harga,quantity,berat,deskripsi,link, idProdukCRUD)
                query = """UPDATE produk SET namaProduk=%s, batch=%s, kategori=%s, harga=%s, quantity=%s, berat=%s, deskripsi=%s, link=%s WHERE idProduk =%s"""
                cur.execute(query,produk_info)
                conn.commit()
                rowChecked = cur.rowcount
                if rowChecked == 0:
                    self.error.setText("Tidak dapat menghapus karena input tidak valid")
                else:
                    self.error.setText('')
                        # QMessageBox.about(self,'Edit Produk', 'Produk berhasil diedit!')
                    
                conn.close()
                # except:
                    # QMessageBox.about(self, 'Edit Produk', 'Produk gagal diupload. Pastikan semua data terisi!')
        except:
            self.error.setText('Pastikan semua data terisi dan valid!')

# Untuk Halaman Tambah Produk
class AddProdukScreen(QDialog):
    def __init__(self):
        super(AddProdukScreen, self).__init__()
        loadUi("tambahProdukKatalog.ui",self)

        # set gambar
        self.logoLM.setPixmap(QPixmap('../img/logo.jpg'))
        self.logoLM.setScaledContents(True)
        # self.searchButton.setIcon(QIcon('./images/search.png'))

        # redirect clicked button
        self.unggahproduk.clicked.connect(self.addProdukFunction)
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

    def reload(self):
        reload = AddProdukScreen()
        widget.addWidget(reload)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def addProdukFunction(self):
        try:
            namaProduk = self.inputNama.text()
            batch = int(self.inputBatch.text())
            kategori = self.inputKategori.text()
            harga = float(self.inputHarga.text())
            quantity = int(self.inputKuantitas.text())
            berat = float(self.inputBerat.text())
            deskripsi = self.inputDeskripsi.toPlainText()
            link = self.inputLink.text()
            
            if ((kategori != 'Atasan') and (kategori != 'Bawahan') and (kategori !='Outer') and (kategori !='Masker' ) and (kategori != 'Aksesoris')):
                self.error.setText("Kategori tidak ada. Pilih salah satu diantara 'Atasan', 'Bawahan', 'Outer', 'Masker', dan 'Aksesoris'")
            else:
                # try: 
                    # connect to the PostgreSQL server
                conn = None
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                produk_info = (namaProduk, batch, kategori,harga,quantity,berat,deskripsi,link)
                query = """INSERT INTO produk(idProduk,namaProduk, batch, kategori, harga, quantity, berat, deskripsi, link) VALUES(DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s)"""
                cur.execute(query,produk_info)
                conn.commit()
                conn.close()
                    # QMessageBox.about(self,'Tambah Produk', 'Produk berhasil ditambah!')
                self.reload()
                self.error.setText('')   
                # except:
                    # QMessageBox.about(self, 'Tambah Produk', 'Produk gagal diupload. Pastikan semua data valid!')
        except:
            self.error.setText('Pastikan semua data terisi dan valid!')   

# Untuk Halaman Konten
class KontenScreen(QDialog):
    def __init__(self):
        super(KontenScreen, self).__init__()
        loadUi("Konten.ui", self)
        self.logo.setPixmap(QPixmap('../img/logo.jpg'))
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
            conn = None
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            query = "DELETE FROM konten WHERE idKonten = \'"+idKonten+"\' AND idKonten NOT IN (SELECT idKonten FROM feedbackblog)"
            cur.execute(query)
            conn.commit()
            rowChecked = cur.rowcount
            if rowChecked == 0:
                self.error.setText("Tidak dapat menghapus karena ada feedback atau tidak valid!")
                cur.close()
            else:
                self.error.setText("Konten berhasil dihapus!")
                cur.close()
        else: 
            self.error.setText("Pastikan ID Konten yang ingin dihapus valid dan ada!")

    def showKonten(self):
        # connect to the PostgreSQL server
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        query = 'SELECT * FROM konten'
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

# Untuk Halaman tambah konten
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
                self.error.setText('')
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
            self.error.setText('')
            # except:
                # self.error.setText('Pastikan semua bagian terisi dengan valid ya!')

# Untuk Event screen       
class EventScreen(QDialog):
    def __init__(self):
        super(EventScreen, self).__init__()
        loadUi("event.ui",self)
        
        #set gambar
        self.logoLM.setPixmap(QPixmap('../img/logo.jpg'))
        self.logoLM.setScaledContents(True)
        # self.searchButton.setIcon(QIcon('./images/search.png'))

        #redirect clicked button
        self.tambahEvent.clicked.connect(self.gotoadd)
        self.editButton.clicked.connect(self.gotoEditEvent)
        self.hapusButton.clicked.connect(self.gotoHapusEvent)
        self.reloadButton.clicked.connect(self.showEventfunction)
        self.showEventfunction()

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

    #fungsi untuk tambah event
    def gotoadd(self):
        addEvent = AddEventScreen()
        widget.addWidget(addEvent)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    #fungsi untuk edit event
    def gotoEditEvent(self):
        editEvent = EditEventScreen()
        widget.addWidget(editEvent)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    #fungsi untuk hapus event
    def gotoHapusEvent(self):
        idEventCRUD = self.inputIdEvent.text()
        if (len(idEventCRUD) != 0):
            try:
                conn = None
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                query = "DELETE FROM event WHERE idEvent =\'"+idEventCRUD+"\'"
                cur.execute(query)
                conn.commit()
                rowChecked = cur.rowcount
                if rowChecked == 0:
                    self.error.setText("idEvent tidak valid")    
                else:
                    self.error.setText("Berhasil menghapus event")
                cur.close()
            except:
                self.error.setText("Pastikan idEvent valid!")
        else: 
            self.error.setText("Anda belum menginput id Event yang ingin dihapus!")
    
    def showEventfunction(self):

        # Membersihkan apabila ada pesan error sebelumnya         
        self.error.setText('')

        # connect to the PostgreSQL server
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        query = 'SELECT * FROM event'
        cur.execute(query)
        conn.commit()
        result = cur.fetchall()

        rowNumber = cur.rowcount
        self.tabelEvent.setRowCount(0)
        if rowNumber ==0:
            self.error.setText("Belum ada data.")
        else:
        # apabila username/ password ga ada
            for row_number,row_data in enumerate(result):
                self.tabelEvent.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tabelEvent.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

# Untuk edit event screen  
class EditEventScreen(QDialog):

    def __init__(self):
        super(EditEventScreen, self).__init__()
        loadUi("editEvent.ui",self)
        # set gambar
        self.logoLM.setPixmap(QPixmap('../img/logo.jpg'))
        self.logoLM.setScaledContents(True)
        # self.searchButton.setIcon(QIcon('./images/search.png'))

        # redirect clicked button
        self.editButton.clicked.connect(self.editEventfunction)
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

    def editEventfunction(self):
        try:
            namaEvent = self.inputNama.text()
            tanggal = self.inputTanggal.text()
            jenis = self.inputJenis.text()
            lokasi = self.inputLokasi.text()
            status = self.inputStatus.text()
            deskripsi = self.inputDeskripsi.toPlainText()
            link = self.inputLink.text()
            idEventCRUD = self.inputIdEvent.text()
            if ((len(idEventCRUD) ==0) or (len(namaEvent)==0) or (len(tanggal)==0)or (len(lokasi)==0)or (len(status)==0)or (len(link)==0)):
                self.error.setText("Pastikan anda menginput data minimal idEvent, nama event, tanggal, lokasi, status, dan link! ")
            else:
                if ((status != 'Available') and (status != 'Unavailable')):
                    self.error.setText("Status tidak valid. Pilih salah satu diantara 'Available' dan 'Unavailable'")
                else: 
                    # try: 
                        # connect to the PostgreSQL server
                    conn = None
                    params = config()
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()
                        # query = 'SELECT password FROM admin WHERE username =\''+user+"\'"
                        # produk_info = [namaProduk, batch, kategori,harga,quantity,berat,deskripsi,link]
                    event_info = (namaEvent, tanggal, jenis, lokasi, deskripsi, link, status, idEventCRUD)
                    query = """UPDATE event SET namaEvent=%s, tglEvent=%s, jenisEvent=%s, lokasiEvent=%s, deskripsi=%s, linkFormDaftar=%s, status=%s WHERE idEvent =%s"""
                    cur.execute(query,event_info)
                    conn.commit()

                    rowChecked = cur.rowcount
                    if rowChecked == 0:
                        self.error.setText("Tidak dapat menghapus karena input tidak valid")
                    else:
                        self.error.setText('')
                            # QMessageBox.about(self,'Edit Event', 'Event berhasil diedit!')
                    conn.close()
                       
                    # except:
                        # QMessageBox.about(self, 'Edit Event', 'Event gagal diupload. Pastikan semua data terisi!')
        except:
            self.error.setText('Pastikan semua data terisi dan valid!')

# Untuk add event screen  
class AddEventScreen(QDialog):
    def __init__(self):
        super(AddEventScreen, self).__init__()
        loadUi("tambahEvent.ui",self)

        # set gambar
        self.logoLM.setPixmap(QPixmap('../img/logo.jpg'))
        self.logoLM.setScaledContents(True)

        # redirect clicked button
        self.unggahEvent.clicked.connect(self.addEventFunction)
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

    def reload(self):
        reload = AddEventScreen()
        widget.addWidget(reload)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def addEventFunction(self):
        try:
            namaEvent = self.inputNama.text()
            tanggal = self.inputTanggal.text()
            jenis = self.inputJenis.text()
            lokasi = self.inputLokasi.text()
            status = self.inputStatus.text()
            deskripsi = self.inputDeskripsi.toPlainText()
            link = self.inputLink.text()
            if ((len(namaEvent)==0) or (len(tanggal)==0)or (len(lokasi)==0)or (len(status)==0)or (len(link)==0)):
                self.error.setText("Pastikan anda menginput data minimal nama event, tanggal, lokasi, status, dan link! ")
            else:
                if ((status != 'Available') and (status != 'Unavailable')):
                    self.error.setText("Status tidak valid. Pilih salah satu diantara 'Available' dan 'Unavailable'")
                else:
                    # try: 
                        # connect to the PostgreSQL server
                    conn = None
                    params = config()
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()
                    event_info = (namaEvent, tanggal, jenis, lokasi, deskripsi, link, status)
                    query = """INSERT INTO event(idEvent,namaEvent, tglEvent, jenisEvent, lokasiEvent, deskripsi, linkFormDaftar, status) VALUES(DEFAULT,%s,%s,%s,%s,%s,%s,%s)"""
                        # namaEvent=%s, tglEvent=%s, jenisEvent=%s, lokasiEvent=%s, deskripsi=%s, linkFormDaftar=%s, status=%s WHERE idEvent =%s"""
                    cur.execute(query,event_info)
                    conn.commit()
                    conn.close()
                        # QMessageBox.about(self,'Tambah Event', 'Event berhasil ditambah!')
                    self.reload()
                    # except:
                        # QMessageBox.about(self, 'Tambah Event', 'Event gagal diupload. Pastikan semua data valid!')
                    
        except:
            self.error.setText('Pastikan semua data terisi dan valid!')   

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
            conn = None
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            query = "DELETE FROM forumdiskusi WHERE idforum = \'"+delete+"\' AND idforum NOT IN (SELECT idforum FROM komentarforum)"
            cur.execute(query)
            conn.commit()
            rowChecked = cur.rowcount
            if rowChecked == 0:
                self.error.setText("Tidak dapat menghapus karena ada komentar atau tidak valid")
                cur.close()
            else:
                self.error.setText("Forum diskusi berhasil dihapus!")
                cur.close()
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
            conn = None
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            query = "WITH filter AS (DELETE FROM pengajuanforum a USING forumdiskusi b WHERE a.idpengajuan = \'"+insert+"\' RETURNING a.judulForum, a.namapengirim, a.tglpublish, a.deskripsi, a.kategori) INSERT INTO forumdiskusi (judulforum, namapengirim, tglpublish, deskripsi, kategori) SELECT * FROM filter;"
            cur.execute(query)
            conn.commit()
            rowChecked = cur.rowcount
            if rowChecked == 0:
                self.error3.setText("Tidak dapat menerima pengajuan karena ID Pengajuan tidak valid")
                cur.close()
            else:
                self.error3.setText("Pengajuan forum berhasil diterima")
                cur.close()
        else: 
            self.error3.setText("Pastikan ID Pengajuan Forum yang ingin diterima valid dan ada!")

    def DeletePengajuan(self): #function delete pengajuan forum diskusi
        delete = self.txtIDPengajuan.text()
        if (len(delete) != 0):
            conn = None
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            query = "DELETE FROM pengajuanforum WHERE idpengajuan = \'"+delete+"\'"
            cur.execute(query)
            conn.commit()
            rowChecked = cur.rowcount
            if rowChecked == 0:
                self.error3.setText("Tidak dapat menolak pengajuan karena ID Pengajuan tidak valid")
                cur.close()
            else:
                self.error3.setText("Pengajuan forum berhasil ditolak")
                cur.close()
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
            conn = None
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            query = "DELETE FROM komentarforum WHERE idkomentar = \'"+delete+"\'"
            cur.execute(query)
            conn.commit()
            rowChecked = cur.rowcount
            if rowChecked == 0:
                self.error.setText("Tidak dapat menghapus karena ada ID Komentar Salah")
                cur.close()
            else:
                self.error.setText("Komentar forum diskusi berhasil dihapus!")
                cur.close()
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
            conn = None
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            komentar_info = (idForum, feedback, namaPengirim)
            query = """INSERT INTO komentarforum(idforum, feedback, namaresponden) VALUES (%s,%s,%s)"""
            cur.execute(query,komentar_info)
            conn.commit()
            conn.close()
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


# PYTEST

@pytest.fixture
def appL(qtbot):
    window = LoginScreen()
    qtbot.addWidget(window)
    return window

def testLogin_inputkosong(appL,qtbot):
    qtbot.keyClicks(appL.usernameField, '')
    qtbot.keyClicks(appL.passwordField, '')
    qtbot.mouseClick(appL.loginButton, QtCore.Qt.LeftButton)
    assert appL.error.text() == "Pastikan tidak ada kolom kosong!"
def testLogin_inputsalah(appL,qtbot):
    qtbot.keyClicks(appL.usernameField, 'salah')
    qtbot.keyClicks(appL.passwordField, 'salah')
    qtbot.mouseClick(appL.loginButton, QtCore.Qt.LeftButton)
    assert appL.error.text() == "Tidak ditemukan username!"

def testLogin_inputpasssalah(appL,qtbot):
    qtbot.keyClicks(appL.usernameField, 'nadiraFM')
    qtbot.keyClicks(appL.passwordField, 'salah')
    qtbot.mouseClick(appL.loginButton, QtCore.Qt.LeftButton)
    assert appL.error.text() == "Invalid username or password"

def testLogin_inputvalid(appL,qtbot):
    qtbot.keyClicks(appL.usernameField, 'nadiraFM')
    qtbot.keyClicks(appL.passwordField, 'xxx')
    qtbot.mouseClick(appL.loginButton, QtCore.Qt.LeftButton)
        # qtbot.waitUntil(app.QtWidgets.QStackedWidget())
    assert appL.error.text() == "Successfully logged in."
        # assert app.error.text() == "Successfully logged in."


#SHOW EVENT
@pytest.fixture
def appES(qtbot):
    window = EventScreen()
    qtbot.addWidget(window)
    return window
    
def testEvent_showeventtabel(appES,qtbot):
    conn = None
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    query = 'SELECT * FROM event'
    cur.execute(query)
    conn.commit()
    result = cur.fetchall()

    rowNumber = cur.rowcount
    appES.tabelEvent.setRowCount(0)
    if rowNumber ==0:
        appES.error.text() == ("Belum ada data.")
    else:
        # apabila ada data
        for row_number,row_data in enumerate(result):
            appES.tabelEvent.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                appES.tabelEvent.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))
                b_item = QtWidgets.QTableWidgetItem(str(data))
                a_item = appES.tabelEvent.item(row_number,column_number)
                assert str(a_item.text()) == str(b_item.text())

#HAPUS EVENT
def testKatalog_HapusEventValid(appES, qtbot):
    qtbot.keyClicks(appES.inputidEvent, 'E1')
    qtbot.mouseClick(appES.hapusButton, QtCore.Qt.LeftButton)
    assert appES.error.text()=="Berhasil menghapus event"

def testKatalog_HapusEventKosong(appES, qtbot):
    qtbot.keyClicks(appES.inputidEvent, '')
    qtbot.mouseClick(appES.hapusButton, QtCore.Qt.LeftButton)
    assert appES.error.text()=="Anda belum menginput id Event yang ingin dihapus!"

def testKatalog_HapusEventKosong(appES, qtbot):
    qtbot.keyClicks(appES.inputidEvent, 'E5')
    qtbot.mouseClick(appES.hapusButton, QtCore.Qt.LeftButton)
    assert appES.error.text()== "Tidak dapat menghapus karena input tidak valid"

#EDIT EVENT
@pytest.fixture
def appEEdit(qtbot):
    window = EditEventScreen()
    qtbot.addWidget(window)
    return window

def testEvent_editInputKosong(appEEdit,qtbot):
    qtbot.keyClicks(appEEdit.inputIdEvent, '')
    qtbot.keyClicks(appEEdit.inputNama, '')
    qtbot.keyClicks(appEEdit.inputTanggal, '')
    qtbot.keyClicks(appEEdit.inputLokasi, '')
    qtbot.keyClicks(appEEdit.inputStatus, '')
    qtbot.keyClicks(appEEdit.inputDeskripsi, '')
    qtbot.keyClicks(appEEdit.inputLink, '')
    qtbot.mouseClick(appEEdit.editButton, QtCore.Qt.LeftButton)
    assert appEEdit.error.text() == "Pastikan anda menginput data minimal idEvent, nama event, tanggal, lokasi, status, dan link! "

def testEvent_editInputValid(appEEdit,qtbot):
    # [EX, Cari jiwax, 2021-12-12,chill,Tangerang,bit.ly/daftar, Available, ini deskripsi]
    qtbot.keyClicks(appEEdit.inputIdEvent, 'E1')
    qtbot.keyClicks(appEEdit.inputNama, 'Cari jiwax')
    qtbot.keyClicks(appEEdit.inputTanggal, '2021-12-12')
    qtbot.keyClicks(appEEdit.inputLokasi, 'Tangerang')
    qtbot.keyClicks(appEEdit.inputStatus, 'Available')
    qtbot.keyClicks(appEEdit.inputDeskripsi, 'ini deskripsi')
    qtbot.keyClicks(appEEdit.inputLink, 'bit.ly/daftar')
    qtbot.mouseClick(appEEdit.editButton, QtCore.Qt.LeftButton)
    assert appEEdit.error.text() == "Edit gagal karena input tidak valid"

def testEvent_editInputTglSalah(appEEdit,qtbot):
    # [EX, Cari jiwa lagi, salahtipe,chill,Tangerang,bit.ly/daftar, Available, ini deskripsi]
    qtbot.keyClicks(appEEdit.inputIdEvent, 'E1')
    qtbot.keyClicks(appEEdit.inputNama, 'Cari jiwax')
    qtbot.keyClicks(appEEdit.inputTanggal, 'salahtipe')
    qtbot.keyClicks(appEEdit.inputLokasi, 'Tangerang')
    qtbot.keyClicks(appEEdit.inputStatus, 'Available')
    qtbot.keyClicks(appEEdit.inputDeskripsi, 'ini deskripsi')
    qtbot.keyClicks(appEEdit.inputLink, 'bit.ly/daftar')
    qtbot.mouseClick(appEEdit.editButton, QtCore.Qt.LeftButton)
    assert appEEdit.error.text() == 'Pastikan semua data terisi dan valid!'

#CREATE/ADD EVENT
@pytest.fixture
def appEAdd(qtbot):
    window = AddEventScreen()
    qtbot.addWidget(window)
    return window

def testEvent_addInputKosong(appEAdd,qtbot):
    qtbot.keyClicks(appEAdd.inputIdEvent, '')
    qtbot.keyClicks(appEAdd.inputNama, '')
    qtbot.keyClicks(appEAdd.inputTanggal, '')
    qtbot.keyClicks(appEAdd.inputLokasi, '')
    qtbot.keyClicks(appEAdd.inputStatus, '')
    qtbot.keyClicks(appEAdd.inputDeskripsi, '')
    qtbot.keyClicks(appEAdd.inputLink, '')
    qtbot.mouseClick(appEAdd.unggahEvent, QtCore.Qt.LeftButton)
    assert appEEdit.error.text() == "Pastikan anda menginput data minimal idEvent, nama event, tanggal, lokasi, status, dan link! "

def testEvent_addInputValid(appEAdd,qtbot):
    # [EX, Cari jiwax, 2021-12-12,chill,Tangerang,bit.ly/daftar, Available, ini deskripsi]
    qtbot.keyClicks(appEAdd.inputIdEvent, 'E1')
    qtbot.keyClicks(appEAdd.inputNama, 'Cari jiwax')
    qtbot.keyClicks(appEAdd.inputTanggal, '2021-12-12')
    qtbot.keyClicks(appEAdd.inputLokasi, 'Tangerang')
    qtbot.keyClicks(appEAdd.inputStatus, 'Available')
    qtbot.keyClicks(appEAdd.inputDeskripsi, 'ini deskripsi')
    qtbot.keyClicks(appEAdd.inputLink, 'bit.ly/daftar')
    qtbot.mouseClick(appEAdd.unggahEvent, QtCore.Qt.LeftButton)
    assert appEAdd.error.text() == "Gagal menambahkan event karena input tidak valid "

def testEvent_addInputTglSalah(appEAdd,qtbot):
    # [EX, Cari jiwax, 2021-12-12,chill,Tangerang,bit.ly/daftar, Available, ini deskripsi]
    qtbot.keyClicks(appEAdd.inputIdEvent, 'E1')
    qtbot.keyClicks(appEAdd.inputNama, 'Cari jiwax')
    qtbot.keyClicks(appEAdd.inputTanggal, 'salahtipe')
    qtbot.keyClicks(appEAdd.inputLokasi, 'Tangerang')
    qtbot.keyClicks(appEAdd.inputStatus, 'Available')
    qtbot.keyClicks(appEAdd.inputDeskripsi, 'ini deskripsi')
    qtbot.keyClicks(appEAdd.inputLink, 'bit.ly/daftar')
    qtbot.mouseClick(appEAdd.unggahEvent, QtCore.Qt.LeftButton)
    assert appEAdd.error.text() == "Gagal menambahkan event karena input tidak valid "