# Apache Doris Cluster Project

This repository contains the configuration and architecture documentation for an **Apache Doris** cluster used for experimentation and demonstration purposes.

## Cluster Architecture

The cluster consists of **1 Frontend (FE)** and **2 Backends (BE)**:
```
                +-------------------+
                |  Frontend (FE)    |
                |  VM4 / 10.0.10.7  |
                |  Port: 8030, 9030 |
                +-------------------+
                         |
            +------------+------------+
            |                         |
   +-------------------+     +-------------------+
   |  Backend (BE1)    |     |  Backend (BE2)    |
   |  VM4 / 10.0.10.7  |     |  VM5 / 10.0.10.8  |
   |  Port: 9050, 9060 |     |  Port: 9050, 9060 |
   +-------------------+     +-------------------+
```

### Key Features

- **High Availability**: Data is replicated across both Backend nodes
- **Distributed Processing**: Parallel query execution across multiple BE nodes
- **Centralized Coordination**: Frontend manages SQL queries and Backend operations
- **Network**: All nodes communicate over the `10.0.10.0/24` subnet

### Port Configuration

| Component | Port | Purpose |
|-----------|------|---------|
| **Frontend (FE)** | 8030 | Web UI and HTTP API |
| | 9030 | MySQL protocol (query port) |
| | 9020 | RPC port |
| | 9010 | Edit log port |
| **Backend (BE)** | 9050 | Heartbeat service port |
| | 9060 | Thrift server port |
| | 8040 | Web UI |
| | 8060 | BRPC port |

## Repository Structure

The repository is organized to clearly separate configuration and documentation for each component:
```
doris-cluster/
├── Doris-Frontend/
│   ├── Doris-FE-config.md          # Frontend configuration guide
│   └── images/                     # Screenshots
│
├── Doris-Backend/
│   └── Doris-BE-config.md          # Backend configuration guide  
│
├── Link-BE-with-FE/
│   └── link-config.md              # Instructions to link BE with FE
│
└── README.md                       # This file
```

### Directory Details

#### 1. **Doris-Frontend/**
Contains all documentation and configuration files related to the Frontend node.
- `Doris-FE-config.md`: Comprehensive installation and configuration guide for FE
- `images/`: Screenshots of the web interface 

#### 2. **Doris-Backend/**
Contains all documentation and configuration files related to the Backend nodes.
- `Doris-BE-config.md`: Detailed setup instructions for BE nodes (VM4 and VM5)

#### 3. **Link-BE-with-FE/**
Contains documentation for cluster integration.
- `link-config.md`: Step-by-step guide to register BE nodes with FE

