## 進捗

### ~ 2020/12/01

* [Djagno Girls](https://tutorial.djangogirls.org/ja/)  
* [Django公式](https://docs.djangoproject.com/ja/2.2/intro/) 

上記のチュートリアルを終了し，ブログ開発をはじめる。  
最終的にはレポートや学習時のメモを投稿できればと考えている。  


チュートリアル自体は他のWebフレームワークを触ったことがあったため問題なく進んだが， 
テストについてはあまり書いたことがなかったため

* [Test-Driven Django Development](https://test-driven-django-development.readthedocs.io/en/latest/)
* [テスト駆動開発(書籍)](https://books.google.co.jp/books/about/%E3%83%86%E3%82%B9%E3%83%88%E9%A7%86%E5%8B%95%E9%96%8B%E7%99%BA.html?id=HHA9DwAAQBAJ&printsec=frontcover&source=kp_read_button&redir_esc=y#v=onepage&q&f=false)

を参考に開発に取り組んだ。


今後は，チュートリアルではあまり触れられなかったユーザー認証や管理についての基本的な流れをつかみたいと考えている。


## スケジュール

* 11 / 11 ~ テスト駆動について学習
* 11 / 15 ~ 設計, UMLなど作成
* 11 / 17 ~ 開発開始 　[【GitHub】Commits](https://github.com/TeppeiHayashi/django-blog/commits/master)




## 制作物について

### 開発環境

* Python 3.7.0
* Django 2.2.4

その他ライブラリやバージョンなどは requirements.txt に記載。


### 実現したいこと

* 記事のCRUDなどの一般的なブログサービス機能。
* 記事はMarkdown形式で記述。
* プログラムコードをハイライトしたい。


### 概要

管理者とそれ以外のユーザ（以下閲覧者と呼ぶ）で区分される。  
[管理者 ⊂ 閲覧者]であり，閲覧者ができることは管理者でもできる。
開発前にあらかじめ作成したユースケース図とER図を以下に示す。
個人開発では，これらを頭で済ませることも多かったので，慣れるために作成。


#### ユースケース図

![usecase_diagram](https://user-images.githubusercontent.com/43464529/100595044-c2d9b000-333d-11eb-9095-070070d2c7df.png)

  
  
#### ER図（物理モデル）

![er_diagram](https://user-images.githubusercontent.com/43464529/100705453-8f089400-33ea-11eb-8e15-4f1d93607289.png)


#### 管理者

* 管理者はログインが必要。
* 管理者は[記事の投稿,編集,削除,公開/非公開設定] [コメントの承認]ができる。

#### 閲覧者

* 記事の閲覧，検索ができる。  
このとき（管理者：すべての記事）（閲覧者：公開済みの記事）が対象となる。
* コメントを投稿できる。
* コメントを閲覧できる。  
このとき（管理者：すべてのコメント）（閲覧者：承認済みのコメント）が対象となる。

### 開発中イメージ

CSSやJSは以前PHPで途中まで作成していたものから流用。

![django-blog-demo](https://user-images.githubusercontent.com/43464529/100710445-13f7ab80-33f3-11eb-95d5-559e4e704e30.gif)


## 参考リンク

### PlantUML

ユースケース図，ER図の作成に利用。
UMLに限らず様々な図をテキストで記述できる。

* [公式](https://plantuml.com/ja/)
* [Visual Studio Code で UML を描こう！ - Qiita](https://qiita.com/couzie/items/9dedb834c5aff09ea7b2#2-%E7%94%BB%E5%83%8F%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%A8%E3%81%97%E3%81%A6%E5%87%BA%E5%8A%9B)
