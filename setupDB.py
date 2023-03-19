from replit import db

db["active"] = []
db["teams"] = {
    "red": [],
    "blue": []
}
db["chars"] = {
    673509755196801057: {
        "current": "Litle",
        "Litle": {
            "active": True,
            "god": "hermes"
        },
        "Heather": {
            "active": False,
            "god": "hecate"
        }
    }
}

print(db.keys())