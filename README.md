# CInsight Backend

## 環境構築
postgresql で Database を作って、
settings.py の以下を編集。
database やパスワードを設定した場合はそれに則って編集。

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'c-insightdb',
        'USER': 'your_user_name',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

その後、

```
pipenv install
pipenv shell
python manage.py makemigrations api
python manage.py migrate api
```

を実行し、マイグレーションを行う。続いて、

```
python manage.py shell_plus
```

を実行し、起動したら、

```
>>> User(username="hoge").save()
>>> user = User.objects.first()
>>> Token.objects.get_or_create(user=user)
>>> Token.objects.first()
```

これで token が生成されるので、この token をクリップボードにコピーして、
daofication の React のレポジトリの.env.development に、

```
REACT_APP_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

という形でペースト。

そして、shell_plus を抜けて、

```
pipenv run server
```

を実行すれば、フロントエンドと連携できる。
