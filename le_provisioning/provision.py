#!/usr/local/bin/python2.7
import sys
import urllib
import subprocess
from subprocess import CalledProcessError, PIPE
sys.stdout = open('/var/log/le-provision.log', 'a')


def provision_single_cert(user, domain):
    domain = domain.lower()
    management_email = "tools@thrivehive.com"
    command = "letsencrypt-auto --text --agree-tos --email {0} certonly --renew-by-default --webroot --webroot-path /home/{1}/public_html/ -d {2}"
    command_fmt = command.format(management_email, user, domain)
    with open("/var/log/le-provision.log", 'a') as out:
        try:
            subprocess.check_call(command_fmt, stderr=out, stdout=out, shell=True)
            out.write("SUCCEEDED GETTING CERT")
            install_cert(domain)
        except CalledProcessError as e:
            out.write("FAILED GETTING CERT")
            return True


# this relies on the install directory being the same as the domain name
# several issues can arise here if we park the same domain a second time but
# prepend www or something similar
def install_cert(domain):
    certfile = "/etc/letsencrypt/live/{0}/cert.pem".format(domain)
    keyfile = "/etc/letsencrypt/live/{0}/privkey.pem".format(domain)
    cafile = "/etc/letsencrypt/live/bundle.txt".format(domain)
    certdata = None
    keydata = None
    cadata = None
    try:
        with open(certfile) as myfile:
            certdata = myfile.read()
            certdata = urllib.quote_plus(certdata)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    try:
        with open(keyfile) as myfile:
            keydata = myfile.read()
            keydata = urllib.quote_plus(keydata)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    try:
        with open(cafile) as myfile:
            cadata = myfile.read()
            cadata = urllib.quote_plus(cadata)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    print(cadata)
    with open("/root/sub.txt", 'a') as out:
        try:
            out.write(cadata)
            out.write(certdata)
            out.write(keydata)
            command_fmt = "/usr/sbin/whmapi1 installssl domain={0} crt={1} key={2} cab={3}".format(
                domain, certdata, keydata, cadata)
            p = subprocess.Popen(command_fmt,
                                 stderr=PIPE, stdout=PIPE, shell=True)
            outdata, err = p.communicate()
            out.write("OUTDATA: " + outdata)
            if "result: 1" not in outdata:
                raise CalledProcessError()
        except CalledProcessError as e:
            out.write("FAILED INSTALLING CERT")
            return
