import asyncio
import logging
import time
import itertools

import os
from lxml import etree as ET
async def getPath():
    return open('D:\\Downloads\\Files\\OpcExport.txt', 'r').read().split("\n") # add path to export.txt file here here

async def xmlexport(children):
    # children = 0: NodeId list with startnode and all children [[i=84,i=61,i=85,i=86,i=87]]
    # children = 1: Attribute list of each node
    # children = 2: RefType and Typedef list with [[predecessorNodeID,NodeId,RefType,TypeDef],...]
    export = await getPath()

    exportList = []
    for i in export[1:-1]: # node1, node2,....
        new = []
        for g in i.split("$$$"): # attr, childList, parentList
            elems = []
            for f in g.split("|||"): # attr1, child1..., parent1 ,...., attr2 # sonst €, aber gibt wohl codec Porbleme
                subelems = []
                #print(f)
                for h in f.split("$"):
                    subelems.append(h)
                elems.append(subelems)
            new.append(elems)
        exportList.append(new)

    returnList = []
    if(children == 0):
        # generates a list looking like: [[NodeId1,child1,child2,...,childN],[NodeId2,child1,...]]
        # first entry is the context node, all following are its children
        for i in exportList:
            # i[0] = Attributes
            # i[1] = Children
            # i[2] = Parents 
            
            start = [i[0][0][1]] # NodeId of startnode, children NodeIds are following
            if len(i[1][0])>1: # dont include empty list
                #print(i[1])
                for f in i[1]:
                    start.append(f[0]) # append all children to start
            returnList.append(start)
            
    
    elif(children == 1):
        # generates a list looking like: [[NodeId,NodeClass,Displayname,Browsename,Description,Value,DataType, UnitURI...],[NodeId,NodeClass,...]]
        # first entry is the context node, all following are its children
        for i in exportList:
            # i[0] = Attributes
            # i[1] = Children
            # i[2] = Parents
            for f in i[0]:
                #print(i)
                nodeData = []
                nodeData.append(f[1]) # NodeId
                nodeData.append(f[0]) # NodeClass
                nodeData.append(f[2]) # DisplayName
                nodeData.append(f[3]) # BrowseName
                nodeData.append(f[4]) # Description
                nodeData.append(f[5]) # Value
                nodeData.append(f[6]) # DataType

                nodeData.append(f[7]) # UnitURI
                nodeData.append(f[8]) # UnitID
                nodeData.append(f[9]) # UnitRangeMin
                nodeData.append(f[10]) # UnitRangeMax
                returnList.append(nodeData)

    elif(children == 2):
        # creates list with RefType and Typedef like [[predecessorNodeID,NodeId,RefType,TypeDef],...]
        for i in exportList:
            # i[0] = Attributes
            # i[1] = Children
            # i[2] = Parents
            if len(i[1][0])>1:
                for f in i[1]:
                    if len(f)>1:
                        # [i[0][0][1]: predecessorNodeID, f[0]: NodeId, f[1/2]: RefType,TypeDef
                        returnList.append([i[0][0][1],f[0],f[1],f[2]])


    if(children == 3):
        # generates a list looking like: [[NodeId1,child1,child2,...,childN],[NodeId2,child1,...]]
        # first entry is the context node, all following are its children
        for i in exportList:
            # i[0] = Attributes
            # i[1] = Children
            # i[2] = Parents 
            print(i)
            start = [i[0][0][1]] # NodeId of startnode, children NodeIds are following
            if len(i[1][0])>1: # dont include empty list
                #print(i[1])
                for f in i[1]:
                    start.append(f[0]) # append all children to start
            returnList.append(start)

    return returnList


async def pathFinder(start,childList,offlineList):
    # return all paths (from the startnode) until:
    # path has no more child nodes or last node already exists in path (loop)
    time1 = time.perf_counter()
    pathList = [[start]] # [[['Object', 'ns=4;i=1001']]]
    result = []
    f = 0
    childList = []
    for i in offlineList:
        temp = [i[0]]
        for child in i[1]:
            temp.append(child)
        childList.append(temp)
    checkList = []
    dontvisit = set()
    # returns list like: [['i=84', 'i=61', 'i=40', 'i=0'],....] first element is the NodeId of browse node, second NodeId of target node, third reftypeId, fourth typedef
    # if the third element is i=40 (HasTypeDefinition), add the second node to blockedNodes
    typeDefnodes = await xmlexport(2) 
    for node in typeDefnodes:
        if node[2]=="i=40":
            dontvisit.add(node[1])
    # i=2274 Server Diagnostics node. Useless Information -> block
    dontvisit.add("i=2274")
    
    # add all unique nodes to checkList
    for i in childList:
        checkList.append(i[0])
    while len(pathList)>0:
        path = pathList.pop(0)
        vertex = path[-1]
        childrenOfVertex = []

        for child in childList:
            if child[0] == vertex:
                childrenOfVertex = child[1:]
                break
        

        if not childrenOfVertex:
            if vertex in dontvisit:
                result.append(path[:-1])
            else: result.append(path)

        for child in childrenOfVertex:
            if vertex in dontvisit:
                # exclude last element
                result.append(path[:-1])
                continue
            if child not in path:
                pathList.append(path + [child])
            else:
                result.append(path + [child])

        f += 1
        if(f%100000==0):
            pathss = set()
            for childrenOfVertex in result:
                for i in childrenOfVertex:
                    pathss.add(i)
            pathssc = set()
            for childrenOfVertex in pathList:
                for i in childrenOfVertex:
                    pathssc.add(i)

            # cycles x1000         # stack            # unique nodes in stack    # result length(number of paths)  # unique nodes in result
            print(str(f/1000)+ " "+ str(len(pathList)) + " "+ str(len(pathssc))+ " "+ str(len(result))+ " "+ str(len(pathss))+ " "+ str(("{:.3f}".format(time.perf_counter()-time1))))
    time2 = time.perf_counter()
    print("all paths calculated in: ", str(time2 - time1) + " seconds")

    print("deleting all duplicate paths...")
    result.sort()
    uniquePaths=list(result for result,_ in itertools.groupby(result))
    print("all duplicates removed.")

    for i in uniquePaths:
        if i.count(i[-1])>1:
            print("Caution, cycles detected")
    return uniquePaths

async def createXML(startnode, offlineList):

    paths = await pathFinder(startnode, await xmlexport(0), offlineList)
    print("paths calculated")
    attrList = await xmlexport(1)
    print("attrList calculated")
    refTypeList = await xmlexport(2)
    print("refTypeList calculated")
    rootnode = []
    for i in attrList:
        if i[0] == startnode:
            rootnode = i
            break
    print("everything calculated")
    root = ET.Element(rootnode[1])
    root.attrib['NodeId']=rootnode[0]
    root.attrib['ReferenceTypeId']=""
    root.attrib['TypeDefinition']=""
    root.attrib['DisplayName']=rootnode[2]
    root.attrib['BrowseName']=rootnode[3]
    root.attrib['Description']=rootnode[4]
    root.attrib['Value']=rootnode[5]
    root.attrib['DataType']=rootnode[6]

    root.attrib['UnitURI']=rootnode[7]
    root.attrib['UnitID']=rootnode[8]
    root.attrib['UnitRangeMin']=rootnode[9]
    root.attrib['UnitRangeMax']=rootnode[10]

    for pfad in paths:
        node = root
        for currentNode in pfad:
            # get attributes of current node
            attribute = []
            for attr in attrList:
                if attr[0] == currentNode:
                    attribute = attr
                    break

            if len(attribute)==0:
                attribute.append(currentNode)
                for i in range(10):
                    attribute.append("error")
            if not currentNode == root.get("NodeId"):
                # get refType and typeDef according to parent node
                refTypeId = ""
                typeDef = ""
                for i in refTypeList:
                    if i[1] == currentNode and i[0] == node.get("NodeId"):
                        refTypeId = i[2]
                        typeDef = i[3]
                        break
                
                # check if the node has children. If not, create node with its parameters,
                # else check if the NodeId of one of the cildren is equal to the next node
                # in pfad. Repeat until pfad is empty or node child NodeId is unequal to node in pfad 
                if len(list(node)): # list(node) returns all children of node
                    nodeExists = 0
                    # Check if pfad[currentNode] is an attribute of a child of node
                    for element in list(node):
                        #if element.get("NodeId") == pfad[currentNode][1]:
                        if element.get("NodeId") == currentNode:
                            nodeExists=element

                    # if pfad[currentNode] already exists, update node to pfad[currentNode]
                    if not nodeExists == 0:
                        node = nodeExists
                    
                    else:
                        eleme = ET.SubElement(node,attribute[1])
                        eleme.attrib['NodeId']=currentNode
                        eleme.attrib['ReferenceTypeId']=refTypeId
                        eleme.attrib['TypeDefinition']=typeDef
                        eleme.attrib['DisplayName']=attribute[2]
                        eleme.attrib['BrowseName']=attribute[3]
                        eleme.attrib['Description']=attribute[4]
                        eleme.attrib['Value']=attribute[5]
                        eleme.attrib['DataType']=attribute[6]

                        eleme.attrib['UnitURI']=attribute[7]
                        eleme.attrib['UnitID']=attribute[8]
                        eleme.attrib['UnitRangeMin']=attribute[9]
                        eleme.attrib['UnitRangeMax']=attribute[10]

                        # sort the nodes by their NodeId
                        prevNodeId = ""
                        for element in list(node):
                            # if currentNode smaller than the first node of all children, add currentNode left/previous to the first node
                            if not prevNodeId:
                                prevNodeId = element.get("NodeId")
                            else:
                                # run until currentNode is smaller than element. If found, add currentNode left/previous to the first node 
                                if currentNode < prevNodeId:
                                    element.addprevious(eleme)
                                    break
                                else:
                                    if currentNode < element.get("NodeId"):
                                        element.addprevious(eleme)
                                        break
                        node = eleme
                else:
                    eleme = ET.SubElement(node,attribute[1])
                    eleme.attrib['NodeId']=currentNode
                    eleme.attrib['ReferenceTypeId']=refTypeId
                    eleme.attrib['TypeDefinition']=typeDef
                    eleme.attrib['DisplayName']=attribute[2]
                    eleme.attrib['BrowseName']=attribute[3]
                    eleme.attrib['Description']=attribute[4]
                    eleme.attrib['Value']=attribute[5]
                    eleme.attrib['DataType']=attribute[6]

                    eleme.attrib['UnitURI']=attribute[7]
                    eleme.attrib['UnitID']=attribute[8]
                    eleme.attrib['UnitRangeMin']=attribute[9]
                    eleme.attrib['UnitRangeMax']=attribute[10]
                    node = eleme
    print("Number of Nodes: ",str(len(root.xpath(".//*"))))
    return ET.tostring(root, pretty_print=True).decode()


async def createOfflineList(startNode):
    # create an array looking like: [[NodeId,[NodeIdChild1,...,NodeIdChildN],[NodeIdParent1,...,NodeIdParentN]],....]
    # this array contains all NodeIds with their cildren and parents
    # This enables the calculation of XQuery expressions without being connected to the OPC UA server.

    export = await getPath()
    exportList = []
    for i in export[1:-1]: # node1, node2,....
        new = []
        for g in i.split("$$$"): # attr, childList, parentList $$$
            elems = []
            for f in g.split("|||"): # attr1, child1..., parent1 ,...., attr2 €
                subelems = []
                for h in f.split("$"):# $
                    subelems.append(h)
                elems.append(subelems)
            new.append(elems)
        exportList.append(new)
    returnList = []
    for i in exportList:
        # i[0] = Attributes
        # i[1] = Children
        # i[2] = Parents 
        nodes = [i[0][0][1]]# NodeId of startnode, children and parent NodeIds are following 
        children = []
        if len(i[1][0])>1: # dont include empty list, # CHILDREN
            for f in i[1]:
                children.append(f[0]) # append all children to start
        nodes.append(children)
        parents=[]
        if len(i[2][0])>1: # dont include empty list, # PARENTS
            for f in i[2]:
                parents.append(f[0]) # append all children to start
        nodes.append(parents)
        returnList.append(nodes)


    # block all Nodes receiving a HasTypeDefinition reference
    blockedNodes = set()
    # returns list like: [['i=84', 'i=61', 'i=40', 'i=0'],....] first element is the NodeId of browse node, second NodeId of target node, third reftypeId, fourth typedef
    # if the third element is i=40 (HasTypeDefinition), add the second node to blockedNodes
    typeDefnodes = await xmlexport(2) 
    for node in typeDefnodes:
        if node[2]=="i=40":
            blockedNodes.add(node[1])
    blockedNodes.add("i=2274") # Server Diagnostics

    # subsetOfNodes are all descendant nodes of the given node. this are all nodes that are in the xml tree
    subsetOfNodes = await getDescendantX([startNode],returnList,blockedNodes)
    allNodes = await getDescendantX(["i=84"],returnList,[])
    # all nodes that are in allNodes but not in subsetOfNodes are invalid nodes
    invalidNodes = allNodes^subsetOfNodes
    
    ret = []
    for i in returnList:
        if i[0] in invalidNodes:
            continue
        children=[]
        for child in i[1]:
            if not child in invalidNodes:
                children.append(child)
        parents=[]
        for parent in i[2]:
            if not parent in invalidNodes:
                parents.append(parent)
        ret.append([str(i[0]),children,parents])
    return ret

async def getDescendantX(nodeList, offlineList, blockedNodes):
    returnSet = set() # this set will be returned
    checkSet = set() # NodeIds to check
    notToCheck = set()
    notToCheck.update(blockedNodes)
    checkSet.update(nodeList) # initialize checkSet with nodeList
    # repeat until checkSet == 0
    while (len(checkSet) > 0): 
        # extract all children from each node in checkSet
        checkSet.update(await childX(checkSet, offlineList)) 
        # checkSet = all elements in checkSet without the elements in notToCheck
        checkSet = checkSet.difference(notToCheck)
        # a = all elements that are not in the intersection of checkSet and returnSet
        # x1 ^ x2 return the set of all elements in either x1 or x2, but not both (symmetric difference)
        a = checkSet^(returnSet.intersection(checkSet)) 
        returnSet.update(checkSet)
        checkSet = a

    return returnSet
async def parentX(nodeList, offlineList):
    return await getChildParentX(nodeList, False, offlineList)

async def childX(nodeList, offlineList):
    return await getChildParentX(nodeList, True, offlineList)

async def getChildParentX(nodeList, direction, offlineList):
    nodeIdSet = set()
    for nodes in nodeList:
        for i in offlineList:
            if(i[0]==nodes): # i[0] = NodeId
                if(direction): # direction == True if Forward, == False if Inverse
                    nodeIdSet.update(set(i[1])) # i[1] = children of i[0]
                    break
                else:
                    nodeIdSet.update(set(i[2]))  # i[2] = parents of i[0]    
                    break
    
    return nodeIdSet 

async def startExportToXML():
    startNode = "i=84"
    offlineList = await createOfflineList(startNode)
    createdXML = await createXML(startNode, offlineList)
    return createdXML


async def main():
    time1 = time.perf_counter()

    file_object = open('D:\\Downloads\\Dateien\\loeaschen.xml', 'w')
    
    for i in await startExportToXML():
        file_object.write(str(i))

    time2 = time.perf_counter()
    print("Dauer: ", str(time2 - time1) + " Sekunden")

    

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    asyncio.run(main())