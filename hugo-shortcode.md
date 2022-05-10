# Hugo ショートコード

## ショートコード

* Hugo は、markdownを基本としているが、ショートコードをいう機能で拡張表現を提供しています。
* カスタムショートコードを作成することで、プロジェクト固有の拡張も可能です。
* Kubernetesでも独自のショートコードをサポートしており、以下にその定義ファイルがあります。

  https://github.com/kubernetes/website/tree/main/layouts/shortcodes 

* カスタムショートコードは、ファイル名がその定義名を示しています。例えば、note.html の定義は、以下のように利用することができます。

  ```text
  {{< note >}}
  補足メッセージをここに書きます
  {{< /note >}}
  ```

* ショートコードを利用する場合には、`{{< shortcode-name >}}` という記述が多く使用されていますが、`{{% shortcode-name %}}` という記述も可能です。

## note.html

Kubernetesでサポートしている note.html は、2022/05/11 時点では以下のように定義されています。

```html
<div class="alert alert-info note callout" role="alert">
  <strong>{{ T "note" }}</strong> {{ trim .Inner " \n" | markdownify }}
</div>
```

簡単に解説します。
* `.Inner` は、`{{< note >}}` ～ `{{< /note >}}` で囲まれた中身です。
* markdownify は、マークダウンの構文解析を実施するコマンドです。
* つまり、この定義は以下の様な内容になります。
  * <div>～</div>で囲ったブロックを作ります
  * その中身には、「**note** メッセージ」という文字列になります。
  * メッセージ部分には、`{{< note >}}` ～ `{{< /note >}} で囲まれた文字列から改行文字を削除しメッセージを表示します。
  * メッセージ部分には、マークダウンの書式を指定することも可能です。

実際にマークダウンファイルに note を記述すると以下のようになります。

```markdown
{{< note >}}
This is *note* message.
{{< /note >}}
```

```html
<div class="alert alert-info note callout" role="alert">
  <strong>Note:</strong> This is <em>note</em> message.
</div>
```


