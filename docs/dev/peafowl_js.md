# peafowl.js说明


peafowl.js中提供了常见的函数定义，缺省情况下，它会在admin_layout.html中自动被加载，所以其中定义的函数
可以被自动使用。

## show_message

```
function show_message(message, category)
```

在窗口上中部显示弹出消息。

参数：

message --
    为要显示的消息内容
category --
    为显示的类型，可选值为：

    * `success` 正确
    * `error` 出错
    * `info` 提示
    * `warning` 警告

    缺省为 `success`

## popup_url

```
function popup_url(target, options, title, callback)
```

用于在当前控件上绑定一个弹出窗口，在点击时会弹出对应的窗口。

参数：

target --
    用来响应点击的控件
options --
    配置项，可以有两种类型，如果是字符串，则表示对应的 URL。如果是plainobject，则为底层webui_popop
    所对应的参数，详情参见 <https://github.com/sandywalker/webui-popover>
title --
    弹出窗的标题
callback --
    窗口关闭时的回调

后台对应的URL返回内容可能是HTML的片段，也可能是完整的HTML页面。当只需要其中部分内容时，可以在返回的内容
中添加 `<!-- form -->` 和 `<!-- end form -->` 的信息，popup_url将只保留这些信息。

对于某些表单内容，希望在点击关闭或提交之类的按钮时，可以自动关闭弹出窗口。那么需要在URL返回的内容中，应该
在点击相应的铵钮之后，触发 `success.form` 事件，如果没有，则只能通过弹窗本身的关闭功能。同时，callback
用于当 `success.form` 被触发之后，窗口在关闭后的回调处理。

## show_popup_url

```
function show_popup_url(target, options, title, callback)
```

此函数和 `popup_url` 类似，只是直接打开。

## validate_submit

```
function validate_submit(target, options)
```

对指定 `target` 绑定jquery.validate校验功能，并且将form提交转为 ajax 方式。

target --
    绑定jquery.validate的form元素
options --
    * rules 校验规则
    * messages 出错提示消息
    * ajax_submit ajax提交函数，缺省使用 `common_ajax_submit` (在peafowl.js中定义)