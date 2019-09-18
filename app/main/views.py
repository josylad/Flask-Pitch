from flask import render_template, request, Blueprint
from app.models import Post


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.posted_date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

