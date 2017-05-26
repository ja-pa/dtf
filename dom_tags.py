#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
todo:
add timeout:http://stackoverflow.com/questions/2712524/handling-urllib2s-timeout-python
make cli interface
save output to json
"""

import threading
import urllib2
import sys
import argparse
import time
import datetime
        
class DomainTags:
    def __init__(self,filename_in=None,filename_out=None):
        self._THREADS=[]
        self._OUTPUT=[]
        self._INPUT=[]
        if filename_in != None:    
            self._INPUT=self._read_domains(filename_in)
        
        self._filename_out = filename_out
        if filename_out != None:
            pass
        
    def _read_domains(self,filename):
        with open(filename)as fp:
            str_list=fp.read().splitlines()
        str_list = filter(None, str_list)
        return str_list
        
        
    def _get_active_count(self):
        ret=0
        for i in self._THREADS:
            if i.is_alive():
                ret+=1
            else:
                self._THREADS.remove(i)
        return ret
    
    def _worker(self,domain):
        dom=self.get_domain_tag(domain)
        self._OUTPUT.append(dom)
        return
    
    def _write_to_file(self):
        with open(self._filename_out,"a") as fp:
            for item in list(self._OUTPUT):
                fp.write(str(item)+"\n")
                self._OUTPUT.remove(item)
        
    def start_domain_tags(self,max_limit=10):
        while len(self._INPUT)>0:
            time.sleep(0.2)
            print "sleeep...."
            active_count=self._get_active_count()
            if self._filename_out!=None:
                self._write_to_file()
            print "active",active_count
            print "OUTPUT",len(self._OUTPUT)
            print "INPUT",len(self._INPUT)
            print "THREADS",len(self._THREADS)    
            while active_count<max_limit:
                if len(self._INPUT)>0:
                    active_count+=1
                    dom=self._INPUT.pop()
                    t = threading.Thread(target=self._worker, args=(dom,))
                    self._THREADS.append(t)
                    t.start()
                else:
                    break
        if self._filename_out!=None:
            self._write_to_file()

    def get_domain_tag(self,domain,out_list=None):
        start_time = time.time()
        response = urllib2.urlopen('https://domain.opendns.com/'+domain)
        html = response.read()
        
        bb=html.split("h3")
    
        if len(bb)==1 or html.find("Not yet decided in any categories")>=0:
            return "notdecided"
        bb=bb[1]
        if bb.find("Be the first to tag this domain")==-1:
            bb= bb.replace(">Tagged:","")
            bb= bb.replace('<span class="normal">',"")
            bb= bb.replace('</span>',"")
            bb= bb.replace('</',"")
            bb= bb.strip()
            if bb.find("Inherited Tag")>=0:
                bb=bb.split(":")[1].strip()
        else:
            bb="unknown"
        timediff= (time.time() - start_time)
        ret = {"category":bb,
              "domain":domain,
              "runtime_sec":timediff,
              "date":datetime.datetime.now()}
        if out_list != None:
            out_list.append(ret)
        return ret


def main():
    parser = argparse.ArgumentParser(description='Domain tags')
    parser.add_argument('--verbose',
        action='store_true',
        help='verbose flag' )
    parser.add_argument('--print-format-csv',
        action='store_true',
        help='Print only output in format DOMAIN;TAG' )
    parser.add_argument('--domain','-d',
        help='Get tag for domain' )
    parser.add_argument('--print-domain','-pd',
        action='store_true',
        help='print domain name' )
    parser.add_argument('--print-runtime','-prt',
        action='store_true',
        help='print domain name' )
    parser.add_argument('--output','-o',
        help='Output file' )
    parser.add_argument('--print-simple','-ps',
        action='store_true',
        help='print domain name' )
            
    args = parser.parse_args()
    if args.domain:
        dom=DomainTags()
        #dom_tagdom.get_domain_tag(args.domain)
        ret = dom.get_domain_tag(args.domain)
        ret["category"]
        if args.print_simple:
            print ret["domain"],";",ret["category"]
        else:
            print ret

if __name__ == '__main__':
    main()
