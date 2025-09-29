#!/bin/bash

# Build script pro HTTP proxy verzi Stravacz MCP serveru (přes mcp-proxy)

set -e

echo "🏗️  Buildování HTTP proxy verze Stravacz MCP serveru..."

# Build Docker image
docker build -f Dockerfile.proxy -t mirecekd/stravacz-mcp:proxy .

echo "✅ HTTP proxy verze úspěšně vybudována!"

echo ""
echo "🚀 Lokální použití:"
echo "docker run -p 8805:8805 \\"
echo "  -e STRAVACZ_USER=USERNAME \\"
echo "  -e STRAVACZ_PASSWORD=PASSWORD \\"
echo "  -e STRAVACZ_CANTEEN_NUMBER=CANTEEN_NUMBER \\"
echo "  mirecekd/stravacz-mcp:proxy"

echo ""
echo "📦 GHCR použití:"
echo "docker run -p 8805:8805 \\"
echo "  -e STRAVACZ_USER=USERNAME \\"
echo "  -e STRAVACZ_PASSWORD=PASSWORD \\"
echo "  -e STRAVACZ_CANTEEN_NUMBER=CANTEEN_NUMBER \\"
echo "  ghcr.io/mirecekd/stravacz-mcp:latest-proxy"

echo ""
echo "🔧 MCP konfigurace pro Claude Desktop:"
echo '{'
echo '  "mcpServers": {'
echo '    "stravacz-mcp": {'
echo '      "url": "http://localhost:8805",'
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
    docker tag mirecekd/stravacz-mcp:proxy ghcr.io/mirecekd/stravacz-mcp:latest-proxy
    docker push ghcr.io/mirecekd/stravacz-mcp:latest-proxy
    
    echo "✅ HTTP proxy verze uspěšně pushed do GHCR!"
else
    echo ""
    echo "💡 Pro push do GHCR nastavte GITHUB_TOKEN environment variable"
    echo "   export GITHUB_TOKEN=your_token"
fi
