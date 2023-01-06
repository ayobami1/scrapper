import help as h
import os
import total
# import os
import subprocess
# import traceback
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import pandas as pd
import gspread
import gspread_dataframe as gd
# import requests
from oauth2client.service_account import ServiceAccountCredentials
# from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
import alert as al

# import re


# chrome_options.add_argument('--headless')


scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name('python.json', scope)

# Authenticate and authorize
client = gspread.authorize(creds)

# Open the spreadsheet
spreadsheet = client.open_by_key(
    'SPREAD_SHEET_ID'
)  

# Open the sheet and write the result here 
worksheet = spreadsheet.worksheet('Sheet1')


def Get_barcode():
    print("get barcodes")
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'python.json', scope)

    # Authenticate and authorize
    client = gspread.authorize(creds)

    
    spreadsheet = client.open_by_key(
        'SPREAD_SHEET_ID'')

    # Open the sheet and  PUll THE BARCODE from HERE
    worksheet = spreadsheet.worksheet('Barcodes_sheet')
    with open("scanned_barcodes.csv", "r") as f:

        reader = csv.reader(f)
        readers_ = [x for i in reader for x in i]

        print("The Total number of Scanned Barcodes: ", len(readers_), "\n")

    f_ = open("NotFound.csv", "r")
    f = [i for i in f_]
    print("The Total number of NotFound Barcodes: ", len(f), "\n")
    f_.close
    f_ = open("verified_barcodes.csv", "r")
    f = [i for i in f_]
    print("The Total number of Verified Barcodes: ", len(f), "\n")
    f_.close

    column_values = worksheet.col_values(1)[len(readers_) + 1:]
    time.sleep(.4)
    QTY = worksheet.col_values(2)[len(readers_) + 1:]
    time.sleep(.4)
    BIN = worksheet.col_values(3)[len(readers_) + 1:]
    new_column = []
    bin = []
    qty = []
    for a,b,c in zip(column_values, QTY, BIN):
      if a =='':
        continue

      else:
       
   
        if a not in readers_:
          new_column.append(a)
          bin.append(c)
          qty.append(b)
      
    # new_column = [i for i in column_values if i not in readers_ and column_values!='']
    print()
    print("Total barcodes To Scan  Remains ! :", len(new_column), "\n")
   
      
  
    return new_column, qty, bin, len(readers_)  #column_values


def Access_web():
    print("acces web")
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    barcodes, QTY, BIN, readers_ = Get_barcode(
    )  # Read and access only 10 barcodes
    # barcodes= [ '887229036320']

    writer_ = []  # store the Html in list.
    # We loop throught the barcodes and we access the Web
    if total.Automation.lower() == "yes":
        users = total.Total_per_scrap
        print()
        print(f" Autonomous Scrap Activated!\nDefault: {users}\n")

    else:
        print()
        print(" Manual Scrap Activated!\n")
        print(
            "You can Enter the number of data to scrap per Between 1 - 100\n\n"
        )
        user = int(input(" Please Enter It here:"))
        if user > 0 and user <= 100:
            users = user
        else:
            users = 50
            print(
                f"OOPs your input is {user}\nBut  should be between 1 & 100 to make it efficiency\nNo Issues Default is 50\nTo change it stop and replay"
            )
    for line, barcode in enumerate(barcodes[0:users]):

        try:
            if barcode == "":
              print("this barcode is Empty \n")
              continue
            url = f"https://www.barcodelookup.com/{barcode}"
            print(line, ".", "Accessing", url, "\n")

            driver.get(url)

            driver.implicitly_wait(10)

            # Get the HTML content of the page

            html_doc = driver.page_source
            writer_.append(html_doc)
            # soup = BeautifulSoup(html_doc, 'html.parser')
            # result = soup.find("div", {"class": "col-50 product-details"})
            # attempt = 0
            # while attempt < 1:

            #     if result is None:
            #         print("BRUTE FORCE ACTIVATED BECAUSE OF :>", result, "\n")
            #         # driver.refresh()
            #         driver.get(url)

            #         html_doc = driver.page_source
            #         soup = BeautifulSoup(html_doc, 'html.parser')
            #         result = soup.find("div",{"class": "col-50 product-details"})
            #         print(f"Result AFTER BRUTE is {result} attempt: {attempt} \n")

            #         attempt += 1
            #         if attempt >= 1:
            #             writer_.append(html_doc)
            #     else:
            #         writer_.append(html_doc)
            #         break
            #     # with open ("scanned_barcodes.csv", 'a', newline='') as f:
            #   writer = csv.writer(f)
            #   writer.writerow([barcode])

        except Exception as e:
            #except StaleElementReferenceException:
            print(e)
            print("Encounter An while Scrapping the web Accessing", url)
            al.send_alert1()
            # driver.quit()
            # print("\nRestarting... after 3 Seconds 😉")
            # time.sleep()
            # subprocess.run(["python3", "main.py"])

    # print(html_doc)
    return writer_, barcodes, QTY, BIN, readers_
    # Parse the HTML content using Beautiful Soup
    driver.quit()



def Write_to_sheet():
    NotFound = []
    #Set up the credentials
    values = worksheet.get_all_values()
    print()
    # print("values", len(values))
    if len(values) == 0:

        new_data = pd.DataFrame({
            "Barcode": [""],
            "Gender": [""],
            "Description": [""],
            "Color": [""],
            "Product Code": [""],
            "QTY": [""],
            "UK Size": [""],
            "US Size": [""],
            "Default Size": [""],
            "BIN NO": [""]
        })
        # df = pd.concat([df, new_data],ignore_index=True)

        # Update the sheet with the modified dataframe
        gd.set_with_dataframe(worksheet, new_data, row=1, col=1)

    datas_, barcodes, qty, bin, readers_ = Access_web(
    )  # Get the Html from the Web Function
    for barcode, p, QTY, BIN in zip(barcodes, range(len(datas_)), qty, bin):

        soup = BeautifulSoup(datas_[p], 'html.parser')
        if soup is None:
            continue
            pass

        else:

            try:
                dic = {}
                att_dic = {}
                attributes = {}
                # Use this to get the description and clean it to be in order
                result = soup.find("div", {"class": "col-50 product-details"})
                # print("RESULT======", result , "\n\n\n")
                string = result.find("h4").text

                if string is None:
                    print(barcode, "Cannot not be found")
                    continue
                else:
                    # print(string)
                    if "'" in string:

                        Description = " ".join(string.split("'")[0:1]) + repr(
                            string.split("'")[1])
                    else:

                        Description = string

                # Extract the All the information into Categories_ vriable   from the HTML content
                category_div = soup.find_all('div',
                                             {'class': 'product-text-label'})

                text = []
                for element in category_div:
                    label = element.text
                    # print(label)
                    text.append(label)

                # Initialize an empty dictionary

                # Loop over the elements in the list
                for s in text:
                    # Split the string at the first ":" character
                    # print(s)
                    key, value = s.split(":", 1)

                    # Strip leading and trailing whitespace from the key and value
                    key = key.strip()
                    value = value.strip()

                    # Add the key-value pair to the dictionary
                    dic[key] = value

                # print(dic)
                att = dic["Attributes"].split('\n')

                # Split the infomations in the Attributes Categories
                att_dic = {}
                for i in att:
                    a, b = i.split(":")
                    # print(a,b)

                    a.strip()
                    b.strip()
                    att_dic[a] = b

                # print("dic:", dic)
                # print("Attributes_dictiobary", att_dic)

                # We Look for Us and Uk size
                results = result.find("h4")

                r = results.text.lower()
                uk_size = ''
                us_size = ''
                size = ''
                if "size" in r and ":" in r:
                    # size =''
                    r_ = r.find("size")

                    r = r[r_:].replace(")", "")

                    # Split Uk and Us sizes
                    key, value = r.split(":")

                    if "us" in value:
                        us_size = value[3:]
                    else:
                        uk_size = value[3:]

                elif "size" in r:
                    r_ = r.find("size")
                    r = r[r_ + 5:r_+8]
                    size = r

                else:
                    # us_size = ""
                    # uk_size = ""
                    if "Size" in att_dic:
                        size = att_dic["Size"]
                    else:
                        size = ""

                #Extract Description from Html and clean it

                print(f"Geting and Filtering Data\n\nWRITING ROW {p+1}\n")
                df = gd.get_as_dataframe(worksheet)
                df = df.filter([
                    "Barcode", "Gender", "Description", "Color",
                    "Product Code", "QTY"
                    "UK Size", "US Size", "Default Size", "BIN NO"
                ])

                # Clean the data to make sure is within Range
                "We clean and access data in the category field"

                if "Color" in att_dic:

                    color = att_dic["Color"]
                else:
                    color = ""
                if "Gender" in att_dic:
                    gender = att_dic["Gender"].upper()
                else:
                    gender = ""
                if "Model" in att_dic:
                    model = att_dic["Model"]
                else:
                    if "MPN" in att_dic:
                        model = att_dic["MPN"]
                    else:
                        model = ""
                # bin_no = BIN
                # QTY = Quantity

                worksheet.append_row([
                    barcode, gender, Description, color, model, QTY, uk_size,
                    us_size, size, BIN
                ])
                # Retrieve the updated data from the worksheet

                with open("verified_barcodes.csv", "a") as f:
                    writer = csv.writer(f)
                    writer.writerow([barcode])
            except Exception as e:
                print(e, "due to None Found in Database\n")
                # print(traceback.tb_lineno(e.__traceback__))
                NotFound.append(barcode)
                with open("NotFound.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([barcode])
                print("The bot  will continue instead", "\n")
                worksheet.append_row(
                    [barcode, "", "", "", "", QTY, "", "", "", BIN])
                continue
    # df = pd.read_csv("append.csv")
    # gd.set_with_dataframe(worksheet, df, row=len(values)+1, col=1)
    # brute_scrape(NotFound)
    return NotFound, len(datas_), readers_, barcodes


if __name__ == "__main__":
    # import subprocess
    # Get_barcode()
    # Access_web()
  try:  
    if os.path.getsize("scanned_barcodes.csv") == 0:
        hint = "software Guide".title()
        hint = "\033[32m" + hint + "\033[0m"
        hint = "\033[1m" + f"{hint:.^50}" + "\033[0m"
        print(hint)
        for i in h.help:
            i = "\033[34m" + i + "\033[0m"
            print(i, flush=True, end="")
            time.sleep(.009)
    barcodes_, length, readers_, barcod_= Write_to_sheet()

    print(barcodes_)
    print("total barcodes per Scan are :", length)
    #
    with open("NotFound.csv", "r") as f:
        # Read the contents of the file
        lines1 = f.read().split("\n")

    # Open the second CSV file in read mode
    with open("verified_barcodes.csv", "r") as f:
        # Read the contents of the file
        lines2 = f.read().split("\n")

    # Concatenate the two lists of lines
    lines = lines1 + lines2

    # Write the concatenated list of lines to a new CSV file
    readers = []
    with open("scanned_barcodes.csv", 'r') as f_:

        reader = csv.reader(f_)
        readers.extend(reader)
    with open("scanned_barcodes.csv", "a") as f:
        # f.writelines("\n".join(lines))
        writer = csv.writer(f)
        reader = [x for i in readers for x in i]
        # print("READER", reader)
        for row in lines:
            if row == "":
                continue
            elif row in reader:
                #  print("yes row in Reader")
                continue
            else:
                writer.writerow([row])
    delay = 5
    print(len(barcod_))
    # if readers_ < len(barcod_):
    #     print(len(barcodes_))
    #     print(f"\nRestarting... after {delay} Seconds 😉")
    #     time.sleep(delay)
    #     process = subprocess.Popen(["python3", "main.py"])
    #       # Wait for the script to finish
    #     process.wait()
    #     print("about to die")
    # #   Kill the script
    #     process.kill()
    # else:
    #   al.send_alert2()
    #     print("Restarting... after 10 Seconds 😉")
    #     time.sleep(5)
    # os.system("python3 main.py")
    # while 1:
    #     print("Restarting... after 10 Seconds 😉")
    #     time.sleep(5)
    #     os.system("python3 main.py")
  except:
    al.send_alert1()
