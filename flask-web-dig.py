#!/bin/env python
from subprocess import Popen, PIPE
from flask import Flask, render_template, request
from time import sleep
from collections import OrderedDict

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

	# Setup DNS server dict:
	dnsserverdict = OrderedDict([
		("ALL DNS", [
			"89.233.43.71",
			"89.104.194.142",
			"8.26.56.26",
			"8.20.247.20",
			"156.154.70.1",
			"156.154.71.1",
			"216.146.35.35",
			"216.146.36.36",
			"8.8.8.8",
			"8.8.4.4",
			"81.218.119.11",
			"209.88.198.133",
			"74.82.42.42",
			"209.244.0.3",
			"209.244.0.4",
			"198.153.192.40",
			"198.153.194.40",
			"208.67.222.222",
			"208.67.220.220",
			"216.87.84.211",
			"23.90.4.6",
			"199.5.157.131",
			"208.71.35.137",
			"109.69.8.51",
			"195.46.39.39",
			"195.46.39.40",
			"184.169.143.224",
			"184.169.161.155",
			"208.76.50.50",
			"208.76.51.51"
			]),
		("censurfridns.dk", [
			"89.233.43.71",
			"89.104.194.142"
		]),
		("Comodo Secure DNS", [
			"8.26.56.26",
			"8.20.247.20"
		]),
		("DNS Advantage", [
			"156.154.70.1",
			"156.154.71.1"
		]),
		("Dyn", [
			"216.146.35.35",
			"216.146.36.36"
		]),
		("Google", [
			"8.8.8.8",
			"8.8.4.4"
		]),
		("GreenTeamDNS", [
			"81.218.119.11",
			"209.88.198.133"
		]),
		("Hurricane Electric", [
			"74.82.42.42"
		]),
		("Level3", [
			"209.244.0.3",
			"209.244.0.4"
		]),
		("Norton ConnectSafe", [
			"198.153.192.40",
			"198.153.194.40"
		]),
		("OpenDNS Home", [
			"208.67.222.222",
			"208.67.220.220"
		]),
		("OpenNIC", [
			"216.87.84.211",
			"23.90.4.6"
		]),
		("Public-Root", [
			"199.5.157.131",
			"208.71.35.137"
		]),
		("puntCAT", [
			"109.69.8.51"
		]),
		("SafeDNS", [
			"195.46.39.39",
			"195.46.39.40"
		]),
		("Securly", [
			"184.169.143.224",
			"184.169.161.155"
		]),
		("SmartViper", [
			"208.76.50.50",
			"208.76.51.51"
		])
	])

	# Determine if we need to display the form
	if request.method == 'POST':
		displayform = None
	else:
		displayform = True
		return render_template("index.html",
			dnsserverdict = dnsserverdict,
			displayform = displayform)

	# List of dns servers
	dnsservers = dnsserverdict[request.form["nameservers"]]

	# Domain to lookup

	domain = request.form["domainname"]

	# Create a dictionary to store our data

	dnslookups = OrderedDict()

	# Add process objects to dictionary

	for dnsserver in dnsservers:
		dnslookups[dnsserver] = {"process": Popen( [ "dig", "@%s" %(dnsserver), domain, "+short"  ], stdout=PIPE )}

	# Wait for all processes to complete

	for dnsserver in dnslookups.keys():
		dnslookups[dnsserver]["process"].wait()

	# retreive results

	for dnsserver in dnslookups.keys():
		dnslookups[dnsserver]["result"] = dnslookups[dnsserver]["process"].communicate()[0]

	return render_template("index.html",
		displayform = displayform,
		dnslookups = dnslookups,
		domain = domain,
		nameservers = request.form["nameservers"])

app.run(debug = True)
