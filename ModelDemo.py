country = input("Enter the country whose risk situation you want to look at: ")

print(f"""Here is the risk report for {country}

    Political risk: 
    Economic risk: 2.472
      
    The reason for the risk are the follwoing events:
        1. Houthi Red Sea attacks - Increases economic and political risk by 3 points
        2. Construction of new capital city - Reduces economic risk by 2 points
        3. Political election in 2024 - Increases political risk by 3 points
        4. Explosion at Indonesia nickel plant - Increases economic risk by 2 points
      
    The following are the bilaterial tensions that {country} faces:
        1. Israel - 5
        2. China - 2.443
        3. The United States - 1.982
        4. Malaysia - 1.636

Overall Indonesia is in a stable position in global geopolitics.

""")

next_step = input("""For an elaboration of the risks, choose one of the options:
                  
    Domestic risk: Enter D followed by the id of the risk in the list
    Bilateral risk: Enter B followed by the id of the risk in the list
                  
                  """)

print("""Here are sources of conflict between Israel and Indonesia:
      1. Indonesia's support of Palestine - https://thediplomat.com/2023/10/the-growing-significance-of-malaysia-and-indonesias-non-recognition-of-israel/
      2. Anti-Israel sentiment - https://edition.cnn.com/2023/03/30/football/fifa-removes-indonesia-hosts-u20-world-cup-intl-hnk-spt/index.html

This leads to the risk score of 5 between the countries.
      
      """)