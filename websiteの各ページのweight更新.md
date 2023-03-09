# websiteのweight更新に関して

## Issue[#35093](https://github.com/kubernetes/website/issues/35093)の概要

weightが同じページは、タイトル文字列の順序でソートされます。ローカライズされたページは、英語のドキュメントと順序が異なる場合があります。
ローカリゼーションチームは、正しい順序にするために、各言語に応じてweightを変更する場合がありますが、英語のドキュメントでweightを変更した方が良いと思います。

そのため、同じ階層（セッション、ディレクトリ）で同じweightを持つ全てのページ(のweight)を設定し直します。

### Issue内のコメント

以下の対応を進めていく

- さらなるコミュニティミーティングにて、英語ドキュメントに取り組んでいる人々がweightの重要性とローカライズされたコンテンツのweightが引き起こす潜在的な問題を理解できるようにします。
- レイジー更新を使用して、ページが更新されるときに英語のページの重みを調整します。CI警告を追加実装すれば、各英語ページの調整をスピードアップするのに役立つと思います。
- ドキュメントにて、同一階層で重複するweightを禁止することを強調する。

以下でenの修正状況を追跡

https://hackmd.io/VtoYICL6SnGaL_QaySrbcw?view


## PullRequest

### ドキュメント更新

同一階層では、重複するweightを使用しないことを明記する。
- Issue: https://github.com/kubernetes/website/issues/36845
- PR: https://github.com/kubernetes/website/pull/36892
- 日本語向けPR: https://github.com/kubernetes/website/pull/38913  (河村が対応)

### weight修正

- [ ] https://github.com/kubernetes/website/pull/37470 content/en/docs/concepts/extend-kubernetes/api-extension/
- [ ] https://github.com/kubernetes/website/pull/37471 content/en/docs/concepts/containers/
- [ ] https://github.com/kubernetes/website/pull/37472 content/en/docs/concepts/workloads/pods/
- [ ] https://github.com/kubernetes/website/pull/37473 content/en/docs/concepts/architecture/
- [x] https://github.com/kubernetes/website/pull/37474 content/en/docs/concepts/overview/working-with-objects/ ([ja] https://github.com/kubernetes/website/pull/38913)
- [ ] https://github.com/kubernetes/website/pull/37476 content/en/docs/reference/kubernetes-api/cluster-resources/ 自動生成されるページのため保留中
- [x] https://github.com/kubernetes/website/pull/37479 content/en/docs/concepts/overview/ ([ja] https://github.com/kubernetes/website/pull/39073)
- [ ] https://github.com/kubernetes/website/pull/37480 content/en/docs/contribute/
- [ ] https://github.com/kubernetes/website/pull/37482 content/en/docs/setup/
- [ ] https://github.com/kubernetes/website/pull/37484 content/en/docs/concepts/cluster-administration/
- [ ] https://github.com/kubernetes/website/pull/37485 content/en/docs/reference/access-authn-authz/
- [ ] https://github.com/kubernetes/website/pull/37488 content/en/docs/tutorials/services/
- [ ] https://github.com/kubernetes/website/pull/37492 content/en/docs/concepts/security/ ([ja] https://github.com/kubernetes/website/pull/39797)
- [X] https://github.com/kubernetes/website/pull/37494 content/en/docs/concepts/services-networking/ ([ja] https://github.com/kubernetes/website/pull/39559)
- [ ] https://github.com/kubernetes/website/pull/37495 content/en/docs/concepts/storage/ ([ja] https://github.com/kubernetes/website/pull/39797)
- [X] https://github.com/kubernetes/website/pull/37511 content/en/docs/concepts/scheduling-eviction/ ([ja] https://github.com/kubernetes/website/pull/39564)
- [ ] https://github.com/kubernetes/website/pull/37678 content/en/docs/concepts/services-networking/
- [ ] https://github.com/kubernetes/website/pull/37716 content/en/docs/concepts/ ([ja] https://github.com/kubernetes/website/pull/39797)
- [ ] https://github.com/kubernetes/website/pull/37717 content/en/docs/reference/ ([ja] https://github.com/kubernetes/website/pull/39771)
- [ ] https://github.com/kubernetes/website/pull/38872 content/en/docs/tutorials/security/
- [ ] https://github.com/kubernetes/website/pull/38887 content/en/docs/tasks/administer-cluster/

tasks配下がまだ残っている様子。

### 自動生成するページの検討

https://github.com/kubernetes/website/issues/37486

- Issue#35093 に従ってページのweightの更新に取り組みました。
- ただし、更新が必要なページの一部は自動生成されています。議論した結果、ページ ジェネレーターを更新して代わりに優先値を生成することは価値があると判断されました。
- 自動生成されたドキュメントのweightが、ドキュメント全体で設定している基準に従うように、これを更新する必要があります。
- 1.26リリース前に優先して実施する。
 
