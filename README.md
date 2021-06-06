# Transforming-XQuery-to-OPC-UA
Is a Python implementation of the XQuery to OPC UA translator.

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
file_object = open('D:\\Downloads\\Dateien\\OpcExport.xml', 'w')
```

After XML expressions have been created, they can be transformed to OPC UA in the file **OPCtranslator.py**.
For this purpose the url of the OPC UA server must be specified in line 290 like
```python
  url = "opc.tcp://.....:53530/OPCUA/SimulationServer"
```


| XQuery        | Function      |
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

## Visualizations
The visualizations folder contains the code to generate all the illustrations shown in chapter 5. Each file can be executed independently and already contains all the necessary information.
