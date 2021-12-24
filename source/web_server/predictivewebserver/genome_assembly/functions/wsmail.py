#!/usr/bin/env python3

import smtplib
import os

import argparse
import requests

def send_simple_message(user_email, user_id):
    	return requests.post(
		"https://api.mailgun.net/v3/sandbox8fad4c5babbc42efa2db9fcb32a17302.mailgun.org/messages",
		auth=("api", "1e6e6a06254d247041962554b4a464ed-2a9a428a-d2afed02"),
		data={"from": "Mailgun Sandbox <postmaster@sandbox8fad4c5babbc42efa2db9fcb32a17302.mailgun.org>",
			"to": f"{user_email}",
			"subject": "Congrats your submitted job on the web server is finished",
			"text": f"""Hello,

                        The submitted job is now finished. Kindly visit this link to download results:
                        http://team2.predict2021.biosci.gatech.edu/ga/result/{user_id}

                        Best,
                        Team 2, BIOL 7210 Computational Genomics 2021
                        Georgia Institute of Technology"""})

def main():
    # parse input parameters to capture the user specifics
    parser = argparse.ArgumentParser(description = "Hola")
    # email id of user
    parser.add_argument("--user_mail", required = True)
    # the uuid specific to results
    parser.add_argument("--user_uuid", required = True)
    args = parser.parse_args()
    
    send_simple_message(args.user_mail, args.user_uuid)

if __name__ == "__main__":
    main()