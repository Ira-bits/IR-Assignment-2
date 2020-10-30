""" Flask app to provide backend for the Search Engine Web Client """

from flask import Flask, request, jsonify, make_response, render_template
from flask_cors import CORS
import os
from helper import perform_lsh, LRUCache, process_query


# Initialize Flask app
app = Flask(
    __name__,
    static_url_path="",
    static_folder="search_client/static",
    template_folder="search_client/templates",
)
CORS(app)
app.config["DEBUG"] = True  # Change to False in Production
id_dict = {}

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
        * Return Format - [(docID, tf-idf score, title, summary)]

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

    query_bucket = process_query(query)


if __name__ == "__main__":

    try:
        # Raise Error if data set doesn't exist.
        if not os.path.isdir("./dataset"):
            raise Exception("Dataset not found")
        perform_lsh()
    except Exception as e:
        print(e)
        print("Aborting! Please Try Again.")
        exit()

    # Start the Server process
    # app.run(use_reloader=False)
