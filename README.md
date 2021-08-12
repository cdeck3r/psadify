# PSADify

PSADify is a tool for converting Port Scan Attack Detector (PSAD) output into HTML.

#### Information

Read about the PSAD tool here: [https://disloops.com/psad-on-raspberry-pi](https://disloops.com/psad-on-raspberry-pi)

This script can be downloaded here: [https://github.com/disloops/psadify](https://github.com/disloops/psadify)

See the live attack data here: [https://psad.disloops.com](https://psad.disloops.com)

#### Disclaimer

THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#### Usage

```
psadify.py [-h] [-o OUTPUT]

-h, --help                      Show this message and exit
-o, --output OUTPUT             The file that is generated with the HTML content
```

#### Run Tests

Use the dockerized dev system below. From bash console within the container

```bash
# cd /PSADify
# python3 -m pytest
```

#### Dev system

**Setup:** Start in project's root dir and create a `.env` file with the content shown below.
```
# .env file

# In the container, this is the directory where the code is found
# Example:
APP_ROOT=/PSADify

# The HOST directory containing directories to be mounted into containers
# This is the directory path where you have cloned this repo.
# Example:
VOL_DIR=/dev/psadify
```

**Create** docker image. Please see [Dockerfiles/Dockerfile.psadify](Dockerfiles/Dockerfile.psadify) for details.
```bash
docker-compose build psadify
```

**Spin up** the container and get a shell from the container
```bash
docker-compose up -d psadify
docker exec -it psadify /bin/bash
```
