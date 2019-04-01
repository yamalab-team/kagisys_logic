# kagisys_logic
7505室自動鍵開閉システムのコア部分

## ソフト側の使い方
### 1. モータに関するソースを`/usr/local/bin`に追加
モータに関するソースを`/usr/local/bin`にコピー。
```shell:
cp -rp ./servo /usr/local/bin
```

### 2. 自動起動設定をする（`rc.local`にコードの追加）
/etc/rc.localの`exit 0`の上辺りに内に以下のコードを追加。
（$filepathはその場に合わせたパスを書く）
```shell:/etc/rc.local
cd $filepath
./kagisys_start 
```

### 3. kagisys.configを書く
../kagisys.configには以下のように書く。
```
[SQL]
host_name=ip
user_name=name
user_password=pass
database_name=name

[Slack]
url=url

[MYSQL]
url=mysql://hogehoge
```

### 4. 再起動
再起動する
```shell
sudo reboot
```

## GPIOの接続（BCM番号）
- LED(解鍵時) -> [20, 21]
- LED(施錠時) -> [16, 13]
- BUTTON(解鍵) -> 19
- BUTTON(施錠) -> 26
- NFCリーダー(SCL) -> 14
- NFCリーダー(SDA) -> 15
- サーボ -> 12
- LCD(SCL) -> 3
- LCD(SDA) -> 2
- LCD(VCC) -> 18
