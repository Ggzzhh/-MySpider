# -MySpider
爬虫练习以及自制爬虫


## Beautiful4 - bs4
* `find(tag, attributes, recursive, text, keywords)`
* `findAll(tag, attributes, recursive, text, limit, keywords) `
    ```text
      tag - 标签名 如： span
      attributes - 属性 如: bsObj.findAll("span", {"color": "red"})
      recursive - 递归参数 布尔值 如果为False 则只抓取一级标签
      text - 文本参数 如: bsObj.findAll(text='the prince') 查找所有包含该文本的标签
      limit - 范围限制参数 如果只想抓取前20个参数则设置 limit=20
      keyword - 可以指定属性 如 id='text' （不推荐）
    ```

* `bsObj.find(……).children` 查找所有的子标签

* `bsObj.find(……).tr.next_siblings` 查找tr之后所有tr的兄弟标签

* `bsObj.find(……).tr.previous_siblings` 查找tr之前所有tr的兄弟标签
    * 当然，还有 next_sibling 和 previous_sibling 函数，与 next_siblings 和 
    previous_siblings 的作用类似，只是它们返回的是单个标签，而不是一组标签。

* 处理父标签 parent 和 parents

* 获取属性
    获取标签的全部属性 `tag.attrs`
    获取部分属性 `tag.attrs["src"]`
    
* 可以在bs中使用 正则表达式(re) 未命名函数(Lambda) 作为条件
    `bsObj.findAll(lambda tag: len(tag.attrs) == 2)`

## 正则表达式 Regex
?! 不包含 如： ^((?![A-Z]).)*$   开头不能为大写字母
