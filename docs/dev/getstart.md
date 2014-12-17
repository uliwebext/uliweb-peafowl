# 入门介绍

## 安装

```
pip install uliweb-peafowl
```

## 配置

在你的应用中的settings.ini中的 `INSTALLED_APPS` 中添加： `uliweb-peafowl`

## 初始化

在你的项目目录下执行：

```
uliweb syncdb -v
```

来创建相关的表结构

## 运行

目前 uliweb-peafowl 会自动使用 `/admin` 作为URL访问的起始路径，所以希望不要和你自已的应用冲突。如果
需要改为其它的值，可以参考 [ADMIN_URL](admin.html#admin_url) 文档进行尝试。

## DEMO

我们已经创建了名为 [uliweb_peafowl_demo](https://github.com/uliwebext/uliweb_peafowl_demo) 的项
目可以参考它的具体使用。