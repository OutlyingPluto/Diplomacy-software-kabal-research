import pickle
from pathlib import Path
from math import exp, log
import random

risk_threshold = 6

with open("countries.bin", "rb") as f:
    NamedCountries = pickle.load(f)

"""
Note: 
When the list NamedCountries is updated, all the weights and node values need to be refreshed. 
For this purpose, delete ALL the files in the Weights folder.
"""

# Define the classes

def classes(code):

    high = code[0]

    try:
        low = int(code[1])
    except IndexError:
        low = ""

    if high == "p":
        if low == "":
            return "Political"
        elif low == 1:
            return "War"
        elif low == 2:
            return "Dividedness"
        elif low == 3:
            return "Scandals"
        elif low == 4:
            return "Cultural diplomacy"
        else:
            return "Incorrect code"
    elif high == "e":
        if low == "":
            return "Economic"
        elif low == 1:
            return "Economic instability"
        elif low == 2:
            return "Government policy"
        elif low == 3:
            return "Economic Stagnation"
        else:
            return "Incorrect code"
    else:
        return "Incorrect code"
    
# Create a node: a class that has the behaviour of a node

class node:
    def __init__(self, country, subclass):
        self.country = country
        self.subclass = subclass

        self.value = 0 # No risk when initialised

        self.events = [] # Store the ids of events that have affected this node

        self.change = 0

        # print(f"Node for {self.country} initialised.")
    
    def update(self, score):
        self.change = score

        score += self.value

        def UpdateFunction(score):
            return - exp(-(score/5 - log(10))) + 10
        
        self.value = UpdateFunction(score)

# Create a class to store bilateral risks

class bilateral:
    def __init__(self, countries):
        self.cause = [] # Refer to an event ID

        self.countries = [] # Countries is a list of length 2 containing class instances of 2 countries; the country with the smaller ID is ahead

        for country in countries:
            self.countries.append(country.name)

        self.political = node(self.countries, classes("p"))
        self.economic = node(self.countries, classes("e"))

        print(f"The nodes {self.political.country} and {self.economic.country} have been initialised.")

        # Weight gives a link from the bilateral relations to the weights of the first country
        self.weights = [[0.5 for i in range(7)] for j in range(2)]

        self.loc = "Weights\\" + "".join(self.countries) + ".bin"
        self.path = Path(self.loc)

        if self.path.is_file():
            with open(self.loc, "rb") as f:
                self.weights = pickle.load(f)
        else:
            self.weights = {"domestic": [[0.5 for i in range(7)] for j in range(2)]}
            with open(self.loc, "wb") as f:
                pickle.dump(self.weights, f)

def GetBilateral(country1id, country2id, countries, BilateralInfo):
    # The input is the ids of two countries

    # The indices can be in any order (the check is below)

    if country2id < country1id:
        temp = country2id
        country2id = country1id
        country1id = temp

    a = [i for i in range(len(countries))]

    loopno = 0

    for i in range(len(a)):
        for j in range(len(a) - i - 1):
            if [a[i], a[j + i + 1]] == [country1id, country2id]:
                # print(f"The countries selected are {BilateralInfo[loopno].countries}, {BilateralInfo[loopno].political.country}, {BilateralInfo[loopno].economic.country}")
                return BilateralInfo[loopno]
            loopno += 1
            
    raise Exception("This combination of countries is invalid")
    
    # The output is the class instace of the bilateral relations between the countries in the list BilateralInfo

def Update(node, change, weight):
    update = change * weight

    # print(f"The update at {node.country} {node.subclass} is {update}.")

    if update > risk_threshold:
        print(f"There is a grave situation in {node.country} in the field of {node.subclass}. The risk increases by the risk score of {update}")
    
    node.update(update)

# Create a class for the different countries in the graph

class domestic:
    def __init__(self, name):
        self.name = name
        self.id = NamedCountries.index(name)
        self.nodes = []

        # Political
        for i in range(1, 5):
            self.nodes.append(node(self.name, classes("p" + str(i))))

        # Economic
        for i in range(1, 4):
            self.nodes.append(node(self.name, classes("e" + str(i))))

        self.loc = "Weights\\" + self.name + ".bin"
        self.path = Path(self.loc)

        if self.path.is_file():
            with open(self.loc, "rb") as f:
                self.weights = pickle.load(f)
        else:
            self.weights = {"domestic": [[random.random() for i in range(7)] for j in range(7)]}
            with open(self.loc, "wb") as f:
                pickle.dump(self.weights, f)

            print(f"The weights linking to {self.name} have been freshly initialised.")

    def AddLink(self, country):
        # Country is a class instance of the domestic class
        if self.name == country.name:
            return None

        self.weights[country.name] = [[random.random() for i in range(9)] for j in range(7)]
        
        # This function only creates weights in one direction
    
    def FindNode(self, code):
        if code[0] == "p":
            return int(code[1]) - 1
        elif code[0] == "e":
            return int(code[1]) + 4
        else:
            print("Invalid subclass code")
            return None
        
        # Thus function returns the node number in the pre-defined format

    def propagate(self, StartNode):
        # Only changes get propagrated, not actual values
        # Self.change has to be updated before this behaviour is called

        # Start node is the number of the node - an integer from 1 to 7

        # Domestic propagation
        for i in range(7):
            if i != StartNode:
                Update(self.nodes[i], self.nodes[StartNode].change, self.weights["domestic"][StartNode][i])
                
                if self.nodes[i].value > 8:
                    print(f"There is a grave situation in {self.name} in the field of {self.nodes[i].subclass} due to an event {self.nodes[StartNode].events[-1]}.")
        
        # International propagation
        for country in self.weights.keys():
            if country != "domestic":
                CountryID = NamedCountries.index(country) # ID of the international country

                for i in range(7):
                    Update(countries[CountryID].nodes[i], self.nodes[StartNode].change, self.weights[country][StartNode][i])
                
                rel = GetBilateral(CountryID, self.id, countries, BilateralInfo)
                i = 7
                Update(rel.political, self.nodes[StartNode].change, self.weights[country][StartNode][i])
                rel.cause.append(self.nodes[StartNode].events[-1])
                
                i = 8
                Update(rel.economic, self.nodes[StartNode].change, self.weights[country][StartNode][i])
                rel.cause.append(self.nodes[StartNode].events[-1])

                if ( rel.political.value + rel.economic.value ) / 2 > 8:
                    print(f"There is a grave situation in the relations between {self.name} and {country} due to the event id {self.nodes[StartNode].events[-1]}.")
                    print(rel.countries, ":", ( rel.political.value + rel.economic.value ) / 2 )

def ExtractNodes(countries, BilateralInfo):
    # This serves to get the value of all the nodes in the network so that they can be compared for the purpose of training

    NodeList = []

    for country in countries:
        NodeList += country.nodes

    NodeListIntl = []

    for relation in BilateralInfo:
        NodeListIntl += [relation.political, relation.economic]

    return NodeList, NodeListIntl

def ReloadNodes(NodeList, NodeListIntl, countries, BilateralInfo):
    # This takes in the list of nodes and then updates them in all the nodes
    
    for country in countries:
        country.nodes = NodeList[0:len(country.nodes)]

        del NodeList[0:len(country.nodes)]

    if NodeList == []:
        print("Successful reloading")
    else:
        raise Exception("Reload error")
    
    i = 0

    for relation in BilateralInfo:
        relation.political = NodeListIntl[i + 0]
        relation.economic = NodeListIntl[i + 1]
        i += 2

def ReadNodes(countries, BilateralInfo):
    # this function reads the values of all the nodes from memory into these two lists of classes

    loc = "Weights\\Nodes.bin"

    try:
        with open(loc, "rb") as f:
            nodes = pickle.load(f)

        ReloadNodes(nodes[0], nodes[1], countries, BilateralInfo)
    except FileNotFoundError:
        AllNodes = ExtractNodes(countries, BilateralInfo)

        with open(loc, "wb") as f:
            pickle.dump(AllNodes, f)

        print("Nodes freshly initialised in Nodes.bin")

def InitModel():
    countries = []

    for name in NamedCountries:
        countries.append(domestic(name))

    # Intialise bilateral relations

    BilateralInfo = []

    for i in range(len(countries)):
        for j in range(len(countries) - i - 1):
            BilateralInfo.append(bilateral([countries[i], countries[j + i + 1]]))

    # Initalise links

    for i in range(len(countries)):
        for j in range(len(countries)):
            if i != j:
                countries[i].AddLink(countries[j])

    ReadNodes(countries, BilateralInfo)

    return countries, BilateralInfo

