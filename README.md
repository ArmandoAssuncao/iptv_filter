# IPTV Filter

Filters m3u file based on pre-defined words.

## Requirements

#### Packages

Install follow packages:
```
pip3 install flask
pip3 install gunicorn
pip3 install requests
```

#### ENVs
Set the envs:
```
IPTV_M3U_URL="https://iptvsite.example/list"
BLACKLIST_GROUPS="GROUP 1;GROUP2;GROUP 3"
API_KEY="YOUR_API_KEY"
```

Or use package `dotenv-python`. 
- Install: `pip3 install dotenv-python` 
- Create file `.env` and put the above envs. 



## Running

Running with `foreman`, first install foreman: `gem install foreman` and execute:
```
foreman start
```

Or running with native python (**Not Recommended**):
```
python3 server.py
```

## Get Started

Access endpoint to get list filtered:

`http://localhost:5000/list?api_key=YOUR_API_KEY`
