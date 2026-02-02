import os

from flask import Flask, render_template

def create_app(test_config=None):
    # アプリ作成と初期設定
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'library.sqlite'),
    )

    if test_config is None:
        # インスタンス設定ファイルがある場合は読み込む
        app.config.from_pyfile('config.py', silent=True)
    else:
        # テスト用設定の読み込み
        app.config.from_mapping(test_config)

    # インスタンスフォルダの作成（DB保存用）
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # データベースの初期設定
    from . import db
    db.init_app(app)

    # 各機能のBlueprint登録
    from . import auth
    app.register_blueprint(auth.bp)

    from . import books
    app.register_blueprint(books.bp)
    
    from . import loans
    app.register_blueprint(loans.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
