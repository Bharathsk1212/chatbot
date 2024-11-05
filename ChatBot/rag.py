from document_retrieval import retrieve_documents
from openai_response_generation import generate_response


def retrieve_and_generate_response(user_input):
    # Step 1: Retrieve related documents or FAQs based on user input
    retrieved_docs = retrieve_documents(user_input)

    # Step 2: If relevant documents are found, use them to generate a response
    if retrieved_docs:
        # Combine document content for response generation
        context = "\n".join([doc['text'] for doc in retrieved_docs])

        # Generate a response based on retrieved documents
        generated_response = generate_response(user_input, context)
        return generated_response

    # Fall back if no documents were retrieved or generated response
    return None
