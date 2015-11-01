Uliweb Peafowl 介绍
=============================

## 它是什么？

[Uliweb](https://github.com/limodou/uliweb) 是一个基于python的WEB开发框架。它主要实现的基础的、
通用的框架功能，带有部分应用相关的app，但是基本上是与具体的应用无关。 [Plugs](https://github.com/limodou/plugs)
是在Uliweb基础之上的偏向于UI和应用部分的通用app的集合，但并不是完整的面向应用。而Uliweb-Peafowl是完整
的面向应用开发的平台，它将提供以下特性：

* 集成一套后台管理的UI框架
* 提供在线Model的定制功能,可以增加新字段，索引，并且发布后自动更新表结构
* 提供在线Form编辑器，可以用在Model的增加、修改、展示等处
* 可定制的查询功能，可以方便生成不同的查询结果
* 可定制的菜单
* 可定制的URL

平台基于以下的开源组件来实现：

* Uliweb
* Plugs
* Bootstrap 3.3+
* Avalon 1.3.7+
* jQuery
* Admin LTE
* pnotify
* select2
* mmGrid (修改版本)
* fontawesome
* require

说明：

动态化可能会带来性能的损失，因此要注意，希望控制在可以接受的范围内


## 前端展示设计思路

Uliweb-Peafowl在前端展示希望引入一些更流行的技术，当然是在能力范围之内，所以可能在某些地方会有一些
实现上的考虑，主要是：

* 静态和动态资源使用混合。对于layout.html模板，会考虑将常用的静态文件直接放在模板中，比如jQuery, Bootstrap等，
  对于动态的静态资源，使用requirejs来处理，因此在Uliweb-Peafowl中对插件进行了重新的整理，用法上也和
  {{use}}之类的方式有很大的差异。为了解决第三方扩展问题，Uliweb-Peafowl还将实现requirejs的config.js
  自动生成的功能，因此当你添加了新的第三方的UI插件后，要根据对config.js的生成要求重新进行生成，以便用在
  项目中。另外这步工作也可以考虑在exportstatic和runserver时自动完成。
* 交互的Ajax化，表单的交互尽量采用Ajax方式来进行处理，对于字段的校验通过jQuery.validate插件来完成。
* 提供js的Form生成。提供兼容Bootstrap3的Form生成机制，并且可以采用js方式在前端生成，从而可以实现前后分离。
* Ajax的批量打包处理。因为Ajax的大量使用，考虑实现Ajax的批量请求自动打包处理的机制，目前考虑由前端手工打包，
  后面可以考虑自动在一段时间内的打包处理。后台提供对批量Ajax请求的响应处理。
* Avalon的使用。将Avalon作为重要的前端渲染的组件。
* 模板功能区域细分。将页面中典型的功能尽量细分，放在单独的模板中，以方便复用。
* 模板功能中的数据尽量配置化，支持配置文件与数据库的混合使用，并且保存在缓存中。实现方便的插拔化，并且可以处理
  当某个组件移除后相关的配置应正确失效。