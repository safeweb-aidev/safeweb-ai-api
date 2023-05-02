# SafeWeb AI 

## General information

This section of documentation presents CI/CD aspects as well as basic API definitions. Extended API information can be found in below API section.

> **Note**
> Within this documentation you will see different `ver`, `worker_ver` and `time` in various example responses. This is due to the fact that the documentation has been completed gradually.

### Overall CI/CD aspects

All microservices are hosted under the same distributed gateway enabling multi-worker processing. Each microservice is defined by at least one property - i.e.`"SIGNATURE"`.
Most microservices such as quiz generators require identification via both `"SIGNATURE"` as well as `"LANGUAGE"`.
Failure to identify the microservice will yield an error. Main repo `push` operation will trigger autobuild of `docker.io/SafeWeb/ai:latest` repo.
Following automatic build a simple `http://<server>:5002/shutdown` command is required to restart and update the Docker container on the server.


On server a simple script is running the container with 
```
nodup ./run.sh`
```

The `run.sh` contains the following script:
```
#!/bin/bash

while true; do
  sudo docker run --pull=always -p 5002-5010:5002-5010 -v sw_vol:/safeweb_ai/output safeweb/ai
  sleep 5
done
```

As a result the data will be persistent from one session to another in the `sw_vol` usually found in `/var/lib/docker/volumes/sw_vol/_data`

A simple Azure or AWS Ubuntu 18+ VM is recommanded. See below the installation instructions.

### Development

#### Docker build

```
docker build -t safeweb/ai .
```

...or a dev local build

```
docker build -t localsw .
```

> **Note**
> Place make sure env is prepared. Currently the env contains a couple neural word embeddings bundled within the env layer.

#### Docker run

```
docker run --pull=always -p 5002-5010:5002-5010 -v sw_vol:/safeweb_ai/output safeweb/ai
```

or run locally

```
docker run -p 5002-5010:5002-5010 localsw
```

> **Note**
> Always include volume `-v` and port forwarding `-p`.

### Usage

The engine itself works as a microservice gateway with multiple servers running their parallel workers. The list of active servers can be queried by running a `POST` on `<address>:5002/list_servers` resulting in a response similar with this 
```
{
    "AVAIL_SERVERS": [
        "dummy_model_a",
        "basic_quiz_model"
    ]
}
```

#### Restart/update all servers within automated container

Run `POST` on `<address>:5002/shutdown` with the following JSON:

```
{
    "SIGNATURE" : "SAFEWEB_AI_KILL_SERVER"
}
```


#### Querying a microservice

Run a `POST` on `<address>:5002/run` with the following JSON:

```
{
    "SIGNATURE" : "basic_quiz_model",
    
    "QUIZ_CATEGORY" : "math-highschool",
    "LANGUAGE" : "ro"
}
```

While `SIGNATURE` is mandatory for any microservice the other fields are dependent of the particular endpoint.

In this case as well as in other quiz-like responses we will obtain something like:
```
{
    "call_id": 1,
    "quizzes" : [
        {
            "answer": "spațiul_încercărilor",
            "max_given_time": 7,
            "options": [
                "spațiul_încercărilor",
                "distribuție",
                "variabilă"
            ],
            "question": "Mulțimea tuturor rezultatelor posibile într-un experiment de probabilitate se numește _______."
        }
    ],
    "signature": "BasicQuizWorker:1",
    "ver": "0.2.2",
    "worker_ver": "1.0.8"
}
```

For more information please see API section below.

#### Azure VM install

To install Docker on an Azure VM with Ubuntu, follow these steps:

1. Update the packages list:
```
sudo apt-get update
```
2. Install prerequisite packages:
```
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
```

3. Add Docker's official GPG key:
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

4. Set up the Docker repository:
```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

5. Update the packages list again:
```
sudo apt-get update
```

6. Install Docker:
```
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

7. Verify the installation by checking the Docker version:
```
docker --version
```

8. Start the Docker service and enable it to start on boot:
```
sudo systemctl enable docker
sudo systemctl start docker
```

9. Create inbound rule with `*` as source and `5002-5010` as destination


## SafeWeb AI API information

In this section specific information about various microservices is provided.


### API definition for utility features

Most of the endpoints have the following utility features

#### Get system health status

Getting system status requires a simple API call `POST <address>:5002/run`:

```
{
    "SYSTEM_STATUS": {
        "info": "Memory Size is in GB. Total and avail mem may be reported inconsistently in containers.",
        "mem_avail": 22.88,
        "mem_gateway": 0.13,
        "mem_servers": {
            "basic_quiz_model": 0.56,
            "dummy_model_a": 0.14
        },
        "mem_sys": 1.14,
        "mem_total": 24.85,
        "mem_used": 0.83
    },
    "time": "2023-05-02 07:46:45",
    "ver": "2.3.2"
}
```

#### Reset warmup dataset (restoring from backups)

In order to replace container warmup dataset for a specific microservice that uses warmup data we have the following call:

```
POST <address>:5002/run


{
    "SIGNATURE" : "basic_quiz_model",    
    "RESET_WARMUP" : "https://www.dropbox.com/s/d19umzv3zcysqbn/basic_warmup_dataset.bin?dl=1"
}
```

In this case the provided URL consists in the default dataset for the `basic_quiz_model` microservices. Results should look similar to the following response:

```
{
    "RESET_WARMUP": {
        "INFO": "Quiz warmup reinitialized from download and reloaded!",
        "SUCCESS": true
    },
    "call_id": 26,
    "signature": "BasicQuizModelWorker:2",
    "time": "2023-05-01 08:13:50",
    "ver": "2.2.0",
    "warning": null,
    "worker_ver": "3.1.7"
}
```


#### Specific query check

Based on a data/question `IDX` we can ask for the specific quiz sample:


```
POST <address>:5002/run

{
    "SIGNATURE" : "basic_quiz_model",    
    "QUIZ_CATEGORY" : "math-highschool",
    "LANGUAGE" : "ro",
    "IDX" : 3281
}
```

In above example the `IDX` 3281 will probably fail for `basic_quiz_model` and a random romanian math-highschool quiz sample will be returned:
```
{
    "call_id": 4,
    "quizzes": [
        {
            "answer": "punct de intersecție",
            "max_given_time": 7,
            "options": [
                "punct de aderență",
                "punct de intersecție",
                "punct de vârf"
            ],
            "question": "Ce se numește punctul unde două raze distincte intersectează perimetrul unui cerc?"
        }
    ],
    "signature": "BasicQuizModelWorker:2",
    "ver": "1.5.1",
    "warning": null,
    "worker_ver": "3.1.6"
}
```
> **Note**
> More about this later when we will add a new observation to the engine warmup dataset

#### Modify a specific quiz

If we need to correct a answer or a pre-generated word we can use the `FEEDBACK` option:

```
POST <address>:5002/run

{
    "SIGNATURE" : "basic_quiz_model",    
    "QUIZ_CATEGORY" : "math-highschool",    
    "LANGUAGE" : "ro",
    "FEEDBACK" : true,
    "IDX" :  1260,
    "MODIFIED_QUESTION" : "O figura plana cu toate laturile egale și toate unghiurile de 60 de grade se numește _____",
    "MODIFIED_ANSWER": "hexagon"
}
```

Prior to this we have to know the `IDX` of the specific observation in question. The response will be:
```
{
    "FEEDBACK": {
        "idx": 1260,
        "info": "Data cache saved.",
        "mod_a": "hexagon",
        "mod_q": "O figura plana cu toate laturile egale și toate unghiurile de 60 de grade se numește _____",
        "orig_a": null,
        "orig_q": null
    },
    "call_id": 2,
    "signature": "BasicQuizModelWorker:3",
    "ver": "1.4.2",
    "warning": null,
    "worker_ver": "3.1.2"
}
```
 
We can also "search" for the observation based on the original question and answer as below:

```
POST <address>:5002/run

{
    "SIGNATURE" : "basic_quiz_model",    
    "QUIZ_CATEGORY" : "math-highschool",    
    "LANGUAGE" : "ro",
    "FEEDBACK" : true,

    "ORIGINAL_QUESTION" : "O figură plană care are toate laturile egale și toate unghiurile de 60 de grade se numește _____.",
    "ORIGINAL_ANSWER" : "hexagon regulat",

    "MODIFIED_QUESTION" : "O figura plana cu toate laturile egale și toate unghiurile de 60 de grade se numește _____",
    "MODIFIED_ANSWER": "hexagon"
}
```

In this scond case no `IDX` is used and the response will be:

```
{
    "FEEDBACK": {
        "idx": null,
        "info": "Data cache saved.",
        "mod_a": "hexagon",
        "mod_q": "O figura plana cu toate laturile egale și toate unghiurile de 60 de grade se numește _____",
        "orig_a": "hexagon regulat",
        "orig_q": "O figură plană care are toate laturile egale și toate unghiurile de 60 de grade se numește _____."
    },
    "call_id": 2,
    "signature": "BasicQuizModelWorker:2",
    "ver": "1.5.1",
    "warning": null,
    "worker_ver": "3.1.6"
}
```

#### New question addition

If we need to add more data to our live quiz "warmup" dataset we can do this using the following microservice call:

```
POST <address>:5002/run

{
    "SIGNATURE" : "basic_quiz_model",    
    "QUIZ_CATEGORY" : "math-highschool",    
    "LANGUAGE" : "ro",
    "ADD_QUESTION" : true,
    "QUESTION" : "Ce au in comun o frunza, un nautil si un fulg de zapada?",
    "ANSWER": "fractal"
}
```

giving a response similar to this:

```
{
    "ADD_QUESTION": {
        "IDX": 3281,
        "INFO": "Data added at IDX=3281. Data cache saved."
    },
    "call_id": 3,
    "signature": "BasicQuizModelWorker:0",
    "ver": "1.5.0",
    "warning": null,
    "worker_ver": "3.1.6"
}
```

At this point the engine will analyze the answer and will "come-up" with various "wrong" answers such as `'multidimensional', 'expresionist', 'impresionist', 'spaţiu-timp', 'uimitor', 'infinit', 'globular', 'imaginativ', 'neastâmpărat', 'univers', 'umanoid', 'fascinant', 'caleidoscop', 'expansiv', 'sferic', 'continuum', 'omuleț', 'genial', 'neobişnuit', 'inepuizabil'` thus running the previous query will now yield the specific 3281 `IDX`.

```
POST <address>:5002/run

{
    "SIGNATURE" : "basic_quiz_model",    
    "QUIZ_CATEGORY" : "math-highschool",
    "LANGUAGE" : "ro",
    "IDX" : 3281
}
```

... will now yield a response similar to this one below:

```
{
    "call_id": 7,
    "quizzes": [
        {
            "answer": "fractal",
            "max_given_time": 5,
            "options": [
                "fractal",
                "univers",
                "fascinant"
            ],
            "question": "Ce au in comun o frunza, un nautil si un fulg de zapada?"
        }
    ],
    "signature": "BasicQuizModelWorker:2",
    "ver": "1.5.1",
    "warning": null,
    "worker_ver": "3.1.6"
}
```

#### Get a full test in one shot

The "normal" interaction and consumption of the API should involve getting a full test not only a single quiz item.
```
POST <address>:5002/run

{
    "SIGNATURE" : "basic_quiz_model",    
    "QUIZ_CATEGORY" : "math-highschool",
    "LANGUAGE" : "ro",
    "N_SAMPLES" : 5
}
```

resulting in a response similar to the below one:

```
{
    "call_id": 2,
    "quizzes": [
        {
            "answer": "liniară",
            "max_given_time": 7,
            "options": [
                "trigonometrică",
                "liniară",
                "exponențială"
            ],
            "question": "O funcție care are o rată constantă de schimbare se numește funcție _______."
        },
        {
            "answer": "distanța",
            "max_given_time": 7,
            "options": [
                "raza",
                "distanța",
                "inclinarea"
            ],
            "question": "Ce se numește distanța dintre un punct și o linie?"
        },
        {
            "answer": "paralelă",
            "max_given_time": 7,
            "options": [
                "paralelă",
                "inocentă",
                "satisfăcătoare"
            ],
            "question": "O linie care se apropie astfel încât să nu se întâlnească niciodată este o linie ____. "
        },
        {
            "answer": "27",
            "max_given_time": 7,
            "options": [
                "45",
                "9",
                "27"
            ],
            "question": "Care este volumul unui cub cu latura de 3?"
        },
        {
            "answer": "intersecție",
            "max_given_time": 7,
            "options": [
                "intersecție",
                "extensie",
                "înșurubare"
            ],
            "question": "Cum se numește punctul  unde o secantă intersectează marginea unei figuri chiulangii?"
        }
    ],
    "signature": "BasicQuizModelWorker:3",
    "time": "2023-04-28 07:22:01",
    "ver": "1.5.3",
    "warning": null,
    "worker_ver": "3.1.6"
}
```

> **Note**
> The backend LLM model is trained to be as entertaining as possible while remaining strict to the subject as much as it can - i.e. "figuri chiulangii?" 


#### Query a particular server features

While the system can encapsulate multiple microservice servers most of the servers have the `GET_STATUS` option implemented. Using below query a status of the pre-generated available data can be requested:
```
POST <address>:5002/run

{
    "SIGNATURE" : "basic_quiz_model",    
    "GET_STATUS" : true
}
```
this will result in a breakdown report similar to below answer:
```
{
    "GET_STATUS": {
        "breakdown": {
            "biology-begin": {
                "en": 102,
                "ro": 116
            },
            "biology-highschool": {
                "en": 99,
                "ro": 101
            },
            "chemistry-begin": {
                "en": 130,
                "ro": 125
            },
            "chemistry-highschool": {
                "en": 101,
                "ro": 104
            },
            "geography": {
                "en": 12,
                "ro": 10
            },
            "geography-highschool": {
                "en": 106,
                "ro": 115
            },
            "math-begin": {
                "en": 456,
                "ro": 275
            },
            "math-highschool": {
                "en": 255,
                "ro": 136
            },
            "math-mid": {
                "en": 303,
                "ro": 110
            },
            "physics-begin": {
                "en": 230,
                "ro": 129
            },
            "physics-highschool": {
                "en": 8,
                "ro": 5
            },
            "physics-mid": {
                "en": 158,
                "ro": 95
            }
        },
        "categs": 12,
        "langs": 2,
        "total": 3281
    },
    "call_id": 1,
    "signature": "BasicQuizModelWorker:1",
    "time": "2023-04-28 06:41:26",
    "ver": "1.5.3",
    "warning": null,
    "worker_ver": "3.1.6"
}
```

### API definition for 'basic_quiz_model' endpoint
 
For the microservice server designated by the `SIGNATURE` with the value `basic_quiz_model`  we have the `math-begin`,`math-mid`,`math-highschool`,`physics-begin`,`physics-highschool`,`geography`,`chemistry-begin`,`biology-begin`,`biology-highschool`,`chemistry-highschool`,`geography-highschool`,`physics-mid` categories and the `ro` and `en` languages.
Requests are made using `POST` requests on the currenly - as of 2023-04-13 - active microservice gateway server as follows:
```
POST http://20.220.208.245:5002/run
```

Beside the above mentioned main server the same microservice gateway server provides other microservice servers - ie. as of 2023-04-13 exposing a neural word similarity endpoint with the temporary signature `dummy_model_a`.
```
{
    "SIGNATURE" : "dummy_model_a",
}
```

#### Microservice #1/24 - Basic_Quiz_Model : Math-Begin : Ro

For basic_quiz_model, language 'ro', domain 'math-begin', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "math-begin",
    "LANGUAGE": "ro"
}
```

And this is a example response for above request of microservice #1:
```
{
    "call_id": 124,
    "quizzes": [
        {
            "answer": "/",
            "max_given_time": 7,
            "options": [
                "/",
                "=",
                "+"
            ],
            "question": "Ce semn matematic se folose\u0219te pentru a indica o \u00eemp\u0103r\u021bire?"
        }
    ],
    "signature": "BasicQuizModelWorker:1",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #2/24 - Basic_Quiz_Model : Math-Mid : Ro

For basic_quiz_model, language 'ro', domain 'math-mid', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "math-mid",
    "LANGUAGE": "ro"
}
```

And this is a example response for above request of microservice #2:
```
{
    "call_id": 125,
    "quizzes": [
        {
            "answer": "dreptunghi",
            "max_given_time": 7,
            "options": [
                "dreptunghi",
                "triunghi echilateral",
                "patrat"
            ],
            "question": "Care este numele obiectului geometric care are patru laturi \u0219i unghiuri toate drepte, dar laturile sale nu sunt toate egale?"
        }
    ],
    "signature": "BasicQuizModelWorker:3",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #3/24 - Basic_Quiz_Model : Math-Highschool : Ro

For basic_quiz_model, language 'ro', domain 'math-highschool', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "math-highschool",
    "LANGUAGE": "ro"
}
```

And this is a example response for above request of microservice #3:
```
{
    "call_id": 126,
    "quizzes": [
        {
            "answer": "cilindru",
            "max_given_time": 7,
            "options": [
                "turbulent",
                "propriu",
                "cilindru"
            ],
            "question": "O figur\u0103 tridimensional\u0103 care are o baz\u0103 circular\u0103 \u0219i o suprafa\u021b\u0103 cilindric\u0103 se nume\u0219te ____. "
        }
    ],
    "signature": "BasicQuizModelWorker:3",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #4/24 - Basic_Quiz_Model : Physics-Begin : Ro

For basic_quiz_model, language 'ro', domain 'physics-begin', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "physics-begin",
    "LANGUAGE": "ro"
}
```

And this is a example response for above request of microservice #4:
```
{
    "call_id": 127,
    "quizzes": [
        {
            "answer": "longitudinal\u0103",
            "max_given_time": 7,
            "options": [
                "electromagnetic\u0103",
                "transversal\u0103",
                "longitudinal\u0103"
            ],
            "question": "O und\u0103 care se propag\u0103 \u00een aceea\u0219i direc\u021bie cu deplasarea particulelor din mediu se nume\u0219te und\u0103 _______."
        }
    ],
    "signature": "BasicQuizModelWorker:0",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #5/24 - Basic_Quiz_Model : Physics-Highschool : Ro

For basic_quiz_model, language 'ro', domain 'physics-highschool', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "physics-highschool",
    "LANGUAGE": "ro"
}
```

And this is a example response for above request of microservice #5:
```
{
    "call_id": 128,
    "quizzes": [
        {
            "answer": "Schimbarea frecven\u021bei percepute datorit\u0103 mi\u0219c\u0103rii relative \u00eentre surs\u0103 \u0219i observator",
            "max_given_time": 7,
            "options": [
                "Schimbarea frecven\u021bei percepute datorit\u0103 mi\u0219c\u0103rii relative \u00eentre surs\u0103 \u0219i observator",
                "Schimbarea amplitudinii sunetului",
                "Schimbarea vitezei de propagare a sunetului"
            ],
            "question": "Care este efectul Doppler \u00een cazul undelor sonore?"
        }
    ],
    "signature": "BasicQuizModelWorker:0",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #6/24 - Basic_Quiz_Model : Geography : Ro

For basic_quiz_model, language 'ro', domain 'geography', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "geography",
    "LANGUAGE": "ro"
}
```

And this is a example response for above request of microservice #6:
```
{
    "call_id": 129,
    "quizzes": [
        {
            "answer": "Pacific",
            "max_given_time": 7,
            "options": [
                "Arctic",
                "Pacific",
                "Southern"
            ],
            "question": "Cel mai mare ocean de pe P\u0103m\u00e2nt este oceanul _______."
        }
    ],
    "signature": "BasicQuizModelWorker:0",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #7/24 - Basic_Quiz_Model : Chemistry-Begin : Ro

For basic_quiz_model, language 'ro', domain 'chemistry-begin', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "chemistry-begin",
    "LANGUAGE": "ro"
}
```

And this is a example response for above request of microservice #7:
```
{
    "call_id": 130,
    "quizzes": [
        {
            "answer": "este absorbit\u0103",
            "max_given_time": 7,
            "options": [
                "este pierdut\u0103",
                "este transformat\u0103",
                "este absorbit\u0103"
            ],
            "question": "Ce se \u00eent\u00e2mpl\u0103 cu energia \u00een timpul unei reac\u021bii de reducere?"
        }
    ],
    "signature": "BasicQuizModelWorker:0",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #8/24 - Basic_Quiz_Model : Biology-Begin : Ro

For basic_quiz_model, language 'ro', domain 'biology-begin', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "biology-begin",
    "LANGUAGE": "ro"
}
```

And this is a example response for above request of microservice #8:
```
{
    "call_id": 131,
    "quizzes": [
        {
            "answer": "Centru de energie",
            "max_given_time": 7,
            "options": [
                "Centru de distrac\u021bie",
                "Centru de frumuse\u021be",
                "Centru de energie"
            ],
            "question": "Ce este mitocondria?"
        }
    ],
    "signature": "BasicQuizModelWorker:0",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #9/24 - Basic_Quiz_Model : Biology-Highschool : Ro

For basic_quiz_model, language 'ro', domain 'biology-highschool', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "biology-highschool",
    "LANGUAGE": "ro"
}
```

And this is a example response for above request of microservice #9:
```
{
    "call_id": 132,
    "quizzes": [
        {
            "answer": "Procesul de diviziune celulara care produce doua celule identice",
            "max_given_time": 7,
            "options": [
                "Procesul de diviziune celulara care produce doua celule identice",
                "Procesul de formare a gametelor",
                "Procesul de diviziune celulara care produce celule diferite"
            ],
            "question": "Ce este mitoza?"
        }
    ],
    "signature": "BasicQuizModelWorker:0",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #10/24 - Basic_Quiz_Model : Chemistry-Highschool : Ro

For basic_quiz_model, language 'ro', domain 'chemistry-highschool', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "chemistry-highschool",
    "LANGUAGE": "ro"
}
```

And this is a example response for above request of microservice #10:
```
{
    "call_id": 133,
    "quizzes": [
        {
            "answer": "O substan\u021b\u0103 cu pH mai mic dec\u00e2t 7",
            "max_given_time": 7,
            "options": [
                "O substan\u021b\u0103 cu pH mai mic dec\u00e2t 7",
                "O substan\u021b\u0103 care nu poate reac\u021biona cu alte substan\u021be",
                "O substan\u021b\u0103 cu pH exact 7"
            ],
            "question": "Ce este un acid?"
        }
    ],
    "signature": "BasicQuizModelWorker:0",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #11/24 - Basic_Quiz_Model : Geography-Highschool : Ro

For basic_quiz_model, language 'ro', domain 'geography-highschool', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "geography-highschool",
    "LANGUAGE": "ro"
}
```

And this is a example response for above request of microservice #11:
```
{
    "call_id": 134,
    "quizzes": [
        {
            "answer": "Mediterana",
            "max_given_time": 7,
            "options": [
                "Mediterana",
                "Adria",
                "Rouge"
            ],
            "question": "Ce mare este situat\u0103 \u00eentre Africa \u0219i Europa?"
        }
    ],
    "signature": "BasicQuizModelWorker:0",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #12/24 - Basic_Quiz_Model : Physics-Mid : Ro

For basic_quiz_model, language 'ro', domain 'physics-mid', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "physics-mid",
    "LANGUAGE": "ro"
}
```

And this is a example response for above request of microservice #12:
```
{
    "call_id": 135,
    "quizzes": [
        {
            "answer": "Nikola Tesla",
            "max_given_time": 7,
            "options": [
                "Nikola Tesla",
                "Guglielmo Marconi",
                "Thomas Edison"
            ],
            "question": "Care a fost inventatorul radioului?"
        }
    ],
    "signature": "BasicQuizModelWorker:0",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #13/24 - Basic_Quiz_Model : Math-Begin : En

For basic_quiz_model, language 'en', domain 'math-begin', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "math-begin",
    "LANGUAGE": "en"
}
```

And this is a example response for above request of microservice #13:
```
{
    "call_id": 136,
    "quizzes": [
        {
            "answer": "Octahedron",
            "max_given_time": 7,
            "options": [
                "Sphere",
                "Cylinder",
                "Octahedron"
            ],
            "question": "What do you call a shape with eight faces?"
        }
    ],
    "signature": "BasicQuizModelWorker:1",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #14/24 - Basic_Quiz_Model : Math-Mid : En

For basic_quiz_model, language 'en', domain 'math-mid', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "math-mid",
    "LANGUAGE": "en"
}
```

And this is a example response for above request of microservice #14:
```
{
    "call_id": 137,
    "quizzes": [
        {
            "answer": "center",
            "max_given_time": 7,
            "options": [
                "chord",
                "center",
                "vertex"
            ],
            "question": "What is the name for the point in the center of a circle?"
        }
    ],
    "signature": "BasicQuizModelWorker:1",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #15/24 - Basic_Quiz_Model : Math-Highschool : En

For basic_quiz_model, language 'en', domain 'math-highschool', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "math-highschool",
    "LANGUAGE": "en"
}
```

And this is a example response for above request of microservice #15:
```
{
    "call_id": 138,
    "quizzes": [
        {
            "answer": "Cone",
            "max_given_time": 7,
            "options": [
                "Cone",
                "Torus",
                "Sphere"
            ],
            "question": "What do you call a 3D object with one circular base and one vertex?"
        }
    ],
    "signature": "BasicQuizModelWorker:0",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #16/24 - Basic_Quiz_Model : Physics-Begin : En

For basic_quiz_model, language 'en', domain 'physics-begin', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "physics-begin",
    "LANGUAGE": "en"
}
```

And this is a example response for above request of microservice #16:
```
{
    "call_id": 139,
    "quizzes": [
        {
            "answer": "centripetal",
            "max_given_time": 7,
            "options": [
                "centripetal",
                "gravity",
                "oscillation"
            ],
            "question": "What force causes an object to move in a circle?"
        }
    ],
    "signature": "BasicQuizModelWorker:2",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #17/24 - Basic_Quiz_Model : Physics-Highschool : En

For basic_quiz_model, language 'en', domain 'physics-highschool', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "physics-highschool",
    "LANGUAGE": "en"
}
```

And this is a example response for above request of microservice #17:
```
{
    "call_id": 140,
    "quizzes": [
        {
            "answer": "Power = Work / Time",
            "max_given_time": 7,
            "options": [
                "Power = Mass \u00d7 Acceleration",
                "Power = Work / Time",
                "Power = Force \u00d7 Distance"
            ],
            "question": "What is the formula for calculating the power of a device?"
        }
    ],
    "signature": "BasicQuizModelWorker:0",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #18/24 - Basic_Quiz_Model : Geography : En

For basic_quiz_model, language 'en', domain 'geography', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "geography",
    "LANGUAGE": "en"
}
```

And this is a example response for above request of microservice #18:
```
{
    "call_id": 141,
    "quizzes": [
        {
            "answer": "France",
            "max_given_time": 7,
            "options": [
                "France",
                "Spain",
                "United Kingdom"
            ],
            "question": "The Statue of Liberty was a gift from _______ to the United States."
        }
    ],
    "signature": "BasicQuizModelWorker:2",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #19/24 - Basic_Quiz_Model : Chemistry-Begin : En

For basic_quiz_model, language 'en', domain 'chemistry-begin', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "chemistry-begin",
    "LANGUAGE": "en"
}
```

And this is a example response for above request of microservice #19:
```
{
    "call_id": 142,
    "quizzes": [
        {
            "answer": "a KNiFe",
            "max_given_time": 7,
            "options": [
                "a KeNi shield",
                "a KNiFe",
                "a NicKFe bomb"
            ],
            "question": "What weapon can you make from the elements potassium, nickel, and iron? _ _ _ _ _ _ _ _ _ _ _ _ _"
        }
    ],
    "signature": "BasicQuizModelWorker:1",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #20/24 - Basic_Quiz_Model : Biology-Begin : En

For basic_quiz_model, language 'en', domain 'biology-begin', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "biology-begin",
    "LANGUAGE": "en"
}
```

And this is a example response for above request of microservice #20:
```
{
    "call_id": 143,
    "quizzes": [
        {
            "answer": "plant",
            "max_given_time": 7,
            "options": [
                "virus",
                "plant",
                "bacteria"
            ],
            "question": "What type of cell contains a cell wall?"
        }
    ],
    "signature": "BasicQuizModelWorker:2",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #21/24 - Basic_Quiz_Model : Biology-Highschool : En

For basic_quiz_model, language 'en', domain 'biology-highschool', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "biology-highschool",
    "LANGUAGE": "en"
}
```

And this is a example response for above request of microservice #21:
```
{
    "call_id": 144,
    "quizzes": [
        {
            "answer": "Adenine, Guanine, Cytosine, Thymine",
            "max_given_time": 7,
            "options": [
                "Adenine, Guanine, Cytosine, Uracil",
                "Adenine, Guanine, Cytosine, Thymine",
                "Lysine, Arginine, Histidine, Aspartic Acid"
            ],
            "question": "What are the four nitrogenous bases found in DNA?"
        }
    ],
    "signature": "BasicQuizModelWorker:1",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #22/24 - Basic_Quiz_Model : Chemistry-Highschool : En

For basic_quiz_model, language 'en', domain 'chemistry-highschool', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "chemistry-highschool",
    "LANGUAGE": "en"
}
```

And this is a example response for above request of microservice #22:
```
{
    "call_id": 145,
    "quizzes": [
        {
            "answer": "Deionization",
            "max_given_time": 7,
            "options": [
                "Deposition",
                "Melting",
                "Deionization"
            ],
            "question": "What is the name of the process by which a plasma turns into a gas?"
        }
    ],
    "signature": "BasicQuizModelWorker:0",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #23/24 - Basic_Quiz_Model : Geography-Highschool : En

For basic_quiz_model, language 'en', domain 'geography-highschool', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "geography-highschool",
    "LANGUAGE": "en"
}
```

And this is a example response for above request of microservice #23:
```
{
    "call_id": 146,
    "quizzes": [
        {
            "answer": "Yen",
            "max_given_time": 7,
            "options": [
                "Yen",
                "Pound",
                "Franc"
            ],
            "question": "What is the currency of Japan?"
        }
    ],
    "signature": "BasicQuizModelWorker:3",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


#### Microservice #24/24 - Basic_Quiz_Model : Physics-Mid : En

For basic_quiz_model, language 'en', domain 'physics-mid', we have the following request BODY:
```
{
    "SIGNATURE": "basic_quiz_model",
    "QUIZ_CATEGORY": "physics-mid",
    "LANGUAGE": "en"
}
```

And this is a example response for above request of microservice #24:
```
{
    "call_id": 147,
    "quizzes": [
        {
            "answer": "P=VI",
            "max_given_time": 7,
            "options": [
                "V=IR",
                "W=Fd",
                "P=VI"
            ],
            "question": "What is the formula for power?"
        }
    ],
    "signature": "BasicQuizModelWorker:2",
    "ver": "0.6.0",
    "worker_ver": "1.4.2"
}
```


