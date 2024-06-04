# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MuensterCityDistrictTool
                                 A QGIS plugin
 Exports a csv or pdf from a selected city district.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-06-04
        copyright            : (C) 2024 by Maximilian Elfers, Hendrik Lüning
        email                : hluening@uni-muenster.de
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MuensterCityDistrictTool class from file MuensterCityDistrictTool.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .muenster_city_district_tool import MuensterCityDistrictTool
    return MuensterCityDistrictTool(iface)
