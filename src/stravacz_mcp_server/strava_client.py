"""
Async wrapper pro strava-cz knihovnu

Umožňuje asynchronní práci s původně synchronní strava-cz knihovnou
pomocí asyncio.to_thread().
"""

import asyncio
import logging
from typing import Optional, List, Dict, Any
from strava_cz import StravaCZ

logger = logging.getLogger(__name__)


class AsyncStravaClient:
    """Asynchronní wrapper pro StravaCZ knihovnu"""
    
    def __init__(self, username: str, password: str, canteen_number: str):
        """
        Inicializace async Strava klienta
        
        Args:
            username: Uživatelské jméno
            password: Heslo
            canteen_number: Číslo jídelny
        """
        self.username = username
        self.password = password
        self.canteen_number = canteen_number
        self._strava: Optional[StravaCZ] = None
        self._logged_in = False
    
    async def _ensure_logged_in(self):
        """Zajistí, že je klient přihlášen"""
        if not self._logged_in:
            await self._login()
    
    async def _login(self):
        """Asynchronní přihlášení"""
        try:
            logger.info(f"Přihlašování uživatele {self.username} do jídelny {self.canteen_number}")
            
            # Vytvoření StravaCZ instance v thread poolu
            self._strava = await asyncio.to_thread(
                StravaCZ,
                username=self.username,
                password=self.password,
                canteen_number=self.canteen_number
            )
            
            self._logged_in = True
            logger.info("Úspěšné přihlášení")
            
        except Exception as e:
            logger.error(f"Chyba při přihlašování: {e}")
            self._logged_in = False
            raise Exception(f"Nepodařilo se přihlásit: {str(e)}")
    
    async def get_menu(self, datum: Optional[str] = None) -> Dict[str, Any]:
        """
        Získání jídelníčku pro zadané datum
        
        Args:
            datum: Datum ve formátu YYYY-MM-DD, pokud None použije se dnešní datum
            
        Returns:
            Dict s jídelníčkem
        """
        await self._ensure_logged_in()
        
        try:
            logger.info(f"Získávání jídelníčku pro datum: {datum or 'dnes'}")
            
            # Volání get_menu v thread poolu
            menu = await asyncio.to_thread(self._strava.get_menu)
            
            return {
                "status": "success",
                "datum": datum or "dnes",
                "menu": menu,
                "pocet_polozek": len(menu) if menu else 0
            }
            
        except Exception as e:
            logger.error(f"Chyba při získávání jídelníčku: {e}")
            return {
                "status": "error",
                "error": f"Nepodařilo se získat jídelníček: {str(e)}"
            }
    
    async def is_ordered(self, meal_id: int) -> Dict[str, Any]:
        """
        Kontrola, jestli je jídlo objednané
        
        Args:
            meal_id: ID jídla
            
        Returns:
            Dict s informací o objednávce
        """
        await self._ensure_logged_in()
        
        try:
            logger.info(f"Kontrola objednávky pro meal_id: {meal_id}")
            
            # Volání is_ordered v thread poolu
            is_ordered = await asyncio.to_thread(self._strava.is_ordered, meal_id)
            
            return {
                "status": "success",
                "meal_id": meal_id,
                "is_ordered": is_ordered
            }
            
        except Exception as e:
            logger.error(f"Chyba při kontrole objednávky: {e}")
            return {
                "status": "error",
                "error": f"Nepodařilo se zkontrolovat objednávku: {str(e)}"
            }
    
    async def order_meals(self, *meal_ids: int) -> Dict[str, Any]:
        """
        Objednání jídel podle meal_id
        
        Args:
            meal_ids: ID jídel k objednání
            
        Returns:
            Dict s výsledkem objednávky
        """
        await self._ensure_logged_in()
        
        try:
            logger.info(f"Objednávání jídel: {meal_ids}")
            
            # Volání order_meals v thread poolu
            await asyncio.to_thread(self._strava.order_meals, *meal_ids)
            
            return {
                "status": "success",
                "message": f"Úspěšně objednáno {len(meal_ids)} jídel",
                "ordered_meal_ids": list(meal_ids)
            }
            
        except Exception as e:
            logger.error(f"Chyba při objednávání: {e}")
            return {
                "status": "error",
                "error": f"Nepodařilo se objednat jídla: {str(e)}"
            }
    
    async def print_menu(self, include_soup: bool = True, include_empty: bool = False) -> Dict[str, Any]:
        """
        Formátované vypsání menu
        
        Args:
            include_soup: Zahrnout polévky
            include_empty: Zahrnout prázdné položky
            
        Returns:
            Dict s formátovaným menu
        """
        await self._ensure_logged_in()
        
        try:
            logger.info(f"Formátování menu (soup: {include_soup}, empty: {include_empty})")
            
            # Volání print_menu v thread poolu
            formatted_menu = await asyncio.to_thread(
                self._strava.print_menu,
                include_soup=include_soup,
                include_empty=include_empty
            )
            
            return {
                "status": "success",
                "formatted_menu": formatted_menu,
                "include_soup": include_soup,
                "include_empty": include_empty
            }
            
        except Exception as e:
            logger.error(f"Chyba při formátování menu: {e}")
            return {
                "status": "error",
                "error": f"Nepodařilo se naformátovat menu: {str(e)}"
            }
    
    async def get_user_info(self) -> Dict[str, Any]:
        """
        Získání informací o uživateli
        
        Returns:
            Dict s informacemi o uživateli
        """
        await self._ensure_logged_in()
        
        try:
            logger.info("Získávání informací o uživateli")
            
            # Přístup k user atributu v thread poolu
            user_info = await asyncio.to_thread(lambda: self._strava.user)
            
            return {
                "status": "success",
                "user": user_info,
                "username": self.username,
                "canteen_number": self.canteen_number
            }
            
        except Exception as e:
            logger.error(f"Chyba při získávání info o uživateli: {e}")
            return {
                "status": "error",
                "error": f"Nepodařilo se získat informace o uživateli: {str(e)}"
            }
    
    async def logout(self) -> Dict[str, Any]:
        """
        Odhlášení uživatele
        
        Returns:
            Dict s výsledkem odhlášení
        """
        try:
            if self._strava and self._logged_in:
                logger.info("Odhlašování uživatele")
                await asyncio.to_thread(self._strava.logout)
            
            self._logged_in = False
            self._strava = None
            
            return {
                "status": "success",
                "message": "Úspěšně odhlášen"
            }
            
        except Exception as e:
            logger.error(f"Chyba při odhlašování: {e}")
            return {
                "status": "error",
                "error": f"Chyba při odhlašování: {str(e)}"
            }
