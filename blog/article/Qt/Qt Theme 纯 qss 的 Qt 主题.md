# Qt Theme 纯 qss 的 Qt 主题

## 简介

源码地址：https://github.com/hubenchang0515/QtTheme/

![预览](https://github.com/hubenchang0515/QtTheme/raw/master/doc/image/dark.png)

Qt Theme 是一个纯 qss 的 Qt 主题项目，能够极为简单对已有项目的风格进行改进。

支持 C++、PyQt5、PyQt6、PySide2、PySide6，并以 WebAssembly 的方式在 [GitHub Pages](https://hubenchang0515.github.io/QtTheme/) 上发布。

## 示例

### 安装

这里演示一下在 Python 上的使用，首先进行安装：  

```bash
pip install QtTheme
```

### 原生样式及代码

让 Deep Seek 随便帮我写个界面作为示例：

![deepseek](https://github.com/hubenchang0515/resource/blob/master/QtTheme/deepseek.png?raw=true)

```python
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Widget 演示界面")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中心widget和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 添加功能区域
        self.create_input_section(main_layout)
        self.create_selection_section(main_layout)
        self.create_display_section(main_layout)
        self.create_progress_section(main_layout)
        
        # 添加状态栏
        self.statusBar().showMessage("就绪")

        # 初始化进度条
        self.progress_value = 0
        self.update_progress()

    def create_input_section(self, layout):
        group = QGroupBox("输入控件")
        grid = QGridLayout()

        # 文本输入
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("单行文本输入...")
        grid.addWidget(QLabel("单行文本:"), 0, 0)
        grid.addWidget(self.line_edit, 0, 1)

        # 多行文本
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("多行文本输入...")
        grid.addWidget(QLabel("多行文本:"), 1, 0)
        grid.addWidget(self.text_edit, 1, 1)

        # 数字输入
        self.spin_box = QSpinBox()
        self.spin_box.setRange(0, 100)
        grid.addWidget(QLabel("数字输入:"), 2, 0)
        grid.addWidget(self.spin_box, 2, 1)

        group.setLayout(grid)
        layout.addWidget(group)

    def create_selection_section(self, layout):
        group = QGroupBox("选择控件")
        hbox = QHBoxLayout()

        # 复选框
        vbox = QVBoxLayout()
        self.check1 = QCheckBox("选项1")
        self.check2 = QCheckBox("选项2")
        vbox.addWidget(self.check1)
        vbox.addWidget(self.check2)
        hbox.addLayout(vbox)

        # 单选框
        vbox = QVBoxLayout()
        self.radio1 = QRadioButton("单选1")
        self.radio2 = QRadioButton("单选2")
        self.radio1.setChecked(True)
        vbox.addWidget(self.radio1)
        vbox.addWidget(self.radio2)
        hbox.addLayout(vbox)

        # 下拉列表
        self.combo = QComboBox()
        self.combo.addItems(["选项A", "选项B", "选项C"])
        hbox.addWidget(self.combo)

        group.setLayout(hbox)
        layout.addWidget(group)

    def create_display_section(self, layout):
        group = QGroupBox("显示控件")
        hbox = QHBoxLayout()

        # 标签
        self.label = QLabel("这是一个标签")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border: 1px solid gray; padding: 10px;")
        hbox.addWidget(self.label)

        # 图片显示
        pixmap = QPixmap(100, 50)
        pixmap.fill(Qt.blue)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        hbox.addWidget(image_label)

        # 列表控件
        self.list_widget = QListWidget()
        self.list_widget.addItems(["项目1", "项目2", "项目3"])
        hbox.addWidget(self.list_widget)

        group.setLayout(hbox)
        layout.addWidget(group)

    def create_progress_section(self, layout):
        group = QGroupBox("进度控件")
        vbox = QVBoxLayout()

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        vbox.addWidget(self.progress_bar)

        # 滑块
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.on_slider_changed)
        vbox.addWidget(self.slider)

        # 控制按钮
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始进度")
        self.start_btn.clicked.connect(self.start_progress)
        self.reset_btn = QPushButton("重置")
        self.reset_btn.clicked.connect(self.reset_progress)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.reset_btn)

        vbox.addLayout(btn_layout)
        group.setLayout(vbox)
        layout.addWidget(group)

    def on_slider_changed(self, value):
        self.progress_bar.setValue(value)
        self.statusBar().showMessage(f"滑块值: {value}")

    def start_progress(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)

    def update_progress(self):
        self.progress_value += 1
        if self.progress_value > 100:
            self.timer.stop()
            return
        self.progress_bar.setValue(self.progress_value)
        self.slider.setValue(self.progress_value)

    def reset_progress(self):
        self.progress_value = 0
        self.progress_bar.setValue(0)
        self.slider.setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    sys.exit(app.exec_())
```

运行起来看看：

![native ui](https://github.com/hubenchang0515/resource/blob/master/QtTheme/%E5%8E%9F%E7%94%9Fui.png?raw=true)

### 设置全局样式

导入 QtTheme，并通过 Qt 资源系统读取并设置样式即可：

```python
from PyQt5.QtCore import QFile
import QtTheme.PyQt5

class DemoWindow(QMainWindow):
    def __init__(self):
        # 省略...

        qss = QFile(":/QtTheme/theme/Flat/Dark/Blue/Pink.qss")
        qss.open(QFile.OpenModeFlag.ReadOnly)
        self.setStyleSheet(qss.readAll().data().decode())
```

![dark ui](https://github.com/hubenchang0515/resource/blob/master/QtTheme/dark-ui.png?raw=true)

### 设置颜色

最后根据需要，通过 `QWidget.setProperty` 对 widgets 设置颜色：  

```python
    def create_progress_section(self, layout):
        # 省略 ...
        self.start_btn.setProperty("Color", "Primary")
        self.reset_btn.setProperty("Color", "Danger")
```

![color ui](https://github.com/hubenchang0515/resource/blob/master/QtTheme/color-ui.png?raw=true)

### 导出资源

你也可以不安装 `QtTheme`，而是通过 [在线页面](https://hubenchang0515.github.io/QtTheme/) 导出资源文件，
通过 [RCC](https://doc.qt.io/qt-6/rcc.html) 将其加入你的项目：   

```bash
pyrcc5 -o resource.py QtTheme.qrc
```

只需要修改导入方式，其余代码一致:  

```python
from PyQt5.QtCore import QFile
import resource   # 改为导入生成的 resource.py

class DemoWindow(QMainWindow):
    def __init__(self):
        # 省略...

        qss = QFile(":/QtTheme/theme/Flat/Dark/Blue/Pink.qss")
        qss.open(QFile.OpenModeFlag.ReadOnly)
        self.setStyleSheet(qss.readAll().data().decode())

```