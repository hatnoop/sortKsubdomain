# -*- coding: UTF-8 -*-

import argparse
import json
import ipaddress

def checkCDN_subdomains(subdomain, cname, ips):
    from CDN.checkCDN import checkCDN
    checkCDNresult = checkCDN(cname, ips)
    return checkCDNresult

def parse_args():
    parser = argparse.ArgumentParser(description='Process some input and output files.')
    parser.add_argument('-f', '--input_file', type=str, required=True, help='input file name')
    parser.add_argument('-o', '--output_file', type=str, required=True, help='output file name')
    parser.add_argument('-d', '--sortSubdomain', action='store_true', help='Save subdomains with not empty or not 0.0.0.0 IPs')
    parser.add_argument('-i', '--sortIps', action='store_true', help='Save IPs with Effective internet ip')
    return parser.parse_args()

def is_internal_ip(ip):
    try:
        ip = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return ip.is_private


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
                "domain": subdomain.split('.')[-2] + '.' + subdomain.split('.')[-1]
                "subdomain": subdomain,
                "CNAME": cname,
                "ip": ip,
                "cdn": checkCdn
            })

    with open(args.output_file, 'w') as f:
        f.write(json.dumps(result, indent=4))

    sortSubdomain = []
    if args.sortSubdomain:
        for item in result:
            if item['ip'] and item['ip'] != ['0.0.0.0'] and item['ip'] != ['127.0.0.1']:
                sortSubdomain.append(item['subdomain'])
        subdomainsfilename = "sortSubdomains-" + args.output_file
        with open(subdomainsfilename, 'w') as f:
            f.write('\n'.join(sortSubdomain))

    sortIps = []
    if args.sortIps:
        for item in result:
            if item['cdn'] == 'notcdn':
                for ip in item['ip']:
                    # 检查IP是否在内网范围
                    if not is_internal_ip(ip):
                        sortIps.append(ip)
        sortIps = list(set(sortIps))
        notCDNIPfilename = "sortIps-" + args.output_file
        with open(notCDNIPfilename, 'w') as f:
            f.write('\n'.join(sortIps))



if __name__ == "__main__":
    args = parse_args()
    main(args)
