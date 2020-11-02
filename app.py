""" Flask app to provide backend for the Search Engine Web Client """

from flask import Flask, request, jsonify, make_response, render_template
from flask_cors import CORS
import os
import pickle
from helper import (
    perform_lsh,
    LRUCache,
    process_query,
    find_similar_docs,
    get_data_for_docId,
)


# Initialize Flask app
app = Flask(
    __name__,
    static_url_path="",
    static_folder="search_client/static",
    template_folder="search_client/templates",
)
CORS(app)
app.config["DEBUG"] = True  # Change to False in Production
docs_buckets = None

# Initialize Cache
cache = LRUCache(100)


@app.route("/", methods=["GET"])
def home():
    """ Route to serve home page of the Web App """
    return render_template("index.html")


@app.route("/api/search-results", methods=["GET"])
def api_search():
    """
    API Route for querying the backend.

        * Params - query="<query_string>"
        * Return Format - [(speciesType, sequence)]

    Processes the query -> Looks in cache -> If results not found, Looks in Index -> Returns results
    """

    params = request.args
    query = params["query"]

    # Validate Request Parameters
    try:
        assert type(query) == str
    except AssertionError:
        response = make_response("Invalid Request Parameters", 400)
        return response

    # Search Query Results in cache
    cache_search = cache.get(query)
    if cache_search != -1:
        results = cache_search
    else:
        print("Processing Non Cache\n")
        query_buckets = process_query(query)
        results = find_similar_docs(query_buckets, docs_buckets)
        cache.put(query, results)
    print("Results", results)
    results_with_data = []
    for docId in results:
        specie_name, dna_seq = get_data_for_docId(docId)
        results_with_data.append((specie_name, dna_seq))

    # Convert the list of results to JSON format.
    return jsonify(results_with_data)


if __name__ == "__main__":

    try:
        # Raise Error if data set doesn't exist.
        if not os.path.isdir("./dataset"):
            raise Exception("Dataset not found")
        if not os.path.isfile("hash.pkl"):
            docs_buckets = perform_lsh()
            f = open("hash.pkl", "wb")
            pickle.dump(docs_buckets, f)
        else:
            f = open("hash.pkl", "rb")
            docs_buckets = pickle.load(f)
    except Exception as e:
        print(e)
        print("Aborting! Please Try Again.")
        exit()

    # Start the Server process
    app.run(use_reloader=False)
    # query = "ATGCCCCAACTAAATACCGCCGTATGACCCACCATAATTACCCCCATACTCCTGACACTATTTCTCGTCACCCAACTAAAAATATTAAATTCAAATTACCATCTACCCCCCTCACCAAAACCCATAAAAATAAAAAACTACAATAAACCCTGAGAACCAAAATGAACGAAAATCTATTCGCTTCATTCGCTGCCCCCACAATCCTAG"
    # query_buckets = process_query(query)
    # results = find_similar_docs(query_buckets, docs_buckets)
    # results_with_data = []
    # for docId in results:
    #     specie_name, dna_seq = get_data_for_docId(docId)
    #     results_with_data.append((specie_name, dna_seq))

    # print(results_with_data)
