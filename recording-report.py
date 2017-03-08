#!/usr/bin/python3
# This module will query a callmanager end user, extract their associated devices, and query directory number, display name, and recording profile configuration into a CSV report.
# You can use this to audit your configurations for errors on recording.
#
# This runs off module from Github repo 
# https://github.com/bobthebutcher/axl
# Clone it and reference it in PYTHONPATH or sys.path.append( shown below in the code)

# Python3 and depends on suds-jurko
# pip3 install suds-jurko


# YOU MUST Import WSDL

# The WSDL files are not included with this library due to licenses terms. pyaxl provides a script to import it and then build a cache directly into the library.

# First of all you need to download the WSDL files. The AXL WSDL is included in the AXL SQL Toolkit download, which is available in Cisco Unified CM. Follow these steps to download the AXL SQL Toolkit from your Cisco Unified CM server:

# Log into the Cisco Unified CM Administration application.
# Go to Application | Plugins
# Click on the Download link by the Cisco CallManager AXL SQL Toolkit Plugin.
# The axlsqltoolkit.zip file contains the complete schema definition for different versions of Cisco Unified CM.
#
# USAGE:
# python3 recording-report.py -u CCMAdmin -p secret -t recordinguser -o outputfile.csv
# -t is your target user to query for associated devices and report on.

import sys, getopt
import csv
#Change path to your axl library from bobthebutcher
sys.path.append('/home/jbarbee/axl')
from axl.foley import AXL

# Change this file to import your Schema File you downloaded and extracted from Callmanager
wsdl = 'file:///home/jbarbee/AXL/schema/11.0/AXLAPI.wsdl'

def main(argv):
   username = ''
   password = ''
   targetuser = ''
   cucm = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hu:p:o:t:c:",["username=","password=","outputfile=","targetuser=","cucm="])
   except getopt.GetoptError:
      print('Arguments: -u <username> -p <password> -t <target user> -o <Output File> -c <callmanagerIP>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('Arguments: -u <username> -p <password> -t <target user> -o <Output File> -c <callmanagerIP>')
         sys.exit()
      elif opt in ("-u", "--username"):
         username = arg
      elif opt in ("-p", "--password"):
         password = arg
      elif opt in ("-t", "--targetuser"):
         targetuser = arg
      elif opt in ("-o", "--outputfile"):
         outputfile = arg
      elif opt in ("-c", "--cucm"):
         cucm = arg
   ucm = AXL(username, password, wsdl, cucm)
   print('Call Recording Report')
   print('Author: Jason Barbee / TekLinks / @jasonbarbee / jbarbee@teklinks.com')
   print('Username:', username)
   print('Password:', password)
   print('Target user:', targetuser)
   print('Outputfile:', outputfile)
   print('Callmanager AXL:', outputfile)
   hosts = []
   with open(outputfile,'w+') as output_file:
     writer = csv.writer(output_file)
     writer.writerow(['Phone','Line Description','Recording Enabled','Recording Profile'])

     result={}
  
     result=ucm.get_user(user_id=targetuser)
     phonecount=0
     for phone in result['response']['associatedDevices']:
        for phone2 in phone[1]:
           phonecount += 1
           dn=ucm.get_phone(phone2)
           for lines in dn['response']['lines']['line']:
              try:
                 print(phone2 + ','  + lines['display'] + ',' + lines['dirn']['pattern'] + ',' + lines['recordingFlag'] + ',' + str(lines['recordingProfileName']['value']) )
                 writer.writerow([phone2,lines['display'],lines['dirn']['pattern'],lines['recordingFlag'], str(lines['recordingProfileName']['value'])])
              except:
                 print(phone2 + ',' + lines['display'] + ',' + lines['dirn']['pattern'] + ',' + lines['recordingFlag'] + ',No Recording Profile')
                 writer.writerow([phone2,lines['display'],lines['dirn']['pattern'],lines['recordingFlag'], 'None'])
   print("Phone Count:" + str(phonecount))


if __name__ == "__main__":
   main(sys.argv[1:])