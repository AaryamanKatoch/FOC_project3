#!/bin/sh

set -e # exit immediately if newman complains
trap 'kill $PID' EXIT # kill the server on exit

./run.sh &
PID=$! # record the PID

newman run forum_multiple_posts.postman_collection.json -e env.json # use the env file
newman run Moderator_forum_post_read_delete.postman_collection.json -n 50 # 50 iterations
newman run threadrange_query.postman_collection.json -n 50
newman run threads.postman_collection.json -n 50
newman run search_posts.postman_collection.json -n 50
newman run search.postman_collection.json -n 50
