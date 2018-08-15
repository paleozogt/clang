BODY="{
    \"request\": {
        \"branch\":\"$CI_COMMIT_REF_NAME\",
        \"config\": {
            \"env\": {
                \"ARTIFACT_URL\": \"$ARTIFACT_URL\"
            }
        }
    }
}"

echo "posting\n$BODY"

curl -s -X POST \
   -H "Content-Type: application/json" \
   -H "Accept: application/json" \
   -H "Travis-API-Version: 3" \
   -H "Authorization: token $TRAVIS_CI_TOKEN" \
   -d "$BODY" \
   "https://api.travis-ci.org/repo/${CI_PROJECT_NAMESPACE}%2F${CI_PROJECT_NAME}/requests" > response.json

echo "response"
cat response.json

exit `grep error response.json | wc -l`
