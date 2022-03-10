wsgi_app = "server:app"
bind = ["0.0.0.0:443"]
keyfile = "/etc/letsencrypt/live/api.wherever.be/privkey.pem"
certfile = "/etc/letsencrypt/live/api.wherever.be/fullchain.pem"
accesslog = "./log.txt"
