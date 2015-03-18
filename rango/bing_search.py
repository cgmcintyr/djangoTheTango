import json
import urllib, urllib2

from keys import BING_API_KEY

def run_query(search_terms):
    """
    Connects to Bing Search API and runs a query of given search terms.

    Arguments:
    search_terms -- (string) terms to search for.

    Returns:
    results -- (dictionary) results of the query
    """
    # Specify the base
    root_url = 'https://api.datamarket.azure.com/Bing/Search/'
    source = 'Web' 

    results_per_page = 10 
    offset = 0  # Specifies where results list to start from.

    # Wrap quotes around query terms as required by Bing API.
    query = "'{0}'".format(search_terms)
    query = urllib.quote(query)

    # Construct the latter part of our request's URL
    # Sets the format of the response to JSON and sets other properties.
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        source,
        results_per_page,
        offset,
        query
    )
    print "search url: {0}".format(search_url)
    # Setup authentication with Bing servers.
    # The username MUST be a blank string.

    username = ''

    # Create a 'password manager' which handles authentication for us.
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, BING_API_KEY)

    # Create our results list which we'll populate.
    results = []

    try:
        # Prepare for connecting to Bing's servers.
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener  = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        
        # Connect to the server and read the response generated.
        response = urllib2.urlopen(search_url).read()

        # Convert the string response to a Python dictionary object.
        json_response = json.loads(response)

        # Loop through each page returned, populating out results list.
        for result in json_response['d']['results']:
            results.append({
                'title': result['Title'],
                'link': result['Url'],
                'summary': result['Description']
            })

    # Catch a URLError exeption - something went wrong when connecting!
    except urllib2.URLError, e:
        print "Error when querying the Bing API: ", e

    # Return the list of results to the calling function
    return results

