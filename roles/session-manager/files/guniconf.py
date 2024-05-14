import multiprocessing

#
# Gunicorn config file
#
wsgi_app = "main:app"

# Server Mechanics
# ========================================
# current directory
chdir = "/root/session-manager"

# daemon mode
daemon = False

# Server Socket
# ========================================
bind = "0.0.0.0:80"

# Worker Processes
# ========================================
num_cores = multiprocessing.cpu_count()
workers = num_cores

# Server Logging
# ========================================
accesslog = "-"
errorlog = "-"
