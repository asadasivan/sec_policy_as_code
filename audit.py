#!/usr/bin/python

'''
/*
 * @File: audit.py
 * @Author: Arunkumar Sadasivan
 * @Date: 10/24/2017
 * @Description: It uses the testssl.sh utility to test SSL/TLS
 * @Usage: python audit.py -p testssl.sh/testssl.sh -t ok -o testssloutput -u 10.200.33.10         
 */
 
'''

import subprocess
import json
import argparse
import utils


# Defaults

csvdelimiter = "@@" # data might contain commas, semicolon etc. So, it is safe to use a delimiter that doesn't exists in the string.
eoldelimiter = "@@@" # end of line delimiter
# testSSLPath = "/home/asadasivan/testssl.sh/testssl.sh"
# outputFile = "/tmp/testSSL.json"
# sev_threshold = "high"
#guidelinesFile = 'guidelines.json'
#threshold = ["critical","high","medium","low","ok","info"]
configFile = 'app.cfg' 
configObj = utils.readConfig(configFile)
reportName = utils.getConfigValue(configObj, 'report', 'reportName')
#threshold = utils.getConfigValue(configObj, 'testssl', 'threshold')

deviceType = "Device type:" + utils.getConfigValue(configObj, 'default', 'devicetype')
version = "Version:" + utils.getConfigValue(configObj, 'default', 'version')
uri = "URI:" + utils.getConfigValue(configObj, 'default', 'uri')
reportTitle = utils.getConfigValue(configObj, 'report', 'reportTitle')


def testSSL(testSSLPath, uri, testSSLoutputFile, sev_threshold):
    #output = subprocess.check_output("testssl.sh --jsonfile " + jsonFile + host)
    print("[Info] Please wait currently running SSL/TLS tests...")
#     # get current date and time 
#     currentDateTime = datetime.datetime.now()
#     # append the file with current date and time
#     outputFile = outputFile + "_" + currentDateTime.strftime("%Y-%m-%d_%H-%M-%S") + ".json"
    testSSLoutputFile = utils.getDateTime(testSSLoutputFile, "json")
    p1 = subprocess.Popen([testSSLPath, "--jsonfile", testSSLoutputFile, uri], stdout=subprocess.PIPE)   
    # Run the command
    output = p1.communicate()[0]
    print (output)
    csvdata = createCSVfindings(testSSLoutputFile,sev_threshold) 
    htmlReportName = utils.getDateTime(reportName, "html") 
    details = [deviceType,version,uri] 
    utils.createHTMLReport(csvdata, htmlReportName, reportTitle, details)


# read the JSON output from testssl.sh script and create a CSV list of all findings based on the severity level or threshold.
def createCSVfindings(testSSLoutputFile, sev_threshold):
    findings = None
    vul_count = 0
    result = "Fail"
    guidelines = readGuidelines() # read the guidelines testssl mapping file.
    csvheader = "Severity" + csvdelimiter + "Issue" + csvdelimiter + "CVE" + csvdelimiter + "Violation Status" + csvdelimiter + "PSO Guidelines" + eoldelimiter
    print("[Info] Creating CSV file....")
    with open(testSSLoutputFile) as json_file:
        json_data = json.load(json_file) # Load the testssl output file
        firsttime = True 
        for data in json_data:
            testSSLid = data["id"]
            severity = data["severity"]
            finding = data["finding"]
            cve = data.get("cve","None") # return none if key doesn't exists
            violation = getViolationStatus(severity)
            if firsttime:
                if checkSevThreshold(severity, sev_threshold):
                    findings = severity.lower() + csvdelimiter + finding + csvdelimiter + cve + csvdelimiter + violation + csvdelimiter + getGuidelinesData(guidelines,testSSLid) + eoldelimiter
                    firsttime = False
                    vul_count = vul_count + 1
            else:
                if checkSevThreshold(severity, sev_threshold):
                    findings = findings + severity.lower() + csvdelimiter + finding + csvdelimiter + cve + csvdelimiter + violation + csvdelimiter + getGuidelinesData(guidelines,testSSLid) + eoldelimiter 
                    vul_count = vul_count + 1
        findings = csvheader + eoldelimiter + findings                       
#     if findings:
#         print(findings)
    if vul_count == 0:
        result = "Pass"
    print("Total Findings:"+ str(vul_count) +  ", Result:" + result)
    return findings    
           
# check if the severity level matches the threshold
def checkSevThreshold(severity, sev_threshold):
    threshold = utils.getConfigValue(configObj, 'testssl', 'threshold')
    threshold_list = threshold.split(",")
    if sev_threshold.lower() == "critical":
        threshold_list.remove("high")
        threshold_list.remove("medium")
        threshold_list.remove("low")
        threshold_list.remove("ok")
        threshold_list.remove("info")
    elif sev_threshold.lower() == "high":
        threshold_list.remove("medium")
        threshold_list.remove("low")
        threshold_list.remove("ok")
        threshold_list.remove("info")
    elif sev_threshold.lower() == "medium":
        threshold_list.remove("low")
        threshold_list.remove("ok")
        threshold_list.remove("info")
    elif sev_threshold.lower() == "low":
        threshold_list.remove("ok")
        threshold_list.remove("info")
    elif sev_threshold.lower() == "ok":
        threshold_list.remove("info")
    
    if severity.lower() in threshold_list:
        return True    
    else:
        return False
    

# check if the PSO guidelines is violated
def getViolationStatus(severity):  
    if severity.lower() == "ok":
        return "pass"
    elif severity.lower() == "info":
        return "warning"
    else:
        return "fail"  
    

# Read the guidelines json file
def readGuidelines():
    guidelinesFile = utils.getConfigValue(configObj, 'guidelines', 'guidelinesFile')
    with open(guidelinesFile, 'r') as json_file:
        json_data = json.load(json_file)
        return json_data
    
   
def getGuidelinesData(guidelines,testSSLID):
    guideline = guidelines.get(testSSLID)
    complianceData = "Not defined"
    if guideline:
        for guideline in guideline:
            print (guideline["PSO Guideline"])
            name = guideline["PSO Guideline"]
            compliance = guideline["Compliance"]
            complianceData = "PSO Guideline Name:" + name + "\n" + "Requirements:" + "\n" + '\n'.join(compliance) + "\n\n"
    return complianceData
    

    
    
    
###############################################################################
# Main
###############################################################################
def main(args):
    testSSLPath = None
    testSSLResultsFile = None
    sev_threshold = None
    uri = None
    
    if args.testsslpath:
        testSSLPath = args.testsslpath
    else:
        utils.getConfigValue(configObj, 'testssl', 'testSSLPath')
    
    if args.outputfile:
        testSSLResultsFile = args.outputfile
    else:
        utils.getConfigValue(configObj, 'testssl', 'testSSLResultsFile')
        
    if args.threshold:
        sev_threshold = args.threshold
    else:
        utils.getConfigValue(configObj, 'testssl', 'min_threshold')
        
    if args.uri:
        uri = args.uri
    else:
        utils.getConfigValue(configObj, 'default', 'uri')  
        
    #threshold = utils.getConfigValue(configObj, 'testssl', 'threshold')   
    threshold = utils.getConfigValue(configObj, 'testssl', 'threshold') 
    threshold_list = threshold.split(",")
    
    if sev_threshold.lower() in threshold_list:
        if uri:
            testSSL(testSSLPath, uri, testSSLResultsFile, sev_threshold)
        else:
            print("[Error] Host or URI not defined...")
            exit
    else:
        print("[Error] Unknown threshold value. Please enter a valid one from the list:critical, high, medium, low, ok or info.")
      
    
if __name__ == "__main__":
    def help_formatter(prog):
        r"Widen the text that is printed when the app is invoked with --help"
        args = dict(max_help_position=60, width=120)
        return argparse.HelpFormatter(prog, **args)

    parser = argparse.ArgumentParser(formatter_class=help_formatter)
    parser.add_argument("-p", "--testsslpath", default=False,
                        required=False,
                        help="Test for SSL or TLS Protocols supported")
    parser.add_argument("-t", "--threshold", type=str, default="info",
                        required=False,
                        help="Minimum threshold (severity) limit that needs to be compliant.")
    parser.add_argument("-o", "--outputfile", type=str, default=None,
                        required=False,
                        help="File name for the SSL results file.")
    parser.add_argument("-u", "--uri", default=False,
                        required=False,
                        help="Host to run the tests")
    args = parser.parse_args()
    try:
        main(args)
    except KeyboardInterrupt:
        pass     