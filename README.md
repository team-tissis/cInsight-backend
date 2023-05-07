# cInsightBackend

## 環境構築

postgresql にログインした状態で

```
create database cinsightdb
```

によって Database を作った後、 `config/settings.sample.py` をコピーする形で `config/settings.py` を作成して、以下の項目を編集 (パスワードを設定した場合はそれに則って編集)。

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cinsightdb',
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

> ※ もし、`relation "auth_user" does not exist` というエラーが出て token 生成に失敗するなら、
>
> ```
> python manage.py migrate auth
> ```
>
> を実行しておく。

そして、shell_plus を抜けて、

```
pipenv run server
```

を実行すれば、フロントエンドと連携できる。
