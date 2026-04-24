import unittest
import os
import json
from movie_manager import MovieManager

class TestMovieManager(unittest.TestCase):
  
    
    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.test_file = "test_movies.json"
        self.manager = MovieManager(self.test_file)
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    
    def test_add_movie_positive(self):
        result = self.manager.add_movie("Inception", "Sci-Fi", "2010", "8.8")
        self.assertTrue(result)
        self.assertEqual(len(self.manager.movies), 1)
        self.assertEqual(self.manager.movies[0]["title"], "Inception")
        self.assertEqual(self.manager.movies[0]["genre"], "Sci-Fi")
        self.assertEqual(self.manager.movies[0]["year"], 2010)
        self.assertEqual(self.manager.movies[0]["rating"], 8.8)
    
    def test_add_multiple_movies(self):
        self.manager.add_movie("Movie 1", "Action", "2020", "7.5")
        self.manager.add_movie("Movie 2", "Comedy", "2021", "8.0")
        self.assertEqual(len(self.manager.movies), 2)
    
    def test_save_and_load_json(self):
        self.manager.add_movie("The Matrix", "Sci-Fi", "1999", "9.0")
        self.manager.save_movies()
        
        new_manager = MovieManager(self.test_file)
        self.assertEqual(len(new_manager.movies), 1)
        self.assertEqual(new_manager.movies[0]["title"], "The Matrix")
    
    def test_filter_by_genre(self):
        self.manager.add_movie("Inception", "Sci-Fi", "2010", "8.8")
        self.manager.add_movie("The Dark Knight", "Action", "2008", "9.0")
        self.manager.add_movie("Interstellar", "Sci-Fi", "2014", "8.6")
        
        filtered = self.manager.filter_movies("genre", "Sci-Fi")
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(m["genre"] == "Sci-Fi" for m in filtered))
    
    def test_filter_by_year(self):
        self.manager.add_movie("Movie 2020", "Drama", "2020", "7.0")
        self.manager.add_movie("Movie 2021", "Comedy", "2021", "8.0")
        
        filtered = self.manager.filter_movies("year", "2020")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["year"], 2020)
    
    def test_delete_movie(self):
        self.manager.add_movie("To Delete", "Action", "2020", "7.0")
        movie_id = self.manager.movies[0]["id"]
        
        result = self.manager.delete_movie(movie_id)
        self.assertTrue(result)
        self.assertEqual(len(self.manager.movies), 0)
    
    def test_get_unique_genres(self):
        self.manager.add_movie("Movie 1", "Action", "2020", "7.0")
        self.manager.add_movie("Movie 2", "Comedy", "2021", "8.0")
        self.manager.add_movie("Movie 3", "Action", "2022", "9.0")
        
        genres = self.manager.get_unique_genres()
        self.assertEqual(set(genres), {"Action", "Comedy"})
    
    def test_get_statistics(self):
        """Тест 8: Получение статистики"""
        self.manager.add_movie("Movie 1", "Action", "2020", "8.0")
        self.manager.add_movie("Movie 2", "Comedy", "2021", "9.0")
        
        stats = self.manager.get_statistics()
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["avg_rating"], 8.5)
    
    
    def test_add_movie_empty_title(self):
        
        with self.assertRaises(ValueError):
            self.manager.add_movie("", "Action", "2020", "7.5")
    
    def test_add_movie_empty_genre(self):
        """Тест 10: Пустой жанр"""
        with self.assertRaises(ValueError):
            self.manager.add_movie("Movie", "", "2020", "7.5")
    
    def test_add_movie_invalid_year_string(self):
        """Тест 11: Год не число"""
        with self.assertRaises(ValueError):
            self.manager.add_movie("Movie", "Action", "abcd", "7.5")
    
    def test_add_movie_year_too_early(self):
        """Тест 12: Год слишком ранний"""
        with self.assertRaises(ValueError):
            self.manager.add_movie("Movie", "Action", "1800", "7.5")
    
    def test_add_movie_year_too_late(self):
        """Тест 13: Год в будущем"""
        with self.assertRaises(ValueError):
            self.manager.add_movie("Movie", "Action", "2030", "7.5")
    
    def test_add_movie_rating_too_high(self):
        """Тест 14: Рейтинг выше 10"""
        with self.assertRaises(ValueError):
            self.manager.add_movie("Movie", "Action", "2020", "11")
    
    def test_add_movie_rating_too_low(self):
        """Тест 15: Рейтинг ниже 0"""
        with self.assertRaises(ValueError):
            self.manager.add_movie("Movie", "Action", "2020", "-1")
    
    def test_add_movie_invalid_rating_string(self):
        """Тест 16: Рейтинг не число"""
        with self.assertRaises(ValueError):
            self.manager.add_movie("Movie", "Action", "2020", "good")
    
    def test_title_too_long(self):
        """Тест 17: Слишком длинное название"""
        long_title = "A" * 101
        with self.assertRaises(ValueError):
            self.manager.add_movie(long_title, "Action", "2020", "7.5")
    
    def test_delete_nonexistent_movie(self):
        result = self.manager.delete_movie(999)
        self.assertFalse(result)
    
    
    def test_year_boundary_minimum(self):
        result = self.manager.add_movie("Movie", "Action", "1888", "7.5")
        self.assertTrue(result)
        self.assertEqual(self.manager.movies[0]["year"], 1888)
    
    def test_year_boundary_maximum(self):
        from datetime import datetime
        current_year = datetime.now().year
        result = self.manager.add_movie("Movie", "Action", str(current_year), "7.5")
        self.assertTrue(result)
        self.assertEqual(self.manager.movies[0]["year"], current_year)
    
    def test_rating_boundary_minimum(self):
        result = self.manager.add_movie("Movie", "Action", "2020", "0")
        self.assertTrue(result)
        self.assertEqual(self.manager.movies[0]["rating"], 0.0)
    
    def test_rating_boundary_maximum(self):
        result = self.manager.add_movie("Movie", "Action", "2020", "10")
        self.assertTrue(result)
        self.assertEqual(self.manager.movies[0]["rating"], 10.0)
    
    def test_title_boundary_100_chars(self):
        """Тест 23: Название из 100 символов (допустимо)"""
        title_100 = "A" * 100
        result = self.manager.add_movie(title_100, "Action", "2020", "7.5")
        self.assertTrue(result)
        
    def test_filter_empty_list(self):
        """Тест 24: Фильтрация пустого списка"""
        filtered = self.manager.filter_movies("genre", "Action")
        self.assertEqual(len(filtered), 0)
    
    def test_filter_year_invalid(self):
        self.manager.add_movie("Movie", "Action", "2020", "7.5")
        filtered = self.manager.filter_movies("year", "invalid")
        self.assertEqual(len(filtered), 0)
    
    def test_title_with_spaces(self):
        result = self.manager.add_movie("  Test Movie  ", "Action", "2020", "7.5")
        self.assertTrue(result)
        self.assertEqual(self.manager.movies[0]["title"], "Test Movie")
    
    def test_rating_decimal(self):
        result = self.manager.add_movie("Movie", "Action", "2020", "7.95")
        self.assertTrue(result)
        self.assertEqual(self.manager.movies[0]["rating"], 7.95)

if __name__ == "__main__":
    unittest.main(verbosity=2)