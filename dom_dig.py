#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import argparse

import subprocess
import datetime
import time

import urllib2
import sys
import csv
import pickle


"""
TODO:

"""


class DigUtils:
    def __init__(self):
        self.__query_timeout=5 # vnutit query time
        self.__timeout=5
        self.__last_query_time={}
        self.__tries=3
        self.__tor_enabled=False
    
    def set_tor(self,enabled=True):
        pass
    
    def get_tor_stat(self):
        pass
    
    def test_tor(self):
        pass
    
    def _test_torsocks(self):
        pass
    
    def set_settings(self,enable_tcp=False, enable_tor=False, time=5, tries=3,query_timeout=5):
        pass

    def __call_dig(self,domain, resolver_ip, enable_tcp=False, enable_tor=False, time=5, tries=3):
        args=[]
        cmd=["dig"]
        args.append("time=%d" % time)
        args.append("tries=%d" % tries)
        if enable_tor==True:
            cmd=["torsocks dig"]
        if enable_tcp==True:
            args.append("+tcp")
        args.append("@%s" % resolver_ip)
        args.append(domain)
        #print "aaaaaaaaa",cmd+args
        proc_call=" ".join(cmd+args)
        proc = subprocess.Popen(proc_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        err_txt=None    
        if err.find("socket() failed:")>=0:
            err_txt="Err Tor not working"
        return out,err

    def dig(self, dom, res_ip, wait=True):
        #return dictionary with full and resolverd ip....
        if res_ip in self.__last_query_time:
            timediff=self.__last_query_time[res_ip]-datetime.datetime.now()
            while abs(timediff.total_seconds()) < self.__query_timeout:
                time.sleep(0.1)                
                timediff=self.__last_query_time[res_ip]-datetime.datetime.now()
        self.__last_query_time[res_ip]=datetime.datetime.now()
        result,result_err=self.__call_dig(dom,
                               res_ip,
                               self.__tor_enabled,
                               self.__tor_enabled,
                               self.__timeout,
                               self.__tries)
        return result
    
    def __conv_answer(self,line):
        if len(line.split())==5:
            dom_name,ttl,dns_class,dns_type,ipaddr=line.split()
            return {"name":dom_name,"ttl":ttl,"class":dns_class,"type":dns_type,"ip":ipaddr}
        return []
        
    def parse_answer(self, dig_text):
        state=0
        out_list=[]
        for line in dig_text.splitlines():
            if line.find(";; ANSWER SECTION:")>=0:
                state=1
            elif state==1 and line.find(";;")<0:
                out_list.append(self.__conv_answer(line))
        return [x for x in out_list if x != []]



class CliUI:
    def __init__(self,res_ip="8.8.8.8", json_out=None, file_in=None, continue_resolv=True, print_simple=True):
        self.__res_ip=res_ip
        self.__json_out=json_out
        self.__file_in=file_in
        self.__continue_resolv=continue_resolv
        self.__out_list=[]
        self.__dig=DigUtils()
        self.__print_simple=print_simple
    
    def update_output(self):
        pass

    def get_domain(self, domain,ip):
        tmp_out=self.__dig.dig(domain,self.__res_ip)
        #print "aaaaaaaaaaaaaaaaaaaaaaaaaa",tmp_out
        tmp_ans=self.__dig.parse_answer(tmp_out)
        self.__out_list.append(tmp_ans)
        self.update_output()
        if self.__print_simple==True:
            print tmp_ans[0]["ip"],";",tmp_ans[0]["name"]
        else:
            print tmp_ans
    
    def get_domain_batch(self):
        with open(self.__file_in,"r") as fp:
            if self.__continue_resolv==True:
                pass
            for line in fp.readlines():
                pass
            
def main():
    aa=None
    parser = argparse.ArgumentParser(description='Domain')
    parser.add_argument('--continue-flag','-cf',
                        action='store_true',
                        help='Continue download flag' )
    parser.add_argument('--print-simple',
                        action='store_true',
                        help="Print data")
    parser.add_argument('--domain','-d',
                        help='Get tag for domain' )
    parser.add_argument('--resolver','-rip',
                        help='Open resolver ip' )   
    parser.add_argument('--output','-o',
                        help='Output file' )
    parser.add_argument('--input','-i',
                        help='Input file' )
    args = parser.parse_args()
    
    if args.resolver==None:
        print "Error resolver must be set"        
        return
    
    if args.input:
        if args.output:
            aa=CliUI(res_ip=args.resolver,
                         json_out=args.output,
                         file_in=args.input,
                         continue_resolv=args.continue_flag,
                         print_simple=args.print_simple)
        
            aa.get_domain(args.domain,args.resolver)                                                                                                                                                                                                                                                                                                                                                
    else:
        aa=CliUI(res_ip=args.resolver,print_simple=args.print_simple)
        aa.get_domain(args.domain,args.resolver)

if __name__ == '__main__':
    main()

