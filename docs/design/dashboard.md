# Dashboard 功能设计

## 功能说明
本功能是准备做一个通用的Dashboard功能，包括功能说明如下：
  * 分成内容面板区和数字面板区 (Content Pane Area, Digital Pane Area)
  * 数字面板区支持配置1-6个数字面板 (Digital Pane),固定显示在上方
  * 内容面板区，支持不限数量的内容面板的显示 
    - 内容面板区，支持布局的选择（二栏，三栏）
    - 内容面板支持拖拽调整位置
    - 内容面板可以支持关闭，最小化（可配置）

## 详细设计

### Dashboard的类别定义
 * DashboardTypeDef
    - 可以使用uliweb-settings进行配置
    - 表示系统中支持多少种Dashboard的类型
    - Peafowl中应当支持通过Dashboard(用户无关，实体无关)，用户相关Dashboard(个人主页)
    - 这个配置是可以扩展的，使用peafowl的项目可以增加自己的类型。

### 数字面板的定义
 * DigitalPaneDef - 数字面板定义表
    - name 名称
    - title 显示名称 
    - count_function 用于计算该数据的Python函数的全路径
    - parameters 面板需要的参数（可空）
    - 其他可能的可修改属性，比如 color 
    - dashboard_type 该面板可用于哪种dashboard，可空，表示全局可以用。

其中：
 * 要求count_function 函数返回值如下：
    - count, 数字，可以有单位，比如"320个", "1000个未处理"
    - description, 描述文字，显示在数字下方，字体较小
    - link (link可能为None) 点击数字后的跳转链接。

* parameters参数用于支持计算与当前用户相关的数据，parameters形式如下：user_id={user_id},unit_id={unit_id},other_param=123，具体
* 其中{user_id}和{unit_id}是预定义的参数 (人员标识，部门标识)，用来传入当前用户的相关参数。该参数是处理是在获取配置信息到前台展现时使用，所以实际替换这些值是具体的Dashboard的显示的view层处理。

### 内容面板的定义
 * ContentPaneDef - 内容面板定义表
    - name 名称
    - title 显示名称
    - type 面板类型
        - IFRAME, IFrame方式嵌入显示一个url链接
        - HTML, 通过ajax从某个url中得到一些html的片段
        - GRID, 通过ajax来显示一个表格数据 json格式
        - 其他可扩展类型，支持json数据的不同展现
    - url 数据访问的url
    - color, closable, foldable其他可配置的功能

其中：
  * url配置中，支持使用预定的当前用户相关的参数，比如{user_id}, {unit_id}等
  * 自定义的查询面板，支持把一个查询条件保存到


### 缺省布局的定义
  * DashboardDef 布局种类定义表
    - display_name Dashboard显示名称
    - name dashboard名称
    - 建设使用配置文件保存支持的布局种类，可扩展
    - view层有一个基类用来处理通用的布局，实体相关的布局，采用扩展类的方式实现，从而增加对于不同的预定义参数，如{user_id}的支持。

  * DashboardLayout 布局表
    - dashboard_name
    - generic_id 关联标识
    - columns 面板布局 （4-8，6-6，4-4-4之类）
    - default 是否是缺省的面板

  * DashboardPane Dashboard上的面板
    - dashboard_id
    - pane_id
    - position 位置(col,row) (1,2), (2,1) 之类

其中:
  * name 要求唯一，支持多种面板，比如person_dashboard，depart_dashboard
  * generic_id 关联的人员或者部门或者其他实体的标识，此值为空的，表示的是缺省的模板
  * position是二元数，表示列与行，如果面板布局和位置表达不一致时，退化到前两列中。比如面局是2栏的，位置中保存了第三列的位置，显所有这一些面板都退化显示在第二列上。
  * DashboardPane也可以以Pickle的形式保存到DashboardLayout表中。

### 用户布局的定义与保存

  * 使用缺省布局，相同的表，dashboard根据类型不同，所关联的generic_name是不一样的。拟支持如下几种：
    - user, dashboard是个人相关的。每个人看到的可以不一样，可以保存与修改到个人
    - depart, dashboard是部门相关的，同一个部门下所有的人看到是一样的。修改后，所有同部门下看到的样式都发生变化。
    - project, dashboard是项目相关的。
    - common, dashboard是全局的，所有的人看到的是同一个。
  * 支持用户删除重置自己的布局，删除后，使用default的布局

### 界面的展现
  * 根据dashboard的类型不同，使用不同的view的类（扩展类型，使用新建子类的方法）
  * 该dashboard的属性，如果是人员或者部门相关，读取该人员或者部门下的配置，如果不存在，读取缺省的配置
  * 读取配置中所有的数字面板和内容面板的定义
  * 前台根据面板的定义与布局位置，生成相应用的代码块。


## 任务的分派
 * 面板块的定义，各种类型面板的测试数据
 * 面板布局定义，后台表结构
 * 面板布局展现，前台支持拖拽
 * 面板布局编辑与保存，前台支持选择与拖拽



