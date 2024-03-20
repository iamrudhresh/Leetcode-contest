import streamlit as st
import time
import requests
import backoff
import json
import pandas as pd
class ForbiddenError(Exception):
    pass

@backoff.on_exception(backoff.expo, ForbiddenError, max_tries=20)
def fetch(contestName,pageNumber):

    headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'cookies' : 'asdweaea',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    
    url = f"https://leetcode.com/contest/api/ranking/{contestName}/?pagination={pageNumber}&region=global"
    response = requests.get(url , headers=headers)

    if response.status_code == 200:
        return response
    elif response.status_code == 403:
        print('error raised')
        raise ForbiddenError('forbidden')
    else :
        return response

st.title("Contest Fetcher")
with open("./data/weekly-contest-388 final contest.json", "r") as json_file:
    completeData = json.load(json_file)

st.write('Fetch entire data from a contest')
contestName = st.text_input("Enter the name of the contest:")
successful = 1

if st.button('fetch h') == 1:
    
    # pageNumber = 1
    # completeData = {}


    # while(True):
        
    #     response = fetch(contestName,pageNumber)

    #     if response.status_code == 200:
    #         json_data = response.json()

    #         if len(json_data) == 0:
    #             st.error("Contest Doesn't exist")
    #             break
            
    #         submissions = json_data['submissions']
    #         total = json_data['total_rank']

    #         # if(len(submissions) == 0):
    #         #     break

    #         if(len(submissions) == 0):
    #             break

    #         for i in range(len(submissions)):
                
    #             userName = total[i]['username'].lower()
    #             rank = total[i]['rank']+1
    #             score = total[i]['score']
    #             problemsSolved = len(submissions[i])

    #             completeData[userName] = {'rank':rank,"score":score, "problemsSolved" : problemsSolved}
            
    #         print(pageNumber)
    #         pageNumber += 1
    #     elif response.status_code == 404:
    #         st.error('Contest not found')
    #         successful = 0
    #         break
    #     else:

    #         print('There might be an error . Try again after some time')
            

        

    # print(len(completeData))

    # json_string = json.dumps(completeData, indent=4)  

    # file_path = f"{contestName} final contest.json"

    # if successful == 1:
    #     with open(file_path, "w") as json_file:
    #         json_file.write(json_string)

    #     print(f"JSON data has been saved to {file_path}")
    #     st.success("Data fetched Successfully")
    #     successful = 2

    # if successful == 1:
        
        


    file = pd.read_csv('.\data\All Year.csv')
    filtered_data = file.copy()

    departments = ["All"] + list(file['Department'].unique())
    sections = ["All"] + list(file['Section'].unique())
    years = ["All"] + list(file['Year'].unique())
    domains = ["All"] + list(file['Domain'].unique())

    year = st.selectbox('Year', years, index=0)
    department = st.selectbox('Department', departments, index=0)
    domain = st.selectbox('Domain', domains, index=0)
    section = st.selectbox('Section' , sections, index=0)


    if year:
        if year != 'All':
            filtered_data = filtered_data[filtered_data['Year'] == year]

    if department:
        if department != 'All':
            filtered_data = filtered_data[filtered_data['Department'] == department]
        
    if section:
        if section != 'All':
            filtered_data = filtered_data[filtered_data['Section'] == section]
                    
    if domain:
        if domain != 'All':
            filtered_data = filtered_data[filtered_data['Domain'] == domain]

   
    if st.button('fetch'):
        
        csv = filtered_data.copy()

        csv['Rank'] = ''
        csv['ProbCount'] = ''
        csv['Score'] = ''
        
        st.write(csv)
      
        for ind , row in csv.iterrows():
            username = row['Username'].lower()

            if username in completeData:
                csv.loc[ind,'Rank'] = completeData[username]['rank']
                csv.loc[ind,'ProbCount'] = completeData[username]['problemsSolved']
                csv.loc[ind,'Score'] = completeData[username]['score']
            else:
                csv.loc[ind,'Rank'] = 0
                csv.loc[ind,'ProbCount'] = 0
                csv.loc[ind,'Score'] = 0

            

        
    
