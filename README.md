# Backend for [wherever.be](https://wherever.be)

The code here exposes a flexible flight search API to [the frontend](https://github.com/wherever-be/frontend/). It uses the internal APIs of European airlines to do the work - so don't use it commercially.

## How to run it

1. Clone this repository.
2. Run `setup-vps.sh` - you probably want to do this manually and not on your own computer, because it configures some things globally :)
3. Run `sudo .venv/bin/gunicorn`. Sudo is needed because we access SSL certificates under `/etc`.
