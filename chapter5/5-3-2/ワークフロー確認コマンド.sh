curl -X POST http://localhost:3001/api/workflow/execute \
    -H "Content-Type: application/json" \
    -d '{
      "query": "AIについての情報",
      "owner": "RyoyaMasuda",
      "repo": "mastra_practice"
    }' | jq