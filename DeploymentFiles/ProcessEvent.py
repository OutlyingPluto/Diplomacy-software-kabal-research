from ModelInit import InitModel, NamedCountries

countries, BilateralInfo = InitModel()

def EventProcess(id, country, subclass, score, propagate, TwoLevel):

    """"
    ID gives the ID of the event in the event database
    Country is the country where the event took place
    Subclass is the subclass of the event (in the code)
    Score is the change in the risk score due to that event
    propagate indicates whether the conseuqneces of the events need to be propagated (boolean)
    TwoLevel indicates whether multiple propagations are required (boolean)
    """
    CountryID = NamedCountries.index(country)
    NodeAffected = countries[CountryID].FindNode(subclass)

    countries[CountryID].nodes[NodeAffected].update(score)
    countries[CountryID].nodes[NodeAffected].events.append(id)

    # The next step is to propagate the change to the surroudning nodes

    if propagate:
        countries[CountryID].propagate(NodeAffected)

    # Add the second level propagation here

    if TwoLevel: 
        pass
