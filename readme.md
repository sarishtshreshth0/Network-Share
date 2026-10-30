<h1 align="center"> Network Share</h1>

<p align="center">
  A simple Python client-server project for sharing data over a network.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="License">
</p>

---

## ✨ Features

- 🖥️ One server handling multiple clients
- 🔌 Socket-based communication
- 📁 Easy to run and extend
- *(add your own features here)*

##  Project Structure

```
network-share/
├── server.py     # Starts the server
├── client.py     # First client
├── client2.py    # Second client
└── README.md
```

## Getting Started

### Requirements

- Python 3.8 or newer

### Installation

```bash
git clone https://github.com/your-username/network-share.git
cd network-share
```

### Usage

> ⚠️ **Order matters:** always start the server first.

**1. Start the server**

```bash
python server.py
```

**2. In a new terminal, start the first client**

```bash
python client.py
```

**3. In another terminal, start the second client**

```bash
python client2.py
```



## 🛠️ Troubleshooting

- **Connection refused?** Make sure `server.py` is running first.
- **Port already in use?** Change the `PORT` value in all three files.



