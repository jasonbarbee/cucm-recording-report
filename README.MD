# Recording User Report
 This module will query a callmanager end user, extract their associated devices, and query directory number, display name, and recording profile configuration into a CSV report.
 
 You can use this to audit your configurations for errors on recording.

 This runs off module from Github repo 
 https://github.com/bobthebutcher/axl
 Clone it and reference it in PYTHONPATH or sys.path.append( shown below in the code)

# Dependencies
 Python3 and depends on suds-jurko
 pip3 install suds-jurko


# YOU MUST Import WSDL

The WSDL files are not included with this library due to licenses terms. pyaxl provides a script to import it and then build a cache directly into the library.

First of all you need to download the WSDL files. The AXL WSDL is included in the AXL SQL Toolkit download, which is available in Cisco Unified CM. Follow these steps to download the AXL SQL Toolkit from your Cisco Unified CM server:

 Log into the Cisco Unified CM Administration application.
 Go to Application | Plugins
 Click on the Download link by the Cisco CallManager AXL SQL Toolkit Plugin.
 The axlsqltoolkit.zip file contains the complete schema definition for different versions of Cisco Unified CM.

# USAGE:
```
 python3 recording-report.py -u CCMAdmin -p secret -t recordinguser -o outputfile.csv
 ```

 -t is your target user to query for associated devices and report on.
