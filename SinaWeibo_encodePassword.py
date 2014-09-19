#!/usr/bin/python
#-*- coding: utf-8 -*-

import rsa
import binascii
def encodePassword(pwd,time,nonce,pubkey):
    '''
    ctxt = PyV8.JSContext()
    ctxt.enter()
    func = ctxt.eval("""
        (function(password,servertime,nonce){
            var o=8; 
            var n=0;
            
            var hex_sha1=function(s){return A(p(z(s),s.length*o))};

            var p=function(x,f){x[f>>5]|=0x80<<(24-f%32);x[((f+64>>9)<<4)+15]=f;var w=Array(80);var a=1732584193;var b=-271733879;var c=-1732584194;var d=271733878;var e=-1009589776;for(var i=0;i<x.length;i+=16){var g=a;var h=b;var k=c;var l=d;var m=e;for(var j=0;j<80;j++){if(j<16)w[j]=x[i+j];else w[j]=v(w[j-3]^w[j-8]^w[j-14]^w[j-16],1);var t=u(u(v(a,5),q(j,b,c,d)),u(u(e,w[j]),r(j)));e=d;d=c;c=v(b,30);b=a;a=t}a=u(a,g);b=u(b,h);c=u(c,k);d=u(d,l);e=u(e,m)}return Array(a,b,c,d,e)};

            var q=function(t,b,c,d){if(t<20)return(b&c)|((~b)&d);if(t<40)return b^c^d;if(t<60)return(b&c)|(b&d)|(c&d);return b^c^d};

            var r=function(t){return(t<20)?1518500249:(t<40)?1859775393:(t<60)?-1894007588:-899497514};

            var u=function(x,y){var a=(x&0xFFFF)+(y&0xFFFF);var b=(x>>16)+(y>>16)+(a>>16);return(b<<16)|(a&0xFFFF)};

            var v=function(a,b){return(a<<b)|(a>>>(32-b))};

            var z=function(a){var b=Array();var c=(1<<o)-1;for(var i=0;i<a.length*o;i+=o)b[i>>5]|=(a.charCodeAt(i/o)&c)<<(24-i%32);return b};

            var A=function(a){var b=n?"0123456789ABCDEF":"0123456789abcdef";var c="";for(var i=0;i<a.length*4;i++){c+=b.charAt((a[i>>2]>>((3-i%4)*8+4))&0xF)+b.charAt((a[i>>2]>>((3-i%4)*8))&0xF)}return c};
            
            return hex_sha1(""+hex_sha1(hex_sha1(password))+servertime+nonce);
        })
    """)
    return func(pwd,time,nonce)
    '''
    rsaPublickey = int(pubkey,16)
    key = rsa.PublicKey(rsaPublickey,65537)
    message = str(time)+'\t'+str(nonce)+'\n'+str(pwd)
    passwd = rsa.encrypt(message,key)
    return binascii.b2a_hex(passwd)
    
