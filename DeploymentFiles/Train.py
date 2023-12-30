from ModelInit import InitModel, NamedCountries

# To achieve training of weights in this directory, ensure the terminal is running from DeploymentFiles

countries, BilateralInfo = InitModel()

# Remember that while training, the events that took place in the past need to be stored as well; they should be able to be retrieved separately

# Here, weights and events files need to be modified