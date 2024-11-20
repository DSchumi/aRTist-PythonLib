# Copyright 2023 Simon Wittl (Deggendorf Institute of Technology)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import socket
import base64
import pathlib
from PIL import Image


class Junction:
    """Remote control of aRTist simulator (this is a test)"""

    def __init__(self, host="localhost", port=3658, bufferSize=1024, timeout=10):
        self.host = host
        self.port = port
        self.bufferSize = bufferSize
        self.timeout = timeout
        self.error = 0
        self.progress = 0
        self.answer = {}

        self.connect()

    def connect(self):
        try:
            self.S = socket.socket()  # Create socket (for TCP)
            self.S.connect((self.host, self.port))  # Connect to aRTist
            self.S.settimeout(self.timeout)
            self.S.setblocking(True)
            self.listen(0)
        except ConnectionRefusedError:
            print(
                "The Connection to aRTist was refused. Is aRTist running and the remote connection enabled?"
            )
        except Exception as e:
            raise e
        return self

    def send(self, command, msgType="RESULT"):
        c = command + "\n"
        self.S.send(c.encode())
        return self.listen(msgType=msgType)

    def listen(self, command_no=1, msgType="RESULT"):
        answer = ""
        stop = False
        if command_no == 0:
            self.S.settimeout(0.2)
        while not stop:  # and ("SUCCESS" not in total) and ("ERROR" not in total):     # Solange server antwortet und nicht "SUCCESS" enthält
            try:
                msg = self.S.recv(self.bufferSize).decode()
            except BaseException as e:
                err = e.args[0]
                if err == "timed out":
                    # print("Timeout\n")
                    answer += "RESULT Timeout\n"
                    # print(answer)
                    stop = True
                    continue
            else:
                if "SUCCESS" in msg:
                    answer += msg
                    stop = True
                    continue
                elif "ERROR" in msg:
                    answer += msg
                    stop = True
                    # global error
                    self.error = self.error + 1
                    continue
                elif "PROGRESS" in msg:
                    try:
                        self.progress = float(msg.strip("PROGRESS "))
                    except ValueError:
                        self.progress = 0
                    continue
                else:
                    if command_no == 0:
                        print(msg)
                    answer += msg
        self.S.settimeout(self.timeout)
        self.answer.update(
            {
                "SUCCESS": self.pick(answer, "SUCCESS"),
                "RESULT": self.pick(answer, "RESULT"),
                "SDTOUT": self.pick(answer, "STDOUT"),
                "BASE64": self.pick(answer, "BASE64"),
                "IMAGE": self.pick(answer, "IMAGE"),
                "FILE": self.pick(answer, "FILE"),
            }
        )
        if msgType != "*":
            answer = self.pick(answer, msgType)
        return answer

    def pick(self, answer, res="RESULT"):
        picked = ""
        for a in answer.split("\n"):
            if a.find(res) == 0:
                picked += a[1 + len(res) :].strip("\r") + "\n"
        if len(picked) == 0:
            return res + " not found."
        return picked

    def get_answer(self, key):
        return self.answer[key]

    def save_image(self, imageName: str):
        imageData = self.answer["BASE64"]
        decodedData = base64.b64decode((imageData))
        imageHeader = self.answer["IMAGE"].split()
        im = np.frombuffer(decodedData, np.double).reshape(
            (int(imageHeader[1]), int(imageHeader[2]))
        )
        Image.fromarray(im).save(imageName)

    def receive_file(self, fileName):
        fileData = self.answer["BASE64"]
        decodedFile = base64.b64decode((fileData))
        artistFile = open(fileName, "wb")
        artistFile.write(decodedFile)
        artistFile.close()

    def send_file(self, fileName):
        outFile = open(fileName, "br")
        fileBytes = outFile.read()
        encBytes = base64.b64encode((fileBytes))
        encString = str(encBytes)
        encString = encString.lstrip("b'").rstrip("'")
        fileExtension = pathlib.Path(fileName).suffix
        com = "::RemoteControl::ReceiveFile " + encString + " " + fileExtension
        recAnswer = self.send(com, "RESULT")
        return recAnswer

    def get_image(self) -> np.ndarray:
        imageData = self.answer["BASE64"]
        decodedData = base64.b64decode((imageData))
        imageHeader = self.answer["IMAGE"].split()
        dtype = np.double
        return np.frombuffer(decodedData, dtype).reshape(
            (int(imageHeader[1]), int(imageHeader[2]))
        )


_rc = Junction()
