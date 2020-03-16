from src.scrapers.mangadex import MangaDex
from src.scrapers.mangaplus import MangaPlus

SCRAPERS = {
    MangaDex.URL: MangaDex,
    MangaPlus.URL: MangaPlus
}
