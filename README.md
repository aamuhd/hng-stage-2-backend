# 🚀 Backend Wizards — Stage 2  
**Intelligence Query Engine Assesment**

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



## Natural Language Query Parsing

The /api/profiles/search endpoint supports plain English queries and converts them into structured filters using a rule-based parser (no AI/LLM involved).

### Endpoint:
**GET `/api/profiles/search?q=your query here`**

## Supported Keywords and Mappings

### The parser recognizes the following keywords and maps them to filters:Keyword / Phrase


| Keyword / Phrase | Mapped Filter(s) | Example Query |
|------------------|------------------|---------------|
| male, males | gender=male | "young males" |
| female, females | gender=female | "females above 30" |
| male and female, males and females | No gender filter (includes both) | "male and female teenagers" |
| teenager, teenagers, teens, teen | age_group=teenager | "teenagers from kenya" |
| adult, adults | age_group=adult | "adult males from nigeria" |
| young | min_age=16, max_age=24 | "young males" |
| above X, over X, older than X | min_age=X | "females above 30", "teenagers above 17" |
| below X, under X, younger than X | max_age=X | "people under 25" |
| Country names | country_id=XY | "people from nigeria", "from kenya" |


### Supported Countries (currently):nigeria → NG
 - kenya → KE
 - angola → AO
 - south africa → ZA
 - central african republic  → CF
 - tanzania → TZ
 - uganda → UG


## How the Parsing Logic Works

1. Lowercase normalization: The entire query is converted to lowercase.
2. Gender Logic:
 - If both "male" and "female" appear → gender filter is ignored (to support "male and female").
 - If only one appears → apply that gender filter.

3. Age Group:
 - "teenager/teens" sets age_group=teenager
 - "adult" sets age_group=adult
 - "young" sets age range 16–24

4. Age Range:
 - Phrases like "above 17", "over 25", "older than 30" set min_age
 - Phrases like "below 40", "under 25" set max_age

5. Country:
 - Simple string matching against a predefined country map.

6. Combination:
 - All detected filters are combined using AND logic (must match all conditions).

#### Example Mappings:
 - "young males" → gender=male, min_age=16, max_age=24
 - "females above 30" → gender=female, min_age=30
 - "male and female teenagers above 17" → age_group=teenager, min_age=17
 - "adult males from kenya" → gender=male, age_group=adult, country_id=KE
 - "people from angola" → country_id=AO


## Limitations & Edge Cases Not Handled

 - No complex boolean logic: Does not support "OR" conditions (e.g. "males or females above 30" will not work properly).
 - No multi-word age groups beyond "young", "teenager", and "adult".
 - No numeric ranges with "between": "between 20 and 30" is not supported yet.
 - Limited country support: Only a few countries are mapped. Unknown countries are ignored.
 - No support for nationality adjectives: "Nigerian males" or "Kenyan females" are not recognized (only "from nigeria", "from kenya").
 - No handling of typos or spelling mistakes.
 - No support for relative ages like "in their 20s", "elderly", "children".
 - Order of words matters slightly: Some phrases may fail if worded unusually (e.g. "above 17 teenagers male").
 - No support for multiple countries in one query.
 - Case sensitivity: Everything is lowercased, so capitalization is ignored, but punctuation may affect matching in rare cases.

#### If the parser cannot extract any meaningful filters from the query, it returns:
```json
{
  "status": "error",
  "message": "Unable to interpret query"
}```


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


