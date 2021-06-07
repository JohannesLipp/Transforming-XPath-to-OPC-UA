# enables offline XQuery expression parsing
import asyncio
import logging
import time
from asyncua import Client, ua

import os
from lxml import etree as ET
from fileAnalysis import createOfflineList, xmlexport


async def following(client, connected, nodeList, offlineList):
    return await precfollow(client, connected, nodeList, False, offlineList)

async def preceding(client, connected, nodeList, offlineList):    
    return await precfollow(client, connected, nodeList, True, offlineList)
 
async def precfollow(client, connected, nodeList, direction, offlineList):
    # 1. ancestor-or-self of ndoeList
    # 2. siblings of all results
    # 3. results in tempSiblings
    tempSiblings = set()
    checkSet = set()
    checkSet.update(await ancestorOrSelf(client,connected,nodeList,offlineList,"i=84"))

    if(direction):# True if preceding
        siblings = await precedingSibling(client, connected, checkSet, offlineList)
    else: # if following
        siblings = await followingSibling(client, connected, checkSet, offlineList)
    tempSiblings.update(siblings)
    #rufe hier descendant or self auf allen elementen aus retrunSet auf
    returnSet = set()
    # returnSet.update(await descendantOrSelf(client, connected, tempSiblings, offlineList))
    for i in tempSiblings:
        returnSet.update(await descendantOrSelf(client, connected, [i], offlineList, returnSet))
    return returnSet

async def precedingSibling(client, connected, nodeList, offlineList):
    return await siblingInit(client, connected, nodeList, offlineList, True)

async def followingSibling(client, connected, nodeList, offlineList):
    return await siblingInit(client, connected, nodeList, offlineList, False)

async def siblingInit(client, connected, nodeList, offlineList, preced):
    returnSet = set()
    for node in nodeList:
        siblings = await getSiblings(client, connected, node, offlineList)       
        returnSet.update(await precfollowSib(siblings, node, preced))

    return returnSet

async def getSiblings(client, connected, nodeList, offlineList):
    siblings = []
    for parentA in await parent(client, connected, [nodeList], offlineList):
        for sibls in await child(client, connected, [parentA], offlineList):
            siblings.append(sibls)
    return siblings

async def precfollowSib(siblings, initalnodeList, precOrFoll):
    # if precOrFoll == True -> preceding. if False-> following
    returnSet = set()
    for sib in siblings:
        if(precOrFoll): # preceding, every left sibling of initial node
            if(sib<initalnodeList):
                returnSet.add(sib)
        else: # following, every right sibling of initial node
            if(initalnodeList<sib):
                returnSet.add(sib)
    return returnSet


async def parent(client, connected, nodeList, offlineList):
    return await getChildParent(client, connected, nodeList, False, offlineList)

async def child(client, connected, nodeList, offlineList):
    return await getChildParent(client, connected, nodeList, True, offlineList)

async def getChildParent(client, connected, nodeList, direction, offlineList):
    nodeIdSet = set()
    if not connected:
        for nodes in nodeList:
            for i in offlineList:
                if(i[0]==nodes): # i[0] = NodeId
                    if(direction): # direction == True if Forward, == False if Inverse
                        nodeIdSet.update(set(i[1])) # i[1] = children of i[0]  
                        break
                    else:
                        nodeIdSet.update(set(i[2]))  # i[2] = parents of i[0]    
                        break
    else:
        
        for nodes in nodeList: #get_references(direction=ua.BrowseDirection.Forward))
            for i in await client.get_node(nodes).get_references():
                if(i.IsForward == direction): # direction == True if Forward, == False if Inverse
                    if not str(i.ReferenceTypeId) == "i=40": # dont allow HasTypeDef references
                        nodeIdSet.add(str(i.NodeId))
                    
        intersecSet = set()
        for nodes in nodeList:
            for i in offlineList:
                if(i[0]==nodes): # i[0] = NodeId  
                    if(direction): # direction == True if Forward, == False if Inverse
                        intersecSet.update(set(i[1])) # i[1] = children of i[0]  
                        break
                    else:
                        intersecSet.update(set(i[2]))  # i[2] = parents of i[0]    
                        break

        nodeIdSet=nodeIdSet.intersection(intersecSet)

    return nodeIdSet   

async def descendant(client, connected, nodeList, offlineList):
    return await getDescendant(client, connected, nodeList, False, offlineList)

async def descendantOrSelf(client, connected, nodeList, offlineList, precfoll=set()):
    return await getDescendant(client, connected, nodeList, True, offlineList, precfoll)

async def ancestor(client, connected, nodeList, offlineList, rootnode):
    return await getAncestor(client, connected, nodeList, False, offlineList, rootnode)

async def ancestorOrSelf(client, connected, nodeList, offlineList, rootnode):
    return await getAncestor(client, connected, nodeList, True, offlineList, rootnode)


async def getDescendant(client, connected, nodeList, orSelf, offlineList, precfoll=set()):
    returnSet = set() # returned set
    checkSet = set() # nodeIds to check
    ancNodes = set() # ancestor nodes
    ancNodes.update(set(await ancestor(client,False,nodeList, offlineList,"i=84")))
    checkSet.update(nodeList) # initialize checkSet with nodeList


    if(len(precfoll)>0):
        returnSet.update(precfoll)

    # repeat until checkSet == 0
    while (len(checkSet) > 0): 
        # extract all children of each node in checkSet
        checkSet.update(await child(client, connected, checkSet, offlineList)) 
        # if flag==True, delete self node in the first cycle
        if(not orSelf): 
            for i in nodeList:
                checkSet.remove(i)
            orSelf = True
        # checkSet = all elements in checkSet without the elements in ancNodes
        checkSet = checkSet.difference(ancNodes)
        # a = all elemente of checkset without the elements in the interstection of checkSet and returnSet
        # x1 ^ x2 returns the set of all elements which are not in the intersection of x1 and x2 (symmetric difference)
        a = checkSet^(returnSet.intersection(checkSet)) 
        returnSet.update(checkSet)
        checkSet = a

    return returnSet


    
async def getAncestor(client, connected, start, orSelf, offlineList, rootnode):
    # start is a list of nodes
    # endnode is always the rootnode
    # This method calculates all valid paths from the startnode
    # to the rootnode and returns a set with all traversed nodes
    pathnodes = set()
    for nodes in start:
        nodes=str(nodes)
        pathList = [[nodes]]
        while len(pathList)>0:
            path = pathList.pop(0)
            #print(path)
            #vertex = path[len(path)-1]
            vertex = path[-1]
            if vertex == rootnode:
                pathnodes.update(path)
            for parentA in (await parent(client, connected, [vertex], offlineList)):
                parentA = str(parentA)
                if parentA not in path:
                    pathList.append(path + [parentA])
        if(not orSelf):
            if pathnodes:
                pathnodes.remove(nodes)
    return pathnodes

async def getAttributes(client, connected, nodeList, attrList):
    nodeAttributes = []
    if connected:
        for node in nodeList:
            # NodeId=1, NodeClass=2, DisplayName=4, BrowseName=3, Description=5, Value=13, DataType=14, UnitURI=100, UnitID=101, UnitRangeMin=102, UnitRangeMax=103
            attrs = await client.get_node(node).read_attributes(attrList)
            tempAttrs = []
            for i in attrList:
                try:
                    #NodeClass
                    if i==2: 
                        attribute = attrs[attrList.index(i)]
                        tempAttrs.append(attribute.Value.Value.name)
                    #NodeId
                    if i==1:
                        attribute = attrs[attrList.index(i)]
                        tempAttrs.append(str(attribute.Value.Value))
                    #DisplayName
                    if i==4:
                        attribute = attrs[attrList.index(i)]
                        tempAttrs.append(attribute.Value.Value.Text)
                    #BrowseName
                    if i==3:
                        attribute = attrs[attrList.index(i)]
                        tempAttrs.append(attribute.Value.Value.Name)
                    #Description
                    if i==5:
                        attribute = attrs[attrList.index(i)]
                        tempAttrs.append(attribute.Value.Value.Text)
                    #Value
                    if i==13:
                        attribute = attrs[attrList.index(i)]
                        val = attribute.Value.Value
                        if type(val) == int or type(val) == bool or type(val) == float or type(val) == str:
                            tempAttrs.append(val)
                        else:
                            tempAttrs.append("None")
                    #DataType
                    if i==14:
                        attribute = attrs[attrList.index(i)]
                        dataType = attribute.Value.Value # NodeId of DataType
                        # DataType String
                        dataTypeString = (await client.get_node(dataType).read_attributes([4]))[0].Value.Value.Text 
                        tempAttrs.append(dataTypeString)
                    
                except:
                    tempAttrs.append("None")
                try:
                    # UnitURI
                    if i==100:
                        if ((await client.get_node(node).read_attributes([14]))[0]).Value.Value.Identifier == 887:
                            tempAttrs.append(((await client.get_node(node).read_attributes([13]))[0]).Value.Value.NamespaceUri)
                        else: tempAttrs.append("None")
                except:
                    tempAttrs.append("None")
                try:
                    # UnitID
                    if i==101:
                        if ((await client.get_node(node).read_attributes([14]))[0]).Value.Value.Identifier == 887:
                            tempAttrs.append(((await client.get_node(node).read_attributes([13]))[0]).Value.Value.UnitId)
                        else: tempAttrs.append("None")
                except:
                    tempAttrs.append("None")
                try:
                    # UnitRangeMin, UnitRangeMax
                    if i==102 or i==103:
                        if ((await client.get_node(node).read_attributes([14]))[0]).Value.Value.Identifier == 884:
                            vals = ((await client.get_node(node).read_attributes([13]))[0])
                            if i==102: tempAttrs.append(vals.Value.Value.Low)
                            else: tempAttrs.append(vals.Value.Value.High)
                        else:
                            tempAttrs.append("None")
                except:
                    tempAttrs.append("None")

            nodeAttributes.append(tempAttrs)
    else:
        # NodeId=1, NodeClass=2, DisplayName=4, BrowseName=3, Description=5, Value=13, DataType=14, UnitURI=100, UnitID=101, UnitRangeMin=102, UnitRangeMax=103
        attrOfNodeList = []
        export = await xmlexport(1)
        for node in nodeList:
            for nodeAttrs in export:
                if node==nodeAttrs[0]:
                    attrOfNodeList.append(nodeAttrs)
                    break
        for node in attrOfNodeList:
            tempAttrs = []
            for AtrNumber in attrList:
                if AtrNumber==1: tempAttrs.append(node[0])# NodeId
                elif AtrNumber==2: tempAttrs.append(node[1])# NodeClass
                elif AtrNumber==4: tempAttrs.append(node[2])# DisplayName
                elif AtrNumber==3: tempAttrs.append(node[3])# BrowseName
                elif AtrNumber==5: tempAttrs.append(node[4])# Description
                elif AtrNumber==13: tempAttrs.append(node[5])# Value
                elif AtrNumber==14: tempAttrs.append(node[6])# DataType
                elif AtrNumber==100: tempAttrs.append(node[7])# UnitURI
                elif AtrNumber==101: tempAttrs.append(node[8])# UnitID
                elif AtrNumber==102: tempAttrs.append(node[9])# UnitRangeMin
                elif AtrNumber==103: tempAttrs.append(node[10])# UnitRangeMax
            nodeAttributes.append(tempAttrs)
    return nodeAttributes



async def main():

    url = "opc.tcp://.....:53530/OPCUA/SimulationServer" # add Server url here

    offlineList = await createOfflineList("i=84")

    async with Client(url=url,timeout=10) as client:

        # some examples:
        print(await(child(client,True,["i=84"],offlineList)))
        print(await(parent(client,True,["i=85"],offlineList)))

        print(await(ancestor(client,True,["i=112"],offlineList,"i=84")))
        print(await(descendant(client,True,["i=85"],offlineList)))


        print(await(preceding(client,True,["i=86"],offlineList)))
        print(await(following(client,True,["i=86"],offlineList)))

        
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    asyncio.run(main())
