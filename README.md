# FAAS Sendmail


## What is it?
A function ready to be deployed to a OpenFAAS server.


## How does it work?
It takes a HTTP POST request containing a pre-defined json structure:
```json
{
    "receiver": string,
    "subject": string,
    "content": [string, string, string]
}
```

Example:
```json
{
    "receiver": "john@example.com",
    "subject": "Meeting next Tuesday...",
    "content": [
        "One of many strings",
        "Another of many strings",
        "..."
    ]
}
```

The contents can contain either plain-text or HTML as long as it is a string!


## Credits
[OpenFAAS]("https://github.com/openfaas/faas") for being awesome and open-sourcing their FAAS software

[Yagmail]("https://github.com/kootenpv/yagmail") for being awesome and open-sourcing mailclient