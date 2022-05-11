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

## Hugoのカスタムショートコードで使える記述方法について

ここに記載があります。

* https://gohugo.io/functions/

## Kubernetesのカスタムショートコード

Kubernetesのショートコードについては、以下に記載があります。

* https://kubernetes.io/docs/contribute/style/style-guide/#shortcodes

  スタイルガイドとして、Note, Caution, Warning の３つについての説明があります。


* https://kubernetes.io/docs/contribute/style/hugo-shortcodes/

  Kubernetesで使用できるカスタムショートコードが記載されています。

### note.html

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

* マークダウンファイル

  ```text
  {{< note >}}
  This is *note* message.
  {{< /note >}}
  ```

* Hugoで出力されるHTMLファイル

  ```html
  <div class="alert alert-info note callout" role="alert">
    <strong>Note:</strong> This is <em>note</em> message.
  </div>
  ```

### tabs.html

Kubernetesでサポートしている note.html は、2022/05/11 時点では以下のように定義されています。

```html
{{- .Page.Scratch.Add "tabset-counter" 1 -}}
{{- $tab_set_id := .Get "name" | default (printf "tabset-%s-%d" (.Page.RelPermalink) (.Page.Scratch.Get "tabset-counter") ) | anchorize -}}
{{- $tabs := .Scratch.Get "tabs" -}}
{{- if .Inner -}}{{- /* We don't use the inner content, but Hugo will complain if we don't reference it. */ -}}{{- end -}}
<ul class="nav nav-tabs" id="{{ $tab_set_id }}" role="tablist">
	{{- range $i, $e := $tabs -}}
	  {{- $id := printf "%s-%d" $tab_set_id $i -}}
	  {{- if (eq $i 0) -}}
		<li class="nav-item"><a data-toggle="tab" class="nav-link active" href="#{{ $id }}" role="tab" aria-controls="{{ $id }}" aria-selected="true">{{- trim .name " " -}}</a></li>
	  {{ else }}
		<li class="nav-item"><a data-toggle="tab" class="nav-link" href="#{{ $id }}" role="tab" aria-controls="{{ $id }}">{{- trim .name " " -}}</a></li>
	  {{- end -}}
{{- end -}}
</ul>
<div class="tab-content" id="{{ $tab_set_id }}">
{{- range $i, $e := $tabs -}}
{{- $id := printf "%s-%d" $tab_set_id $i -}}
{{- if (eq $i 0) -}}
  <div id="{{ $id }}" class="tab-pane show active" role="tabpanel" aria-labelledby="{{ $id }}">
{{ else }}
  <div id="{{ $id }}" class="tab-pane" role="tabpanel" aria-labelledby="{{ $id }}">
{{ end }}
<p>
	{{- with .content -}}
		{{- . -}}
	{{- else -}}
		{{- if eq $.Page.BundleType "leaf" -}}
			{{- /* find the file somewhere inside the bundle. Note the use of double asterisk */ -}}
			{{- with $.Page.Resources.GetMatch (printf "**%s*" .include) -}}
				{{- if ne .ResourceType "page" -}}
				{{- /* Assume it is a file that needs code highlighting. */ -}}
				{{- $codelang := $e.codelang | default ( path.Ext .Name | strings.TrimPrefix ".") -}}
				{{- highlight .Content $codelang "" -}}
				{{- else -}}
					{{- .Content -}}
				{{- end -}}
			{{- end -}}
		{{- else -}}
		{{- $path := path.Join $.Page.File.Dir .include -}}
		{{- $page := site.GetPage "page" $path -}}
		{{- with $page -}}
			{{- .Content -}}
		{{- else -}}
		{{- errorf "[%s] tabs include not found for path %q" site.Language.Lang $path -}}
		{{- end -}}
		{{- end -}}
	{{- end -}}
</div>
{{- end -}}
</div>
```


## トラブル

2022/05/11時点では、tabs + list + note で書式が乱れる事象が報告されています。

### 具体例

```text
{{< tabs name="test-tab" >}}

{{% tab name="Page-1" %}}

This is page-1.

* List-1

* List-2

  {{< note >}}
  This is note on page-1.
  {{< /note >}}

{{% /tab %}}

{{% tab name="Page-2" %}}

This is page-2.

{{% /tab %}}

{{< /tabs >}}
```

上記の記述とした場合、HTMLファイルが以下のようになります。(一部のみ抜粋し、改行やインデント等の編集を加えています)

```html
<ul class="nav nav-tabs" id="test-tab" role="tablist">
  <li class="nav-item"><a data-toggle="tab" class="nav-link active" href="#test-tab-0" role="tab" aria-controls="test-tab-0" aria-selected="true">Page-1</a></li>
  <li class="nav-item"><a data-toggle="tab" class="nav-link" href="#test-tab-1" role="tab" aria-controls="test-tab-1">Page-2</a></li>
</ul>

<div class="tab-content" id="test-tab">
  <div id="test-tab-0" class="tab-pane show active" role="tabpanel" aria-labelledby="test-tab-0">
    <p>
    <p>This is page-1.</p>
    <ul>
      <li>
        <p>List-1</p>
      </li>
      <li>
        <p>List-2</p>
        <div class="alert alert-info note callout" role="alert">
        <strong>Note:</strong> This is note on page-1.                 　<-- ここに</div> が無く
      </li>
    </ul>
        </div>                                                           <-- ここに来てしまう
  </div>
  <div id="test-tab-1" class="tab-pane" role="tabpanel" aria-labelledby="test-tab-1">
    <p>
    <p>This is page-2.</p>
  </div>
</div>
```

リストだけでは、このようなことは起きません。

```text
* List-1

* List-2

  {{< note >}}
  This is note.
  {{< /note >}}
```

上記で出力されるHTMLは以下です。

```html
<ul>
  <li>
    <p>List-1</p>
  </li>
  <li>
    <p>List-2</p>
    <div class="alert alert-info note callout" role="alert">
      <strong>Note:</strong> This is note.
    </div>                                                   <-- これは正しい位置にある
  </li>
</ul>
```
