# Golang JSON 序列化时动态忽略字段

在使用 JSON 时经常遇到需要忽略字段的情况，例如返回用户信息时不能返回密码，通常将注解 TAG 设为 `json:"-"` 即可:  

```go
type User struct {
	Account  string `json:"account"`
	Password string `json:"-"`
	Nickname string `json:"nickname"`
}
```

但这样的静态配置会使字段在任何情况下都被忽略，有时希望可以根据需求动态的决定是否忽略某些字段。

可以通过反射将读取对象的字段名和字段值，过滤忽略的字段后存入一个 `map[string]any` 中，然后进行序列化:  

```go
package utils

import (
	"encoding/json"
	"reflect"
)

func JsonMarshalWithFilter(data any, ignore []string) ([]byte, error) {
	filter := make(map[string]bool)
	for i := range ignore {
		name := ignore[i]
		filter[name] = true
	}
	m := make(map[string]any)
	metaType := reflect.TypeOf(data)
	metaValue := reflect.ValueOf(data)
	n := metaType.NumField()
	for i := 0; i < n; i++ {
		field := metaType.Field(i)
		name := field.Tag.Get("json")
		if filter[name] {
			continue
		}
		value := metaValue.Field(i).Interface()
		m[name] = value
	}

	return json.Marshal(m)
}
```

调用:    

```go
package main

import "utils"

type User struct {
	Account  string `json:"account"`
	Password string `json:"password"`
	Nickname string `json:"nickname"`
}

func main() {
	user := schema.User{
		Account:  "hubenchang0515",
		Password: "xxxxxxxxx",
		Nickname: "planc0515",
	}

	data, _ := utils.JsonMarshalWithFilter(user, []string{"password"})
	println(string(data))
}
```

```
$ go run .
{"account":"hubenchang0515","nickname":"planc0515"}
```