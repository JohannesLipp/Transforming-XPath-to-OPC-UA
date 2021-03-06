# Transforming XPath to OPC-UA (X2OPC)
X2OPC is a Python implementation of the XPath to OPC UA translator.

Authors: Max Kocher, Johannes Theissen-Lipp, Patrick Sapel, and Mauritius Schmitz.

## Requirements
- Python3
- A running OPC UA server (e.g., the [Prosys Simulation Server](https://www.prosysopc.com/products/opc-ua-simulation-server/))

## Usage
To run the files, **fileAnalysis.py** and **OPCtranslator.py** must be in the same folder.  
To extract the address space of the OPC UA Server you have to execute the file **extractor.py**.  
You have to specify the url of the OPC UA server in line 175 like
```python
url = "opc.tcp://...:53530/OPCUA/SimulationServer/"
```
and the path of the output file in line 179 like
```python
path = 'D:\\Downloads\\Files\\OpcExport.txt'
```
After the execution the file OpcExport.txt is created.

The XML image of the export is created with the **fileAnalysis.py** file.  
To run the file, the path of the OpcExport.txt file must be specified in line 9 like
```python
open('D:\\Downloads\\Files\\OpcExport.txt', 'r').read().split("\n")
```
and the path of the XML file to be generated must be specified in line 419 like
```python
file_object = open('D:\\Downloads\\Files\\OpcExport.xml', 'w')
```

After XML expressions have been created, they can be transformed to OPC UA in the file **OPCtranslator.py**.  
For this purpose the url of the OPC UA server must be specified in line 290 like
```python
  url = "opc.tcp://.....:53530/OPCUA/SimulationServer"
```

The following table describes ten axes and their counterpart in OPC UA:

| XPath        | Function      |
| ------------- |:-------------:| 
| child      | child(client, connected, nodeList, offlineList) | 
| parent      | parent(client, connected, nodeList, offlineList)      |
| ancestor | ancestor(client, connected, nodeList, offlineList, rootnode)|
| ancestor-or-self      | ancestorOrSelf(client, connected, nodeList, offlineList, rootnode) | 
| descendant      | descendant(client, connected, nodeList, offlineList)      |
| descendant-or-self | descendantOrSelf(client, connected, nodeList, offlineList)   |
| preceding      | preceding(client, connected, nodeList, offlineList) | 
| following      | following(client, connected, nodeList, offlineList)      |
| preceding-sibling      | precedingSibling(client, connected, nodeList, offlineList) | 
| following-sibling      | followingSibling(client, connected, nodeList, offlineList)      |

The **client** parameter references the server specified by the url.  
The parameter **connected** can be True or False and indicates whether the server or the server's export is used.  
The parameter **nodeList** contains a list of NodeIds on which the function is executed.  
The **offlineList** parameter contains the information of the server's export and is defined in line 292.  
The **rootnode** parameter contains the nodeId of the server's root node. 


## Visualizations
The visualizations folder contains the code to generate all the illustrations shown in chapter 5. Each file can be executed independently and already contains all the necessary information.
