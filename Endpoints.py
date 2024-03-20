import backoff
import requests
import re
from bs4 import BeautifulSoup as bs

class ForbiddenError(Exception):
    pass

@backoff.on_exception(backoff.expo, ForbiddenError, max_tries=20)
def returnQuery(username, name, regno, year, dept, section, domain, mail, phone):
    url = 'https://leetcode.com/graphql'


    headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'cookies' : 'asdfads',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

    }
    
    query = '''
        query combinedQueries($username: String!) {
            matchedUser(username: $username) {
                submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
            }
            userContestRanking(username: $username) {
                attendedContestsCount
                rating
                globalRanking
                totalParticipants
                topPercentage
                badge {
                    name
                }
            }
        }
    '''

    variables = {
        "username": f"{username}"
    }

    payload = {
        'query': query,
        'variables': variables
    }

    response = requests.post(url, json=payload, headers=headers)


    if response.status_code == 200:
        json_dict = response.json()

        if not json_dict:
            return None

        matchedUser = json_dict['data']['matchedUser']

        contestCount,rating,globalRank,topPercent = 0,0,0,0
        easy, medium, hard, total = 0, 0, 0, 0

        if  matchedUser:
            problems_solved = matchedUser['submitStatsGlobal']['acSubmissionNum']

            for pair in problems_solved:
                if pair['difficulty'] == 'All':
                    total = pair['count']
                elif pair['difficulty'] == 'Easy':
                    easy = pair['count']
                elif pair['difficulty'] == 'Medium':
                    medium = pair['count']
                elif pair['difficulty'] == 'Hard':
                    hard = pair['count']

            score = easy + medium * 2 + hard * 3

        else:
            return {'Name' : name, 'Reg Number' : regno, 'Year' : year, 'Department' : dept, 'Section' : section, 'Domain' : domain, 'Username' : username, 'Mail ID' : mail, 'Mobile Number' : phone}, False


        contest = json_dict['data']['userContestRanking']

        if  contest:

            for key, value in contest.items():
                if key == 'attendedContestsCount':
                    contestCount = value
                elif key == 'rating':
                    rating = value
                elif key == 'globalRanking':
                    globalRank = value
                elif key == 'topPercentage':
                    topPercent = value

        return {'Name' : name, 'Reg Number' : regno, 'Year' : year, 'Department' : dept, 'Section' : section, 'Domain' : domain, 'Username' : username,'Easy' : easy, 'Medium' : medium, 'Hard' : hard, 'Total' : total, 'Score' : score,'Total Contests Count' : contestCount, 'Contest Rating' : rating, 'Global Rank' : globalRank, 'Top%' : topPercent, 'Mail ID' : mail, 'Mobile Number' : phone}, True

    
    elif response == 404:
       
        return {'Name' : name, 'Reg Number' : regno, 'Year' : year, 'Department' : dept, 'Section' : section, 'Domain' : domain, 'Username' : username, 'Mail ID' : mail, 'Mobile Number' : phone}, False
        
    else :
        print(username)

        raise ForbiddenError("Received a 403 Forbidden response")