from ModelInit import InitModel, NamedCountries, GetBilateral

countries, BilateralInfo = InitModel()

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