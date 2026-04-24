import json
import os
from typing import List, Dict, Any
from datetime import datetime

class MovieManager:
    """Класс для управления коллекцией фильмов"""
    
    def __init__(self, filename: str = "movies.json"):
        self.filename = filename
        self.movies: List[Dict[str, Any]] = []
        self.load_movies()
    
    def add_movie(self, title: str, genre: str, year: str, rating: str) -> bool:
        """
        Добавление нового фильма с валидацией
        """
        # Валидация названия
        if not title or not title.strip():
            raise ValueError("Название фильма не может быть пустым")
        
        if len(title) > 100:
            raise ValueError("Название фильма не должно превышать 100 символов")
        
        # Валидация жанра
        if not genre or not genre.strip():
            raise ValueError("Жанр не может быть пустым")
        
        # Валидация года
        try:
            year_int = int(year)
            current_year = datetime.now().year
            if year_int < 1888 or year_int > current_year:
                raise ValueError(f"Год должен быть между 1888 и {current_year}")
        except ValueError:
            raise ValueError("Год должен быть целым числом")
        
        # Валидация рейтинга
        try:
            rating_float = float(rating)
            if rating_float < 0 or rating_float > 10:
                raise ValueError("Рейтинг должен быть от 0 до 10")
        except ValueError:
            raise ValueError("Рейтинг должен быть числом")
        
        # Создание записи о фильме
        movie = {
            "id": len(self.movies) + 1,
            "title": title.strip(),
            "genre": genre.strip(),
            "year": year_int,
            "rating": rating_float,
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.movies.append(movie)
        self.save_movies()
        return True
    
    def delete_movie(self, movie_id: int) -> bool:
        """Удаление фильма по ID"""
        for i, movie in enumerate(self.movies):
            if movie["id"] == movie_id:
                self.movies.pop(i)
                self.save_movies()
                return True
        return False
    
    def filter_movies(self, filter_type: str = "all", value: str = None) -> List[Dict[str, Any]]:
        """
        Фильтрация фильмов
        filter_type: "all", "genre", "year"
        """
        if filter_type == "all":
            return self.movies
        elif filter_type == "genre" and value:
            return [m for m in self.movies if m["genre"].lower() == value.lower()]
        elif filter_type == "year" and value:
            try:
                year_int = int(value)
                return [m for m in self.movies if m["year"] == year_int]
            except ValueError:
                return []
        return self.movies
    
    def get_unique_genres(self) -> List[str]:
        """Получение списка уникальных жанров"""
        genres = set(movie["genre"] for movie in self.movies)
        return sorted(list(genres))
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получение статистики по фильмам"""
        if not self.movies:
            return {"total": 0, "avg_rating": 0, "genre_count": {}}
        
        avg_rating = sum(m["rating"] for m in self.movies) / len(self.movies)
        
        genre_count = {}
        for movie in self.movies:
            genre_count[movie["genre"]] = genre_count.get(movie["genre"], 0) + 1
        
        return {
            "total": len(self.movies),
            "avg_rating": round(avg_rating, 2),
            "genre_count": genre_count
        }
    
    def save_movies(self):
        """Сохранение фильмов в JSON файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
    
    def load_movies(self):
        """Загрузка фильмов из JSON файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.movies = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.movies = []
        else:
            self.movies = []