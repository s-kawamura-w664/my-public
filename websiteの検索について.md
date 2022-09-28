# websiteの検索について

kubernetesドキュメントサイト( https://kubernetes.io/docs/home/ )の検索処理についての調査結果です。

## 課題

1. 日本語キーワードで検索できない
2. ページのアンカーが使いにくい
3. 検索結果が無い場合に、検索中メッセージ("Fetching results...")のままになる

## 結論

* 日本の場合、本来はGoogleエンジンが使用されるはずだが、Bingエンジンで検索してしまっている
* Bingエンジンは中国向け
* 接続元の国名取得サイト( https://ipinfo.io )へアクセスできないと、中国として扱っている（プロキシで接続エラーになっている）
    * cookieに "is_china=true"が保存される
* Bingエンジンで、日本語キーワードを検索する場合、キーワードがURLエンコードされていて正しく検索できない

## 対処法：cookie(is_china)を変更

以下にEdgeでの編集方法を示しますが、Chromeでも類似の方法で編集できそう。

1. ブラウザで"https://kubernetes.io" に接続
    * 検索を実行して、"is_china=true" を予め作っておく
2. 右クリックメニューから「開発者ツールで調査する」を選択
3. 上段のメニューから「アプリケーション」を選択
4. 左側のメニューから「ストレージ」－「Cookie」を展開し、"https://kubernetes.io" を選択
5. is_chinaのtrueのところで右クリックし、メニューから「値を編集する」を選択
6. "false"を入力しリターン

cookieの有効期限が１週間程度しかないので、期限切れしたら再編集が必要と思います。
有効期限を延長しても良いと思います。

## 検索処理の流れ

1. 検索画面は以下で定義されています。

    https://github.com/kubernetes/website/blame/main/layouts/_default/search.html#L42-L46
    
    関連箇所は以下
    
    ```html
    <script src="{{ "js/search.js" | relURL }}"></script>
    <gcse:searchresults-only linktarget="_parent">
      <div id="bing-results-container">{{ T "layouts_docs_search_fetching" }}</div>
      <div id="bing-pagination-container"></div>
    </gcse:searchresults-only>    
    ```

2. 検索を実行すると、search.js ( https://github.com/kubernetes/website/blob/main/static/js/search.js )が実行されます。

    ```js
    if (getCookie("is_china") === "") {
        $.ajax({
            url: "https://ipinfo.io?token=796e43f4f146b1",
            dataType: "jsonp",
            success: function (response) {
                if (response.country == 'CN') {
                    window.renderBingSearchResults()
                    document.cookie = "is_china=true;" + path + expires
                } else {
                    window.renderGoogleSearchResults()
                    document.cookie = "is_china=false;" + path + expires;
                }
            },
            error: function () {
                window.renderBingSearchResults()
                document.cookie = "is_china=true;" + path + expires;
            },
            timeout: 3000
        });
    } else if (getCookie("is_china") === "true") {
        window.renderBingSearchResults()
    } else {
        window.renderGoogleSearchResults()
    }
    ```
    
    * 最初は"is_china"がありませんので、cookieにis_chinaを登録します。
      プロキシにより "https://ipinfo.io?token=796e43f4f146b1" へのアクセスがブロックされてしまうと、error条件となり"is_china=true"が設定されます。
    * is_china=trueの場合は、検索エンジンにBingが使用されます。
    * is_china=falseの場合は、検索エンジンにGoogleが使用されます。

3. Bingエンジンの場合、renderBingSearchResults()が呼ばれます。

    ```js
    window.renderBingSearchResults = () => {
        var searchTerm  = window.location.search.split("=")[1].split("&")[0].replace(/%20/g,' '),
            page        = window.location.search.split("=")[2],
            q           = "site:kubernetes.io " + searchTerm;                       // ★(1)

        page = (!page) ?  1 : page.split("&")[0];

        var results = '', pagination = '', offset = (page - 1) * 10, ajaxConf = {};

        ajaxConf.url = 'https://api.cognitive.microsoft.com/bingcustomsearch/v7.0/search';
        ajaxConf.data =  { q: q, offset: offset, customConfig: '320659264' };
        ajaxConf.type = "GET";
        ajaxConf.beforeSend = function(xhr){ xhr.setRequestHeader('Ocp-Apim-Subscription-Key', '51efd23677624e04b4abe921225ea7ec'); };

        $.ajax(ajaxConf).done(function(res) {
            if (res.webPages == null) return; // If no result, 'webPages' is 'undefined'          // ★(2)
            var paginationAnchors = window.getPaginationAnchors(Math.ceil(res.webPages.totalEstimatedMatches / 10));
            res.webPages.value.map(ob => { results += window.getResultMarkupString(ob); })

            if($('#bing-results-container').length > 0) $('#bing-results-container').html(results);     // ★(3)
            if($('#bing-pagination-container').length > 0) $('#bing-pagination-container').html(paginationAnchors);     // ★(4)
        });
    }
    ```
    
    * (1)のところで検索条件を設定していますが、searchTerm がURLエンコードされたままです。
    * (2)のところで検索結果がnull(検索結果が無い)場合の処理がありません。
      ここに処理が無いため、"Fetching results..." から画面が更新されません。
    * 検索結果がある場合には、(3)のところで検索結果を表示しています。
    * さらに、(4)のところで、検索結果のページ用アンカーを表示しています。
      ページ用アンカーは、getPaginationAnchors() で生成しています。
      ```js
      window.getPaginationAnchors = (pages) => {
          var pageAnchors = '', searchTerm  = window.location.search.split("=")[1].split("&")[0].replace(/%20/g, ' ');
          var currentPage = window.location.search.split("=")[2];
          currentPage = (!currentPage) ?  1 : currentPage.split("&")[0];

          for(var i = 1; i <= 10; i++){
              if(i > pages) break;
              pageAnchors += '<a class="bing-page-anchor" href="/search/?q='+searchTerm+'&page='+i+'">';
              pageAnchors += (currentPage == i) ? '<b>'+i+'</b>' : i;
              pageAnchors += '</a>';
          }
          return pageAnchors;
      }
      ```

4. Googleエンジンの場合、renderGoogleSearchResults()が呼ばれます。

    ```js
    window.renderGoogleSearchResults = () => {
        var cx = '013288817511911618469:elfqqbqldzg';
        var gcse = document.createElement('script');
        gcse.type = 'text/javascript';
        gcse.async = true;
        gcse.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + '//cse.google.com/cse.js?cx=' + cx;
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(gcse, s);
    }    
    ```

## Bingエンジンで検索結果がnullの場合の対処例

**修正方法を検討しましたが、中国向けの検索エンジンと分かり、日本では関係なくなった**

```
window.renderBingSearchResults = () => {
    var searchTerm  = window.location.search.split("=")[1].split("&")[0].replace(/%20/g,' '),
        page        = window.location.search.split("=")[2],
        q           = "site:kubernetes.io " + searchTerm;

    page = (!page) ?  1 : page.split("&")[0];

    var results = '', pagination = '', offset = (page - 1) * 10, ajaxConf = {};

    ajaxConf.url = 'https://api.cognitive.microsoft.com/bingcustomsearch/v7.0/search';
    ajaxConf.data =  { q: q, offset: offset, customConfig: '320659264' };
    ajaxConf.type = "GET";
    ajaxConf.beforeSend = function(xhr){ xhr.setRequestHeader('Ocp-Apim-Subscription-Key', '51efd23677624e04b4abe921225ea7ec'); };

    $.ajax(ajaxConf).done(function(res) {
        if (res.webPages == null){                                  //(1)
            $('#bing-results-container').html("No Results.");          //★ "No Results."を表示
            return;
        }
        var paginationAnchors = window.getPaginationAnchors(Math.ceil(res.webPages.totalEstimatedMatches / 10));
        res.webPages.value.map(ob => { results += window.getResultMarkupString(ob); })

        if($('#bing-results-container').length > 0) $('#bing-results-container').html(results);     //(2)
        if($('#bing-pagination-container').length > 0) $('#bing-pagination-container').html(paginationAnchors);     //(3)
    });
}
```

* 修正前

    | ![](images/website_search/bing_search_1.png) |
    | --- |

* 修正後

    | ![](images/website_search/bing_search_2.png) |
    | --- |

## Bingエンジンの検索結果のページ用アンカーの表示改善例

**修正方法を検討しましたが、中国向けの検索エンジンと分かり、日本では関係なくなった**

```js
window.getPaginationAnchors = (pages) => {
    var pageAnchors = '', searchTerm  = window.location.search.split("=")[1].split("&")[0].replace(/%20/g, ' ');
    var currentPage = window.location.search.split("=")[2];
    currentPage = (!currentPage) ?  1 : currentPage.split("&")[0];


    for(var i = 1; i <= 10; i++){
        if(i > pages) break;
        pageAnchors += '<a class="bing-page-anchor" href="/search/?q='+searchTerm+'&page='+i+'">';
        pageAnchors += (currentPage == i) ? '<b>'+i+'</b>' : i;
        pageAnchors += '</a>';
        pageAnchors += '&nbsp;&nbsp;&nbsp;'     //★ アンカーの間にスペースを入れる
    }
    return pageAnchors;
}
```

* 修正前

    | ![](images/website_search/bing_anchor_1.png) |
    | --- |

* 修正後

    | ![](images/website_search/bing_anchor_2.png) |
    | --- |

## Bingエンジンで日本語対応の対応例

**修正方法を検討しましたが、中国向けの検索エンジンと分かり、この修正が必要かどうか分からない**

```js
window.renderBingSearchResults = () => {
    var searchTerm  = window.location.search.split("=")[1].split("&")[0].replace(/%20/g,' '),
        page        = window.location.search.split("=")[2],
        q           = "site:kubernetes.io " + decodeURI(searchTerm);        //★searchTermをdecodeURIする

    page = (!page) ?  1 : page.split("&")[0];

    var results = '', pagination = '', offset = (page - 1) * 10, ajaxConf = {};

    ajaxConf.url = 'https://api.cognitive.microsoft.com/bingcustomsearch/v7.0/search';
    ajaxConf.data =  { q: q, offset: offset, customConfig: '320659264' };
    ajaxConf.type = "GET";
    ajaxConf.beforeSend = function(xhr){ xhr.setRequestHeader('Ocp-Apim-Subscription-Key', '51efd23677624e04b4abe921225ea7ec'); };

    $.ajax(ajaxConf).done(function(res) {
        if (res.webPages == null) {
            $('#bing-results-container').html("No Results.");
            return;
        } // If no result, 'webPages' is 'undefined'
        var paginationAnchors = window.getPaginationAnchors(Math.ceil(res.webPages.totalEstimatedMatches / 10));
        res.webPages.value.map(ob => { results += window.getResultMarkupString(ob); })

        if($('#bing-results-container').length > 0) $('#bing-results-container').html(results);
        if($('#bing-pagination-container').length > 0) $('#bing-pagination-container').html(paginationAnchors);
    });
}
```

* 修正前

    | ![](images/website_search/bing_japanese_1.png) |
    | --- |

* 修正後

    | ![](images/website_search/bing_japanese_2.png) |
    | --- |

## 検索エンジンをGoogleに変更すると

* 検索結果

    | ![](images/website_search/google_result_1.png) |
    | --- |
    
* ページのアンカー

    | ![](images/website_search/google_result_2.png) |
    | --- |

* 検索結果が無い

    | ![](images/website_search/google_no_result.png) |
    | --- |

## 関連するPR

* https://github.com/kubernetes/website/pull/9845
* https://github.com/kubernetes/website/pull/10166
* https://github.com/kubernetes/website/pull/21823
