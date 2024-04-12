import csv
from connectionDB import connect_db, create_db, insert_db, select_db, count_localidades


def read_csv():
    with open("localidades.csv", mode="r") as read:
        reader = csv.DictReader(read)
        db = connect_db()
        create_db(db)
        rows_to_insert = []
        for row in reader:
            provincia = row["provincia"]
            id = int(row["id"])
            localidad = row["localidad"]
            cp = int(row["cp"]) if row["cp"] != "" else None
            id_prov_mstr = int(row["id_prov_mstr"]) if row["id_prov_mstr"] != "" else 0
            
            rows_to_insert.append((provincia, int(id), localidad, cp, int(id_prov_mstr)))
        insert_db(db, rows_to_insert)


def create_csv():
    db = connect_db()
    result = select_db(db)
    count = count_localidades(db)

    provincias = {}
    provincia_total = {}

    for row in result:
        provincia = row[0]
        if provincia not in provincias:
            provincias[provincia] = []
        provincias[provincia].append(row)

    for row in count:
        provincia = row[0]
        total = row[1]
        provincia_total[provincia] = total

    for provincia, localidades in provincias.items():
        with open(f"{provincia}.csv", mode="w", encoding="utf-8", newline="") as f:
            fieldnames = ["localidad"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for localidad in localidades:
                writer.writerow({"localidad": localidad[2]})

        with open(f"{provincia}.csv", mode="a", encoding="utf-8", newline="") as f:
            fieldnames = ["Total de localidades"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for pro_total, total in provincia_total.items():
                if provincia == pro_total:
                    writer.writerow({"Total de localidades": total})


read_csv()
create_csv()
