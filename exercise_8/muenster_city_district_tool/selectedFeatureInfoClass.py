from qgis.core import QgsProject
from PyQt5.QtWidgets import QMessageBox

class DistrictInfo:
    def __init__(self):
        pass

    def checkGeometryWithinDistrict(self, district, featu):
        if featu is not None:
            # set variables
            amount_in_district = 0
            feature_ids = []
            
            for feat in featu.getFeatures():
                # get geometry of feature
                feat_geom = feat.geometry() 
                # get geometry of districts
                district_geom = district.geometry()
                
                # check if it is within the district
                if feat_geom.within(district_geom): 
                    feature_ids.append(feat.id())
                    if 'Number' in feat: 
                        amount_in_district += int(feat['Number'])
                    else:
                        amount_in_district += 1
            
            # selects all features within; used in the creation of the charts
            featu.selectByIds(feature_ids)
            return amount_in_district # return the amount of features in the given district 
            
            
        else:
            # error handling
            QMessageBox.information(self, "Warning", "No features in district found!")
            return

    def getDistrictArea(self, district):
        # returns the area in m2 of the given district
        return district.geometry().area() 

    def getHousholdsInDistrict(self, district):
        # Load House_Number layer from TOC
        house_numbers = QgsProject.instance().mapLayersByName('House_Numbers')[0]  
        return self.checkGeometryWithinDistrict(district, house_numbers)
        
    def getParcelsInDistrict(self, district):
        # Load Muenster_Parcels layer from TOC
        muenster_parcels = QgsProject.instance().mapLayersByName('Muenster_Parcels')[0] 
        return self.checkGeometryWithinDistrict(district, muenster_parcels)
        
    def getPoolsInDistrict(self, district, school_pool):
        # Load public_swimming_pools layer from TOC
        pools = QgsProject.instance().mapLayersByName('public_swimming_pools')[0] 
        count = self.checkGeometryWithinDistrict(district, pools)
        return (count, "Pools")
    
    def getSchoolsInDistrict(self, district, school_pool):
        # Load Schools layer from TOC
        schools = QgsProject.instance().mapLayersByName('Schools')[0] 
        count = self.checkGeometryWithinDistrict(district, schools)
        return (count, "Schools")

    def checkFeatureCount(self, selected_features, window):
        if len(selected_features) == 1:
            return True
        else:
            # Output error message in QMessageBox
            QMessageBox.critical(window, "Error", "Please select exactly one feature.")
            return False

    def getSelectedCityDistrict(self):
        # Get the selected features
        city_districts = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
        selected_features = city_districts.selectedFeatures()
        return selected_features