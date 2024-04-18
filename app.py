from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_posts():
    with open('posts.json', 'r') as file:
        posts = json.load(file)
        for post in posts:
            post.setdefault('likes', 0)
    return posts

posts = load_posts()

def save_posts(posts):
    with open('posts.json', 'w') as file:
        json.dump(posts, file)

@app.route('/')
def home():
    return render_template('index.html', posts=posts)

# Global variable to keep track of the next available ID
next_post_id = 3  # Assuming you already have two posts with IDs 1 and 2

@app.route('/add', methods=['GET', 'POST'])
def add():
    global next_post_id  # Use the global variable inside the function

    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        new_post = {
            'id': next_post_id,
            'author': author,
            'title': title,
            'content': content
        }

        next_post_id += 1

        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for('home'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            break

    save_posts(posts)
    return redirect(url_for('home'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        save_posts(posts)
        return redirect(url_for('home'))

    return render_template('update.html', post=post)

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)

    if post is None:
        return "Post not found", 404

    post['likes'] += 1
    save_posts(posts)
    return redirect('/')

if __name__ == '__main__':
    app.run()
