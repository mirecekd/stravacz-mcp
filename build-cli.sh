#!/bin/bash

# Build script pro CLI (stdio) verzi Stravacz MCP serveru

set -e

echo "🏗️  Buildování CLI (stdio) verze Stravacz MCP serveru..."

# Build Docker image
docker build -f Dockerfile.cli -t mirecekd/stravacz-mcp:cli .

echo "✅ CLI verze úspěšně vybudována!"

echo ""
echo "🚀 Lokální použití:"
echo "docker run --rm -i mirecekd/stravacz-mcp:cli --user USERNAME --password PASSWORD --canteen_number CANTEEN_NUMBER"

echo ""
echo "📦 GHCR použití:"
echo "docker run --rm -i ghcr.io/mirecekd/stravacz-mcp:latest-cli --user USERNAME --password PASSWORD --canteen_number CANTEEN_NUMBER"

echo ""
echo "🔧 MCP konfigurace pro Claude Desktop:"
echo '{'
echo '  "mcpServers": {'
echo '    "stravacz-mcp": {'
echo '      "command": "docker",'
echo '      "args": ['
echo '        "run", "--rm", "-i", "ghcr.io/mirecekd/stravacz-mcp:latest-cli",'
echo '        "--user", "YOUR_USER",'
echo '        "--password", "YOUR_PASSWORD",'
echo '        "--canteen_number", "YOUR_CANTEEN_NUMBER"'
echo '      ],'
echo '      "transportType": "stdio"'
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
    docker tag mirecekd/stravacz-mcp:cli ghcr.io/mirecekd/stravacz-mcp:latest-cli
    docker push ghcr.io/mirecekd/stravacz-mcp:latest-cli
    
    echo "✅ CLI verze uspěšně pushed do GHCR!"
else
    echo ""
    echo "💡 Pro push do GHCR nastavte GITHUB_TOKEN environment variable"
    echo "   export GITHUB_TOKEN=your_token"
fi
