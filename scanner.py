#!/usr/bin/env python3
import socket, argparse, csv
from concurrent.futures import ThreadPoolExecutor

def scan(host,start,end):
    results=[]
    for port in range(start,end+1):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            if s.connect_ex((host,port))==0:
                results.append((port,"OPEN"))
                print(f"{port:<6} OPEN")
        except Exception:
            pass
        finally:
            s.close()
    return results

def threaded(host,start,end,workers):
    ports=list(range(start,end+1))
    chunks=[ports[i::workers] for i in range(workers)]
    results=[]
    def worker(chunk):
        out=[]
        for p in chunk:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(0.5)
            try:
                if s.connect_ex((host,p))==0:
                    print(f"{p:<6} OPEN")
                    out.append((p,"OPEN"))
            finally:
                s.close()
        return out
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for r in ex.map(worker,chunks):
            results.extend(r)
    return results

def main():
    ap=argparse.ArgumentParser(description="Simple TCP Port Scanner")
    ap.add_argument("host")
    ap.add_argument("-p","--ports",default="1-1024")
    ap.add_argument("-t","--threads",type=int,default=1)
    ap.add_argument("--csv",help="Save results to CSV")
    args=ap.parse_args()
    start,end=map(int,args.ports.split("-"))
    try:
        host=socket.gethostbyname(args.host)
    except socket.gaierror:
        print("Invalid host"); return
    print(f"Scanning {args.host} ({host}) ports {start}-{end}")
    res=threaded(host,start,end,args.threads) if args.threads>1 else scan(host,start,end)
    if args.csv:
        with open(args.csv,"w",newline="") as f:
            w=csv.writer(f); w.writerow(["Port","Status"]); w.writerows(res)
        print("Saved:",args.csv)

if __name__=="__main__":
    main()
