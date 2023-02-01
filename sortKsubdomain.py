# -*- coding: UTF-8 -*-

import argparse
import json

def checkCDN_subdomains(subdomain, cname, ips):
    from CDN.checkCDN import checkCDN
    checkCDNresult = checkCDN(cname, ips)
    return checkCDNresult

def parse_args():
    parser = argparse.ArgumentParser(description='Process some input and output files.')
    parser.add_argument('-f', '--input_file', type=str, required=True, help='input file name')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='output file name')
    return parser.parse_args()

def main(args):
    result = []

    with open(args.input_file) as f:
        for line in f:
            subdomain, *rest = line.strip().split("=>")
            ip = []
            cname = []
            for item in rest:
                if item.startswith("CNAME"):
                    cname.append(item.replace("CNAME ", ""))
                else:
                    ip.append(item)
            checkCdn = checkCDN_subdomains(subdomain, cname, ip)
            result.append({
                "subdomain": subdomain,
                "CNAME": cname,
                "ip": ip,
                "cdn": checkCdn
            })

    with open(args.output_file, 'w') as f:
        f.write(json.dumps(result, indent=4))

if __name__ == "__main__":
    args = parse_args()
    main(args)
