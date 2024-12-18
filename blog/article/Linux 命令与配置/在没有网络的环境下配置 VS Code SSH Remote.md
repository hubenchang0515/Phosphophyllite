# 在没有网络的环境下配置 VS Code SSH Remote

VS Code SSH Remote 连接时需要在远程主机上下载 VS Code Server，没有网络时无法自动下载，需要手动下载并复制到正确的路径中去。

点击 VS Code菜单栏 `Help->About` ，查看当前客户端版本的 `<Commit-ID>`:

![help-about](https://github.com/hubenchang0515/resource/blob/master/VSCode/help-about.png)

```
Version: 1.73.1
Commit: 6261075646f055b99068d3688932416f2346dd3b
Date: 2022-11-09T03:54:53.913Z
Electron: 19.0.17
Chromium: 102.0.5005.167
Node.js: 16.14.2
V8: 10.2.154.15-electron.0
OS: Linux x64 5.15.0-53-generic
Sandboxed: No
```

根据 `<Commit-ID>` 下载对应版本的 VS Code Server:  

```
https://vscode.cdn.azure.cn/stable/<Commit-ID>/vscode-server-<OS-Name>-<ARCH>.tar.gz
```

例如:  

```
https://vscode.cdn.azure.cn/stable/6261075646f055b99068d3688932416f2346dd3b/vscode-server-linux-arm64.tar.gz
```

将其解压并命名为 `<Commit-ID>`，然后复制到 `~/.vscode-server/bin/` 目录中。