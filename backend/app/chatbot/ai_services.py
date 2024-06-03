from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import json
from flask import current_app
from .db_services import get_all_query_logs
from .map_services import *

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

embedder = OpenAIEmbeddings(
    api_key=OPENAI_API_KEY, model="text-embedding-3-large")

llm = OpenAI(model_name="gpt-3.5-turbo-instruct",
             openai_api_key=OPENAI_API_KEY)


def find_similar_queries(query, k=5):
    # Prepare embeddings of all queries
    query_logs = get_all_query_logs()
    texts = [query_log['query'] for query_log in query_logs]
    query_db = FAISS.from_texts(texts, embedder)
    retriever = query_db.as_retriever()

    # Search for query
    result_docs = retriever.invoke(query=query,
                                   search_type="similarity_score_threshold",
                                   search_kwargs={"score_threshold": 0.7,
                                                  "k": k}
                                   )

    return [doc.page_content for doc in result_docs]


def classify_query(query):
    prompt = f"""
    Please analyze the following user query, classify it into one of three categories: 'place_details', 'local_services', or 'general'. Extract relevant details based on the category and return the information in the following JSON structure:
    - For 'place_details': {{ "query_type": "place_details", "details": {{ "place_name": "<name of the place>" }} }}
    - For 'local_services': {{ "query_type": "local_services", "details": {{ "service_type": "<type of service (one of restaurant, park, parking, or hospital)>", "place_name": "CURRENT_LOCATION" if referring to the user's current location, otherwise the specific place name. }} }}
    - For general inquiries (any other inquiries that do not fall into the above categories): {{ "query_type": "general", "details": {{ }} }}
    Based on this user input: '{query}'
    """
    response = llm(prompt)
    current_app.logger.info(f'classify result: {response}')
    return response


def get_query_response(query, context, lat, lng):
    # Classify the query first
    type_details_json = classify_query(query)
    type_details = json.loads(type_details_json)

    # Format the prompt
    if type_details['query_type'] == "place_details":
        place_name = type_details['details']['place_name']
        place_details = fetch_place_details(place_name)
        prompt = PromptTemplate.from_template(
            "You are an AI designed to provide detailed information about places." +
            "User asks: '{query}'." +
            "Additionally, here's the context of this conversation: '{context}'." +
            "Additionally, here's the extra information: {details}." +
            "Please provide detailed information about {place_name} based on the provide information.",
        )
        completed_prompt = prompt.format(
            query=query, context=context, details=place_details, place_name=place_name)
    elif type_details['query_type'] == 'local_services':
        service_type = type_details["details"]["service_type"]
        place_name = type_details["details"]["place_name"]
        if place_name == "CURRENT_LOCATION":
            place_location = f"{lat},{lng}"
        else:
            location = geocode(place_name)
            if location:
                place_location = f"{location[0]},{location[1]}"
            else:
                # That's where the legendary rickroll MV was shot
                place_location = f"51.512608,-0.219139"
        vicinity_details = fetch_vicinity_details(place_location, service_type)
        prompt = PromptTemplate.from_template(
            "You are an AI specialized in providing information about local services." +
            "User asks: '{query}'." +
            "Additionally, here's the context of this conversation: '{context}'." +
            "Additionally, here's the extra information: {details}." +
            "Please provide information about nearby {service_type} services based on the provided context."
        )
        completed_prompt = prompt.format(query=query, context=context,
                                         details=vicinity_details, service_type=service_type)
    else:
        prompt = PromptTemplate.from_template(
            "You are an AI equipped to handle a wide range of queries." +
            "User asks: '{query}'." +
            "Additionally, here's the context of this conversation: '{context}'." +
            "Give a good and proper response based on the provided context."
        )
        completed_prompt = prompt.format(query=query, context=context)

    response = llm(completed_prompt)
    return response
