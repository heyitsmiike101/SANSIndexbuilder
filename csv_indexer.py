import os
import csv
import html


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


def find_csv_files(directory: str) -> str:
    """
    Search the given directory for CSV files and handle selection if multiple files are found.

    Parameters:
    directory (str): The path of the directory to search for CSV files.

    Returns:
    str: The path of the selected CSV file or None if no CSV files are found.
    """
    # List all files in the directory
    files = os.listdir(directory)

    # Filter out the CSV files
    csv_files = [file for file in files if file.lower().endswith(".csv")]

    if len(csv_files) == 0:
        print("No CSV files found in the directory.")
        return None
    elif len(csv_files) == 1:
        print(f"One CSV file found: {csv_files[0]}")
        return os.path.join(directory, csv_files[0])
    else:
        print("Multiple CSV files found:")
        for idx, file in enumerate(csv_files, start=1):
            print(f"{idx}: {file}")

        # Ask the user to select a file
        while True:
            try:
                choice = int(input("Enter the number of the file you want to select: "))
                if 1 <= choice <= len(csv_files):
                    return os.path.join(directory, csv_files[choice - 1])
                else:
                    print("Invalid selection. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")


def define_headers(data: list[list]):

    headers = {"book": -1, "page": -1, "description": -1, "title": -1}

    row_index = 0
    for row in data[0]:
        if row.lower() == "book":
            headers["book"] = row_index
        if row.lower() == "page":
            headers["page"] = row_index
        if row.lower() == "description":
            headers["description"] = row_index
        if "title" in row.lower() or "tool" in row.lower() or "keyword" in row.lower():
            headers["title"] = row_index
        row_index += 1
    return headers


def sort_list_of_lists(
    data: list[list], column_index: int, reverse: bool = False
) -> list[list]:
    """
    Sorts a list of lists based on a specified column index.
    """
    if column_index < 0 or column_index >= len(data[0]):
        raise IndexError("Column index is out of range.")

    return sorted(data, key=lambda x: x[column_index], reverse=reverse)


def main():
    filename = find_csv_files(os.getcwd())
    csv_data = import_csv(filename)
    headers = define_headers(csv_data)

    userin = input("Do you want to sort by the title?([y]/n])").strip().lower()
    if userin in ("", "y", "yes"):
        csv_data = sort_list_of_lists(csv_data, column_index=headers["title"])

    body_data = ""
    line_count = 0
    for i in csv_data[1:]:
        # Title,Description,Page,Book
        bookpage = "[b{b}/p{p}]".format(
            b=str(i[headers["book"]]), p=str(i[headers["page"]])
        )
        row_str = '<span style="color: blue; font-weight: bold;"> {title}</span><span style="font-style: italic;"> {bookpage}</span> {description}<br>\n'.format(
            title=html.escape(i[headers["title"]]),
            bookpage=bookpage,
            description=html.escape(i[headers["description"]]),
        )
        body_data += row_str
        line_count += 1

    print("Total Lines:", line_count)

    htmldata = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SANS Index</title>
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
