from random import randint, choice, shuffle
from pathlib import Path
import os, csv
from string import ascii_lowercase

class WordSearch():
    EASY_MAP_LENGTH = 10
    EASY_MAP_WIDTH  = 10
    MEDIUM_MAP_WIDTH = 10
    MEDIUM_MAP_LENGTH = 20
    HARD_MAP_WIDTH = 10
    HARD_MAP_LENGTH = 20
    VERY_HARD_MAP_WIDTH = 10
    VERY_HARD_MAP_LENGTH = 20

    def __init__(self, cwd_path:Path=None):
        self.folder_path = Path(os.path.dirname(os.path.abspath(__file__))) if cwd_path is None else cwd_path
        self.word_search_file_path = None
        self.word_search_answer_file_path = None
        self.used_words_file_path = None
        self.search_words = []
        self.longest_word_len = 0
        self.map_width =  0
        self.map_length = 0
        self.word_map = []
        self.n_coords = 0
        self.map_vectors = [(1,1), (-1,1), (-1,-1), (1,-1), (0,1), (0,-1), (1,0), (-1,0)]
        self.inserted_words = []

    def generate(self, words:list, difficulty:str):
        self.inserted_words = []
        self.search_words = words
        self.longest_word_len = len(max(self.search_words))
        self.set_map_dimensions(difficulty)
        self.word_map = self.initialize_word_map()
        self.n_coords = self.map_length*self.map_width
        self.set_file_paths(difficulty)
        self.insert_search_words_to_map()
        self.output_word_search_to_file(self.word_search_answer_file_path)
        self.output_used_words_to_file()
        self.insert_rand_letters_into_word_search()
        self.output_word_search_to_file(self.word_search_file_path)
        
    def initialize_word_map(self) -> list:
        return [[""]*self.map_width for _ in range(self.map_length)]

    def set_map_dimensions(self, difficulty:str):
        if difficulty == "easy":
            width = self.EASY_MAP_WIDTH
            length = self.EASY_MAP_LENGTH
        elif difficulty == "medium":
            width = self.MEDIUM_MAP_WIDTH
            length = self.MEDIUM_MAP_LENGTH
        elif difficulty == "hard":
            width = self.HARD_MAP_WIDTH
            length = self.HARD_MAP_LENGTH
        else:
            width = self.VERY_HARD_MAP_WIDTH
            length = self.VERY_HARD_MAP_LENGTH
        self.initialize_map_dimensions(width, length)

    def initialize_map_dimensions(self, default_width:int, default_height:int):
        self.map_width = default_width if default_width > self.longest_word_len else self.longest_word_len
        self.map_length = default_height if default_height > self.longest_word_len else self.longest_word_len

    def set_file_paths(self, difficulty:str):
        self.word_search_file_path = self.folder_path / f"word_search_{difficulty}.csv"
        self.word_search_answer_file_path = self.folder_path / f"word_search_{difficulty}_answer.csv"
        self.used_words_file_path = self.folder_path / f"used_words_{difficulty}.txt"

    def insert_search_words_to_map(self):
        for word in self.search_words:
            generated_coords = []
            for _ in range(self.n_coords):
                word_coord = self.generate_rand_coord(generated_coords)
                generated_coords.append(word_coord)
                if not self.is_usable_coord(word_coord, word):
                    continue
                is_word_inserted = self.insert_search_word_to_map(word_coord, word)
                if is_word_inserted:
                    self.inserted_words.append(word)
                    break
                
    def generate_rand_coord(self, generated_coords:list) -> tuple:
        rand_coord = (randint(0,self.map_length-1), randint(0,self.map_width-1))
        while(rand_coord in generated_coords):
            rand_coord = (randint(0,self.map_length-1), randint(0,self.map_width-1))
        return rand_coord

    def is_usable_coord(self, coord:tuple, word:str) -> bool:
        map_value = self.word_map[coord[0]][coord[1]]
        if map_value == "" or map_value == word[0]:
            return True
        return False

    def insert_search_word_to_map(self, coord:tuple, word:str) -> bool:
        shuffle(self.map_vectors)
        for vector in self.map_vectors:
            if not self.is_valid_direction(vector, coord, word):
                continue
            current_coord = list(coord)
            for letter in word:
                self.word_map[current_coord[0]][current_coord[1]] = letter
                current_coord[0] += vector[0]
                current_coord[1] += vector[1]
            return True
        return False

    def is_valid_direction(self, vector:tuple, coord:tuple, word:str) -> bool:
        if not self.can_fit_word(vector, coord, word):
            return False
        if self.has_letter_conflict(vector, coord, word):
            return False
        return True
        
    def can_fit_word(self, vector:tuple, coord:tuple, word:str) -> bool:
        # Subtract 1 to make the starting length of the word 0
        word_len = len(word)-1
        end_coord = (coord[0]+vector[0]*word_len, coord[1]+vector[1]*word_len)
        if end_coord[0] >= self.map_length or end_coord[0] < 0:
            return False
        if end_coord[1] >= self.map_width or end_coord[1] < 0:
            return False
        return True
    
    def has_letter_conflict(self, vector:tuple, coord:tuple, word:str) -> bool:
        current_coord = list(coord)
        for letter in word:
            map_letter = self.word_map[current_coord[0]][current_coord[1]]
            if not(letter == map_letter or map_letter == ""):
                return True
            current_coord[0] += vector[0]
            current_coord[1] += vector[1]
        return False
    
    def output_word_search_to_file(self, file_path:Path):
        with open(file_path, mode="w", newline="") as f:
            csv_writer = csv.writer(f)
            for map_row in self.word_map:
                csv_writer.writerow(map_row)

    def output_used_words_to_file(self):
        output_str = ",".join(self.inserted_words)
        with open(self.used_words_file_path, mode="w") as f:
            f.writelines(output_str)

    def insert_rand_letters_into_word_search(self):
        for row_i, map_row in enumerate(self.word_map):
            for col_i, letter in enumerate(map_row):
                if letter == "":
                    self.word_map[row_i][col_i] = choice(ascii_lowercase)

if __name__ == "__main__":
    word_search = WordSearch()
    words = ["cat","dog","hamster","parrot","mouse"]
    word_search.generate(words,"medium")
