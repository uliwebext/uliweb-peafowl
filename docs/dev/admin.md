# Admin介绍

## 介绍

Admin主要提供后台管理的通用框架，包括：

* Admin的用户登录和注销
* Admin的菜单配置

## 登录和注销

Peafowl 实现了自已的登录和注销，是为了与通常的相区分

## 开发要求

### ADMIN_URL 前缀使用 {#admin_url}

在需要反向生成链接时，简单就是拼URL，但是如果复用时，URL需要调整就不方便了。而使用url_for等相对也不是太方便，
所以在 `admin/settings.ini` 中定义了：

```
[ADMIN]
ADMIN_URL = '/admin'
```

使用时，只要获得 `settings` 对象后，即可： `settings.ADMIN.ADMIN_URL` 这样来使用。

同时为了使用方便(模板和View函数中)还将上面的值注入到了环境中，因此可以在view函数(只能是直接与expose绑定的函数，
不包括它调用的其它的外部函数)和模板中可以直接使用 `ADMIN_URL` 这个变量，效果是一样的。

因此需要在拼URL的地方使用这个配置项即可，这样也方便用户修改。当然，这个 `/admin` 是要与view函数中的 `expose`
相配合的。它只是用来拼URL字符串，本身并不影响原来的expose定义。所以如果，URL的前缀发生变化，还需要修改APP
的URL定义的前缀才可以，需要在settings.ini中添加：

```
[URL]
uliweb_peafowl.admin = '/new_admin_path'
```

这样在 uliweb_peafowl.admin 下定义的所有view函数都会替换为新的URL前缀。