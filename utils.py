#!/usr/bin/python

'''
/*
 * @File: utils.py
 * @Author: Arunkumar Sadasivan
 * @Date: 11/01/2017
 * @Description: utils.py contains common methods that are used by different python modules and classes.
 * @Usage: N/A
 */
 
'''
import os
import datetime
import configparser

# Defaults

csvdelimiter = "@@" # data might contain commas, semicolon etc. So, it is safe to use a delimiter that doesn't exists in the string.
eoldelimiter = "@@@" # end of line delimiter

'''
########################## Config Parser #################################################################################
'''
# Read configuration file
def readConfig(configFile):
    """
    Returns the config object
    """
    if not os.path.exists(configFile):
        print("[Error] Unable to find the configuration file:" + configFile)
        exit
    else:
        config = configparser.ConfigParser()
        config.read(configFile)
        return config   # returns config object
    

# get the config value
def getConfigValue(configObj,section,key): 
    return configObj.get(section,key)   
    
'''
########################## Date/Time #################################################################################
'''
   
# This method is to get the current date and time
def getDateTime(fileName,fileExt):
    # get current date and time 
    currentDateTime = datetime.datetime.now()
    # append the file with current date and time
    fileName = fileName + "_" + currentDateTime.strftime("%Y-%m-%d_%H-%M-%S") + "." + fileExt
    return fileName

'''
########################## HTML Report #################################################################################
'''

# Convert a CSV data into html report. 
def createHTMLReport(csvdata, htmlReportName, reportTitle, details):
    csvArry = csvdata.split(eoldelimiter) # convert the CSV string into list)
    csvArry = filter(None, csvArry) # remove empty values
    #print(csvArry)
    print("[Info] Creating HTML report...")
    with open(htmlReportName, 'w') as fileHandle: #enter the output filename
        fileHandle.write("<!-- Latest compiled and minified CSS -->" + "\n")
        fileHandle.write("<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.8.1/bootstrap-table.min.css'>" + "\n") 
        fileHandle.write("<!-- Latest compiled and minified CSS -->" + "\n")
        fileHandle.write("<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css'>" + "\n")       
        fileHandle.write("<table data-toggle = 'table' data-pagination = 'true'>" + "\n")
        fileHandle.write("<h3 align='center'> <font color='blue'> " + reportTitle +  " </font> </h3>" + "\n")
        if details:
            for detail in details:
                fileHandle.write("<h4 align='left'> <font color='black'> " + detail +  " </font> </h4>" + "\n")                
#         fileHandle.write("<h3 align='center'> <font color='blue'> " + "Device type:RealPresense Group 300" +  " </font> </h3>" + "\n")
#         fileHandle.write("<h3 align='center'> <font color='blue'> " + "Device type:6.2" +  " </font> </h3>" + "\n")
#         fileHandle.write("<h3 align='center'> <font color='blue'> " + "URI:" + uri + " </font> </h3>" + "\n")
        fileHandle.write("<style type='text/css'>" + "\n")
        fileHandle.write("table { color: #333; /* Lighten up font color */ font-family: Helvetica, Arial, sans-serif; /* Nicer font */  width: 100%; border-collapse:collapse; border-spacing: 0; }"+ "\n")
        fileHandle.write("table, td, th, tr { border-style: solid; border-width: 2px;}" + "\n")
        fileHandle.write("td, th { height: 30px;} /* Make cells a bit taller */" + "\n")
        fileHandle.write("th { background: #FFFFFF; /* Light grey background */ font-weight: bold; /* Make sure they\"re bold */ text-align: left; /* align text to left */} " + "\n")
        fileHandle.write("td { background: #DFDFDF; /* White background */ text-align: left; /* align text to left */ } " + "\n")
        fileHandle.write("</style>" + "\n")
        firstrow = True
        for row in csvArry:
            print(row)
            rows = row.split(csvdelimiter)
            if firstrow:
                fileHandle.write("\n\n\n\n\t" + "<thead>" + "\n" + "\t\t" + "<tr>" + "\n")
                for col in rows:
                    fileHandle.write("\t\t\t" + "<th data-sortable='true'>" +  col + "</th>" + "\n")
                fileHandle.write("\t\t" + "</tr>" + "\n\t" + "</thead>"  + "\n")
                fileHandle.write("\t" + "<tbody>" + "\n")
                firstrow = False
            else:
                fileHandle.write("\t\t" + "<tr>" + "\n")
                for col in rows:
                    col = col.replace("\n","<br />")
                    fileHandle.write("\t\t\t" + "<td>"  + col + "</td>" + "\n")
                fileHandle.write("\t\t" + "</tr>" + "\n")
        fileHandle.write("\t" + "</tbody>" + "\n")
        fileHandle.write("</table>" + "\n")
        fileHandle.write("<!-- jQuery (necessary for Bootstrap\'s JavaScript plugins) -->" + "\n")
        fileHandle.write("<script src='https://ajax.googleapis.com/ajax/libs/jquery/2.1.0/jquery.min.js'></script>" + "\n")
        fileHandle.write("<!-- Latest compiled and minified JavaScript -->"  + "\n")
        fileHandle.write("<script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js'></script>" + "\n")
        fileHandle.write("<!-- Latest compiled and minified JavaScript -->" + "\n")
        fileHandle.write("<script src='https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.8.1/bootstrap-table.min.js'></script>" + "\n")
    print("[Done] Custom HTML report successfully created: " + htmlReportName)
    