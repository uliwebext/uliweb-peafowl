Form 布局扩展介绍
=============================

## 扩展Form布局

在Uliweb 0.5版本以后，Form的布局类可以定义为字符串名字。实际的布局类需要在 `settings.ini` 中进行配置。详情
可以参见 Uliweb-doc 中关于 Form 的文档。

在 uliweb_peafowl 中目前提供了三个 Layout 类，分别为：

bs3v --
    BootstrapVLayout 标签显示在控件之上，使用div进行布局控制
bs3h --
    BootstrapHLayout 标签显示在控件左侧，使用div进行布局控制
bs3t --
    BootstrapTLayout 表格布局，标签显示在控件左侧，使用Table作为整体布局的处理

使用这几个 Layout 类，除指定名称之外，还需要提供布局数据，如：

    class MyForm(Form):
        layout_class = 'bs3v'
        layout = {
            'rows':[          #用来设置具体的布局说明，详情见下面说明
            ],
            'readonly: False, #如果为True则表示整个Form是只读的
            'form_class': '', #form标签的class属性，对于bs3h
                              #布局，将会自动在后面添加 form-horizontal
            'label_width': 0, #对于bs3h用于设置标签的列宽，注意是按每列来计算
                              #的，整个列总宽度为12
            'button_offset': 0, #对于设置按钮行的偏移量，以12为总宽度
            'fields':{},      #用来修改某个字段的显示相关的属性
        }

### rows 说明

可以把rows想像成为一个表格，它由若干行组行，每行又由若干列组成，其中还存在单列的情况，即
一行就一个字段。

对于行的定义，可以使用 list 或 tuple 来定义，如 `['field1', 'field2']`. 对于单列
可以只定义一个字段元素。一行可以由一个或多个字段元素组成。

关于字段元素的定义参见下节。

rows有几种定义方式：

省略 --
    则自动使用Form中所有字段，按创建顺序生成单列的布局。这是最简单的一种。
简单布局 --
    例如：

        rows: [
            ['field1', 'field2'],
            'field3',
            {'name':'field4', 'attrs':{'class':'xxx'}, 'inline':True},
            [{'name':'field5'}, 'field6'],
            [{'name':'field6', 'cols':...}, 'field7'},
        ]
分段布局 --
    例如：

        rows: [
            '-- basic --',
            ['field1', 'field2'],
            'field3',

            '-- extend --',
            {'name':'field4', 'attrs':{'class':'xxx'}, 'inline':True},
            [{'name':'field5'}, 'field6'],
            [{'name':'field6', 'cols':...}, 'field7'},

        ]

    这里使用 `-- xxx --` 将Form的展示分为若干段，每一段使用 `fieldset` 来处理。

### 字段元素的定义

对于字段元素的定义，可以使用：字符串（表示对应的字段名或者是一段HTML代码），字典（其中需要有一个 `name` 的属性
表示对应的字段名， `name` 值可以为空，表示不需要对应真正的字段名）。比如： `'field'`，
`'<p class='alert alert-success'>xxx</p>'` 和
`{'name':'field', 'attrs':{'class':'xxxx'}}` 就是一个合法的字段元素的定义。只使用
字符串，无法定义复杂的展示属性，所以需要采用字典方式。目前一个字段元素可以支持以下属性：

```
{
'name':     #字段名，如果给出建议与Form的字段名一致
'attrs':    #定义输入控件上将要设置的属性，它将与Form字段中的 html_attrs 属性进行合并
            #比如，向底层的控件添加一个新的类名，如 'attrs':{'class':'new-class'}
            #常见的有：
            #    'class' css 的类名
            #    'placeholder' 缺省显示文本
            #    'widget' 每种Form字段类都对应一个类型名，如StringField对应 str
            #         可以使用它来进行js的处理，根据类型转换为想要的js控件
            #    其它的属性，将转为控件上的属性值
'label':    #显示标签，缺省为对应Form字段的标签，如果为 ''则表示不显示标签
'inline':   #对于checkbox, radios, checkboxes这类的控件，用于控制排列方向与标签显示的位置
            #为True时，将水平排列。对于checkbox来说，标签将显示在后面
'format':   #当readonly时，对于特殊的字段使用format进行内容的转换处理，它需要是一个函数
            #格式为： def func(value, all_data)
            #其中 value 为当前字段元素的值，all_data为整个Form的所有值
'cols':     #对于复杂的情况，某个字段元素可能是一个复合内容，所以它可以是一个或若干个字段元素组成，
            #如：'field', '<p class='alert alert-success'>xxx</p>',
            #['field', '<p class='alert alert-success'>xxx</p>']
            #都是合法的
'buttons':  #定义Form的按钮
'wrap':     #定义包裹内容，它需要是一个二元素的list或tuple，如： `['<div>', '</div>']`
}
```

### fields 说明

从上面rows中可以看到，字段元素定义时可以设置与展示相关的属性，但是在简单情况下，我们可能想
使用缺省布局，只是修改某些字段的显示属性，所以不想把每个元素在 rows 中定义一遍，这样我们
就可以在 `fields` 中定义。如果在 rows 和 fields 中对相同的字段都进行了定义，则与rows
中的为准。

在fields中，key为要定义的字段名，值为相应的显示相关的属性，具体属性值参见上面的字段元素的定义
除了'name'之外的内容。