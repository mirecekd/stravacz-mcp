#!/bin/bash

# Build script pro HTTP streaming verzi Stravacz MCP serveru

set -e

echo "🏗️  Buildování HTTP streaming verze Stravacz MCP serveru..."

# Build Docker image
docker build -f Dockerfile.http -t mirecekd/stravacz-mcp:http .

echo "✅ HTTP streaming verze úspěšně vybudována!"

echo ""
echo "🚀 Lokální použití:"
echo "docker run -p 8809:8809 mirecekd/stravacz-mcp:http --user USERNAME --password PASSWORD --canteen_number CANTEEN_NUMBER"

echo ""
echo "📦 GHCR použití:"
echo "docker run -p 8809:8809 ghcr.io/mirecekd/stravacz-mcp:latest-http --user USERNAME --password PASSWORD --canteen_number CANTEEN_NUMBER"

echo ""
echo "🔧 MCP konfigurace pro Claude Desktop:"
echo '{'
echo '  "mcpServers": {'
echo '    "stravacz-mcp": {'
echo '      "url": "http://localhost:8809",'
echo '      "transportType": "http"'
echo '    }'
echo '  }'
echo '}'

# Volitelné push do GHCR (pokud je nastaven GITHUB_TOKEN)
if [ ! -z "$GITHUB_TOKEN" ]; then
    echo ""
    echo "🔐 Pushing do GitHub Container Registry..."
    
    # Login do GHCR
    echo $GITHUB_TOKEN | docker login ghcr.io -u mirecekd --password-stdin
    
    # Tag a push
    docker tag mirecekd/stravacz-mcp:http ghcr.io/mirecekd/stravacz-mcp:latest-http
    docker push ghcr.io/mirecekd/stravacz-mcp:latest-http
    
    echo "✅ HTTP streaming verze uspěšně pushed do GHCR!"
else
    echo ""
    echo "💡 Pro push do GHCR nastavte GITHUB_TOKEN environment variable"
    echo "   export GITHUB_TOKEN=your_token"
fi
