#!/bin/env python
from subprocess import Popen, PIPE
from flask import Flask, render_template, request
from time import sleep

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

	# Setup DNS server dict:
	dnsserverdict = {
		"ALL DNS": [
			"8.8.8.8",
			"8.8.4.4",
			"208.67.222.222",
			"208.67.220.220"
		],
		"Google": [
			"8.8.8.8",
			"8.8.4.4"
		],
		"OpenDNS": [
			"208.67.222.222",
			"208.67.220.220"
		]
	}

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

	dnslookups = {}

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
