# 🚀 Backend Wizards — Stage 1  
**Data Persistence & API Design Assessment**

## 📌 Overview

This project is a FastAPI backend service that:

- Accepts a name input
- Fetches data from three external APIs
- Applies classification logic
- Stores results in a database
- Exposes RESTful endpoints to manage profiles

---

## ⚙️ Tech Stack

- FastAPI
- SQLModel
- SQLite
- httpx
- Pydantic
- UUID v7

---

## 🌐 External APIs

- https://api.genderize.io?name={name}
- https://api.agify.io?name={name}
- https://api.nationalize.io?name={name}

---

## 🧠 Business Logic

### Age Classification

| Age Range | Group |
|----------|------|
| 0–12 | child |
| 13–19 | teenager |
| 20–59 | adult |
| 60+ | senior |

---

### Nationality Selection

- Select the country with the highest probability from Nationalize API

---

## 📡 API Endpoints

---

### 1. Create Profile  
**POST `/api/profiles`**

#### Request
```json
{
  "name": "ella"
}
```

### Success Response
```json
{
  "status": "success",
  "data": {
    "id": "019d9610-57e5-74af-8b7c-f7f0eb87388e",
    "name": "ella",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 97517,
    "age": 53,
    "age_group": "adult",
    "country_id": "CM",
    "country_probability": 0.09677289106552395,
    "created_at": "2026-04-16T11:32:26.725514"
  }
}
```

### Duplicate Case
```json
{
  "status": "success",
  "message": "Profile already exists",
  "data": { ...existing profile... }
}
```



### Get Single Profile

**GET `/api/profiles/{id}`**

### Response (200)
```json
{
  "status": "success",
  "data": { ...profile... }
}
```


### 3. Get All Profiles

**GET `/api/profiles`**

#### Query Parameters (optional)
*gender
*country_id
*age_group

👉 Case-insensitive filtering

### Example
```bash
 curl /api/profiles?gender=male&country_id=NG
```

### Response (200)
```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": "id-1",
      "name": "emmanuel",
      "gender": "male",
      "age": 25,
      "age_group": "adult",
      "country_id": "NG"
    }
  ]
}
```

### 4. Delete Profile

**DELETE `/api/profiles/{id}`**

### Response
204 No Content



## Error Responses

### 400 Bad Request

* Missing or empty `name` 

```json
{ "status": "error", "message": "Missing or empty name parameter" }
```

---

### 422 Unprocessable Entity

* `name` is not a string

```json
{ "status": "error", "message": "Invalid type" }
```

---

### 500 / 502 Server Errors

* Upstream API failure or internal error

```json
{ "status": "502", "message": "${externalApi} returned an invalid response" }
```

---

## Genderize Edge Cases

If the API returns:

* `gender: null`
* OR `count: 0`

Response:

```json
{ "status": "error", "message": "${externalApi} returned an invalid response" }
```

---

## CORS

The API allows all origins:

```end
allow_origins = ["*"]
```

## Installation
* create and activate venv
* ```bash
  pip install -r requirements.txt
  ```

---

## Run the Server

```bash
fastapi dev
```


