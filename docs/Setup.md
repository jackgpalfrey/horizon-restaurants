# Setup Git 
```bash
git config --global user.name "Your Name"
git config --global user.email "Your Email"
git config --global core.editor "vscode --wait"
```

# Clone down the repo
```bash
git clone https://github.com/jackgpalfrey/horizon-restaurants.git
git pull 
```

# Create venv
```bash
py -m venv .venv # Might take a while
WINDOWS: .\.venv\Scripts\activate.bat
LINUX: source .venv/bin/activate
py -m pip install -r requirements.txt
```

# Setup Docker
Hopefully you should just be able to install [Docker Desktop](https://www.docker.com/products/docker-desktop/). 
