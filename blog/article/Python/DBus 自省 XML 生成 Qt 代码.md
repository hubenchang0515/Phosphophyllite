# DBus 自省 XML 生成 Qt 代码

各种支持 DBus 的开发框架都能够通过 XML 自动生成代码，例如 Glib 的 `gdbus-codegen` 和 Qt 的 `qdbusxml2cpp`。

通过 DBus 对象 `org.freedesktop.DBus.Introspectable` 接口下的 `Introspect` 方法可以自省 XML，这样就不需要手写了。

但是 d-feet、dbus-send 等工具会给返回值加上类型标注或者换行符导致需要人工修改。因此需要自己写一个脚本来自省 DBus。


使用示例:  
```
$ ./introspect.py -t system -n org.freedesktop.NetworkManager -p /org/freedesktop/NetworkManager
$ ./introspect.py -t system -n org.freedesktop.NetworkManager -p /org/freedesktop/NetworkManager/Devices/5
$ ls -1
introspect.py  
org.freedesktop.NetworkManager.Device.Statistics.xml  
org.freedesktop.NetworkManager.Device.WifiP2P.xml  
org.freedesktop.NetworkManager.Device.xml
org.freedesktop.NetworkManager.xml
$ qdbusxml2cpp -c NetworkManager -p NetworkManager org.freedesktop.NetworkManager.xml --no-namespaces
$ qdbusxml2cpp -c Device -p Device org.freedesktop.NetworkManager.Device.xml --no-namespaces
$ qdbusxml2cpp -c WifiP2P -p WifiP2P org.freedesktop.NetworkManager.Device.WifiP2P.xml --no-namespaces
$ ls -1
Device.cpp
Device.h
introspect.py
NetworkManager.cpp
NetworkManager.h
org.freedesktop.NetworkManager.Device.Statistics.xml
org.freedesktop.NetworkManager.Device.WifiP2P.xml
org.freedesktop.NetworkManager.Device.xml
org.freedesktop.NetworkManager.xml
WifiP2P.cpp
WifiP2P.h
```

> 使用 `--no-namespaces` 选项的原因是，`qdbusxml2cpp` 会把 DBus Name 的最后一项作为类名，而之前项作为命名空间名
> 即 `org.freedesktop.NetworkManager` 生成 `::org::freedesktop::NetworkManager` 类。
> 而 `org.freedesktop.NetworkManager.Device` 生成的 `::org::freedesktop::NetworkManager::Device` 类。
> 这两者会发生冲突。前者的 `NetworkManager` 是类名，而后者的是命名空间明。

验证生成的代码:  

```cpp
#include <QDebug>
#include "NetworkManager.h"
#include "Device.h"
#include "WifiP2P.h"

int main(void)
{
    NetworkManager networkManager{"org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager", QDBusConnection::systemBus()};
    auto devicePathes = networkManager.devices();
    for (auto& devicePath : devicePathes)
    {
        Device device("org.freedesktop.NetworkManager", devicePath.path(), QDBusConnection::systemBus());
        qDebug() << "check wifi p2p device" << devicePath.path();
        if (device.deviceType() == 30)
        {
            qDebug() << "found wifi p2p device" << devicePath.path();
            break;
        }
    }
}
```

```
17:06:43: Starting /home/planc/miracast/build-wifi-p2p-unknown-Default/wifi-p2p...
check wifi p2p device "/org/freedesktop/NetworkManager/Devices/1"
check wifi p2p device "/org/freedesktop/NetworkManager/Devices/2"
check wifi p2p device "/org/freedesktop/NetworkManager/Devices/5"
found wifi p2p device "/org/freedesktop/NetworkManager/Devices/5"
17:06:43: /home/planc/miracast/build-wifi-p2p-unknown-Default/wifi-p2p exited with code 0
```

> 如果看不到日志打印可以参考 [Qt 日志模块的使用](https://gist.github.com/hubenchang0515/76508e9e3392110abbe9f7f78c213106) 进行配置

```python
#! /usr/bin/env python3
import dbus
from dbus.proxies import ProxyObject
import xml.dom.minidom as minidom
from typing import Callable, List, Set, Dict
from argparse import ArgumentParser, Namespace

# 不需要的 Interface
filter:Set[str] = {
    "org.freedesktop.DBus.Introspectable",
    "org.freedesktop.DBus.Peer",
    "org.freedesktop.DBus.Properties",
}

class DBusTypeParser(object):
    dbusQtContainerType:Dict[str,str] = {
        "<array>": "QList",
        "<struct>": "QVariant",
        "<dict>": "QMap",
    }

    dbusQtType:Dict[str,str] = {
        "y": "quint8",
        "b": "bool",
        "n": "qint16",
        "q": "quint16",
        "i": "qint32",
        "u": "quint32",
        "x": "qint64",
        "t": "quint64",
        "d": "double",
        "h": "quint32",
        "s": "QString",
        "o": "QDBusObject",
        "g": "QString",
        "v": "QVariant",
    }

    def __init__(self) -> None:
        # 状态
        self.currentState:str = "<normal>"
        self.stateStack:List[str] = []

        # dict里的第几个参数
        self.currentIndex:int = 0
        self.indexStack:List[int] = []

    def pushState(self, state:str) -> None:
        if state == "<dict>":
            self.pushIndex(self.currentIndex)
            self.currentIndex = 0
        self.stateStack.append(state)

    def popState(self) -> str:
        state:str = self.stateStack.pop()
        if state == "<dict>":
            self.currentIndex = self.popIndex()
        return state

    def pushIndex(self, index:int) -> None:
        self.indexStack.append(index)

    def popIndex(self) -> int:
        return self.indexStack.pop()

    def parse(self, signature:str) -> str:
        self.currentState = "<normal>"
        self.currentIndex = 0
        qtype:str = ""
        while len(signature) > 0:
            ch:str = signature[0]
            signature = signature[1:]

            if ch in DBusTypeParser.dbusQtType:
                if self.currentState == "<normal>":
                    qtype += self.parseNormal(ch)
                elif self.currentState == "<struct>":
                    qtype += self.parseStruct(ch)
                elif self.currentState == "<dict>":
                    qtype += self.parseDict(ch)
                elif self.currentState == "<array>":
                    qtype += self.parseArray(ch)
            elif ch == "a" and signature:
                if self.currentState == "<dict>" and self.currentIndex == 0:
                    qtype += DBusTypeParser.dbusQtContainerType['<dict>'] + "<"
                self.pushState(self.currentState)
                self.currentState = "<array>"
            elif ch == "(":
                if self.currentState == "<dict>" and self.currentIndex == 0:
                    qtype += DBusTypeParser.dbusQtContainerType['<dict>'] + "<"
                self.pushState(self.currentState)
                self.currentState = "<struct>"
            elif ch == "{":
                # a{ 开启dict模式，之前为暂态的array模式，不push
                self.currentState = "<dict>"
            elif ch == ")":
                qtype += self.parseStruct(ch)
                if self.currentState == "<dict>" and self.currentIndex == 0:
                    qtype += ", "
                    self.currentIndex += 1
            elif ch == "}":
                self.currentState = self.popState()
                qtype += self.parseDict(ch)
                if self.currentState == "<dict>" and self.currentIndex == 0:
                    qtype += ", "
                    self.currentIndex += 1
            else:
                print(f"{ch}")
                raise f"Unknown signature '{ch}'"
        return qtype

    def parseNormal(self, ch:str) -> str:
        return DBusTypeParser.dbusQtType[ch]
        
    def parseArray(self, ch:str) -> str:
        self.currentState = self.popState()
        return f"{DBusTypeParser.dbusQtContainerType['<array>']}<{DBusTypeParser.dbusQtType[ch]}>"

    def parseStruct(self, ch:str) -> str:
        if ch != ")":
            return ""

        self.currentState = self.popState()
        if self.currentState == "<struct>":
            return ""

        if self.currentState == "<normal>":
            return DBusTypeParser.dbusQtContainerType["<struct>"]

        if self.currentState == "<dict>":
            return DBusTypeParser.dbusQtContainerType["<struct>"]

        if self.currentState == "<array>":
            self.currentState = self.popState()
            return f"{DBusTypeParser.dbusQtContainerType['<array>']}<{DBusTypeParser.dbusQtContainerType['<struct>']}>"

    def parseDict(self, ch:str) -> str:
        if ch == "}":
            return ">"

        self.currentIndex += 1
        if self.currentIndex == 1:
            return DBusTypeParser.dbusQtContainerType['<dict>'] + "<" + DBusTypeParser.dbusQtType[ch] + ", "
        else:
            return DBusTypeParser.dbusQtType[ch]

dbusTypeParser = DBusTypeParser()

parser:ArgumentParser = ArgumentParser(description='DBus Introspect XML')
parser.add_argument("-t", "--type", default="session", help="bus type, system or session")
parser.add_argument("-n", "--name", help="bus namae")
parser.add_argument("-p", "--path", help="object path")
args:Namespace = parser.parse_args()

bus:dbus.Bus = dbus.SystemBus() if args.type == "system" else dbus.SessionBus() 
proxy:ProxyObject = bus.get_object(args.name, args.path)
xmlString:str = proxy.Introspect(dbus_interface='org.freedesktop.DBus.Introspectable')

root:minidom.Document = minidom.parseString(xmlString)
interfaces:List[minidom.Element] = root.getElementsByTagName("interface")

neededInterfaces:List[minidom.Element] = []
for interface in interfaces:
    name:str = interface.getAttribute("name")
    if name in filter:
        continue

    methods:List[minidom.Element] = interface.getElementsByTagName("method")
    for method in methods:
        inIndex:int = 0
        outIndex:int = 0
        methodArgs:List[minidom.Element] = method.getElementsByTagName("arg")
        for arg in methodArgs:
            sign:str = arg.getAttribute("type")
            qtype:str = dbusTypeParser.parse(sign)
            annotation:minidom.Element = root.createElement("annotation")
            
            if arg.getAttribute("direction") == "in":
                annotation.setAttribute("name", f"org.qtproject.QtDBus.QtTypeName.In{inIndex}")
                inIndex += 1
            if arg.getAttribute("direction") == "out":
                annotation.setAttribute("name", f"org.qtproject.QtDBus.QtTypeName.Out{outIndex}")
                outIndex += 1

            annotation.setAttribute("value", qtype)
            method.appendChild(annotation)

    properties = interface.getElementsByTagName("property")
    for property in properties:
        sign:str = property.getAttribute("type")
        qtype:str = dbusTypeParser.parse(sign)
        annotation:minidom.Element = root.createElement("annotation")
        annotation.setAttribute("name", "org.qtproject.QtDBus.QtTypeName")
        annotation.setAttribute("value", qtype)
        property.appendChild(annotation)
    
    neededInterfaces.append(interface)


for interface in neededInterfaces:
    with open(interface.getAttribute("name") + ".xml", "w") as fp:
        fp.write(interface.toprettyxml())
```