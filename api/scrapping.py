from requests import get
from bs4 import BeautifulSoup


def getConsoles() -> list:
    consoles: list = []
    site = get("http://www.tudo-para-android.com/")
    html = BeautifulSoup(site.text, "html.parser")
    for console in html.findAll("div", class_="third-menu-item"):
        newConsole: dict = {}
        try:
            newConsole["name"] = console.find("div", itemprop="name").text
            if "hack" in newConsole["name"].lower():
                continue
            newConsole["url"] = console.find("a", itemprop="url").get("href")
            newConsole["image"] = console.find("img", itemprop="image").get("src")
        except Exception:
            continue
        consoles.append(newConsole)
    return consoles


def getGames(url: str) -> list:
    games: list = []
    site = get(url)
    html = BeautifulSoup(site.text, "html.parser")
    for game in html.findAll("div", class_="third-menu-item"):
        newGame: dict = {}
        try:
            newGame["name"] = game.find("div", itemprop="name").text
            newGame["image"] = game.find("img", itemprop="image").get("src")
            downloads = game.findAll("a")
            newGame["mega"] = downloads[0].get("href")
            newGame["gdrive"] = downloads[1].get("href")
        except Exception:
            continue
        games.append(newGame)
    return games
