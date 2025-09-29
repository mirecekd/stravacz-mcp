#!/bin/bash

# Build script pro všechny verze Stravacz MCP serveru

set -e

echo "🚀 Buildování všech verzí Stravacz MCP serveru..."
echo ""

# Build CLI verze
echo "1️⃣  CLI (stdio) verze..."
./build-cli.sh

echo ""
echo "2️⃣  HTTP streaming verze..."
./build-http.sh

echo ""
echo "3️⃣  HTTP proxy verze..."
./build-proxy.sh

echo ""
echo "🎉 Všechny verze úspěšně vybudovány!"
echo ""

echo "📋 Přehled vybudovaných images:"
echo "  • CLI (stdio):     mirecekd/stravacz-mcp:cli"
echo "  • HTTP streaming:  mirecekd/stravacz-mcp:http"
echo "  • HTTP proxy:      mirecekd/stravacz-mcp:proxy"

if [ ! -z "$GITHUB_TOKEN" ]; then
    echo ""
    echo "📦 GHCR images:"
    echo "  • CLI (stdio):     ghcr.io/mirecekd/stravacz-mcp:latest-cli"
    echo "  • HTTP streaming:  ghcr.io/mirecekd/stravacz-mcp:latest-http"
    echo "  • HTTP proxy:      ghcr.io/mirecekd/stravacz-mcp:latest-proxy"
fi

echo ""
echo "🔧 Rychlé testování:"
echo "  CLI:     docker run --rm -i mirecekd/stravacz-mcp:cli --help"
echo "  HTTP:    docker run -p 8809:8809 mirecekd/stravacz-mcp:http --help"
echo "  Proxy:   docker run -p 8805:8805 mirecekd/stravacz-mcp:proxy"
