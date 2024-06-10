# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MuensterCityDistrictToolDialog
                                 A QGIS plugin
 Exports a csv or pdf from a selected city district.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-06-04
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Maximilian Elfers, Hendrik Lüning
        email                : hluening@uni-muenster.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import time

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.utils import iface

from qgis.core import QgsProject

from .getDataDialog import Ui_Dialog_get 
from .exportDataDialog import Ui_Dialog_export
from .selectedFeatureInfoClass import DistrictInfo

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'muenster_city_district_tool_dialog_base.ui'))


class MuensterCityDistrictToolDialog(QtWidgets.QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        super(MuensterCityDistrictToolDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # Create the event listeners for the buttons
        self.btnGetData.clicked.connect(self.getDataButton)
        self.btnExportData.clicked.connect(self.exportDataButton)

    def getDataButton(self):
        dInfo = DistrictInfo()
        getDataDialog = QtWidgets.QDialog()
        ui = Ui_Dialog_get()
        ui.setupUi(getDataDialog) # Create UI for the Dialog
        selected_features = dInfo.getSelectedCityDistrict() # Get the selected city district
        if dInfo.checkFeatureCount(selected_features, self): # Check if only one city district is selected
            information_array = self.createInformationArray(selected_features[0], dInfo) # create the information array
            ui.fillInputField(information_array) # Fill the input fields with the information
            getDataDialog.exec_()
        self.close()

    def exportDataButton(self):
        exportDataDialog = QtWidgets.QDialog()
        ui = Ui_Dialog_export()
        ui.window = self
        ui.setupUi(exportDataDialog) # Create UI for the Dialog
        exportDataDialog.exec_()
        self.close()

    def createInformationArray(self, district, dInfo):
        # Create an array with the information
        # This is done with the help of the DistrictInfo class
        return [district['Name'], 
                district['P_District'], 
                dInfo.getDistrictArea(district), 
                dInfo.getHousholdsInDistrict(district), 
                dInfo.getParcelsInDistrict(district), 
                dInfo.getSchoolsInDistrict(district, 0), 
                dInfo.getPoolsInDistrict(district, 1)]
    
