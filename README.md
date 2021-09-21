# File Daemon

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```
Make a request to localhost:5000


```bash
curl --location --request GET 'localhost:5000?hash={hash}'
curl --location --request POST 'localhost:5000' --form 'file=@"{file_path}'
curl --location --request DELETE 'localhost:5000?hash={hash}'
```
