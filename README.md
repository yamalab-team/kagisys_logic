# kagisys_logic
7505室自動鍵開閉システムのコア部分

webui未着手

## ソフト側の使い方
### 1. モータに関するソースを`/usr/local/bin`に追加
モータに関するソースを`/usr/local/bin`にコピー。
```shell:
cp -rp ./servo /usr/local/bin
```

### 2. 自動起動設定をする（systemctl）
/etc/systemd/system にファイルを作成（例: kagisys.service）
```shell:/etc/systemd/system/kagisys.service
[Unit]
Description=名前

[Service]
ExecStart=/usr/bin/python  任意のパス/kagisys_logic/kagisys_start

[Install]
WantedBy=multi-user.target
```
`# systemctl enable kagisys.service`

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
- LED(解鍵時) -> [21]
- LED(施錠時) -> [13]
- LED(内側のフルカラー) -> 18
- BUTTON(左) -> 20
- BUTTON(中) -> 19
- BUTTON(右) -> 26
- NFCリーダー(SCL) -> 14
- NFCリーダー(SDA) -> 15
- サーボ -> 12
- LCD(SCL) -> 3
- LCD(SDA) -> 2
- LCD(VCC) -> 17
