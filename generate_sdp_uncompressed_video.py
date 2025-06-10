#!/usr/bin/env python3


import argparse
import sys
import re

def parse_resolution(res_str):
    try:
        width, height = map(int, res_str.lower().split("x"))
        return width, height
    except:
        raise argparse.ArgumentTypeError("解像度は 1920x1080 の形式で指定してください / Format must be WIDTHxHEIGHT like 1920x1080")

def prompt_with_default(prompt_text, default):
    user_input = input(f"{prompt_text} [Default: {default}]: ").strip()
    return user_input if user_input else default

def prompt_int_with_default(prompt_text, default):
    user_input = input(f"{prompt_text} [Default: {default}]: ").strip()
    return int(user_input) if user_input else default

def sanitize_filename(name):
    name = name.lower().strip()
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'[^a-z0-9_]', '', name)
    return name + ".sdp"

def interactive_mode():
    print("🛠 SDPファイルを生成します（対話モード）\n🛠 Generating SDP file (Interactive Mode)\n")

    src1 = input("Primary送信元IPアドレス (Primary Source IP Address): ").strip()
    grp1 = input("PrimaryマルチキャストIPアドレス (Primary Multicast IP Address): ").strip()
    port1 = prompt_int_with_default("Primaryポート番号 (Primary Port)", 30000)

    use_secondary = input("セカンダリも設定しますか？ (Do you want to configure secondary/ST2022-7?) [yes/no]: ").strip().lower() == "yes"
    if use_secondary:
        src2 = input("Secondary送信元IPアドレス (Secondary Source IP Address): ").strip()
        grp2 = input("SecondaryマルチキャストIPアドレス (Secondary Multicast IP Address): ").strip()
        port2 = prompt_int_with_default("Secondaryポート番号 (Secondary Port)", 30000)
    else:
        src2 = grp2 = port2 = None

    mac1 = prompt_with_default("Primary MACアドレス (Primary MAC Address)", "00-09-0D-01-2B-EE")
    mac2 = prompt_with_default("Secondary MACアドレス (Secondary MAC Address)", "00-09-0D-01-2B-EF")
    resolution = prompt_with_default("解像度 (Resolution, e.g., 1920x1080)", "1920x1080")
    framerate = prompt_with_default("フレームレート (Framerate, e.g., 30000/1001)", "30000/1001")
    interlace = prompt_with_default("インターレース？ (Interlace? yes/no)", "yes").lower() == "yes"
    session = prompt_with_default("セッション名（Session name, e.g., uncompressed_video_feed）", "uncompressed_video_feed")
    outfile = prompt_with_default("出力ファイル名 (Output filename)", sanitize_filename(session))

    return {
        "source_ip_1": src1,
        "multicast_ip_1": grp1,
        "port_1": port1,
        "source_ip_2": src2,
        "multicast_ip_2": grp2,
        "port_2": port2,
        "mac_1": mac1,
        "mac_2": mac2,
        "output_file": outfile,
        "resolution": tuple(map(int, resolution.split("x"))),
        "framerate": framerate,
        "interlace": interlace,
        "session": session
    }

def generate_sdp(source_ip_1, multicast_ip_1, port_1,
                 source_ip_2, multicast_ip_2, port_2,
                 mac_1, mac_2, output_file,
                 resolution, framerate, interlace,
                 session):

    width, height = resolution
    fmtp_parts = [
        f"sampling=YCbCr-4:2:2",
        f"width={width}",
        f"height={height}",
        f"depth=10",
        f"exactframerate={framerate}"
    ]
    if interlace:
        fmtp_parts.append("interlace")
    fmtp_parts += [
        "colorimetry=BT709",
        "TCS=SDR",
        "SSN=ST2110-20:2017",
        "TP=2110TPN",
        "PM=2110BPM"
    ]
    fmtp_common = '; '.join(fmtp_parts) + ";"

    origin = f"OPERATOR 1112223333 1112223333 IN IP4 {source_ip_1}"

    sdp = f"""v=0
o={origin}
s={session}
t=0 0"""

    st2022_7_enabled = all([source_ip_2, multicast_ip_2, port_2])
    if st2022_7_enabled:
        sdp += "\na=group:DUP primary secondary"

    sdp += f"""
m=video {port_1} RTP/AVP 96
c=IN IP4 {multicast_ip_1}/64
a=rtpmap:96 raw/90000
a=fmtp:96 {fmtp_common}
a=source-filter: incl IN IP4 {multicast_ip_1} {source_ip_1}
a=ts-refclk:localmac={mac_1}
a=mediaclk:direct=0
a=mid:primary
"""

    if st2022_7_enabled:
        sdp += f"""
m=video {port_2} RTP/AVP 96
c=IN IP4 {multicast_ip_2}/64
a=rtpmap:96 raw/90000
a=fmtp:96 {fmtp_common}
a=source-filter: incl IN IP4 {multicast_ip_2} {source_ip_2}
a=ts-refclk:localmac={mac_2}
a=mediaclk:direct=0
a=mid:secondary"""

    with open(output_file, "w") as f:
        f.write(sdp.strip() + "\n")
    print(f"✅ SDPファイルが生成されました: {output_file}（ST2022-7 {'対応 / Enabled' if st2022_7_enabled else '非対応 / Disabled'}）")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        args_dict = interactive_mode()
        generate_sdp(**args_dict)
    else:
        parser = argparse.ArgumentParser(
            description="SDPファイル生成（非圧縮映像 / ST2110準拠）Generate SDP file (uncompressed video, ST2110)"
        )

        parser.add_argument("-s1", "--src1", required=True, help="Primary Source IP Address")
        parser.add_argument("-g1", "--grp1", required=True, help="Primary Multicast IP Address")
        parser.add_argument("-p1", "--port1", type=int, required=True, help="Primary Port")
        parser.add_argument("-s2", "--src2", help="Secondary Source IP Address")
        parser.add_argument("-g2", "--grp2", help="Secondary Multicast IP Address")
        parser.add_argument("-p2", "--port2", type=int, help="Secondary Port")
        parser.add_argument("-m1", "--mac1", default="00-09-0D-01-2B-EE", help="Primary MAC Address")
        parser.add_argument("-m2", "--mac2", default="00-09-0D-01-2B-EF", help="Secondary MAC Address")
        parser.add_argument("-r", "--resolution", type=parse_resolution, default=(1920, 1080), help="Resolution (e.g., 1920x1080)")
        parser.add_argument("-f", "--framerate", default="30000/1001", help="Framerate (e.g., 30000/1001)")
        parser.add_argument("-i", "--interlace", choices=["yes", "no"], default="yes", help="Interlace (yes/no)")
        parser.add_argument("--session", required=True, help="SDP session name (e.g., uncompressed_video_feed)")
        parser.add_argument("-o", "--out", help="Output filename")

        args = parser.parse_args()
        output_file = args.out or sanitize_filename(args.session)

        generate_sdp(
            args.src1, args.grp1, args.port1,
            args.src2, args.grp2, args.port2,
            args.mac1, args.mac2, output_file,
            resolution=args.resolution,
            framerate=args.framerate,
            interlace=(args.interlace == "yes"),
            session=args.session
        )
