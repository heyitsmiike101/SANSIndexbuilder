import os
import csv


def import_csv(filename: str) -> list[list]:
    # logging.info("CSV import running.")
    if not os.path.splitext(filename.lower())[-1] == ".csv":
        print("File type error")
        exit()
    data = []

    try:
        with open(filename, "r", encoding="utf-8-sig") as f:
            data = list(list(rec) for rec in csv.reader(f, delimiter=","))
        f.close()
    except:
        with open(filename, "r") as f:
            data = list(list(rec) for rec in csv.reader(f, delimiter=","))
        f.close()
    return data


def export_text_file(data: str, filename: str):
    try:
        with open(filename, "w", encoding="utf-8-sig") as f:
            f.write(data)
        f.close()
    except IOError:
        print(
            "IOError: "
            + filename
            + " File with this name may already be open. Press enter once the file is closed or press 'q' then enter to quit."
        )


def main():
    filename = "Index.csv"
    csv_data = import_csv(filename)

    body_data = ""
    for i in csv_data[1:]:
        # Title,Description,Page,Book
        bookpage = "[b{b}/p{p}]".format(b=str(i[3]), p=str(i[2]))
        row_str = '<span style="color: blue; font-weight: bold;"> {title}</span><span style="font-style: italic;"> {bookpage}</span> {description}<br>\n'.format(
            title=i[0], bookpage=bookpage, description=i[1]
        )
        body_data += row_str

    htmldata = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chrissy's Index</title>
    </head>
<body>
    <p>
        {body}
    </p>
</body>
</html>
""".format(
        body=body_data
    )

    export_text_file(htmldata, "export_html.html")


if __name__ == "__main__":
    main()
