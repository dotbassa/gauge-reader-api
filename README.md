# 📊 Gauge Reader API

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![MQTT](https://img.shields.io/badge/Protocol-MQTT-orange.svg)](https://mqtt.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Note:** Image processing algorithms are proprietary and not included in this repository due to NDA requirements. The implementation demonstrates architectural design, API development, and IoT integration capabilities.

## Overview

A production-ready FastAPI microservice that integrates with X1 Sensing IoT cameras via MQTT protocol to capture and process gauge readings in real-time. The system features a RESTful API architecture with automated image acquisition, processing pipeline integration, and data exposure through versioned endpoints.

### Key Technical Highlights

- **IoT Integration:** Real-time MQTT communication with industrial IoT cameras
- **RESTful API Design:** Clean, versioned API architecture following industry best practices
- **Async Processing:** Asynchronous event-driven architecture for optimal performance
- **Modular Architecture:** Service-oriented design with clear separation of concerns
- **Production Ready:** Includes configuration management, error handling, and API documentation

## Table of Contents

- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Camera Setup](#camera-setup)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Skills Demonstrated](#skills-demonstrated)
- [License](#license)

## Technology Stack

- **Backend Framework:** FastAPI (async Python web framework)
- **Communication Protocol:** MQTT (Message Queuing Telemetry Transport)
- **IoT Hardware:** X1 Sensing Camera (Milesight)
- **MQTT Broker:** Mosquitto
- **Data Validation:** Pydantic schemas
- **API Documentation:** OpenAPI/Swagger
- **Deployment:** Uvicorn ASGI server

## Architecture

The application follows a clean, modular architecture pattern:

```
┌─────────────────┐         MQTT          ┌──────────────────┐
│  X1 Sensing     │ ───────────────────►  │  MQTT Broker     │
│  Camera         │    (Topic: Snapshot)  │  (Mosquitto)     │
└─────────────────┘                       └──────────────────┘
                                                   │
                                                   ▼
                                          ┌──────────────────┐
                                          │  MQTT Service    │
                                          │  (Subscriber)    │
                                          └──────────────────┘
                                                   │
                                                   ▼
                                          ┌──────────────────┐
                                          │  Processing      │
                                          │  Service*        │
                                          └──────────────────┘
                                                   │
                                                   ▼
                ┌─────────────────────────────────────────────┐
                │          FastAPI Application                │
                │  ┌────────────┐  ┌──────────────┐          │
                │  │  Router    │  │  Endpoints   │          │
                │  │  (v1 API)  │  │  (Handlers)  │          │
                │  └────────────┘  └──────────────┘          │
                │  ┌────────────┐  ┌──────────────┐          │
                │  │  Schemas   │  │  Config      │          │
                │  │  (Pydantic)│  │  Management  │          │
                │  └────────────┘  └──────────────┘          │
                └─────────────────────────────────────────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │  REST API        │
                          │  Consumers       │
                          └──────────────────┘
```

_\*Image processing algorithms are proprietary and protected under NDA_

## Requirements

- **Python:** 3.9 or higher
- **MQTT Broker:** Mosquitto or compatible MQTT broker
- **Hardware:** X1 Sensing Camera (Milesight SC541)
- **OS:** Linux (recommended) or Windows with WSL

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd gauge-reader-api
```

### 2. Install MQTT Broker (Mosquitto)

```bash
sudo apt install mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

### 3. Configure Mosquitto

```bash
sudo nano /etc/mosquitto/mosquitto.conf
```

Add these lines to the configuration file:

```
listener 1883 0.0.0.0
allow_anonymous true
```

Restart Mosquitto to apply changes:

```bash
sudo systemctl restart mosquitto
```

### 4. Set Up Python Environment

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file in the project root (see [Environment Variables](#environment-variables) section).

### 7. Run the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

## Environment Variables

Create a `.env` file in the project root with the following configuration:

```env
# MQTT Configuration
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883
MQTT_USERNAME=admin
MQTT_PASSWORD=admin
MQTT_TOPIC=X1SensingCamera/Snapshot
MQTT_CLIENT_ID=gauge-api-client

# API Configuration
API_TITLE=Gauge Reader API
API_VERSION=1.0.0
API_PREFIX=/api

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
```

Refer to `.env.example` for additional configuration options.

## Camera Setup

### Initial Setup

1. Power on the X1 Sensing Camera via battery or USB Type-C
2. Press the capture button to wake up the device
3. Verify the LED light is on
4. Connect to the camera's access point from a computer or smartphone:
   - SSID: `SC541_XXXXXX` (where XXXXXX is unique to your camera)

### Web GUI Configuration

1. Open a web browser and navigate to `192.168.1.1`
2. Access the web interface with default credentials
3. Configure the camera for WLAN connection:
   - Connect to the same WiFi network as your API server

### Data Report Configuration

1. In the camera's web interface, navigate to **"Device Maintenance"**
2. **Important:** Unselect "Development Platform Takeover" to enable the Data Report section
3. Navigate to the **Data Report** section and configure:

   | Parameter | Value                                    |
   | --------- | ---------------------------------------- |
   | Platform  | Other MQTT Platform                      |
   | Host      | [Your API server's IP address]           |
   | MQTT Port | 1883                                     |
   | Topic     | X1SensingCamera/Snapshot                 |
   | Client ID | gauge-camera (unique from API client ID) |
   | QoS       | QoS 1                                    |
   | Username  | admin (or as configured in your `.env`)  |
   | Password  | admin (or as configured in your `.env`)  |

4. Click **"Save"** to apply the configuration

### Capture Settings

1. Navigate to **"Capture Settings"** section
2. Enable "Scheduled Capture"
3. Set "Capture Mode" to "Interval Capture"
4. Configure "Capture Interval" as needed (e.g., 1 minute)
5. Scroll to the bottom and click "Sleep Mode" to apply settings

## API Endpoints

### Overview

| Endpoint                      | Method | Description                                 |
| ----------------------------- | ------ | ------------------------------------------- |
| `/api/`                       | GET    | API health check and MQTT connection status |
| `/api/docs`                   | GET    | Interactive Swagger UI documentation        |
| `/api/v1/gauge-reader/latest` | GET    | Retrieve the most recent gauge reading      |

### Root Endpoint

**GET** `/api/`

Returns basic API information and MQTT connection status.

**Response Example:**

```json
{
  "message": "Gauge Reader API",
  "version": "1.0.0",
  "mqtt_connected": true
}
```

### Interactive Documentation

**GET** `/api/docs`

Access the auto-generated Swagger UI for interactive API testing and documentation.

### Gauge Reader Endpoints

**GET** `/api/v1/gauge-reader/latest`

Retrieves the most recent gauge reading processed from the camera.

**Response Example:**

```json
{
  "timestamp": "2026-02-04T10:30:00Z",
  "value": 42.5,
  "unit": "PSI",
  "camera_id": "SC541_XXXXXX"
}
```

## Development

### Project Structure

The codebase follows a modular, service-oriented architecture:

```
gauge-reader-api/
├── app/
│   ├── __init__.py
│   ├── main.py                     # Application entry point & lifecycle management
│   ├── api/                        # API layer
│   │   ├── __init__.py
│   │   └── v1/                     # API version 1
│   │       ├── __init__.py
│   │       ├── api.py              # Route aggregation
│   │       └── endpoints/          # Endpoint controllers
│   │           ├── __init__.py
│   │           └── gauge_reader.py # Gauge reading endpoints
│   ├── core/                       # Core application components
│   │   ├── __init__.py
│   │   └── config.py               # Settings & environment configuration
│   ├── schemas/                    # Data models & validation
│   │   ├── __init__.py
│   │   └── gauge_reader.py         # Gauge data schemas (Pydantic)
│   └── services/                   # Business logic layer
│       ├── __init__.py
│       ├── gauge_processing.py     # Image processing service*
│       ├── mqtt_manager.py         # MQTT interface abstraction
│       └── mqtt_service.py         # MQTT client implementation
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

_\*Note: Proprietary processing algorithms are not included in this repository._

### Design Patterns & Best Practices

- **Dependency Injection:** Services are loosely coupled and easily testable
- **Repository Pattern:** Data access abstraction through service layer
- **API Versioning:** Routes organized by version for backward compatibility
- **Schema Validation:** Pydantic models ensure type safety and data validation
- **Configuration Management:** Environment-based settings using `.env` files
- **Async/Await:** Non-blocking I/O for optimal performance

## Skills Demonstrated

This project showcases proficiency in:

- ✅ **Backend Development:** FastAPI, async Python, RESTful API design
- ✅ **IoT Integration:** MQTT protocol, industrial IoT camera integration
- ✅ **System Architecture:** Microservices, service-oriented design, clean architecture
- ✅ **API Design:** Versioning, documentation, schema validation
- ✅ **DevOps:** Configuration management, environment setup, deployment
- ✅ **Protocol Implementation:** MQTT pub/sub patterns, QoS handling
- ✅ **Documentation:** Comprehensive technical documentation and API specs

## License

This project is licensed under the MIT License.

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Paho MQTT Python Client](https://pypi.org/project/paho-mqtt/)
- [X1 Sensing Camera User Guide](https://resource.milesight.com/milesight/iot/document/sc541-user-guide-en.pdf)
- [MQTT Protocol Specification](https://mqtt.org/)

---

**Developed by Daniel Bassano** | [GitHub](https://github.com/dotbassa) | [LinkedIn](www.linkedin.com/in/dotbassa)
