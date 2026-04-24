# Stravacz MCP Server

MCP (Model Context Protocol) server pro **strava.cz** - systém a webová/mobilní aplikace pro objednávání stravy v českých jídelnách, například školních. Strávníci mohou prostřednictvím systému kontrolovat jídelníčky, přihlašovat a odhlašovat jídlo, sledovat historii objednávek, platby a přeplatky.


<div align="center">

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/mirecekdg) [!["PayPal.me"](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate/?business=LJ5ZF7Q9KMTRW&no_recurring=0&currency_code=USD)

</div>

## ⚠️ Upozornění

**!! K používání tohoto projektu je potřeba trošku umět s dockerem/pythonem a vědět, jak funguje připojení MCP k danému LLM klientu !!**

> 💡 **Poznámka:** Tento projekt není nijak spojen se systémem strava.cz. Jedná se o neoficiální MCP server vytvořený komunitou na základě projektů [strava-cz-python](https://github.com/jsem-nerad/strava-cz-python) a [strava-cli](https://github.com/StuckInVim-dev/strava-cli).

[![Docker Build](https://github.com/mirecekd/stravacz-mcp/actions/workflows/docker-build.yml/badge.svg)](https://github.com/mirecekd/stravacz-mcp/actions/workflows/docker-build.yml)
[![PyPI Publish](https://github.com/mirecekd/stravacz-mcp/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/mirecekd/stravacz-mcp/actions/workflows/pypi-publish.yml)

## ⚡ Rychlý start

### 🐳 Docker (doporučeno)

```bash
# CLI (stdio) verze
docker run --rm -i ghcr.io/mirecekd/stravacz-mcp:latest-cli \
  --user USERNAME --password PASSWORD --canteen_number CANTEEN_NUMBER

# HTTP streaming verze (port 8809)
docker run -p 8809:8809 ghcr.io/mirecekd/stravacz-mcp:latest-http \
  --user USERNAME --password PASSWORD --canteen_number CANTEEN_NUMBER
```

### 📦 uvx (PyPI)

```bash
# Instalace z PyPI a spuštění
uvx --from stravacz-mcp stravacz-mcp-server \
  --user USERNAME --password PASSWORD --canteen_number CANTEEN_NUMBER
```

## 🔧 Dostupné transport metody

Stravacz MCP Server podporuje tři transport metody podle vzoru [bakalari-mcp](https://github.com/mirecekd/bakalari-mcp):

| Transport | Port | Docker Image | Popis |
|-----------|------|--------------|-------|
| **CLI (stdio)** | - | `ghcr.io/mirecekd/stravacz-mcp:latest-cli` | Přímá MCP komunikace přes stdin/stdout |
| **HTTP Streaming** | 8809 | `ghcr.io/mirecekd/stravacz-mcp:latest-http` | Nativní HTTP streaming transport |
| **HTTP Proxy** | 8805 | `ghcr.io/mirecekd/stravacz-mcp:latest-proxy` | HTTP server pomocí mcp-proxy |

## 🛠️ MCP Tools

Server poskytuje následující nástroje pro práci se strava.cz:

### `get_menu(datum=None)`
Získání jídelníčku pro zadané datum (YYYY-MM-DD) nebo dnešní datum.

### `is_ordered(meal_id)`
Kontrola, jestli je jídlo s daným ID objednané.

### `order_meals(*meal_ids)`
Objednání více jídel podle jejich ID.

### `print_menu(include_soup=True, include_empty=False)`
Formátované vypsání menu s možností filtrace.

### `get_user_info()`
Získání informací o přihlášeném uživateli a jídelně.

### `logout()`
Odhlášení ze strava.cz systému.

## 📋 MCP konfigurace

### Claude Desktop (CLI verze)
```json
{
  "mcpServers": {
    "stravacz-mcp": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i", "ghcr.io/mirecekd/stravacz-mcp:latest-cli",
        "--user", "YOUR_USER",
        "--password", "YOUR_PASSWORD", 
        "--canteen_number", "YOUR_CANTEEN_NUMBER"
      ],
      "transportType": "stdio"
    }
  }
}
```

### Claude Desktop (HTTP streaming)
```json
{
  "mcpServers": {
    "stravacz-mcp": {
      "url": "http://localhost:8809",
      "transportType": "http"
    }
  }
}
```

## 🏗️ Vývoj a build

### Lokální vývoj
```bash
# Klonování repositáře
git clone https://github.com/mirecekd/stravacz-mcp.git
cd stravacz-mcp

# Instalace závislostí
pip install -e .

# Spuštění ze zdrojových kódů
python src/stravacz_mcp_server/server.py --user USER --password PASS --canteen_number NUM
```

### Docker build
```bash
# Build všech verzí
./build-all.sh

# Nebo jednotlivě
./build-cli.sh     # CLI verze
./build-http.sh    # HTTP streaming verze  
./build-proxy.sh   # HTTP proxy verze
```

### Python packaging
```bash
# Build Python balíčku
python -m build

# Lokální instalace z wheel
pip install dist/stravacz_mcp-1.0.0-py3-none-any.whl
```

## 🔍 Technické detaily

### Závislosti
- **strava-cz** >= 1.0.0 - Hlavní knihovna pro strava.cz API
- **fastmcp** >= 0.9.0 - MCP framework  
- **aiohttp** >= 3.8.0 - Async HTTP klient

### Async wrapper
Server používá async wrapper pro původně synchronní `strava-cz` knihovnu pomocí `asyncio.to_thread()`, což umožňuje neblokující operace.

### Multi-arch Docker images
Všechny Docker images podporují:
- **linux/amd64** (Intel/AMD x64)
- **linux/arm64** (Apple Silicon, ARM64)

## ⚠️ Důležité upozornění

Tento projekt používa neoficiální web scraping API pro strava.cz. Server může přestat fungovat při změnách na webu strava.cz. Používejte zodpovědně a neautomatizujte masivní množství požadavků.

## 📄 Licence

MIT License - viz [LICENSE](LICENSE) soubor.

## 🤝 Přispívání

Contributions jsou vítané! Prosím vytvořte issue nebo pull request.

## 🔗 Související projekty

- [strava-cz-python](https://github.com/jsem-nerad/strava-cz-python) - Původní Python knihovna pro strava.cz
- [bakalari-mcp](https://github.com/mirecekd/bakalari-mcp) - Další můj MCP server - pro Bakaláři API
- [strava-cli](https://github.com/StuckInVim-dev/strava-cli) - CLI nástroj pro strava.cz

---

**Vytvořeno s ❤️ pro českou AI/MCP komunitu**

## Support

If this tool is useful to you, you can support development:

<div align="center">

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/mirecekdg) [!["PayPal.me"](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate/?business=LJ5ZF7Q9KMTRW&no_recurring=0&currency_code=USD)

</div>
