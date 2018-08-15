BODY="{
    \"accountName\": \"$CI_PROJECT_NAMESPACE\",
    \"projectSlug\": \"$CI_PROJECT_NAME\",
    \"branch\": \"$CI_COMMIT_REF_NAME\",
    \"commitId\": \"$CI_COMMIT_SHA\",
    \"environmentVariables\": {
       \"ARTIFACT_URL\": \"$ARTIFACT_URL\"
    }
}"

echo "posting\n$BODY"

curl -s -X POST \
   -H "Content-Type: application/json" \
   -H "Accept: application/json" \
   -H "Travis-API-Version: 3" \
   -H "Authorization: Bearer $APPVEYOR_CI_TOKEN" \
   -d "$BODY" \
   "https://ci.appveyor.com/api/builds" > response.json

echo "response"
cat response.json

exit `grep error response.json | wc -l`
