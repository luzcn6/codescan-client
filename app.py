from time import sleep

import requests
import os
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="{%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)


class Client:
    def __init__(self):
        self.base_url = os.getenv("CODESCAN_URL")
        self.token = os.getenv("TOKEN")
        self.headers = {
            "Authorization": "Bearer %s" % self.token,
        }

    def run(self):
        with open("release_ids.txt", "r") as file:
            line = file.readline()
            while line:
                self._send_request(line.replace('"', "").strip())
                line = file.readline()

                # to avoid the server side rate limit
                sleep(1)

    def _send_request(self, release_id):
        print(os.path.join(self.base_url, release_id))
        response = requests.request(
            "POST",
            url=os.path.join(self.base_url, release_id),
            headers=self.headers,
            data={},
        )
        if response.status_code != 200:
            logging.error("status=failed %s" % response.text)
        else:
            logging.info("status=success %s" % response.text)


def main():
    client = Client()
    client.run()


if __name__ == "__main__":
    main()
