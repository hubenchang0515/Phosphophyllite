# MUI 集成 nextjs


## 安装依赖包

首先确认安装了 next 和 MUI：  

```bash
npm install next react react-dom @mui/material @emotion/react @emotion/styled
```

然后安装 MUI 的 nextjs 兼容包：

```bash
npm install @mui/material-nextjs @emotion/cache
```

## 配置

### 基本配置

编辑 `app/layout.tsx`，添加 APP Router:

```tsx
import { AppRouterCacheProvider } from '@mui/material-nextjs/v15-appRouter';

export default function RootLayout(props) {
    return (
        <html lang="en">
            <body>
                <AppRouterCacheProvider>
                    {props.children}
                </AppRouterCacheProvider>
            </body>
        </html>
    );
}
```

### 主题配置

创建单独的 `theme.ts` 文件:  

```ts
'use client';
import { blue, pink } from '@mui/material/colors';
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
    // 使用 CSS 主题变量，防止 SSR 闪烁
    cssVariables: {
        colorSchemeSelector: 'class'
    },

    // 颜色配置
    colorSchemes: {
        light: {
            palette: {
                primary: blue
                secondary: pink,
                mode: 'light',
            },
        },
        dark: {
            palette: {
                primary: blue
                secondary: pink,
                mode: 'dark',
            },
        }
    },

    // 字体配置
    typography: {
        fontFamily: 'var(--font-roboto)',   
    }, 
});

export default theme;
```

编辑 `app/layout.tsx`， 添加主题配置:

```tsx
import { AppRouterCacheProvider } from '@mui/material-nextjs/v15-appRouter';
import { ThemeProvider } from "@mui/material";
import InitColorSchemeScript from "@mui/material/InitColorSchemeScript";
import theme from "theme";

export default function RootLayout(props) {
    return (
        <html lang="en" suppressHydrationWarning>
            <body>
                <AppRouterCacheProvider>
                    <ThemeProvider theme={theme}>
                        <InitColorSchemeScript attribute="class" />
                        {props.children}
                    </ThemeProvider>
                </AppRouterCacheProvider>
            </body>
        </html>
    );
}
```

使用 `useColorScheme` 来获取和操作主题：  

```ts
const {mode, setMode} = useColorScheme();
```

参考文档：https://mui.com/material-ui/integrations/nextjs/