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
    parser.add_argument('-d', '--empty_ips', action='store_true', help='Save subdomains with not empty or not 0.0.0.0 IPs')
    parser.add_argument('-i', '--not_cdn', action='store_true', help='Save IPs with cdn value notcdn')

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

    empty_ips = []
    if args.empty_ips:
        for item in result:
            if item['ip'] and item['ip'] != ['0.0.0.0']:
                empty_ips.append(item['subdomain'])
        subdomainsfilename = "subdomains-" + args.output_file
        with open(subdomainsfilename, 'w') as f:
            f.write('\n'.join(empty_ips))

    not_cdn = []
    if args.not_cdn:
        for item in result:
            if item['cdn'] == 'notcdn':
                not_cdn.extend(item['ip'])
        not_cdn = list(set(not_cdn))
        notCDNIPfilename = "notCDNIP-" + args.output_file
        with open(notCDNIPfilename, 'w') as f:
            f.write('\n'.join(not_cdn))


if __name__ == "__main__":
    args = parse_args()
    main(args)
