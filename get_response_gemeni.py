def AskGemeni(in_str):
    # Imports
    try:
        import chromadb
    except Exception as e:
        import traceback
        traceback.print_exc()
    import chromadb.utils.embedding_functions as embedding_functions
    from google import genai
    # import google.generativeai as genai
    # Create a Chromdb to store embeddings
    chroma_client = chromadb.PersistentClient(path = "database")
    # chroma_client_autosar_theory = chromadb.PersistentClient(path = "Database_B")
    # Create a collection with Google Gemeni API for embedding
    google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key="AIzaSyCymU7yIntvND2XceqMMJl1ysu0SM51k00", task_type="RETRIEVAL_QUERY")
    collection = chroma_client.get_or_create_collection(name="GoogleCollection", embedding_function=google_ef)
    collection_autosarTheory = chroma_client.get_or_create_collection(name="autosar_book", embedding_function=google_ef)
    # Ask the user for question
    # in_str = input("What do you want to know about AUTOSAR ? \n")
    results = collection.query(query_texts=[in_str], n_results=30)
    results2 = collection_autosarTheory.query(query_texts=[in_str], n_results=30)
    # print(results["documents"])
    system_prompt = """
    You are a helpful assistant. You answer questions related to AUTOSAR which is a software achitecture for automotive domain. 
    But you should only answer based on knowledge I'm providing you. You can pull in information that you already know about the question only if
    you cannot find relavent info in the data below. Always prioratise getting data form what is provided below. Incase if you are basing your aswer outside of the info
    provided then please add a note to indicate the same below the answer
    If you don't know the answer even after that please just type: I don't know. Do not try to guess. This information needs to be as accurate as possible
    The data provided below is in 2 parts. Theory and Technical documentation. Choose appropritate data according to what question is asked
    --------------------
    Theory:
    """+str(results2['documents'])+"""
    --------------------
    technical documentation:
    """+str(results['documents'])+"""
    """
    client = genai.Client(api_key="AIzaSyCymU7yIntvND2XceqMMJl1ysu0SM51k00")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=system_prompt + "\n\nQuestion: " + in_str
    )
    # print(response.text)

    return response.text


def AskRequirements(in_str):
    # Imports
    try:
        import chromadb
    except Exception as e:
        import traceback
        traceback.print_exc()
    import chromadb.utils.embedding_functions as embedding_functions
    from google import genai
    # import google.generativeai as genai
    # Create a Chromdb to store embeddings
    chroma_client = chromadb.PersistentClient(path = "database")
    # chroma_client_autosar_theory = chromadb.PersistentClient(path = "Database_B")
    # Create a collection with Google Gemeni API for embedding
    google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key="AIzaSyCymU7yIntvND2XceqMMJl1ysu0SM51k00", task_type="RETRIEVAL_QUERY")
    collection = chroma_client.get_or_create_collection(name="su17_requirements", embedding_function=google_ef)
    # Ask the user for question
    # in_str = input("What do you want to know about AUTOSAR ? \n")
    results = collection.query(query_texts=[in_str], n_results=30)
    # print(results["documents"])
    system_prompt = """
    You are a helpful assistant. You answer questions related to requirements of a embedded C project that I share. 
    Since this is a project specific requirement, you wont use your internal knowlage to answer anything. Everything should be based on the 
    information that is shared to you below after work Requirements. If the information is not there in below text then you just simply reply
    "I can't find appropriate information related to your query in SU17 requirements".

    Requirements:
    """+str(results['documents'])+"""
    """
    client = genai.Client(api_key="AIzaSyCymU7yIntvND2XceqMMJl1ysu0SM51k00")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=system_prompt + "\n\nQuestion: " + in_str
    )
    # print(response.text)

    return response.text
