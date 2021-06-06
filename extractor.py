import asyncio
import logging
import time
from asyncua import Client, ua


async def getChildParent(clienta, nodea, nsarr):
    children = []
    parent = []
    nodeAttrs = []

    # NodeClass=2, NodeId=1, DisplayName=4, BrowseName=3, Description=5, Value=13, DataType=14
    attrs = await clienta.get_node(nodea).read_attributes([2,1,4,3,5,13,14])
    for i in attrs:
        try:
            #NodeClass
            if attrs.index(i)==0: 
                nodeAttrs.append(i.Value.Value.name)
            #NodeId
            if attrs.index(i)==1: 
                nodeAttrs.append(str(i.Value.Value))
            #DisplayName
            if attrs.index(i)==2: 
                nodeAttrs.append(i.Value.Value.Text)
            #BrowseName
            if attrs.index(i)==3: 
                nodeAttrs.append(i.Value.Value.Name)
            #Description
            if attrs.index(i)==4: 
                nodeAttrs.append(i.Value.Value.Text)
            #Value
            if attrs.index(i)==5: 
                val = i.Value.Value
                if type(val) == int or type(val) == bool or type(val) == float or type(val) == str:
                    nodeAttrs.append(val)
                else:
                    nodeAttrs.append("None")
            #DataType
            if attrs.index(i)==6:
                dataType = i.Value.Value # NodeId of DataType
                # DataType String
                dataTypeString = (await clienta.get_node(dataType).read_attributes([4]))[0].Value.Value.Text 
                nodeAttrs.append(dataTypeString)

        except:
            nodeAttrs.append("None")
    # add UnitURI, UnitID, UnitRangeMin, UnitRangeMax
    try:
        # check if Identifier(attrs[6]) of Datatype == EUInformation(id=887) and append NamespaceURI        
        if (attrs[6]).Value.Value.Identifier == 887:
            nodeAttrs.append((attrs[5]).Value.Value.NamespaceUri)
            nodeAttrs.append((attrs[5]).Value.Value.UnitId)
        else:
            for i in range(2):
                nodeAttrs.append("None")
    except:
        for i in range(2):
                nodeAttrs.append("None")
    try:            
        # check if Identifier(attrs[6]) of Datatype == Range(id=884) and append Low Value
        if (attrs[6]).Value.Value.Identifier == 884:
            nodeAttrs.append((attrs[5]).Value.Value.Low)
            nodeAttrs.append((attrs[5]).Value.Value.High)
        else:
            for i in range(2):
                nodeAttrs.append("None")
    except:
        for i in range(2):
                nodeAttrs.append("None")

    # NodeClass, NodeId, ReferenceTypeId, TypeDefinition, DisplayName, BrowseName
    for i in await clienta.get_node(nodea).get_references():
        nodeidy = str(i.NodeId)
        try:
            reftypeid = str(i.ReferenceTypeId)
            typedef = str(i.TypeDefinition)
        except:
            reftypeid = "None"
            typedef = "None"

        if(i.IsForward == True):
            children.append([nodeidy,reftypeid,typedef])
        else:
            parent.append([nodeidy,reftypeid,typedef])
    export = [nodeAttrs,children,parent]
    return export

async def getDescendant(clienta, nodea, path):
    time1total = time.perf_counter()

    nsarr = await clienta.get_namespace_array()
    returnSet = set() # this set is returned
    checkSet = set() # NodeIds to check
    checkSet.update(nodea) # initialize checkSet with nodea

    file_object = open(path, 'w')
    for namespace in nsarr:
        if not nsarr.index(namespace) == 0:
            file_object.write("$"+str(namespace))
        else:
            file_object.write(str(namespace))
    file_object.write("\n")
    inSet = set()
    counter = 0
    timerList = []
    while (len(checkSet) > 0): # repeat until checkSet == 0
        childrenOfNode = set()
        for currentNode in checkSet:
            time1 = time.perf_counter()
            children = await getChildParent(clienta, currentNode, nsarr)
            time2 = time.perf_counter()
            timerList.append(time2-time1)
            print("Pass through nodes: ",str(counter)," Time: ", str(time2 - time1) + " Seconds")
            counter += 1
            # get nodeid
            if len(children[1]):
                for i in children[1]:
                    childrenOfNode.add(i[0])
                    
            if not currentNode in inSet:
                # add all attributes to file
                first = True
                for attr in children[0]:
                    if not first:
                        file_object.write("$"+str(attr))
                    else:
                        file_object.write(str(attr))
                        first = False
                file_object.write("$$$")

                posCounter = 0
                for child in children[1]:
                    # add all children to file
                    for elem in range(len(child)):
                        if elem == 0:
                            file_object.write(str(child[elem]))
                        else:
                            file_object.write("$"+str(child[elem]))
                    posCounter += 1
                    if not posCounter == len(children[1]):
                        file_object.write("|||")
                file_object.write("$$$")
                posCounter = 0
                for parent in children[2]:
                    # add all parents to file
                    for elem in range(len(parent)):
                        if elem == 0:
                            file_object.write(str(parent[elem]))
                        else:
                            file_object.write("$"+str(parent[elem]))
                    posCounter += 1
                    if not posCounter == len(children[2]):
                        file_object.write("|||")

                file_object.write("\n")
            inSet.add(currentNode)
        checkSet.update(childrenOfNode)
        # a = all elements that are not in the intersection of checkSet and returnSet
        # x1 ^ x2 return the set of all elements in either x1 or x2, but not both
        a = checkSet^(returnSet.intersection(checkSet)) 
        returnSet.update(checkSet)
        checkSet = a

    for duration in timerList:
        formatted_duration = "{:.4f}".format(duration)
        file_object.write(str(formatted_duration+","))
    
    time2total = time.perf_counter()
    file_object.write(str("{:.4f}".format(time2total - time1total)))
    return returnSet


async def main():

    url = "opc.tcp://...:53530/OPCUA/SimulationServer/" # add server url here
    
    async with Client(url=url, timeout=30) as client:
        
        path = 'D:\\Downloads\\Files\\OpcExport.txt' # Insert the path of the export file here (where it should be saved)
        await getDescendant(client,["i=84"],path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    asyncio.run(main())