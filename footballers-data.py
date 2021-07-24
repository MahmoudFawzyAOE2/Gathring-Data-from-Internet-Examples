from bs4 import BeautifulSoup
import os
import requests
import pandas as pd

# We'll check first if the file is already downloaded or not
# In both cases the first 10 lines will be displayed
filename = 'ballers.csv'
for dirpath, dirnames, filenames in os.walk(os.getcwd()): #to display the files within the directory
    print('\nCurrent path: ',dirpath)
    print('Directories within the path: ',dirnames)
    print('Fileswithin the path:',filenames)

    # if the file is already downloaded (available in the directory), we'll read it directly
    if filename in filenames :
        print('\nthe file is downloaded \n')
        df = pd.read_csv(filename)
        break

    # # if the file is not downloaded (not available in the directory), we'll download it
    print ('\nthe file is not downloaded \nDownloading {} ....'.format(filename))

    df_list = []  #an empty list to collect the data in it,  then we'll transform it to DataFrame

    for player_num in range(1,101):
        #we want to get the data of the first 100 players, so we'll loop on their 100 web pages
        print(player_num)

        #to get the tags soup from the web page
        site = 'https://www.futhead.com/21/players/{}'.format(player_num)   #the site differs with the player number in this formula
        response = requests.get(site)                                       # the file on the internet in the given URL is now in the variable response
        soup = BeautifulSoup(response.content, 'lxml')                      # to transform the responce into an soup of tags

        # getting the data from the tags soup
        name=soup.find('div', class_="playercard-name").contents[0].strip()
        rating=soup.find('div', class_="playercard-rating").contents[0].strip()
        position=soup.find('div', class_="playercard-position").contents[0].strip()
        club=soup.find('div', class_="tab-group margin-t-20 padding-t-6").find_all('a', class_="futhead-link")[0].contents[0]
        league=soup.find('div', class_="tab-group margin-t-20 padding-t-6").find_all('a', class_="futhead-link")[1].contents[0]
        nation=soup.find('div', class_="tab-group margin-t-20 padding-t-6").find_all('a', class_="futhead-link")[2].contents[0]

        # fixing wrong data
        if club == 'Piemonte Calcio' : club = 'Juventus FC'
        if club == 'Generic Capitale' : club = 'AS Roma'

        # append the players's data dictionary to the list
        df_list.append({'Name': name,'Overall Rating': rating,'Position': position,'Nation': nation,'Club': club,'League': league})

    # after getting all data we'll transform list of dictionaries to a data DataFrame
    df = pd.DataFrame(df_list, columns = ['Name', 'Overall Rating','Position','Nation','Club','League'])

    #saving into .csv file
    df.to_csv('ballers.csv', index=False) #this will save the dataframe into a csv file

#sorting
df = df.set_index('Name').sort_values(by=['Overall Rating'], ascending=False)

print(df.head(10))
