from qgis.PyQt.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProject,
                       QgsFeatureRequest,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFileDestination)
from qgis import (processing)
from qgis.utils import iface
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Image
from reportlab.lib.units import inch
import os


class ccdpAlgorithm(QgsProcessingAlgorithm):

    district = 'DISTRICT'
    school_pool = 'SCHOOLORPOOL'
    output_pdf = 'OUTPUTPDF'
    districts_complete = []

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ccdpAlgorithm()

    def name(self):
        return 'createCityDistrictProfile'

    def displayName(self):
        return self.tr('Create City District Profile')

    def group(self):
        return self.tr('Exercise07')

    def groupId(self):
        return 'exercise7'

    def shortHelpString(self):
        return self.tr("This algorithm create a PDF Profile of a selected City District")

    def getSortedCityDistricts(self):
        
        # initiate request for features and ordering
        request = QgsFeatureRequest()
        nameClause = QgsFeatureRequest.OrderByClause("Name", ascending = True)
        orderby = QgsFeatureRequest.OrderBy([nameClause])
        request.setOrderBy(orderby)
        
        # Get the City Districs layer from the TOC
        city_districts = QgsProject.instance().mapLayersByName('Muenster_City_Districts')[0]
        
        # Store all feature names in a list
        if city_districts is not None:
            districts_names = []
            # Iterate over every city district
            for feature in city_districts.getFeatures(request): # This requests the features in a storted order
                self.districts_complete.append(feature) # add all features of the districts to a global variable to be used later
                name = feature["Name"]
                # Add the name of the city district to the list
                districts_names.append(name)
            # return the sorted list of city districts
            return districts_names
        else: 
            return
            # Error handling einbauen

    def initAlgorithm(self, config=None):
        
        # get the sorted City District list
        sortedCityDistrics = self.getSortedCityDistricts()
        
        # Add Parameter for the District
        self.addParameter(
            QgsProcessingParameterEnum(
                self.district, 
                'Select the City District', 
                options=sortedCityDistrics,
                optional=False
            )
        )
        
        # Add Parameter for Schools / Pools
        self.addParameter(
            QgsProcessingParameterEnum(
                self.school_pool, 
                'Select additional Info to be added', 
                options=['Schools', 'Pools'],
                optional=False
            )
        )
        
        # Add Parameter for File Destination
        self.addParameter(
            QgsProcessingParameterFileDestination(
            'PDF_OUTPUT',
            self.tr('Output PDF file'),
            fileFilter='PDF files (*.pdf)'
            )
        )

    def checkGeometryWithinDistrict(self, district, featu):
        
        if featu is not None:
            
            amount_in_district = 0
            
            for feat in featu.getFeatures():
                
                feat_geom = feat.geometry() # get geometry of feature
                district_geom = district.geometry() # get geometry of districts
                
                if feat_geom.within(district_geom): # check if it is within the district
                
                    if 'Number' in feat: 
                        amount_in_district += int(feat['Number'])
                    else:
                        amount_in_district += 1
                    
            return amount_in_district # return the amount of features in the given district 
            
        else:
            # Add error handling
            return
    
    def getDistrictArea(self, district):
        
        return district.geometry().area() # returns the area in m2 of the given district
    
    def getHousholdsInDistrict(self, district):
    
        house_numbers = QgsProject.instance().mapLayersByName('House_Numbers')[0] # Load House_Number layer from TOC 
        
        return self.checkGeometryWithinDistrict(district, house_numbers)
            
    def getParcelsInDistrict(self, district):
        
        muenster_parcels = QgsProject.instance().mapLayersByName('Muenster_Parcels')[0] # Load Muenster_Parcels layer from TOC
        
        return self.checkGeometryWithinDistrict(district, muenster_parcels)
            
    def getSchoolsOrPoolsInDistrict(self, district, school_pool):
        
        if school_pool == 'Schools':
            schools = QgsProject.instance().mapLayersByName('Schools')[0] # Load Schools layer from TOC
            return (self.checkGeometryWithinDistrict(district, schools), "Schools")
        else: 
            pools = QgsProject.instance().mapLayersByName('public_swimming_pools')[0] # Load public_swimming_pools layer from TOC
            return (self.checkGeometryWithinDistrict(district, pools), "Pools")
    
    def getMapImage(self, district):

        # Get the extent of the district geometry
        extent = district.geometry().boundingBox()

        # Set the map canvas extent
        iface.mapCanvas().setExtent(extent)

        # Refresh the map canvas
        iface.mapCanvas().refresh()
        
        # Create time buffer for the refresh
        time.sleep(5)
        
        # Set picture path
        picturePath = 'district_extent.png'
        
        # Save map as Image
        iface.mapCanvas().saveAsImage(picturePath)
    
    def createPDF(self, pdf_output, feedback, parameters):
        
        # Store district feature in variable 
        district_feat = self.districts_complete[parameters[self.district]]
        
        district_name = district_feat['Name'] # Store Name of selected District
        district_parent_name = district_feat['P_District'] # Store Name of parent District
        district_size = self.getDistrictArea(district_feat) # Store Area size of district
        district_housholds = self.getHousholdsInDistrict(district_feat) # Store amount of households in districts
        district_parcels = self.getParcelsInDistrict(district_feat) # Store amount of parcels in districts
        district_schools_or_pools, sop_array = self.getSchoolsOrPoolsInDistrict(district_feat, parameters[self.school_pool]) # Store amount of schools or pools in districts
        self.getMapImage(district_feat) # Create the map image 
        
        feedback.setProgressText(str(district_housholds))
        feedback.setProgressText(str(district_parcels))
        feedback.setProgressText(str(district_schools_or_pools))
        
        
        
        c = canvas.Canvas(parameters['PDF_OUTPUT'], pagesize=letter)
    
        # Set title
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(300, 750, f"City District Profile: {district_name}")
    
        # Add information
        c.setFont("Helvetica", 12)
        c.drawString(50, 700, f"Parent District: {district_parent_name}")
        c.drawString(50, 680, f"Size of the Area: {district_size} sq. units")
        c.drawString(50, 660, f"Number of Households: {district_housholds}")
        c.drawString(50, 640, f"Number of Parcels: {district_parcels}")
    
        # Number of schools or pools
        if district_schools_or_pools == 0:
            c.drawString(50, 620, f"No {sop_array} in this district")
        else:
            c.drawString(50, 620, f"Number of {sop_array}: {district_schools_or_pools}")
            
        # Add a line below the title for emphasis
        c.line(50, 740, 550, 740)  # Draw a line below the title
    
        # Add map image
        #map_image_path = "district_extent.png"
        #map_image = Image(map_image_path, width=400, height=400)
        #map_image.drawOn(c, 100, 350)
    
        c.save()

    def processAlgorithm(self, parameters, context, feedback):
        
        pdf_output = self.parameterAsFileOutput(parameters, 'PDF_OUTPUT', context)
        
        self.createPDF(pdf_output, feedback, parameters)
        
        return {'PDF_OUTPUT': pdf_output}
