"""
HTTP streaming MCP server pro strava.cz

Implementuje Model Context Protocol server s HTTP streaming transportem.
"""

import argparse
import asyncio
import logging
import sys
from typing import Dict, Any, Optional, List
from fastmcp import FastMCP
from .strava_client import AsyncStravaClient

# Nastavení loggingu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Globální instance klienta
strava_client: Optional[AsyncStravaClient] = None

# Vytvoření MCP serveru
server = FastMCP("Stravacz MCP Server HTTP")


@server.tool()
async def get_menu(datum: Optional[str] = None) -> Dict[str, Any]:
    """
    Získání jídelníčku pro zadané datum
    
    Args:
        datum: Datum ve formátu YYYY-MM-DD. Pokud není zadáno, použije se dnešní datum.
        
    Returns:
        Dict obsahující jídelníček pro zadaný den
    """
    if not strava_client:
        return {"error": "Strava klient není inicializován"}
    
    try:
        result = await strava_client.get_menu(datum)
        logger.info(f"Získán jídelníček pro datum: {datum or 'dnes'}")
        return result
    except Exception as e:
        logger.error(f"Chyba při získávání jídelníčku: {e}")
        return {"error": f"Chyba při získávání jídelníčku: {str(e)}"}


@server.tool()
async def is_ordered(meal_id: int) -> Dict[str, Any]:
    """
    Kontrola, jestli je jídlo objednané
    
    Args:
        meal_id: ID jídla (unikátní identifikační číslo jídla v jídelníčku)
        
    Returns:
        Dict obsahující informaci o tom, jestli je jídlo objednané
    """
    if not strava_client:
        return {"error": "Strava klient není inicializován"}
    
    try:
        result = await strava_client.is_ordered(meal_id)
        logger.info(f"Zkontrolována objednávka pro meal_id: {meal_id}")
        return result
    except Exception as e:
        logger.error(f"Chyba při kontrole objednávky: {e}")
        return {"error": f"Chyba při kontrole objednávky: {str(e)}"}


@server.tool()
async def order_meals(meal_ids: List[int]) -> Dict[str, Any]:
    """
    Objednání jídel podle meal_id
    
    Args:
        meal_ids: Seznam ID jídel k objednání
        
    Returns:
        Dict s výsledkem objednávky
    """
    if not strava_client:
        return {"error": "Strava klient není inicializován"}
    
    if not meal_ids:
        return {"error": "Nejsou zadána žádná meal_ids k objednání"}
    
    try:
        result = await strava_client.order_meals(*meal_ids)
        logger.info(f"Objednána jídla s IDs: {meal_ids}")
        return result
    except Exception as e:
        logger.error(f"Chyba při objednávání: {e}")
        return {"error": f"Chyba při objednávání: {str(e)}"}


@server.tool()
async def print_menu(include_soup: bool = True, include_empty: bool = False) -> Dict[str, Any]:
    """
    Formátované vypsání menu
    
    Args:
        include_soup: Zahrnout polévky do výpisu (výchozí: True)
        include_empty: Zahrnout prázdné položky (výchozí: False)
        
    Returns:
        Dict s formátovaným menu jako string
    """
    if not strava_client:
        return {"error": "Strava klient není inicializován"}
    
    try:
        result = await strava_client.print_menu(include_soup, include_empty)
        logger.info(f"Vytištěno formátované menu")
        return result
    except Exception as e:
        logger.error(f"Chyba při formátování menu: {e}")
        return {"error": f"Chyba při formátování menu: {str(e)}"}


@server.tool()
async def get_user_info() -> Dict[str, Any]:
    """
    Získání informací o přihlášeném uživateli
    
    Returns:
        Dict obsahující informace o uživateli a připojené jídelně
    """
    if not strava_client:
        return {"error": "Strava klient není inicializován"}
    
    try:
        result = await strava_client.get_user_info()
        logger.info("Získány informace o uživateli")
        return result
    except Exception as e:
        logger.error(f"Chyba při získávání informací o uživateli: {e}")
        return {"error": f"Chyba při získávání informací o uživateli: {str(e)}"}


@server.tool()
async def logout() -> Dict[str, Any]:
    """
    Odhlášení ze strava.cz systému
    
    Returns:
        Dict s výsledkem odhlášení
    """
    if not strava_client:
        return {"error": "Strava klient není inicializován"}
    
    try:
        result = await strava_client.logout()
        logger.info("Uživatel byl odhlášen")
        return result
    except Exception as e:
        logger.error(f"Chyba při odhlašování: {e}")
        return {"error": f"Chyba při odhlašování: {str(e)}"}


async def run_http_server(username: str, password: str, canteen_number: str, port: int = 8809):
    """
    Spuštění HTTP streaming MCP serveru
    
    Args:
        username: Uživatelské jméno pro strava.cz
        password: Heslo pro strava.cz
        canteen_number: Číslo jídelny
        port: Port pro HTTP server (výchozí: 8809)
    """
    global strava_client
    
    try:
        # Inicializace Strava klienta
        logger.info(f"Inicializace Strava klienta pro uživatele: {username}")
        strava_client = AsyncStravaClient(username, password, canteen_number)
        
        # Spuštění HTTP streaming serveru
        logger.info(f"Spouštění HTTP streaming MCP serveru na portu {port}...")
        await server.run(transport="http", port=port, host="0.0.0.0")
        
    except KeyboardInterrupt:
        logger.info("HTTP server zastaven uživatelem")
    except Exception as e:
        logger.error(f"Kritická chyba HTTP serveru: {e}")
        raise
    finally:
        # Odhlášení při ukončování
        if strava_client:
            try:
                await strava_client.logout()
                logger.info("Dokončeno odhlášení")
            except Exception as e:
                logger.error(f"Chyba při závěrečném odhlášení: {e}")


def parse_args():
    """Parsování argumentů příkazové řádky"""
    parser = argparse.ArgumentParser(
        description="Stravacz MCP HTTP Server - HTTP streaming MCP server pro strava.cz"
    )
    
    parser.add_argument(
        "--user",
        required=True,
        help="Uživatelské jméno pro strava.cz"
    )
    
    parser.add_argument(
        "--password",
        required=True,
        help="Heslo pro strava.cz"
    )
    
    parser.add_argument(
        "--canteen_number",
        required=True,
        help="Číslo jídelny"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8809,
        help="Port pro HTTP server (výchozí: 8809)"
    )
    
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host pro HTTP server (výchozí: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Úroveň logování (výchozí: INFO)"
    )
    
    return parser.parse_args()


def main():
    """Hlavní funkce pro spuštění HTTP serveru"""
    args = parse_args()
    
    # Nastavení úrovně logování
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    logger.info("=== Stravacz MCP HTTP Server ===")
    logger.info(f"Uživatel: {args.user}")
    logger.info(f"Jídelna: {args.canteen_number}")
    logger.info(f"HTTP port: {args.port}")
    logger.info(f"HTTP host: {args.host}")
    logger.info(f"Log level: {args.log_level}")
    
    try:
        # Spuštění HTTP serveru
        asyncio.run(run_http_server(args.user, args.password, args.canteen_number, args.port))
    except KeyboardInterrupt:
        logger.info("\nHTTP Server zastaven")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Neočekávaná chyba: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
