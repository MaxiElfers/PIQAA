from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Image
from reportlab.lib.units import inch
from qgis.utils import iface
import time
import os

class PDFprint:

    district_name, district_parent_name, district_size, district_housholds, district_parcels, district_schools, district_pools = "", "", "", "", "", "", ""
    mapPath = ""

    # Setter for all data fields using an array that contains the information
    def setData(self, information_array):
        self.district_name = str(information_array[0])
        self.district_parent_name = str(information_array[1])
        self.district_size = str(information_array[2])
        self.district_housholds = str(information_array[3])
        self.district_parcels = str(information_array[4])
        self.district_schools = str(information_array[5][0])
        self.district_pools = str(information_array[6][0])

    # Function to get the map image of the district
    def getMapImage(self, district):
        # Get the extent of the district geometry
        extent = district.geometry().boundingBox()
        # Set the map canvas extent
        iface.mapCanvas().setExtent(extent)
        # Refresh the map canvas
        iface.mapCanvas().refresh()
        # Create time buffer for the refresh
        time.sleep(10)
        # Save map as Image
        iface.mapCanvas().saveAsImage(self.mapPath)

    def createPDF(self, district_feat, pdf_output):
        # Set the path of the map image
        self.mapPath = pdf_output
        
        self.getMapImage(district_feat) # Create the map image 
        
        # Start the canvas
        c = canvas.Canvas(pdf_output, pagesize=letter)
    
        # Set title
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(300, 750, f"City District Profile: {self.district_name}")
    
        # Add information
        c.setFont("Helvetica", 12)
        c.drawString(50, 700, f"Parent District: {self.district_parent_name}")
        c.drawString(50, 680, f"Size of the Area: {self.district_size} sq. units")
        c.drawString(50, 660, f"Number of Households: {self.district_housholds}")
        c.drawString(50, 640, f"Number of Parcels: {self.district_parcels}")
    
        # Number of schools
        if self.district_schools == "0":
            c.drawString(50, 620, f"No Schools in this district")
        else:
            c.drawString(50, 620, f"Number of Schools: {self.district_schools}")
        
        # Number of pools
        if self.district_pools == "0":
            c.drawString(50, 600, f"No Pools in this district")
        else:
            c.drawString(50, 600, f"Number of Pools: {self.district_pools}")
            
            
        # Add a line below the title for emphasis
        c.line(50, 740, 550, 740)  # Draw a line below the title
    
        # Add map image
        c.drawImage(self.mapPath, 80, 200, 200, 200)
        
        # Delete the map image after it has been added to the PDF
        os.remove(self.mapPath)
        
        # Save the PDF
        c.save()
