# SafeWeb AI 

This documentation presents both CI/CD aspects as well as API definitions for APIs currently usable.

## Overall CI/CD aspects

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

## Development

### Docker build

```
docker build -t safeweb/ai .
```


### Docker run

```
docker run --pull=always -p 5002-5010:5002-5010 safeweb/ai
```


## Usage


### Querying a microservice

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



### Azure VM install

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


## API definition for 'basic_quiz_model' endpoint
 
Overall we have the `math-begin`,`math-mid`,`math-highschool`,`physics-begin`,`physics-highschool`,`geography`,`chemistry-begin`,`biology-begin`,`biology-highschool`,`chemistry-highschool`,`geography-highschool`,`physics-mid` categories and `ro`,`en` languages
Requests are made using:
```
POST http://20.220.208.245:5002/run
```



### Microservice #1/24 - Basic_Quiz_Model : Math-Begin : Ro

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


### Microservice #2/24 - Basic_Quiz_Model : Math-Mid : Ro

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


### Microservice #3/24 - Basic_Quiz_Model : Math-Highschool : Ro

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


### Microservice #4/24 - Basic_Quiz_Model : Physics-Begin : Ro

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


### Microservice #5/24 - Basic_Quiz_Model : Physics-Highschool : Ro

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


### Microservice #6/24 - Basic_Quiz_Model : Geography : Ro

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


### Microservice #7/24 - Basic_Quiz_Model : Chemistry-Begin : Ro

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


### Microservice #8/24 - Basic_Quiz_Model : Biology-Begin : Ro

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


### Microservice #9/24 - Basic_Quiz_Model : Biology-Highschool : Ro

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


### Microservice #10/24 - Basic_Quiz_Model : Chemistry-Highschool : Ro

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


### Microservice #11/24 - Basic_Quiz_Model : Geography-Highschool : Ro

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


### Microservice #12/24 - Basic_Quiz_Model : Physics-Mid : Ro

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


### Microservice #13/24 - Basic_Quiz_Model : Math-Begin : En

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


### Microservice #14/24 - Basic_Quiz_Model : Math-Mid : En

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


### Microservice #15/24 - Basic_Quiz_Model : Math-Highschool : En

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


### Microservice #16/24 - Basic_Quiz_Model : Physics-Begin : En

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


### Microservice #17/24 - Basic_Quiz_Model : Physics-Highschool : En

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


### Microservice #18/24 - Basic_Quiz_Model : Geography : En

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


### Microservice #19/24 - Basic_Quiz_Model : Chemistry-Begin : En

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


### Microservice #20/24 - Basic_Quiz_Model : Biology-Begin : En

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


### Microservice #21/24 - Basic_Quiz_Model : Biology-Highschool : En

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


### Microservice #22/24 - Basic_Quiz_Model : Chemistry-Highschool : En

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


### Microservice #23/24 - Basic_Quiz_Model : Geography-Highschool : En

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


### Microservice #24/24 - Basic_Quiz_Model : Physics-Mid : En

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


