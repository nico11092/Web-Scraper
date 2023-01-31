import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import openpyxl

import Components.Main_window as myWindow
import Class.ScraperClass.Scraper as myWin_Scapper
import Class.ExportClass.Export as myExport 

import Class.DataClass.Parameters_Google as Param_G
import Class.DataClass.Parameters_Contact as Param_C

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.ui = myWindow.Ui_MainWindow()

        self.filename_open = ""
        self.filename_close = ""
        self.wb = openpyxl.Workbook()

        self.verif_error_G = False
        self.verif_error_C = False

        self.MyParam_G = None

        self.ui.setupUi(self)

    #functions (slots) for the menu 
    #File 
    def slot_open_file(self):
        self.filename_open, ext = QFileDialog.getOpenFileName(self, "Open a file", "./")

    def slot_save(self):
        if self.filename_close == "":
            self.slot_save_as()
        else:
            self.wb.save(str(self.filename_close)+".xlsx")

    def slot_save_as(self):
        self.filename_close, ext = QFileDialog.getSaveFileName(self, "Save a file", "./")

        self.Export = myExport.Export_Excel(self.wb, self.keywords, self.nb_results, self.language, self.domaine)
        self.Export.save_data(self.liste_link)

        self.wb.save(str(self.filename_close)+".xlsx")

    #Edit 
    def slot_cut(self):
        if self.ui.obj_keywords.hasFocus():
            self.ui.obj_keywords.cut()

    def slot_copy(self):  
        if self.ui.obj_keywords.hasFocus():
            self.ui.obj_keywords.copy()

    def slot_paste(self):
        if self.ui.obj_keywords.hasFocus():
            self.ui.obj_keywords.paste()

    #View
    def clear(self):
        #objectif is to clear the obj_table
        if self.ui.tabWidget.currentIndex() == 0:
            self.ui.obj_table.setRowCount(0)
        if self.ui.tabWidget.currentIndex() == 1:
            self.ui.obj_contact_result.clear()

    #Run 
    def slot_search(self):
        if self.ui.tabWidget.currentIndex() == 0:
            self.search()
        if self.ui.tabWidget.currentIndex() == 1:
            self.search_contact()
        
    #function button search 
    def search(self):
        self.keywords = self.ui.obj_keywords.text()
        if self.keywords != "" or self.verif_error_G == True:
            self.verif_error_G = False

            self.MyParam_G = Param_G.Parameters_G(self.keywords, self.ui.obj_results.currentText(), self.ui.obj_lang.currentText(), self.ui.obj_dom.currentText())

            #clear actual obj_table
            self.clear()

            #init the scraper
            myScrapper = myWin_Scapper.Windows_Scraper(self.MyParam_G)

            #search, retour : liste link 
            self.liste_link = myScrapper.search()
            
            #on ajoute la liste de resultat à obj_table 
            self.set_obj_table()
        else:
            button = QMessageBox.question(self, "Error", "You have not entered a keyword, do you want to continue?")

            if button == QMessageBox.Yes:
                self.verif_error_G = True
                self.search()

    def search_contact(self):
        self.url_contact = self.ui.obj_contact_url.text()
        if self.url_contact != "" or self.verif_error_C == True:
            self.verif_error_C = False
            
            self.MyParam_C = Param_C.Parameters_C(self.url_contact)

            self.clear()

            myScraper_contact = myWin_Scapper.Windows_Scraper(None, self.MyParam_C)

            self.list_contact, self.list_link_contact = myScraper_contact.search_contact()

            self.set_obj_contact_result()
        else:
            button = QMessageBox.question(self, "Error", "You have not entered a URL, do you want to continue?")

            if button == QMessageBox.Yes:
                self.verif_error_C = True
                self.search_contact()

    def set_obj_contact_result(self):
        for i in range(len(self.list_contact)):
            for j in range(len(self.list_contact[i])):
                self.ui.obj_contact_result.append(self.list_contact[i][j])

        self.ui.obj_contact_result.append("\nPage contact :")
        for i in range(len(self.list_link_contact)):
            self.ui.obj_contact_result.append(self.list_link_contact[i])

    def set_obj_table(self):
        liste_check = self.get_check()

        self.ui.obj_table.setRowCount(len(self.liste_link))

        for i in range(len(self.liste_link)):
            items = [QTableWidgetItem(self.liste_link[i].Url), QTableWidgetItem(self.liste_link[i].Title), QTableWidgetItem(self.liste_link[i].Description)]
            for j in range(3):
                if liste_check[j]:
                    self.ui.obj_table.setItem(i, j, items[j])

    def get_check(self):
        check_url = self.ui.obj_URL.isChecked()
        check_title = self.ui.obj_title.isChecked()
        check_descr = self.ui.obj_descr.isChecked()
        liste_check = [check_url, check_title, check_descr]

        return liste_check



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()