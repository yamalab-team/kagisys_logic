# kagisys_logic
部室自動鍵開閉システムのコア部分

## ソフト側の使い方
### 1. モータに関するソースを`/usr/local/bin`に追加
```shell
cp -rp /servo /usr/local/bin
```

### 2. 自動起動設定をする（`rc.local`にコードの追加）
/etc/rc.localの`exit 0`の上辺りに内に以下のコードを追加。
（$filepathはその場に合わせたパスを書く）
```shell:/etc/rc.local
cd $filepath
./kagisys_start 
```

### 3. kagisys.configを書く
../kagisys.config
```
[SQL]
host_name=ip
user_name=name
user_password=pass
database_name=name

[Slack]
url=url
```

### 4. reboot
