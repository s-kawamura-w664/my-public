# hugo-shortcodeで作られたapi-referenceショートコードについて

https://github.com/kubernetes/website/pull/34272 にて、api-reference ショートコードを修正しましたので、その概要を説明します。

## api-referenceショートコードとは

k8s のwebsiteは、mdファイルで記述した文書をHugoがHTMLに変換して表示しています。
ショートコードとは、mdファイルに記述できる拡張構文のようなものです。

具体的には、以下の様な記述が可能です。

```md
詳細は、{{< api-reference page="workload-resources/pod-v1" anchor="PodSpec" >}}や{{< api-reference page="workload-resources/pod-v1" anchor="environment-variables"  text="Environment Variable">}}のAPIリファレンスを参照ください。
```

これをドキュメントサイトで見ると、以下の様なイメージで表示されます。

```html
詳細は、<a href=>docs/reference/kubernetes-api/workload-resources/pod-v1/#PodSpec>PodSpec</a> や <a href=>docs/reference/kubernetes-api/workload-resources/pod-v1/#environment-variables>Environment Variable</a>のAPIリファレンスを参照ください。
```

api-referenceショートコードでは、具体的に以下の様な記述が可能です。

1. {{< api-reference page="workload-resources/pod-v1" >}}
2. {{< api-reference page="workload-resources/pod-v1" anchor="PodSpec" >}}
3. {{< api-reference page="workload-resources/pod-v1" anchor="environment-variables" text="Environment Variable" >}}

上記はWebSite上では以下のように表示されます。

|項番    |表示     |ハイパーリンク|備考  |
|---|---|---|---|
|1|Pod |https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/ |表示文字列はリンク先のMetadata.Kind |
|2|PodSpec |https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#PodSpec |表示文字列はanchorパラメータ |
|3|Environment Variable |https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#environment-variables |表示文字列はtextパラメータ|

ショートコードが展開されると以下の様なHTMLになります。

`<a href="[ハイパーリンク先URL]#[anchorパラメータ]">[textパラメータ(or anchorパラメータ or metadata.kind)]</a>`

## layouts/shortcodes/api-reference.html

### 修正前

```html
{{ $base := "docs/reference/kubernetes-api" }}
{{ $pageArg := .Get "page" }}
{{ $anchorArg := .Get "anchor" }}
{{ $textArg := .Get "text" }}
{{ $page := site.GetPage "page" (printf "%s/%s" $base $pageArg) }}
{{ $metadata := $page.Params.api_metadata }}
<a href="{{ $page.RelPermalink }}{{if $anchorArg}}#{{ $anchorArg }}{{end}}">{{if $textArg}}{{ $textArg }}{{else if $anchorArg}}{{ $anchorArg }}{{else}}{{ $metadata.kind }}{{end}}</a> 
```

### 修正後

```html
{{ $base := "docs/reference/kubernetes-api" }}
{{ $pageArg := .Get "page" }}
{{ $anchorArg := .Get "anchor" }}
{{ $textArg := .Get "text" }}
{{ $pagePath := path.Join $base $pageArg }}
{{ $page := site.GetPage "page" $pagePath }}
{{ with $page }}{{else}}{{ range where site.Home.AllTranslations "Language.Lang" "en" }}{{ $page = .Site.GetPage "page" $pagePath }}{{ end }}{{ end }}
{{ $metadata := $page.Params.api_metadata }}
<a href="{{ $page.RelPermalink }}{{if $anchorArg}}#{{ $anchorArg }}{{end}}">{{if $textArg}}{{ $textArg }}{{else if $anchorArg}}{{ $anchorArg }}{{else}}{{ $metadata.kind }}{{end}}</a> 
```

### 差分

```diff
 {{ $base := "docs/reference/kubernetes-api" }}
 {{ $pageArg := .Get "page" }}
 {{ $anchorArg := .Get "anchor" }}
 {{ $textArg := .Get "text" }}
-{{ $page := site.GetPage "page" (printf "%s/%s" $base $pageArg) }}
+{{ $pagePath := path.Join $base $pageArg }}
+{{ $page := site.GetPage "page" $pagePath }}
+{{ with $page }}{{else}}{{ range where site.Home.AllTranslations "Language.Lang" "en" }}{{ $page = .Site.GetPage "page" $pagePath }}{{ end }}{{ end }}
 {{ $metadata := $page.Params.api_metadata }}
 <a href="{{ $page.RelPermalink }}{{if $anchorArg}}#{{ $anchorArg }}{{end}}">{{if $textArg}}{{ $textArg }}{{else if $anchorArg}}{{ $anchorArg }}{{else}}{{ $metadata.kind }}{{end}}</a>
```

## 説明

* 基本的に golang に準拠
* `{{ }}` で囲むとその中に golang っぽく処理が記述できます。それ以外は、htmlコードとして扱われます。

```
{{ $base := "docs/reference/kubernetes-api" }}
⇒　固定文字列の代入。APIリファレンスのルートURL

{{ $pageArg := .Get "page" }}
⇒　ショートコード指定のpageパラメータを取得。
　　具体例では、{{< api-reference page="workload-resources/pod-v1" anchor="environment-variables" text="Environment Variable" >}} と書いた場合の"page="の部分

{{ $anchorArg := .Get "anchor" }}
⇒　ショートコード指定のanchorパラメータを取得。

{{ $textArg := .Get "text" }}
⇒　ショートコード指定のいtextパラメータを取得。

{{ $pagePath := path.Join $base $pageArg }}
⇒　APIリファレンスのルートURL と pageパラメータを結合
　　具体例では、"docs/reference/kubernetes-api/workload-resources/pod-v1" となります。

{{ $page := site.GetPage "page" $pagePath }}
⇒　現在の(言語の)Webサイトの"docs/reference/kubernetes-api/workload-resources/pod-v1"のページ内容を取得します。
　　ページが存在しない場合はnilになります。

{{ with $page }}{{else}}{{ range where site.Home.AllTranslations "Language.Lang" "en" }}{{ $page = .Site.GetPage "page" $pagePath }}{{ end }}{{ end }}
⇒　nilの場合に処理します。
　　すべての翻訳ページから、"Lang=en"を探して、その(言語の)Webサイトのリンク先を取得します。
　　具体例では、"en/docs/reference/kubernetes-api/workload-resources/pod-v1"のページ内容を取得します。

{{ $metadata := $page.Params.api_metadata }}
⇒　取得したリンク先ページのmetadataを取得します。

<a href="{{ $page.RelPermalink }}{{if $anchorArg}}#{{ $anchorArg }}{{end}}">{{if $textArg}}{{ $textArg }}{{else if $anchorArg}}{{ $anchorArg }}{{else}}{{ $metadata.kind }}{{end}}</a> 
⇒　この行は{{}}で囲まれていませんので、HTML記述のまま展開されます。
　　$page.RelPermalink で相対的なのリンク先URLになります。
```
