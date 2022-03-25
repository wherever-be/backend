wsgi_app = "server:app"
bind = ["0.0.0.0:443"]
keyfile = "/etc/letsencrypt/live/wherever.be/privkey.pem"
certfile = "/etc/letsencrypt/live/wherever.be/fullchain.pem"
accesslog = "./log.txt"
