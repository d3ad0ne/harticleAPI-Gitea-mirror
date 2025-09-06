# Habr article API

This is a simple API that can be deployed on your server to access habr.com's articles content, as well as keeping a record of articles and their ratings which you can manage by connecting to corresponding endpoints.

From here on on out we will call a pair "article_url" - "rating" an **entry**.

## API Reference




### Ping

```http
  GET /api/ping
```

A basic ping endpoint.

#### Response on success

`application/json`
```json
{
  "message": "pong"
}
```



### See current entries


```http
  GET /api/rates
```

Returns all entries in the PostreSQL DB.

#### Response on success

`application/json`
```json
{
  "article_url_1": rating(0 or 1),
  "article_url_2": rating(0 or 1),
  ...
}
```



### Make a new entry


```http
  POST /api/article/rate
```

Save a new entry to the DB.

#### Request body

`application/json`
```json
{
  "url": {article_url},
  "rating": {integer, 0 or 1}
}
```


#### Response on success

`application/json`
```json
{
  "message": "success",
  "url": "{article_url}",
  "rating": {integer, 0 or 1}
}
```



### Delete an entry


```http
  POST /api/article/remove_rate
```

Delete an existing entry from the DB.

#### Request body

`application/json`
```json
{
  "url": "{article_url}"
}
```


#### Response on success

`application/json`
```json
{
  "message": "success"
}
```





### Get article html

```http
  POST /api/article/api/article/get/html
```

Get hmtl of a desired habr article body encoded in base64.

#### Request body

`application/json`
```json
{
  "url": "{article_url}"
}
```

#### Response on success

`text/plain`
```
{article_url}

{b64 encoded html}
```





### Get article MD

```http
  POST /api/article/api/article/get/md
```

Get md of a desired habr article body encoded in base64.

#### Request body

`application/json`
```json
{
  "url": "{article_url}"
}
```

#### Response on success

`text/plain`
```
{article_url}

{b64 encoded md}
```





### Get html of N articles from habr.com/feed

```http
  POST /api/article/api/articles/get/html
```

Get html bodies of N last articles from [habr.com/feed](habr.com/feed)

#### Request body

`application/json`
```json
{
  "amount": {articles_amount}
}
```

#### Response on success

`application/json`
```json
{
  "{article_url_1}": "{b64_encoded_html}",
  "{article_url_2}": "{b64_encoded_html}",
  ...
  "{article_url_n}": "{b64_encoded_html}"
}
```





### Get MD of N articles from habr.com/feed

```http
  POST /api/article/api/articles/get/html
```

Get MD of N last articles from [habr.com/feed](habr.com/feed)

#### Request body

`application/json`
```json
{
  "amount": {articles_amount}
}
```

#### Response on success

`application/json`
```json
{
  "{article_url_1}": "{b64_encoded_md}",
  "{article_url_2}": "{b64_encoded_md}",
  ...
  "{article_url_n}": "{b64_encoded_md}"
}
```