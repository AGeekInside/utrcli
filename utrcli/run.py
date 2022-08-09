import json

import click
from environs import Env
import requests

env = Env()

UTR_URL = "https://app.universaltennis.com/api"
UTR_EMAIL = env.str("UTR_EMAIL")
UTR_PASSWORD = env.str("UTR_PASSWORD")


class UTRServer():

    def __init__(self):
        self.session = requests.Session()
        self.email = UTR_EMAIL
        self.password = UTR_PASSWORD
        self.utr_url = UTR_URL
        self.login()

    def login(self):

        uri = "/v1/auth/login"
        url = f"{self.utr_url}/{uri}"

        headers = {"Content-Type": "application/json"}
        body = {"email": self.email, "password": self.password}
        response = self.session.post(
            url,
            headers=headers,
            json=body,
        )
        if response.ok is False:
            raise Exception(f"Error logging in: {response.text}")

    def get_results(self, userid: str):
        uri = f"v1/player/{userid}/results"

        results = self.get_response(uri)
        
        return results

    def get_events(self, userid: str):
        uri = f"v1/player/{userid}/events"

        events = self.get_response(uri)

        return events

    def get_profile(self, userid: str):
        uri = f"/v1/player/{userid}"

        player_profile = self.get_response(uri)

        return player_profile

    def get_name(self, userid: str):
        player_profile = self.get_profile(userid)

        player_name = f"{player_profile['firstName']} {player_profile['lastName']}"

        return player_name

    def get_response(self, uri: str):
        url = f"{self.utr_url}/{uri}"

        response = self.session.get(url)

        if response.ok is False:
            raise Exception(f"Error retrieving results for {uri}")

        return response.json()


@click.group()
def cli():
    pass

@cli.command()
@click.argument('userid')
def events(userid: str):
    utr_server = UTRServer()

    player_name = utr_server.get_name(userid)

    print(player_name)

    events = utr_server.get_events(userid)

    print(json.dumps(events, sort_keys=True, indent=4))


@cli.command()
@click.argument('userid')
def results(userid: str):

    utr_server = UTRServer()
    results = utr_server.get_results(userid)

    print(json.dumps(results, sort_keys=True, indent=4))