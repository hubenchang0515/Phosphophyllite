# Gio::DBus 中创建复合类型的参数

首先，需要知道两个基本知识:  
* 每一个参数都需要被包装为 Variant。
* 全体参数需要被整体包装成一个 Tuple。

> 即使只有一个参数也需要包装为 Tuple，例如一个 string:  
> ```c++
> const auto arg1 = Glib::Variant<Glib::ustring>::create("hello world");
> Glib::VariantContainerBase args = Glib::VariantContainerBase::create_tuple(arg1);
> ```

`Glib::Variant` 是模板，是不完全的类型，所以要使用它的基类 `Glib::VariantBase` 来表示任意类型的 Variant 对象。

因此，一个 `a{sv}` 类型的参数类型为 `Glib::Variant<std::map<Glib::ustring, Glib::VariantBase>>`