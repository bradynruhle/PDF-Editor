# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 12:04:09 2016

@author: User
"""
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QApplication)
from Ui_PDFeditor import Ui_MainWindow
from pathlib import Path

class PDF:
    def __init__(self, docName, docUrl, fileReader):
        self.docName = docName
        self.docUrl = docUrl
        self.fileReader = fileReader
        
# The class that handles the application itself
class ApplicationWindow(QMainWindow):
    def __init__(self):
# Handle the application display
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionImport.triggered.connect(self.callback_open)
        self.ui.actionSave.triggered.connect(self.callback_save)
        self.ui.actionDelete.triggered.connect(self.callback_delete)
        self.listPDF = []
        
    def callback_open(self):
        home_dir = str(Path.home())
        filters = "PDF files (*.pdf)"
        fname = QFileDialog.getOpenFileName(self, 'Open file', 
                                            home_dir, filters)
        if fname[0]:
            reader = PdfFileReader(fname[0]);
            numPages = reader.getNumPages()
            docName = Path(fname[0]).stem  
            newPDF = PDF(docName, fname[0], reader)
            self.listPDF.append(newPDF)
            pdf = self.ui.treeWidget.addItem([docName, str(numPages), 
                                              fname[0]],"parent")
            for i in range(1, numPages+1):
                self.ui.treeWidget.addItem([docName, str(i), fname[0]], "children", pdf)
                
    def callback_delete(self):
        item = self.ui.treeWidget.selectedItems()
        if item:
            if item[0].parent() == None:
                docName = str(item[0].text(0)) 
                docUrl = str(item[0].text(2)) 
                index = self.ui.treeWidget.indexOfTopLevelItem(item[0])
                self.ui.treeWidget.takeTopLevelItem(index)
                #check no children are using it
                children = False
                root = self.ui.treeWidget.invisibleRootItem()
                parentCount = root.childCount()   
                for i in range(parentCount):
                    if not children:
                        parent = root.child(i)
                        if parent != item[0]:                        
                            child_count = parent.childCount()
                            for j in range(child_count):
                                if not children:
                                    childDocName = str(parent.child(j).text(0))
                                    childDocUrl = str(parent.child(j).text(2))
                                    if childDocName == docName and childDocUrl == docUrl:
                                        children = True

                if not children:
                    for pdf in self.listPDF:
                        if pdf.docName == docName and pdf.docUrl == docUrl:
                            del pdf


            else:
                docName = str(item[0].text(0)) 
                docUrl = str(item[0].text(2)) 
                parent = item[0].parent()
                index = parent.indexOfChild(item[0])
                parent.takeChild(index)
                #check no other children are using it
                noSibling = True
                root = self.ui.treeWidget.invisibleRootItem()
                parentCount = root.childCount()   
                for i in range(parentCount):
                    if noSibling:
                        parent = root.child(i)
                        child_count = parent.childCount()
                        for j in range(child_count):
                            if noSibling:
                                childDocName = str(parent.child(j).text(0))
                                childDocUrl = str(parent.child(j).text(2))
                                if childDocName == docName and childDocUrl == docUrl:
                                    noSibling = False

                if noSibling:
                    for pdf in self.listPDF:
                        if pdf.docName == docName and pdf.docUrl == docUrl:
                            del pdf

    def callback_save(self):
        home_dir = str(Path.home())
        filters = "PDF files (*.pdf)"
        fname = QFileDialog.getSaveFileName(self, 'Save File', 
                                            home_dir, filters)
        if fname[0]:
            output = PdfFileWriter()
            root = self.ui.treeWidget.invisibleRootItem()
            parentCount = root.childCount()   
            for i in range(parentCount):
                item = root.child(i)
                docUrl = str(item.text(2)) 
                file = None
                docName = str(item.text(0)) 
                for pdf in self.listPDF:
                    if pdf.docName == docName and pdf.docUrl == docUrl:
                        file = pdf.fileReader
                child_count = item.childCount()
                for j in range(child_count):
                    page = int(item.child(j).text(1))-1
                    childDocName = str(item.child(j).text(0))
                    childUrl = str(item.child(j).text(2))
                    childFile = None
                    if docUrl != childUrl:
                        for pdf in self.listPDF:
                            if pdf.docName == childDocName and pdf.docUrl == childUrl:
                                childFile = pdf.fileReader
                        print('child result for' + childUrl + ' %i' % page) 
                        output.addPage((childFile.getPage(page)))                               
                    else:
                        print('result for' + docUrl + ' %i' % page) 
                        output.addPage((file.getPage(page)))
            with open(fname[0], "wb") as outputStream:
                output.write(outputStream)

                
def main():
	print("Loading...")
	app = QApplication(sys.argv)
	application = ApplicationWindow()
	print("Application loaded.")
	application.show()
	sys.exit(app.exec_())

# Provides a start point for out code
if __name__ == "__main__":
	main()