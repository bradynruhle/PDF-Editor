# -*- coding: utf-8 -*-
"""
Created on Sun April 3 11:33:54 2016

@author: User
"""
from PyQt5.QtWidgets import (QTreeWidget, QTreeWidgetItem, QAbstractItemView)
from PyQt5.QtCore import Qt


class DropTreeWidget(QTreeWidget):
    def __init__(self,settings, parent=None):
        QTreeWidget.__init__(self, parent)
        #self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setItemsExpandable(True)
        self.setAnimated(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.settings=settings

        root=self.invisibleRootItem()
        root.setData(0,Qt.ToolTipRole,"root")
        
    def addItem(self,strings,category,parent=None):
        if category not in self.settings:
            print("category n/a " +str(category))
            return False
        if parent is None:
            parent=self.invisibleRootItem()

        item=QTreeWidgetItem(parent,strings)
        item.setData(0,Qt.ToolTipRole,category)
        item.setExpanded(True)
        item.setFlags(self.settings[category][1])
        return item
    
    def dragMoveEvent(self, event):
        role=Qt.ToolTipRole
        itemToDropIn = self.itemAt(event.pos())
        itemBeingDragged=self.currentItem()
        whitelist=self.settings[itemBeingDragged.data(0,role)][0]

        if itemToDropIn is None:
            itemToDropIn=self.invisibleRootItem()

        if itemToDropIn.data(0,role) in whitelist:
            super(DropTreeWidget, self).dragMoveEvent(event)
            return
        else:
            # possible "next to drop target" case
            parent=itemToDropIn.parent()
            if parent is None:
                parent=self.invisibleRootItem()
            if parent.data(0,role) in whitelist:
                super(DropTreeWidget, self).dragMoveEvent(event)
                return
        event.ignore()

    def dropEvent(self, event):
        role=Qt.ToolTipRole

        #item being dragged
        itemDragged=self.currentItem()
        whitelist=self.settings[itemDragged.data(0,role)][0]

        #parent before the drag
        oldParent=itemDragged.parent()
        if oldParent is None:
            oldParent=self.invisibleRootItem()
        oldIndex=oldParent.indexOfChild(itemDragged)

        #accept any drop
        super(DropTreeWidget,self).dropEvent(event)

        #look at where itemBeingDragged end up
        newParent=itemDragged.parent()
        if newParent is None:
            newParent=self.invisibleRootItem()

        if newParent.data(0,role) in whitelist:
            # drop was ok
            return
        else:
            # drop was not ok, put back the item
            newParent.removeChild(itemDragged)
            oldParent.insertChild(oldIndex,itemDragged)