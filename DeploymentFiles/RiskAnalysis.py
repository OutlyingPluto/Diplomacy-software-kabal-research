from ModelInit import InitModel, NamedCountries, GetBilateral

countries, BilateralInfo = InitModel()


def BilateralRisk():
    country1 = input("Enter the country whose risk situation you want to look at:")

    CountryID1 = NamedCountries.index(country1)

    country2 = input("Enter the country with respect to which you want to look at the risk situation:")

    CountryID2 = NamedCountries.index(country2)

    bilateral = GetBilateral(CountryID1, CountryID2, countries, BilateralInfo)

    print(f"The following is the bilateral relations between {bilateral.countries[0]} and {bilateral.countries[1]}")

    print(f"""Political risk: {bilateral.political.value}
    Economic risk: {bilateral.economic.value}

    The reason for this risk are the following events:
    {bilateral.cause}
    """)

def CountryRisk():
    country = input("Enter the country whose risk situation you want to look at: ")

    CountryID = NamedCountries.index(country)

    RiskValues = countries[CountryID].nodes

    # Political
    PolScore = 0

    for i in range(4):
        PolScore += RiskValues[i].value

    PolScore = PolScore / 4

    # Economic
    EconScore = 0

    for i in range(4, 7):
        EconScore += RiskValues[i].value
    
    EconScore = EconScore / 4

    print(f"""Here is the risk report for {country} :
          
    Political risk: {PolScore}
    Economic risk: {EconScore}

    The reason for this risk are the following events:
    # This needs to be retrieved from the database; get all the entries for the country and sort them in order of their risk score
    
    The following are the bilaterial risk that {country} faces:
    # Next to do: Risks from all other countries need to be displayed as well
    """)

    