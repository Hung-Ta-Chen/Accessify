from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import json
from flask import current_app
from .db_services import get_all_query_logs, get_all_places
from .map_services import *
from .utils import format_document_text

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

embedder = OpenAIEmbeddings(
    api_key=OPENAI_API_KEY, model="text-embedding-3-large")

llm = OpenAI(model_name="gpt-3.5-turbo-instruct",
             openai_api_key=OPENAI_API_KEY, max_tokens=1000)


def initalize_faiss_index():
    '''Initialize FAISS index'''
    places = list(get_all_places())
    texts = [format_document_text(place) for place in places]
    place_faiss_index = FAISS.from_texts(texts, embedder)
    return place_faiss_index


def retrieve_similar_places(query, k=5):
    place_faiss_index = initalize_faiss_index()
    result_docs = place_faiss_index.similarity_search(query, k=k)
    result_texts = [result_doc.page_content for result_doc in result_docs]
    return result_texts


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
    Analyze the user query and classify it into one of the following categories based on the user's intent:
    - 'place_details': Return details about a specific place. 
    - 'recommendation': Provide suggestions tailored to the user's interests, including requests for places with specific features or attributes, regardless of their proximity.
    - 'local_services': Return information about services in vicinity. 
    - 'general': Handle any other types of inquiries.
    Determine the appropriate category and provide relevant details in JSON format as follows:
    - For 'place_details': {{ "query_type": "place_details", "details": {{ "place_name": "<name of the place>" }} }}
    - For 'local_services': {{ "query_type": "local_services", "details": {{ "service_type": "<type of service (one of restaurant, park, parking, or hospital)>", "place_name": "CURRENT_LOCATION" if referring to the user's current location, otherwise the specific place name. }} }}
    - For 'recommendation': {{ "query_type": "recommendation", "details": {{ "interest": "details about user's interest", "place_name": "CURRENT_LOCATION" if referring to the user's current location, otherwise "<specific location name>" }} }}
    - For 'general': {{ "query_type": "general", "details": {{ }} }}
    Based on the user input: '{query}'
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
        completed_prompt = get_place_details_prompt(
            type_details, query, context)
    elif type_details['query_type'] == 'recommendation':
        completed_prompt = get_recommendation_prompt(
            type_details, query, context, lat, lng)
    elif type_details['query_type'] == 'local_services':
        completed_prompt = get_local_services_prompt(
            type_details, query, context, lat, lng)
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


def get_place_details_prompt(type_details, query, context):
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
    return completed_prompt


def get_recommendation_prompt(type_details, query, context, lat, lng):
    interest = type_details['details']['interest']
    place_name = type_details['details'].get('place_name', '')

    # Load some data
    place_location = place_name_to_code(place_name, lat, lng)
    fetch_vicinity_details(place_location)

    # Query vectorstore
    query = f"{interest} near {place_name}"
    recommendations = retrieve_similar_places(
        query, 5)  # Assuming 5 recommendations
    prompt = PromptTemplate.from_template(
        "You are an AI designed to offer recommendations." +
        " User is interested in {interest} near {place_name}." +
        " Based on user preferences, here are some recommendations: {recommendations}." +
        " Additionally, here's the context of this conversation: '{context}'." +
        " Please provide recommendations to the users based on the provided context. (Don't list the formatted address)"
    )
    completed_prompt = prompt.format(
        interest=interest, place_name=place_name, recommendations=', '.join(recommendations), context=context)
    return completed_prompt


def get_local_services_prompt(type_details, query, context, lat, lng, k=5):
    service_type = type_details["details"].get("service_type", '')
    place_name = type_details["details"].get(
        "place_name", 'Pokémon GO Lab.')
    current_app.logger.info(f'Place name: {place_name}')
    place_location = place_name_to_code(place_name, lat, lng)
    vicinity_details = fetch_vicinity_details(place_location, service_type)[:k]
    prompt = PromptTemplate.from_template(
        "You are an AI specialized in providing information about local services." +
        "User asks: '{query}'." +
        "Additionally, here's the context of this conversation: '{context}'." +
        "Additionally, here's the extra information: {details}." +
        "Please provide information about top (not all) nearby {service_type} services based on the provided context.  (Don't list the formatted address)"
    )
    completed_prompt = prompt.format(query=query, context=context,
                                     details=vicinity_details, service_type=service_type)
    return completed_prompt
