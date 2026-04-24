import json
import os
from typing import List, Dict, Any
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from movie_manager import MovieManager

class MovieLibraryApp:
    """Графический интерфейс приложения Movie Library"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("1100x700")
        
        # Центрирование окна
        self.center_window()
        
        self.movie_manager = MovieManager()
        self.current_filter = "all"
        self.filter_value = None
        
        self.setup_ui()
        self.refresh_movie_list()
        self.update_genre_filter()
        self.update_statistics()
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = 1100
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка растяжения
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # === Панель добавления фильма ===
        add_frame = ttk.LabelFrame(main_frame, text="➕ Добавить новый фильм", padding="15")
        add_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        add_frame.columnconfigure(1, weight=1)
        
        # Название
        ttk.Label(add_frame, text="Название:*", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.title_entry = ttk.Entry(add_frame, width=50, font=("Arial", 10))
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.title_entry.focus()
        
        # Жанр
        ttk.Label(add_frame, text="Жанр:*", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.genre_entry = ttk.Entry(add_frame, width=50, font=("Arial", 10))
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Год
        year_frame = ttk.Frame(add_frame)
        year_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Год выпуска:*", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.year_entry = ttk.Entry(year_frame, width=15, font=("Arial", 10))
        self.year_entry.grid(row=0, column=0, padx=(0, 10))
        self.year_entry.insert(0, "2024")
        
        ttk.Label(year_frame, text="(1888-2024)", font=("Arial", 8, "italic")).grid(row=0, column=1, sticky=tk.W)
        
        # Рейтинг
        rating_frame = ttk.Frame(add_frame)
        rating_frame.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Рейтинг (0-10):*", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.rating_entry = ttk.Entry(rating_frame, width=15, font=("Arial", 10))
        self.rating_entry.grid(row=0, column=0, padx=(0, 10))
        self.rating_entry.insert(0, "7.5")
        
        self.rating_scale = ttk.Scale(rating_frame, from_=0, to=10, orient=tk.HORIZONTAL, length=150, command=self.update_rating)
        self.rating_scale.grid(row=0, column=1, padx=(0, 10))
        self.rating_scale.set(7.5)
        
       
        add_btn = ttk.Button(add_frame, text="Добавить фильм", command=self.add_movie)
        add_btn.grid(row=4, column=0, columnspan=2, pady=15)
        
     
        ttk.Label(add_frame, text="* - обязательные поля", font=("Arial", 8, "italic"), foreground="gray").grid(row=5, column=0, columnspan=2)
        
     
        filter_frame = ttk.LabelFrame(main_frame, text="🔍 Фильтрация", padding="10")
        filter_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Кнопки быстрой фильтрации
        btn_frame = ttk.Frame(filter_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(btn_frame, text="📋 Все фильмы", command=lambda: self.apply_filter("all")).pack(side=tk.LEFT, padx=5)
        
        # Фильтр по жанру
        genre_filter_frame = ttk.Frame(filter_frame)
        genre_filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(genre_filter_frame, text="Фильтр по жанру:", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        self.genre_filter_combo = ttk.Combobox(genre_filter_frame, width=20, state="readonly")
        self.genre_filter_combo.pack(side=tk.LEFT, padx=5)
        ttk.Button(genre_filter_frame, text="🔍 Применить", command=lambda: self.apply_filter("genre", self.genre_filter_combo.get())).pack(side=tk.LEFT, padx=5)
        
      
        year_filter_frame = ttk.Frame(filter_frame)
        year_filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(year_filter_frame, text="Фильтр по году:", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        self.year_filter_entry = ttk.Entry(year_filter_frame, width=10)
        self.year_filter_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(year_filter_frame, text="🔍 Применить", command=lambda: self.apply_filter("year", self.year_filter_entry.get())).pack(side=tk.LEFT, padx=5)
        
        # Кнопка сброса
        ttk.Button(filter_frame, text="🔄 Сбросить все фильтры", command=self.reset_filters).pack(pady=10)
        
        # === Таблица с фильмами ===
        list_frame = ttk.LabelFrame(main_frame, text="🎬 Моя коллекция фильмов", padding="10")
        list_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Создание таблицы
        columns = ("ID", "Название", "Жанр", "Год", "Рейтинг", "Дата добавления")
        self.movie_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Настройка колонок
        col_widths = {"ID": 50, "Название": 300, "Жанр": 150, "Год": 80, "Рейтинг": 120, "Дата добавления": 150}
        for col in columns:
            self.movie_tree.heading(col, text=col)
            self.movie_tree.column(col, width=col_widths.get(col, 100))
        
        self.movie_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
      
        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.movie_tree.yview)
        scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.movie_tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.movie_tree.xview)
        scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.movie_tree.configure(xscrollcommand=scrollbar_x.set)
        
     
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, pady=(0, 10))
        
        ttk.Button(control_frame, text="🗑 Удалить выбранный фильм", command=self.delete_movie).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="ℹ️ Информация о фильме", command=self.show_movie_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🔄 Обновить список", command=self.refresh_movie_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="📊 Экспорт статистики", command=self.export_statistics).pack(side=tk.LEFT, padx=5)
        

        stats_frame = ttk.LabelFrame(main_frame, text="📊 Статистика коллекции", padding="10")
        stats_frame.grid(row=4, column=0, sticky=(tk.W, tk.E))
        
        self.stats_label = ttk.Label(stats_frame, text="Загрузка...", font=("Arial", 10))
        self.stats_label.pack()
        
        # Статусная строка
        self.status_label = ttk.Label(main_frame, text="✅ Готов к работе", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Привязка событий
        self.movie_tree.bind('<Delete>', lambda e: self.delete_movie())
        self.movie_tree.bind('<Double-Button-1>', lambda e: self.show_movie_details())
        self.root.bind('<Return>', lambda e: self.add_movie())
    
    def update_rating(self, value):
        """Обновление поля рейтинга при перемещении слайдера"""
        self.rating_entry.delete(0, tk.END)
        self.rating_entry.insert(0, f"{float(value):.1f}")
    
    def update_genre_filter(self):
        """Обновление списка жанров в фильтре"""
        genres = self.movie_manager.get_unique_genres()
        self.genre_filter_combo['values'] = [""] + genres if genres else [""]
        if genres:
            self.genre_filter_combo.set("")
    
    def add_movie(self):
        """Добавление нового фильма"""
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()
        rating = self.rating_entry.get()
        
        try:
            self.movie_manager.add_movie(title, genre, year, rating)
            messagebox.showinfo("Успех! 🎉", f"Фильм \"{title}\" успешно добавлен в коллекцию!")
            self.clear_input_fields()
            self.refresh_movie_list()
            self.update_genre_filter()
            self.update_statistics()
            self.status_label.config(text=f"✅ Добавлен фильм: {title}")
        except ValueError as e:
            messagebox.showerror("Ошибка валидации ❌", str(e))
            self.status_label.config(text=f"❌ Ошибка: {str(e)}")
    
    def delete_movie(self):
        """Удаление выбранного фильма"""
        selected = self.movie_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение ⚠️", "Выберите фильм для удаления")
            return
        
        movie_id = int(self.movie_tree.item(selected[0])['values'][0])
        movie_title = self.movie_tree.item(selected[0])['values'][1]
        
        if messagebox.askyesno("Подтверждение", f"Удалить фильм \"{movie_title}\" из коллекции?"):
            self.movie_manager.delete_movie(movie_id)
            self.refresh_movie_list()
            self.update_genre_filter()
            self.update_statistics()
            self.status_label.config(text=f"🗑 Удалён фильм: {movie_title}")
            messagebox.showinfo("Удаление", f"Фильм \"{movie_title}\" удалён")
    
    def apply_filter(self, filter_type, value=None):
        """Применение фильтрации"""
        if filter_type == "genre":
            if not value or value == "":
                messagebox.showwarning("Предупреждение ⚠️", "Выберите жанр для фильтрации")
                return
        elif filter_type == "year":
            if value and not value.isdigit():
                messagebox.showerror("Ошибка ❌", "Год должен быть числом")
                return
            if value and (int(value) < 1888 or int(value) > 2024):
                messagebox.showerror("Ошибка ❌", "Год должен быть от 1888 до 2024")
                return
        
        self.current_filter = filter_type
        self.filter_value = value
        self.refresh_movie_list()
        
        if filter_type == "all":
            self.status_label.config(text="📋 Показаны все фильмы")
        elif filter_type == "genre":
            self.status_label.config(text=f"🎭 Показаны фильмы жанра: {value}")
        elif filter_type == "year":
            self.status_label.config(text=f"📅 Показаны фильмы {value} года")
    
    def reset_filters(self):
        """Сброс всех фильтров"""
        self.current_filter = "all"
        self.filter_value = None
        self.genre_filter_combo.set('')
        self.year_filter_entry.delete(0, tk.END)
        self.refresh_movie_list()
        self.status_label.config(text="🔄 Фильтры сброшены, показаны все фильмы")
    
    def refresh_movie_list(self):
        """Обновление списка фильмов в таблице"""
        # Очистка таблицы
        for item in self.movie_tree.get_children():
            self.movie_tree.delete(item)
        
        # Получение отфильтрованных фильмов
        movies = self.movie_manager.filter_movies(self.current_filter, self.filter_value)
        
        # Заполнение таблицы
        for movie in movies:
            # Визуализация рейтинга звёздами
            rating_value = movie["rating"]
            stars = "⭐" * int(rating_value) + "☆" * (10 - int(rating_value))
            rating_display = f"{rating_value:.1f} {stars}"
            
            item = self.movie_tree.insert("", tk.END, values=(
                movie["id"],
                movie["title"],
                movie["genre"],
                movie["year"],
                rating_display,
                movie["added_date"][:10]
            ))
            
            # Цветовая индикация
            if rating_value >= 8:
                self.movie_tree.tag_configure("high_rating", background="#d4edda", foreground="#155724")
                self.movie_tree.item(item, tags=("high_rating",))
            elif rating_value <= 4:
                self.movie_tree.tag_configure("low_rating", background="#f8d7da", foreground="#721c24")
                self.movie_tree.item(item, tags=("low_rating",))
        
        # Информация о количестве
        filter_info = ""
        if self.current_filter == "genre" and self.filter_value:
            filter_info = f" (жанр: {self.filter_value})"
        elif self.current_filter == "year" and self.filter_value:
            filter_info = f" (год: {self.filter_value})"
        
        self.status_label.config(text=f"📊 Найдено фильмов: {len(movies)}{filter_info}")
    
    def update_statistics(self):
        """Обновление статистики"""
        stats = self.movie_manager.get_statistics()
        
        stats_text = f"📊 Всего фильмов: {stats['total']} | "
        stats_text += f"⭐ Средний рейтинг: {stats['avg_rating']}/10"
        
        if stats['genre_count']:
            top_genre = max(stats['genre_count'], key=stats['genre_count'].get)
            top_count = stats['genre_count'][top_genre]
            stats_text += f" | 🎭 Популярный жанр: {top_genre} ({top_count} шт.)"
        
        self.stats_label.config(text=stats_text)
    
    def show_movie_details(self):
        """Показ детальной информации о фильме"""
        selected = self.movie_tree.selection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите фильм для просмотра деталей")
            return
        
        values = self.movie_tree.item(selected[0])['values']
        
        details = f"""
        
    📽 ДЕТАЛЬНАЯ ИНФОРМАЦИЯ О ФИЛЬМЕ 
    
 Название: {values[1]}
 Жанр: {values[2]}
 Год выпуска: {values[3]}
 Рейтинг: {values[4]}
 Дата добавления: {values[5]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Совет: Используйте фильтрацию для поиска
   фильмов по жанру или году выпуска
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        messagebox.showinfo("Информация о фильме", details)
    
    def export_statistics(self):
        """Экспорт статистики в текстовый файл"""
        from datetime import datetime
        
        stats = self.movie_manager.get_statistics()
        
        export_text = f"""
MOVIE LIBRARY - СТАТИСТИКА КОЛЛЕКЦИИ
=====================================
Дата экспорта: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

 ОСНОВНАЯ СТАТИСТИКА:
   • Всего фильмов: {stats['total']}
   • Средний рейтинг: {stats['avg_rating']}/10

 РАСПРЕДЕЛЕНИЕ ПО ЖАНРАМ:
"""
        for genre, count in stats['genre_count'].items():
            export_text += f"   • {genre}: {count} фильм(ов)\n"
        
        export_text += f"""
 СПИСОК ВСЕХ ФИЛЬМОВ:
"""
        for movie in self.movie_manager.movies:
            export_text += f"   • {movie['title']} ({movie['year']}) - {movie['genre']} - Рейтинг: {movie['rating']}/10\n"
        
        try:
            filename = f"movie_library_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(export_text)
            messagebox.showinfo("Экспорт завершён", f"Статистика экспортирована в файл:\n{filename}")
            self.status_label.config(text=f"📁 Статистика экспортирована в {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {e}")
    
    def clear_input_fields(self):
        """Очистка полей ввода"""
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.year_entry.insert(0, "2024")
        self.rating_entry.delete(0, tk.END)
        self.rating_entry.insert(0, "7.5")
        self.rating_scale.set(7.5)
        
       
        self.title_entry.focus()
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()
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
