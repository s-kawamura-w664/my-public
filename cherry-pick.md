# Cherry Pick の方針についてのまとめ

以下のURLの内容を翻訳して、整理したものです。

<https://github.com/kubernetes/community/blob/master/contributors/devel/sig-release/cherry-picks.md>

## 前提条件

* masterブランチにマージ済みであること
* リリースブランチがあること（例:release-1.18）
* kubernetes の GitHubにPushする環境があること
* GitHub CLI (gh) がインストールされていること

後述しますが、Cherry Pickを作成するためのシェルが用意されており、そのシェルは、Cherry PickのPRを作成するところまで実施してくれます。
そのため、GitHubへのPush環境が必要であり、PRを作成するために gh が必要となっています。

## Cherry Pick に望ましいPRとは

以下の様な重大なバグを修正したものに重点を置いて対処しています。

* データの消失
* メモリ破壊
* パニック、クラッシュ、ハング
* セキュリティ

もし、Cherry Pickを提案していて、それが重要なバグフィックスであることが明確でない場合には、PRを補足してください。

* 問題の詳細が記載されたIssue
* 変更の範囲
* 変更のリスク
* 関連するリグレッションのリスク
* テストケースの追加と実施
* 主要なSIGステークホルダーのレビューア／アプルーバが、バックポートが必要であると確信していること

## Cherry Pick を作る

1. Cherry Pick スクリプトを実行します (https://git.k8s.io/kubernetes/hack/cherry_pick_pull.sh)
2. マージには通常のルール(レビュー＆承認)が適用されますが、追加の注意事項があります。

# Cherry Pick スクリプト

## 環境変数

* DRY_RUN
* REGENERATE_DOCS
* UPSTREAM_REMOTE
* FORK_REMOTE



