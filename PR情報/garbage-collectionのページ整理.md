# garbage-collectionの説明ページを整理する

## 関連するPR

https://github.com/kubernetes/website/pull/28870

英語ページを修正を実施して、2021/07/27 にマージされた

### 修正対象のページツリー

```
content/en/docs
  +-- concepts
    +-- architecture
      +-- garbage-collection.md                new
    +-- cluster-administration
      +-- kubelet-garbage-collection.md        delete
    +-- containers
      +-- images.md                            modify
    +-- overview
      +-- working-with-objects
        +-- finalizers.md                      new
        +-- owners-dependents.md               new
    +-- workloads
      +-- controllers
        +-- garbage-collection.md              delete
    +-- reference
      +-- glossary
        +-- finalizer.md                       new
        +-- garbage-collection.md              new
    +-- tasks
      +-- administer-cluster
        +-- use-cascading-deletion.md          new
static
  +-- _redirects                               modify
```

### 修正対象のページ一覧

|ファイル名     |状態|コメント|
|---            |--- |---     |
|content/en/docs/concepts/architecture/garbage-collection.md                    |new    |#31063でjaにも作成済み(2022/4/3 マージされた) |
|content/en/docs/concepts/cluster-administration/kubelet-garbage-collection.md  |delete |jaにはまだ残っている        |
|content/en/docs/concepts/containers/images.md                                  |modify |#35809でjaも最新化されており反映済み(2022/9/9 マージされた) |
|content/en/docs/concepts/overview/working-with-objects/finalizers.md           |new    |#38768でjaにも作成済み(2023/2/3 マージされた) |
|content/en/docs/concepts/overview/working-with-objects/owners-dependents.md    |new    |#38794でjaにも作成済み(2023/2/3 マージされた) |
|content/en/docs/concepts/workloads/controllers/garbage-collection.md           |delete |jaにはまだ残っている        |
|content/en/docs/reference/glossary/finalizer.md                                |new    |#38768でjaにも作成済み(2023/2/3 マージされた) |
|content/en/docs/reference/glossary/garbage-collection.md                       |new    |#39948でjaのレビュー中        |
|content/en/docs/tasks/administer-cluster/use-cascading-deletion.md             |new    |#39960でjaのレビュー中        |
|static/_redirects                                                              |modify |言語共通                    |

現在、#39948、#39960 でレビュー中のため、この２件が完了すると、deleteを除いてすべて作業済みとなるため、deleteしてしまっても問題ない。
