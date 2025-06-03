# 🧰 generate_sdp_uncompressed_video

非圧縮映像（SMPTE ST 2110-20）向けの SDP ファイルを簡単に生成するための Python CLI ツールです。  
This is a simple Python CLI tool to generate SDP files for uncompressed video (SMPTE ST 2110-20).

ST 2022-7（冗長化）対応や、解像度・フレームレート・インターレースの指定にも対応しています。  
It supports ST 2022-7 redundancy and allows customization of resolution, framerate, and interlace settings.

---

## ✨ 特徴 / Features

- ST 2110-20（非圧縮映像）に準拠した SDP ファイルを生成  
  Generate SDP files compliant with ST 2110-20 (uncompressed video)
- ST 2022-7（冗長化）対応（セカンダリ入力が指定された場合）  
  Supports ST 2022-7 redundancy (if secondary stream is provided)
- 解像度、フレームレート、インターレースの指定が可能  
  Supports custom resolution, framerate, and interlace settings
- コマンドライン引数または対話モードでの入力に対応  
  Supports both command-line and interactive input modes
- セッション名から自動的にファイル名を生成  
  Automatically generates output filename from session name
- Python 標準ライブラリのみを使用（外部依存なし）  
  Uses only Python standard libraries (no external dependencies)

---

## 🛠 インストール / Installation

Python 3.6 以降が必要です。  
Python 3.6 or later is required.

```bash
git clone https://github.com/yourusername/generate_sdp_uncompressed_video.git
cd generate_sdp_uncompressed_video
chmod +x generate_sdp_uncompressed_video.py
```

---

## 🚀 使い方 / Usage

### ✅ 対話モード / Interactive Mode

引数なしで実行すると、対話モードが起動します。  
Run without arguments to launch the interactive prompt.

```bash
./generate_sdp_uncompressed_video.py
```

### ✅ コマンドライン引数 / Command-Line Arguments

必要な情報を引数で指定して実行できます。  
Specify all required information via arguments.

```bash
./generate_sdp_uncompressed_video.py \
  -s1 10.30.71.10 -g1 239.107.1.1 -p1 50020 \
  --session "uncompressed_video_feed"
```

追加オプションの例：  
Optional parameters:

```bash
  -s2 10.30.71.11 -g2 239.107.1.2 -p2 50021 \
  -r 1920x1080 -f 30000/1001 -i yes \
  -o output.sdp
```

---

## 📄 出力例 / Sample Output

以下は、生成される SDP ファイルの一部です：  
Example output from the generated SDP file:

```
v=0
o=OPERATOR 1112223333 1112223333 IN IP4 10.0.0.10
s=uncompressed_video_feed
t=0 0
a=group:DUP primary secondary
m=video 30000 RTP/AVP 96
c=IN IP4 239.1.1.1/64
a=rtpmap:96 raw/90000
a=fmtp:96 sampling=YCbCr-4:2:2; width=1920; height=1080; depth=10; exactframerate=30000/1001; interlace; colorimetry=BT709; TCS=SDR; SSN=ST2110-20:2017; TP=2110TPN; PM=2110BPM;
a=source-filter: incl IN IP4 239.1.1.1 10.0.0.10
a=ts-refclk:localmac=00-09-0D-11-22-EE
a=mediaclk:direct=0
a=mid:primary
```

---

## 🤝 貢献 / Contribution

このツールは、放送現場での手作業を減らすために作成しました。  
This tool was developed to reduce manual steps in broadcast environments.

ご意見や改善提案がありましたら、Issue や Pull Request をお寄せください。  
Feel free to contribute via Issues or Pull Requests.

---

## 📜 ライセンス / License

MIT License

---

ご利用いただきありがとうございます。  
Thank you for using this tool.  

このツールが皆様の業務の一助となれば幸いです。  
I hope it helps streamline your workflow.
