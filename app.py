from flask import Flask, render_template, request, redirect, url_for, flash
from collections import deque

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False

class Library:
    def __init__(self):
        self.books = []
        self.borrowed_books = []
        self.undo_stack = []
        self.borrow_queue = deque()

    def add_book(self, title, author):
        book = Book(title, author)
        self.books.append(book)

    def issue_book(self, title):
        for book in self.books:
            if book.title == title and not book.is_borrowed:
                book.is_borrowed = True
                self.borrowed_books.append(book)
                return True
        return False

    def return_book(self, title):
        
        for book in self.borrowed_books:
            if book.title == title:
                book.is_borrowed = False
                self.borrowed_books.remove(book)
                self.undo_stack.append(book)
                return True
        return False

    def view_borrowed_books(self):
        return self.borrowed_books

    def undo_return(self):
        if self.undo_stack:
            book = self.undo_stack.pop()
            book.is_borrowed = True
            self.borrowed_books.append(book)

library = Library()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        library.add_book(title, author)
        flash(f'Added: {title} by {author}')
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        title = request.form['title']
        if library.issue_book(title):
            flash(f'Issued: {title}')
        else:
            flash(f'Book "{title}" is not available.')
        return redirect(url_for('index'))
    return render_template('issue_book.html')

@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        title = request.form['title']
        if library.return_book(title):
            flash(f'Returned: {title}')
        else:
            flash(f'Book "{title}" was not borrowed.')
        return redirect(url_for('index'))
    return render_template('return_book.html')

@app.route('/view_borrowed')
def view_borrowed():
    borrowed_books = library.view_borrowed_books()
    return render_template('view_borrowed.html', borrowed_books=borrowed_books)

@app.route('/undo_return')
def undo_return():
    library.undo_return()
    flash('Last return operation undone.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)