import random

import requests
import json


def getQuestionContent(titleSlug="two-sum"):
    query = """
    query getQuestionContent($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            content
        }
    }
    """

    url = "https://leetcode.com/graphql"
    payload = {
        "query": query,
        "variables": {"titleSlug": titleSlug},
        "operationName": "getQuestionContent"
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data['data']['question']['content']
    else:
        print(f"Error: {response.status_code}")
        return None


def getQuestionCode(titleSlug="two-sum"):
    query = """
    query questionEditorData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            codeSnippets {
                lang
                code
                langSlug
            }
        }
    }
    """

    url = "https://leetcode.com/graphql"
    payload = {
        "query": query,
        "variables": {"titleSlug": titleSlug},
        "operationName": "questionEditorData"
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        for code in data['data']['question']['codeSnippets']:
            if code['lang'] == "Python3":
                return code['code']
    else:
        print(f"Error: {response.status_code}")
        return None

def getQuestions(player_amount=1):
    # Define the GraphQL query
    query = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
      problemsetQuestionList: questionList(
        categorySlug: $categorySlug
        limit: $limit
        skip: $skip
        filters: $filters
      ) {
        total: totalNum
        questions: data {
          frontendQuestionId: questionFrontendId
          paidOnly: isPaidOnly
          titleSlug
        }
      }
    }
    """

    # Define the variables for the GraphQL query
    variables = {
        "categorySlug": "algorithms",
        "skip": 0,
        "limit": 1000,
        "filters": {"difficulty": "EASY"}
    }

    # Define the endpoint URL for the GraphQL API
    url = "https://leetcode.com/graphql"

    # Prepare the payload to send in the POST request
    payload = {
        "query": query,
        "variables": variables,
        "operationName": "problemsetQuestionList"
    }

    # Send the POST request
    response = requests.post(url, json=payload)
    questions = []

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        while len(questions) < player_amount:
            x = random.randint(0, int(data['data']['problemsetQuestionList']["total"]))
            if data['data']['problemsetQuestionList']["questions"][x]["paidOnly"]:
                continue
            question = getQuestionContent(data['data']['problemsetQuestionList']["questions"][x]["titleSlug"])
            code = getQuestionCode(data['data']['problemsetQuestionList']["questions"][x]["titleSlug"])
            questions.append((question, code))
    else:
        print(f"Error: {response.status_code}")

    return questions


getQuestions()
