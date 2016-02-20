import sys
from PyQt4 import QtCore, QtGui, uic
from model import *

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
      super(MainWindow, self).__init__()
      uic.loadUi('main_window.ui', self)
#      self.equipmentUsedLineEdit.setValidator(QtGui.QIntValidator(0, 99999999999, self))
      self.addUsageButton.clicked.connect(self.add_usage)
      self.tableWidget_2.itemChanged.connect(self.change_equipment_amount)
      
    def change_equipment_amount(self, item):
      session = Session()
      with session.begin():
        if (item.text().toInt()[1]):
          amount_available = item.text().toInt()[0]
          equipment_id = self.tableWidget_2.item(item.row(), 0).text().toInt()[0]
          session.update_equipment(equipment_id, amount_available)
        draw_data = self.get_draw_data(session)
      self.draw(draw_data)
      
    def add_usage(self):
      
      if (self.equipmentUsedLineEdit.text().toInt()[1]):
        equipment_id = self.equipmentUsedLineEdit.text().toInt()[0]
        usage = self.amountUsedSpinBox.value()
        session = Session()
        with session.begin():
          session.add_usage(equipment_id, usage)
          session.commit()
          draw_data = self.get_draw_data(session)
        self.draw(draw_data) 
      else:
        self.equipmentUsedLineEdit.clear()
        self.amountUsedSpinBox.setValue(1)

      
    def __set_row(self, row, key, value):
      self.tableWidget.setItem(row, 0, self.create_read_only_table_widget_item(str(key)))
      self.tableWidget.setItem(row, 1, self.create_read_only_table_widget_item(str(value)))
      
    def __set_row_2(self, row, key, value):
      self.tableWidget_2.setItem(row, 0, self.create_read_only_table_widget_item(str(key)))
      self.tableWidget_2.setItem(row, 1, self.create_table_widget_item(str(value)))
      
    def __draw_usage(self, current_treatment):
      self.tableWidget.clearContents()
      
      row_count = len(current_treatment.equipment_usages)
      self.tableWidget.setRowCount(row_count)
      for row in range(row_count):
        usage = current_treatment.equipment_usages[row]
        self.__set_row(row, usage.equipment_id, usage.amount_used)
      
    def __draw_state(self, all_equipment):
      self.tableWidget_2.blockSignals(True)
      self.tableWidget_2.clearContents()
      
      
      row_count = len(all_equipment)
      self.tableWidget_2.setRowCount(row_count)
      for row in range(row_count):
        usage = all_equipment[row]
        self.__set_row_2(row, usage.id, usage.amount_available)
      self.tableWidget_2.blockSignals(False)
      
    def get_draw_data(self, session):
      all_equipment = session.all_equipment()
      current_treatment = session.get_current_or_create()
      return (all_equipment, current_treatment)
      
    def draw(self, draw_data):
      (all_equipment, current_treatment) = draw_data
      self.__draw_usage(current_treatment)
      self.__draw_state(all_equipment)
      

    def create_read_only_table_widget_item(self, string):  
      item = QtGui.QTableWidgetItem(string)
      item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
      return item
  
    def create_table_widget_item(self, string):
      item = QtGui.QTableWidgetItem(string)
      return item
      

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    session = Session()
    with session.begin():
      myapp.draw(session)
    sys.exit(app.exec_())
