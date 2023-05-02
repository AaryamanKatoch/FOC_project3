Aaryaman Katoch  akatoch@stevens.edu
the URL of your public GitHub repo
an estimate of how many hours you spent on the project : 16 hours

a description of how you tested your code : Manually using postman interface and using automated postman scripts.

any bugs or issues you could not resolve : All my functionalities and endpoints are working correctly when I tested manually using postman. I was facing issues writing automation scripts for test cases. I am still getting an assertionError in the basic functionalities.

an example of a difficult issue or bug and how you resolved : It was difficult to implement the threaded replies as I needed to traverse back to the parent thread.

a list of the five extensions you’ve chosen to implement; be sure to describe the endpoints you’ve added to support this, using a documentation format similar to ours
detailed summaries of your tests for each of your extensions, i.e., how to interpret your testing framework and the tests you’ve written

1. Threaded replies:
endpoint : '/post'
POST
Add a reply_to_id field in the json body which will contain the id of the post to which the post is replying.

2. Date- and time-based range queries
endpoint : '/post/search'
GET
Pass start_date_time and end_date_time as request.args to get results.

3. Thread-based range queries:
endpoint : '/post/threads/<int:id>'
GET
Add an API endpoint that lets the user search for all posts in a “thread”: that is, the transitive reply chains up and down.
It is implemented by using "reply_to_id" and "replies" field in the post object.
 
4. Fulltext search
endpoint : '/post/search/fulltext'
GET
Pass the query ("q") as req.args.

5. Moderator
endpoint:'/post/<int:id>/delete'
DELETE
Implemented by creating a moderator array with keys of moderators and checking while deleting if user is a moderator.
Pass 'key' in req.json(request body)


Testing :

1. Threaded replies:
endpoint : '/post'
The API endpoint URL and a sample thread ID are two variables that are set up in the first few lines and will be used in our test scenarios.

The first test case sends a POST request with a JSON body that has an array of reply objects in the responses field, a title field, a description field, and other fields to the API endpoint. The pm.expect statements make sure the answer has a status code of 200, the title field in the response body includes the same value as the title field in the request, and the replies field contains an array of reply objects.

The second test case sends an empty JSON body along with a POST request to the API endpoint. The pm.expect statements verify that the response has a status code of 400 and that an error field with the value "Missing title or description" is present in the response body.

The third test case sends a POST request with a JSON body that only contains a title field and no description field to the API endpoint. The pm.expect statements verify that the response has a status code of 400 and that an error field with the value "Missing title or description" is present in the response body.

The fourth test case sends a POST request with a JSON body that only contains a description field and no title field to the API endpoint. The pm.expect statements verify that the response has a status code of 400 and that an error field with the value "Missing title or description" is present in the response body.

The fifth test case, which is the last, makes a POST request with a JSON body that has a title field, a description field, but not a responses field, to the API endpoint. The pm.expect statements verify that the response has a status code of 200, that the title field in the response body includes the same value as the request's title field, and that the responses field is an empty array.

2. Fulltext search
endpoint : /post/search/fulltext

"Search posts with valid query" ability to search articles using a legitimate query. The goal of the test case is to confirm that the API endpoint responds with a 200 status code and a JSON object containing an array of search results that match the search query.

"Search posts with empty query" is a test case for the situation in which a user enters a blank search query. This test checks to see if the API can effectively accept empty queries.
The following assertions are part of this test case:
The expected HTTP response status code is 400.
An "error" property needs to be present in the JSON response.
The "error" attribute should have the value "Query cannot be empty".
These claims verify that when an empty query is provided, the API responds with the proper error message. The test will fail if any one of these claims is false.

The "Search posts with non-matching query" test case contains a single test event that utilizes a script to submit a POST request with a JSON body containing the query "qwertyuiop" to the URL supplied in the "url" variable.

The "Search posts with matching query" is a Postman test script in JSON format that tests a POST request to search for posts with a matching query.

3. Thread-based range queries
endpoint: '/post/threads/<int:id>'

The first test case sends a POST request with a JSON body that has an array of reply objects in the responses field, a title field, a description field, and other fields to the API endpoint. The pm.expect statements make sure the answer has a status code of 200, the title field in the response body includes the same value as the title field in the request, and the replies field contains an array of reply objects.

The second test case sends an empty JSON body along with a POST request to the API endpoint. The pm.expect statements verify that the response has a status code of 400 and that an error field with the value "Missing title or description" is present in the response body.

The third test case sends a POST request with a JSON body that only contains a title field and no description field to the API endpoint. The pm.expect statements verify that the response has a status code of 400 and that an error field with the value "Missing title or description" is present in the response body.

The fourth test case sends a POST request with a JSON body that only contains a description field and no title field to the API endpoint. The pm.expect statements verify that the response has a status code of 400 and that an error field with the value "Missing title or description" is present in the response body.

The fifth test case, which is the last, makes a POST request with a JSON body that has a title field, a description field, but not a responses field, to the API endpoint. The pm.expect statements verify that the response has a status code of 200, that the title field in the response body includes the same value as the request's title field, and that the responses field is an empty array.

4. Date- and time-based range queries
endpoint : '/post/search'
A search with valid start and finish dates is put to the test in the first test case. It sends a GET request with the parameters "start" and "end" set to valid dates in ISO 8601 format to the URL "http://localhost:5000/post/search". It anticipates a response body containing a JSON array and a response status code of 200.

Search with invalid date format"" examines a search using a date format that is not valid. With the'start' and 'end' parameters adjusted to dates in a different format, it sends a GET request to the same URL as in the first test case. It anticipates a JSON object with the response status code set to 400 and the 'error' field set to 'bad request' in the response body.

"Search without specifying start or end date" tests a search without specifying start or end date. It sends a GET request to the same URL as in the first test case without any parameters. It expects a JSON object in the response body with an 'error' property set to 'bad request' and a response status code of 400.

"Search with start date in future" expects the API to return an empty array since the start date is in the future and no posts should be found for that range.

 "Search with date range containing no posts" .

 5. Moderator Role:
 endpoint : '/post/<int:id>/delete'
 "Delete post with missing key"
 "Delete post with invalid key"
 "Successful DEletion of post"