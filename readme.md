<h1 align="center">Project ScrapeBook</h1>

<p align="left">This is my first project to learn the basics of Python, Git, GitHub and a Terminal. It contains three scripts that read book informations from the website "https://books.toscrape.com/" and saves them in a *.csv file.

- SingleBook.py<br>
Reads book informations for one book and stores them in the file "single_book.csv" inside the subfolder "SingleBook".

- CategoryBooks.py<br>
Reads book informations for a category and stores them in the file "category_books.csv" inside the subfolder "CategoryBook".

- AllBooks.py<br>
Reads book informations for the entire website "https://books.toscrape.com/" and stores them in the file "category name_books.csv" in the respective subfolders "category name". Additionally, the covers of the books are stored in the same folder.
</p>

## Prerequisite

- [Python](https://www.python.org/ "Python") Installed

## Installation Steps

1. Clone the repository

```Bash
git clone https://github.com/aschickhoff/ScrapeBook.git
```

2. Change the working directory

```Bash
cd ScrapeBook
```

3. Add needed packages to run the scripts

```Bash
pip install -r requirements.txt
```

4. Run the script using terminal

```Bash
python SingleBook.py
```

```Bash
python CategoryBooks.py
```

```Bash
python AllBooks.py
```
